# Qodo vs CodeRabbit Benchmark

실제 Flask 회귀 이력을 바탕으로 Qodo와 CodeRabbit의 탐지, 오탐, 근거 품질, 반복 안정성을 블라인드 비교하는 저장소입니다.

- 실험 명세: [PLAN.md](PLAN.md)
- 원본 Flask 안내: [UPSTREAM_README.md](UPSTREAM_README.md)
- 원본 이력·GitHub 메타데이터: [benchmark/ARCHIVE.md](benchmark/ARCHIVE.md)
- 원본 프로젝트: <https://github.com/pallets/flask>

리뷰가 끝나기 전에는 `.benchmark-private/`의 정답표나 숨은 테스트를 커밋하지 않습니다.

## 현재 상태

- [x] 원본 코드 스냅샷
- [x] 전체 Git 이력 bundle
- [x] 이슈, PR, 댓글, 리뷰 댓글, 라벨, 마일스톤, 릴리스, 보안 권고 snapshot
- [x] 실험·판정 명세
- [ ] Qodo / CodeRabbit 저장소 설치
- [x] 파일럿 브랜치 4개 + 정상 대조군 2개(앱 설치 뒤 PR 생성)
- [ ] 블라인드 리뷰 수집과 oracle 공개
