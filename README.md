# 플라스크 기반 Qodo·CodeRabbit 비교 실험

여기는 Flask의 실제 과거 버그로 Qodo와 CodeRabbit의 실력을 비교하는 저장소야.

- [전체 실험을 쉽게 설명한 문서](플라스크-경쟁사-비교-실험서.md)
- [원본 Flask 안내](UPSTREAM_README.md)
- [원본 이력과 GitHub 자료](benchmark/ARCHIVE.md)
- [원본 Flask 저장소](https://github.com/pallets/flask)

실험 흐름은 간단해.

```text
실제 Flask 버그 선택
↓
버그가 들어간 PR 생성
↓
Qodo와 CodeRabbit 리뷰
↓
숨은 테스트로 정답 확인
↓
둘 다 놓친 부분에서 우리 기능 찾기
```

## 현재 상태

- [x] 원본 코드 스냅샷
- [x] 전체 Git 이력 bundle
- [x] 이슈, PR, 댓글, 리뷰 댓글, 라벨, 마일스톤, 릴리스, 보안 권고 snapshot
- [x] 실험·판정 명세
- [ ] Qodo / CodeRabbit 저장소 설치
- [x] 파일럿 draft PR 4개 + 정상 대조군 draft PR 2개
- [ ] 블라인드 리뷰 수집과 oracle 공개
