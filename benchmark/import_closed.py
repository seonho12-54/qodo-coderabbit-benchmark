#!/usr/bin/env python3
"""Import Flask's closed issues and PR records as closed GitHub issues."""

from __future__ import annotations

import argparse
import collections
import concurrent.futures
import gzip
import json
import re
import subprocess
import tarfile
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = ROOT / "benchmark/flask-github-metadata-2026-09-03.tar.gz"
CLOSERS = ROOT / "benchmark/flask-issue-closing-prs-2026-09-03.jsonl.gz"
STATE = ROOT / ".benchmark-private/import-state.jsonl"
REPOSITORY = "seonho12-54/qodo-coderabbit-benchmark"


def clean(text: str | None, limit: int = 60_000) -> str:
    text = (text or "").replace("@", "@\u200b")
    return text if len(text) <= limit else f"{text[:limit]}\n\n[truncated; see original]"


def clean_title(text: str) -> str:
    return clean(text).replace("\n", " ")[:250]


def archive_rows(name: str) -> list[dict]:
    with tarfile.open(ARCHIVE, "r:gz") as archive:
        member = next(m for m in archive.getmembers() if m.name.lstrip("./") == name)
        stream = archive.extractfile(member)
        assert stream is not None
        return [json.loads(line) for line in stream]


def closer_maps() -> tuple[dict[int, list[dict]], dict[int, list[int]]]:
    by_issue: dict[int, list[dict]] = {}
    by_pr: dict[int, list[int]] = collections.defaultdict(list)
    with gzip.open(CLOSERS, "rt") as stream:
        for line in stream:
            row = json.loads(line)
            by_issue[row["number"]] = row["closed_by"]
            for pull in row["closed_by"]:
                by_pr[pull["number"]].append(row["number"])
    return by_issue, by_pr


def grouped_comments(rows: list[dict], url_field: str) -> dict[int, list[dict]]:
    result: dict[int, list[dict]] = collections.defaultdict(list)
    for row in rows:
        result[int(row[url_field].rstrip("/").rsplit("/", 1)[1])].append(row)
    return result


def imported_numbers(token: str, label: str, prefix: str) -> set[int]:
    found: set[int] = set()
    page = 1
    while True:
        request = urllib.request.Request(
            f"https://api.github.com/repos/{REPOSITORY}/issues"
            f"?state=all&labels={label}&per_page=100&page={page}",
            headers=headers(token),
        )
        with urllib.request.urlopen(request) as response:
            rows = json.load(response)
        for row in rows:
            word = "(?:issue )?" if prefix == "issue" else f"{prefix} "
            match = re.match(rf"\[Flask {word}#(\d+)\]", row["title"])
            if match:
                found.add(int(match.group(1)))
        if len(rows) < 100:
            return found
        page += 1


def headers(token: str) -> dict[str, str]:
    return {
        "Accept": "application/vnd.github.golden-comet-preview+json",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "flask-review-benchmark-importer",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def submit(token: str, payload: dict) -> dict:
    request = urllib.request.Request(
        f"https://api.github.com/repos/{REPOSITORY}/import/issues",
        data=json.dumps(payload).encode(),
        headers=headers(token),
        method="POST",
    )
    delay = 2
    while True:
        try:
            with urllib.request.urlopen(request) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            if error.code not in {403, 429, 500, 502, 503, 504}:
                raise RuntimeError(error.read().decode()) from error
            time.sleep(min(int(error.headers.get("Retry-After", delay)), 60))
            delay = min(delay * 2, 60)


def imported_comment(row: dict, location: str = "") -> dict:
    author = (row.get("user") or {}).get("login", "unknown")
    source = row.get("html_url", "")
    prefix = f"> Original comment by `{author}`{location}\n> {source}\n\n"
    return {"created_at": row["created_at"], "body": clean(prefix + (row.get("body") or ""))}


def issue_payload(row: dict, comments: list[dict], closed_by: list[dict]) -> dict:
    links = "\n".join(f"- {item['url']} — {clean(item['title'], 500)}" for item in closed_by)
    metadata = (
        f"> Mirror of `pallets/flask#{row['number']}` by `{(row.get('user') or {}).get('login', 'unknown')}`\n"
        f"> Original: {row['html_url']}\n"
        f"> Created: {row['created_at']} | Closed: {row.get('closed_at') or ''}\n"
        f"> Original labels: {', '.join(label['name'] for label in row['labels']) or '(none)'}\n"
    )
    if links:
        metadata += f"> Closed by source PR:\n{links}\n"
    body = clean(f"{metadata}\n---\n\n{row.get('body') or ''}")
    return {
        "issue": {
            "title": clean_title(f"[Flask issue #{row['number']}] {row['title']}"),
            "body": body,
            "created_at": row["created_at"],
            "closed": True,
            "labels": ["source-issue"],
        },
        "comments": [imported_comment(comment) for comment in comments],
    }


def pr_payload(
    row: dict,
    comments: list[dict],
    reviews: list[dict],
    closed_issues: list[int],
) -> dict:
    links = "\n".join(
        f"- https://github.com/pallets/flask/issues/{number}" for number in closed_issues
    )
    metadata = (
        f"> Mirror of `pallets/flask` PR #{row['number']} by `{(row.get('user') or {}).get('login', 'unknown')}`\n"
        f"> Original: {row['html_url']}\n"
        f"> Created: {row['created_at']} | Closed: {row.get('closed_at') or ''}"
        f" | Merged: {row.get('merged_at') or 'no'}\n"
        f"> Original labels: {', '.join(label['name'] for label in row['labels']) or '(none)'}\n"
    )
    if links:
        metadata += f"> Closed source issues:\n{links}\n"
    imported = [imported_comment(comment) for comment in comments]
    imported.extend(
        imported_comment(
            review,
            f" on `{review.get('path', '')}` line {review.get('line') or review.get('original_line') or '?'}",
        )
        for review in reviews
    )
    imported.sort(key=lambda item: item["created_at"])
    return {
        "issue": {
            "title": clean_title(f"[Flask PR #{row['number']}] {row['title']}"),
            "body": clean(f"{metadata}\n---\n\n{row.get('body') or ''}"),
            "created_at": row["created_at"],
            "closed": True,
            "labels": ["source-pr"],
        },
        "comments": imported,
    }


def run(kind: str, pause: float, workers: int) -> None:
    token = subprocess.check_output(["gh", "auth", "token"], text=True).strip()
    issue_comments = grouped_comments(archive_rows("issue-comments.jsonl"), "issue_url")
    review_comments = grouped_comments(
        archive_rows("pull-review-comments.jsonl"), "pull_request_url"
    )
    closed_by_issue, closed_issues_by_pr = closer_maps()
    jobs: list[tuple[str, int, dict]] = []

    if kind in {"issues", "all"}:
        existing = imported_numbers(token, "source-issue", "issue")
        for row in archive_rows("issues.jsonl"):
            if row["state"] == "closed" and row["number"] not in existing:
                jobs.append(
                    (
                        "issue",
                        row["number"],
                        issue_payload(
                            row,
                            issue_comments[row["number"]],
                            closed_by_issue.get(row["number"], []),
                        ),
                    )
                )

    if kind in {"prs", "all"}:
        existing = imported_numbers(token, "source-pr", "PR")
        for row in archive_rows("pull-requests.jsonl"):
            if row["state"] == "closed" and row["number"] not in existing:
                jobs.append(
                    (
                        "pr",
                        row["number"],
                        pr_payload(
                            row,
                            issue_comments[row["number"]],
                            review_comments[row["number"]],
                            closed_issues_by_pr[row["number"]],
                        ),
                    )
                )

    STATE.parent.mkdir(exist_ok=True)
    submitted = set()
    if STATE.exists():
        submitted = {(row["kind"], row["source_number"]) for row in map(json.loads, STATE.read_text().splitlines())}
    jobs = [job for job in jobs if (job[0], job[1]) not in submitted]
    print(f"queued={len(jobs)} already_imported_or_submitted={len(submitted)}", flush=True)

    def import_one(job: tuple[str, int, dict]) -> tuple[str, int, dict]:
        job_kind, number, payload = job
        result = submit(token, payload)
        time.sleep(pause)
        return job_kind, number, result

    with STATE.open("a") as state, concurrent.futures.ThreadPoolExecutor(
        max_workers=workers
    ) as pool:
        for index, (job_kind, number, result) in enumerate(pool.map(import_one, jobs), 1):
            state.write(
                json.dumps(
                    {
                        "kind": job_kind,
                        "source_number": number,
                        "import_id": result["id"],
                        "status_url": result["url"],
                    }
                )
                + "\n"
            )
            state.flush()
            if index % 25 == 0 or index == len(jobs):
                print(f"submitted={index}/{len(jobs)} last={job_kind}#{number}", flush=True)


def self_test() -> None:
    assert clean("hi @user") == "hi @\u200buser"
    assert clean("abcd", 3).startswith("abc")
    assert grouped_comments([{"issue_url": "https://api.github.com/x/42"}], "issue_url")[42]
    print("ok")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--kind", choices=("issues", "prs", "all"), default="all")
    parser.add_argument("--pause", type=float, default=0.2)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    self_test() if args.self_test else run(args.kind, args.pause, args.workers)
