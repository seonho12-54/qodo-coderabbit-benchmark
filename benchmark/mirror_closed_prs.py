#!/usr/bin/env python3
"""Recreate Flask's closed pull requests as real GitHub pull requests."""

from __future__ import annotations

import argparse
import concurrent.futures
import gzip
import json
import subprocess
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "benchmark/flask-closed-pull-requests-2026-09-03.jsonl.gz"
STATE = ROOT / ".benchmark-private/pr-mirror-state.jsonl"
REPOSITORY = "seonho12-54/qodo-coderabbit-benchmark"
OWNER = REPOSITORY.split("/", 1)[0]
STATE_LOCK = threading.Lock()


def clean(text: str | None, limit: int = 60_000) -> str:
    value = (text or "").replace("@", "@\u200b")
    return value if len(value) <= limit else value[:limit] + "\n\n[truncated; see original]"


def rows() -> list[dict]:
    with gzip.open(SOURCE, "rt") as stream:
        return [json.loads(line) for line in stream]


def body(row: dict) -> str:
    author = (row.get("user") or {}).get("login", "ghost")
    labels = ", ".join(label["name"] for label in row.get("labels", [])) or "(none)"
    source_state = "merged" if row.get("merged_at") else "closed without merge"
    metadata = (
        f"> Exact-code mirror of `pallets/flask#{row['number']}` by `{author}`\n"
        f"> Original: {row['html_url']}\n"
        f"> Source state: **{source_state}**\n"
        f"> Created: {row['created_at']} | Closed: {row.get('closed_at') or ''}"
        f" | Merged: {row.get('merged_at') or 'no'}\n"
        f"> Base: `{row['base']['ref']}@{row['base']['sha']}`"
        f" ← Head: `{row['head']['ref']}@{row['head']['sha']}`\n"
        f"> Original labels: {labels}\n"
        "> The branches point at the original base and head commits, so Files changed"
        " shows the source PR diff. GitHub's public API cannot backdate the target PR"
        " or assign its original author.\n"
    )
    return clean(f"{metadata}\n---\n\n{row.get('body') or ''}")


def api(token: str, method: str, path: str, payload: dict | None = None) -> dict:
    url = f"https://api.github.com/repos/{REPOSITORY}/{path}"
    data = json.dumps(payload).encode() if payload is not None else None
    delay = 2
    while True:
        request = urllib.request.Request(
            url,
            data=data,
            method=method,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "User-Agent": "flask-pr-mirror",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        try:
            with urllib.request.urlopen(request) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            message = error.read().decode()
            if error.code == 422 and method == "POST" and path == "pulls":
                raise ValueError(message) from error
            if error.code not in {403, 429, 500, 502, 503, 504}:
                raise RuntimeError(f"{error.code}: {message}") from error
            wait = min(int(error.headers.get("Retry-After", delay)), 60)
            print(f"retry status={error.code} wait={wait}s body={message[:200]}", flush=True)
            time.sleep(wait)
            delay = min(delay * 2, 60)


def find_existing(token: str, source_number: int) -> dict | None:
    query = urllib.parse.urlencode(
        {"state": "all", "head": f"{OWNER}:archive/pr/{source_number}", "per_page": 1}
    )
    result = api(token, "GET", f"pulls?{query}")
    return result[0] if result else None


def load_state() -> dict[int, dict]:
    if not STATE.exists():
        return {}
    return {row["source_number"]: row for row in map(json.loads, STATE.read_text().splitlines())}


def append_state(record: dict) -> None:
    STATE.parent.mkdir(exist_ok=True)
    with STATE_LOCK, STATE.open("a") as stream:
        stream.write(json.dumps(record) + "\n")


def push_refs(items: list[dict], batch_size: int) -> None:
    for start in range(0, len(items), batch_size):
        batch = items[start : start + batch_size]
        refspecs: list[str] = []
        for row in batch:
            number = row["number"]
            base_sha = row["base"]["sha"]
            head_ref = f"refs/remotes/upstream/pr/{number}"
            subprocess.run(["git", "cat-file", "-e", f"{base_sha}^{{commit}}"], check=True)
            subprocess.run(["git", "cat-file", "-e", f"{head_ref}^{{commit}}"], check=True)
            refspecs.extend(
                [
                    f"{base_sha}:refs/heads/archive/base/{number}",
                    f"{head_ref}:refs/heads/archive/pr/{number}",
                ]
            )
        subprocess.run(["git", "push", "--quiet", "origin", *refspecs], check=True)
        print(f"refs={min(start + len(batch), len(items))}/{len(items)}", flush=True)


def run(
    limit: int | None, pause: float, batch_size: int, skip_push: bool, workers: int
) -> None:
    token = subprocess.check_output(["gh", "auth", "token"], text=True).strip()
    state = load_state()
    pending = [row for row in rows() if state.get(row["number"], {}).get("stage") != "closed"]
    if limit is not None:
        pending = pending[:limit]
    print(f"source=2897 completed={sum(x.get('stage') == 'closed' for x in state.values())} pending={len(pending)}", flush=True)

    if not skip_push:
        push_refs([row for row in pending if row["number"] not in state], batch_size)

    def mirror(row: dict) -> tuple[int, int]:
        number = row["number"]
        saved = state.get(number)
        target = saved.get("target_number") if saved else None
        if target is None:
            try:
                created = api(
                    token,
                    "POST",
                    "pulls",
                    {
                        "title": clean(f"[Flask PR #{number}] {row['title']}", 250),
                        "head": f"archive/pr/{number}",
                        "base": f"archive/base/{number}",
                        "body": body(row),
                    },
                )
            except ValueError:
                created = find_existing(token, number)
                if created is None:
                    raise
            target = created["number"]
            saved = {"source_number": number, "target_number": target, "stage": "created"}
            append_state(saved)
            time.sleep(pause)

        api(token, "PATCH", f"pulls/{target}", {"state": "closed"})
        saved = {"source_number": number, "target_number": target, "stage": "closed"}
        append_state(saved)
        time.sleep(pause)
        return number, target

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        completed = concurrent.futures.as_completed(pool.submit(mirror, row) for row in pending)
        for index, future in enumerate(completed, 1):
            number, target = future.result()
            state[number] = {
                "source_number": number,
                "target_number": target,
                "stage": "closed",
            }
            if index % 25 == 0 or index == len(pending):
                print(
                    f"closed={index}/{len(pending)} source=#{number} target=#{target}",
                    flush=True,
                )


def self_test() -> None:
    sample = {
        "number": 1,
        "user": {"login": "alice"},
        "html_url": "https://example.test/1",
        "created_at": "2020-01-01T00:00:00Z",
        "closed_at": "2020-01-02T00:00:00Z",
        "merged_at": None,
        "base": {"ref": "main", "sha": "base"},
        "head": {"ref": "fix", "sha": "head"},
        "labels": [],
        "body": "hello @team",
    }
    result = body(sample)
    assert "closed without merge" in result
    assert "@\u200bteam" in result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int)
    parser.add_argument("--pause", type=float, default=1.05)
    parser.add_argument("--batch-size", type=int, default=40)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--skip-push", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        run(args.limit, args.pause, args.batch_size, args.skip_push, args.workers)
