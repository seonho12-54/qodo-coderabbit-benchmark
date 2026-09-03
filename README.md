# Flask 기반 Qodo·CodeRabbit 실전 비교

여기는 **Flask의 실제 과거 버그를 시험 문제로 바꿔 Qodo와 CodeRabbit의 코드 리뷰 실력을 검증하는 저장소**야.

원래 경쟁 제품은 기능표만 보면 비슷해 보여.

```text
PR 요약
↓
버그 탐지
↓
수정 제안
↓
보안 검사
```

근데 우리가 알고 싶은 건 기능의 존재가 아니야.

> 실제 장애 원인과 발생 조건을 정확히 찾고, 틀린 경고는 적게 남기며, 제안한 수정이 테스트를 통과하는가?

## 실험 흐름

```text
Flask의 실제 과거 버그 선택
↓
정답과 숨은 테스트 분리
↓
버그 PR과 정상 대조군 PR 준비
↓
Qodo와 CodeRabbit을 같은 조건으로 실행
↓
리뷰 원문과 시간을 저장
↓
숨은 테스트로 탐지와 수정 제안을 검증
↓
두 제품이 반복해서 놓친 부분을 제품 요구사항으로 전환
```

## 지금 상태

| 작업 | 상태 |
|---|---|
| Flask 코드와 전체 Git 이력 보관 | 완료 |
| closed 이슈 2,765개 아카이브·미러 | 완료 |
| closed PR 2,897개 메타데이터 아카이브 | 완료 |
| 실제 closed PR 객체 복원 | 500개에서 의도적으로 중단 |
| 결함 PR 4개와 정상 대조군 PR 2개 | 완료 |
| 제품별 쌍둥이 PR 12개 준비 | 완료 |
| Qodo 1차 리뷰 6개 실행 | 완료 |
| CodeRabbit 1차 리뷰 6개 실행 | 완료 |
| 실행 기반 1차 판정 | 완료 |
| 독립 판정자 블라인드 재판정 | 대기 |
| 공통 허점 변형 재시험 | 대기 |

전체 closed PR의 원문 데이터는 이미 `benchmark/`에 있어. GitHub의 Pull Requests 탭에는 사용자가 정한 범위인 500개만 실제 PR 객체로 복원했어.

## 문서 읽는 순서

1. [전체 진행 계획](문서/00-전체-진행계획.md)
2. [Flask를 선택한 이유](문서/01-플라스크를-선택한-이유.md)
3. [Qodo·CodeRabbit의 공식 주장](문서/02-경쟁사-공식주장.md)
4. [평가와 판정 기준](문서/03-평가와-판정기준.md)
5. 결함 케이스: [P01](실험-케이스/케이스-001.md), [P02](실험-케이스/케이스-002.md), [P03](실험-케이스/케이스-003.md), [P04](실험-케이스/케이스-004.md)
6. 정상 대조군: [C01](실험-케이스/대조군-001.md), [C02](실험-케이스/대조군-002.md)
7. [공개한 정답 테스트와 실행 기록](benchmark/oracles/pilot-2026-09-03/README.md)
8. [Qodo 결과](실험-결과/Qodo-결과.md), [CodeRabbit 결과](실험-결과/CodeRabbit-결과.md)
9. [한눈에 보는 비교표](04-한눈에-보는-비교표.md)
10. [두 제품이 놓친 문제](05-두제품이-놓친-문제.md)
11. [우리가 만들어야 할 기능](06-우리가-만들어야할-기능.md)

한 장으로 먼저 보고 싶으면 [전체 실험 설명서](플라스크-경쟁사-비교-실험서.md)를 읽으면 돼.

## 저장소 지도

```text
src/
= 실험에 사용하는 Flask 실제 코드

tests/
= 제품도 볼 수 있는 Flask 공개 테스트

.benchmark-private/
= 제품에게 보여주면 안 되는 정답과 숨은 테스트

benchmark/
= 원본 Git 이력, 이슈, PR, 댓글, 보안 자료

문서/
= 실험을 같은 방식으로 반복하기 위한 규칙

실험-케이스/
= 제품에게 공개해도 되는 중립적인 시험 요구사항

실험-결과/
= 제품별 리뷰 원문, 시간, 판정 기록
```

## 실행한 파일럿 PR

각 행의 두 PR은 base SHA, head SHA, diff가 완전히 같아. 자동 리뷰는 껐고 해당 제품만 수동으로 호출했어.

| 구분 | CodeRabbit 전용 | Qodo 전용 | 1차 결과 |
|---|---:|---:|---|
| 결함 P01 | [#6](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6) | [#6174](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6174) | 둘 다 정확히 탐지 |
| 결함 P02 | [#7](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/7) | [#6175](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6175) | 둘 다 주 결함 놓침, 같은 부수 결함 탐지 |
| 결함 P03 | [#8](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/8) | [#6176](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6176) | 둘 다 정확히 탐지 |
| 결함 P04 | [#9](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/9) | [#6177](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6177) | 둘 다 주 결함 탐지, Qodo가 추가 회귀도 탐지 |
| 정상 C01 | [#10](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/10) | [#6178](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6178) | 둘 다 오탐 없음 |
| 정상 C02 | [#11](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/11) | [#6179](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6179) | 둘 다 오탐 없음 |

원본 링크, 판정 근거, 시간과 수정 제안 실행 결과는 [한눈에 보는 비교표](04-한눈에-보는-비교표.md)와 제품별 결과 문서에 있어.

## 실험 전에 지켜야 할 것

- `.benchmark-private/`의 내용을 리뷰 제품이 읽는 브랜치에 올리지 않는다.
- Qodo가 남긴 댓글을 CodeRabbit이 보거나 그 반대가 되지 않게 제품별 쌍둥이 PR을 쓴다.
- 실행 전에 버전, 요금제, 권한, 설정 파일 SHA를 기록한다.
- 결과를 본 뒤 판정 기준을 바꾸지 않는다.
- 댓글 개수가 아니라 정확한 원인·발생 조건·결과를 찾았는지 본다.

딱 기억해.

**Flask 버그가 시험 문제고, 숨은 테스트가 정답지며, 두 제품의 공통 실패가 우리가 만들 기능의 출발점이야.**
