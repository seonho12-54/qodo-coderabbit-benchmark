# Flask source archive

기준일: 2026-09-03  
원본: <https://github.com/pallets/flask>  
원본 snapshot commit: `d318b683471101618febed18996405ad26462110`

## 파일

| 파일 | 내용 | SHA-256 |
|---|---|---|
| `flask-full-history.bundle` | 원본 Git 전체 이력과 refs | `175e989f911fbc8d2cef7e268e73e4180053c34dcc4cddb0dea85ef2041917d4` |
| `flask-github-metadata-2026-09-03.tar.gz` | GitHub REST/GraphQL 메타데이터 | `e0f99248721accb4c0f6b9758e041cd7ea089c808d2a2601ca42fdf1517e5dc6` |

메타데이터 압축 파일에는 다음이 들어 있다.

- `repository.json`
- `issues.jsonl`: 2,766개
- `pull-requests.jsonl`: 2,900개
- `issue-comments.jsonl`: 14,780개
- `pull-review-comments.jsonl`: 1,304개
- `labels.json`
- `milestones.json`: 38개
- `releases.json`: 38개
- `security-advisories.json`: 3개
- `projects-v2.json`: 0개(원 조직에 공개 조회되는 Project v2가 없음)

## 복원

```bash
git clone benchmark/flask-full-history.bundle flask-upstream
mkdir flask-metadata
tar -xzf benchmark/flask-github-metadata-2026-09-03.tar.gz -C flask-metadata
shasum -a 256 benchmark/flask-full-history.bundle benchmark/flask-github-metadata-2026-09-03.tar.gz
```

압축 아카이브를 둔 이유는 기본 브랜치의 리뷰 제품 인덱스에 과거 정답이 평문으로 섞이지 않게 하기 위해서다. 실험 운영자는 로컬에서 복원해 원본 이슈와 수정 PR을 분석한다.

