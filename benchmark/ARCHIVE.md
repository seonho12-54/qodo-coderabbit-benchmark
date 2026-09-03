# Flask source archive

기준일: 2026-09-03  
원본: <https://github.com/pallets/flask>  
원본 snapshot commit: `d318b683471101618febed18996405ad26462110`

## 파일

| 파일 | 내용 | SHA-256 |
|---|---|---|
| `flask-full-history.bundle` | 원본 Git 전체 이력과 refs | `175e989f911fbc8d2cef7e268e73e4180053c34dcc4cddb0dea85ef2041917d4` |
| `flask-github-metadata-2026-09-03.tar.gz` | GitHub REST/GraphQL 메타데이터 | `e0f99248721accb4c0f6b9758e041cd7ea089c808d2a2601ca42fdf1517e5dc6` |
| `flask-closed-issues-2026-09-03.jsonl.gz` | closed 이슈 2,765개만 분리한 JSONL | `b232cf13863e2a224da03a65a68472bb7249cfc667ec5f4f466c2a1bb0fca20a` |
| `flask-closed-pull-requests-2026-09-03.jsonl.gz` | closed PR 2,897개만 분리한 JSONL | `e99a755bd6f4ec2d3939ca7fcbef37d3f491f296de2e88a9db87835430ed15a6` |
| `flask-projects-2026-09-03.json` | open/closed GitHub Projects v2 조회 결과 | 해당 없음 |

메타데이터 압축 파일에는 다음이 들어 있다.

- `repository.json`
- `issues.jsonl`: 2,766개(2,765 closed, 1 open)
- `pull-requests.jsonl`: 2,900개(2,897 closed, 3 open, 1,633 merged)
- `issue-comments.jsonl`: 14,780개
- `pull-review-comments.jsonl`: 1,304개
- `labels.json`
- `milestones.json`: 38개
- `releases.json`: 38개
- `security-advisories.json`: 3개
- `projects-v2.json`: 0개(원 조직과 Flask 저장소 모두 open/closed Project v2가 없음)

## 복원

```bash
git clone benchmark/flask-full-history.bundle flask-upstream
mkdir flask-metadata
tar -xzf benchmark/flask-github-metadata-2026-09-03.tar.gz -C flask-metadata
shasum -a 256 benchmark/flask-full-history.bundle benchmark/flask-github-metadata-2026-09-03.tar.gz
gzip -dc benchmark/flask-closed-issues-2026-09-03.jsonl.gz | jq -s 'length'
gzip -dc benchmark/flask-closed-pull-requests-2026-09-03.jsonl.gz | jq -s 'length'
```

압축 아카이브를 둔 이유는 기본 브랜치의 리뷰 제품 인덱스에 과거 정답이 평문으로 섞이지 않게 하기 위해서다. 실험 운영자는 로컬에서 복원해 원본 이슈와 수정 PR을 분석한다.
