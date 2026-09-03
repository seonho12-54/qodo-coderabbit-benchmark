# Flask 코드로 Qodo와 CodeRabbit 비교하기

이 저장소는 **Flask의 실제 과거 문제로 Qodo와 CodeRabbit을 비교하는 실험 저장소**야.

이번 실행은 별도 저장소를 만들지 않고 이 저장소에서 진행한다. 정답 단서가 있을 수 있으므로 결과는 **완전한 블라인드 시험이 아닌 내부 비교**로만 사용한다. 실행 범위는 결함 4개와 정상 코드 2개, 총 12개 PR로 끝낸다.

## 무엇을 확인했나

```text
Flask의 과거 버그를 고름
↓
현재 코드에 버그를 다시 넣음
↓
같은 코드로 Qodo용 PR과 CodeRabbit용 PR을 만듦
↓
두 제품이 서로의 댓글을 못 보게 따로 리뷰시킴
↓
우리가 숨겨둔 정답 테스트로 결과를 확인
```

중요한 것은 댓글 개수가 아니야.

**실제 버그의 원인, 버그가 생기는 조건, 사용자에게 생기는 문제를 맞혔는지**가 중요해.

## 예비시험 결과 — 본시험 점수에는 넣지 않음

| 확인한 것 | Qodo | CodeRabbit |
|---|---:|---:|
| 버그 4개 중 제대로 찾은 수 | 3개 | 3개 |
| 정상 코드 2개에 잘못 경고한 수 | 0개 | 0개 |
| 버그를 처음 제대로 찾기까지 걸린 가운데 시간 | 70초 | 142초 |
| 바로 적용할 수 있는 코드 수정안 | 0개 | 2개 |

둘 다 P01·P03·P04는 찾았고 P02는 못 찾았어.

CodeRabbit은 P03과 P04에 코드 수정안을 줬어. 우리가 직접 적용해 보니 P03은 완전히 고쳤고 P04는 일부 문제만 고쳤어.

이 결과는 문제 수가 적고 정답 단서가 같은 저장소에 남아 있어서 방향 참고용이야. 최종 성적이나 승자를 정하는 데 쓰지 않아.

## 테스트 결과를 읽는 법

```text
P01~P04
+= 일부러 버그를 넣은 시험
+
+C01~C02
+= 버그가 없는 정상 코드 시험
+
+정답 테스트 실패
+= 버그가 진짜 발생함
+
+정답 테스트 통과
+= 그 버그가 없음
```

P01~P04에서 정답 테스트가 실패한 것은 실험이 실패했다는 뜻이 아니야. 우리가 일부러 넣은 버그가 실제로 발생했다는 뜻이야.

## 문서 읽는 순서

1. [이번 12개 PR 결과](실험-결과/구조확인-12개PR-결과.md)
2. [전체 계획](문서/00-전체-진행계획.md)
3. [기존 예비시험의 한계와 실제 사전 검사](문서/02-기존예비시험의-한계.md)
4. [실제 Flask 문제 후보 20개](문서/04-문제선정과-정답봉인.md)
5. [쌍둥이 PR을 만드는 방법](문서/03-쌍둥이PR-실험방법.md)
6. [점수를 정하는 방법](문서/05-평가와-판정기준.md)
7. [MUOT 제품 명세](06-MUOT-제품명세.md)

기존 예비시험 결과를 보고 싶으면 다음 문서를 이어서 읽으면 돼.

8. [예비시험 한눈에 보기](04-한눈에-보는-비교표.md)
9. [Qodo 예비시험 결과](실험-결과/Qodo-결과.md)
10. [CodeRabbit 예비시험 결과](실험-결과/CodeRabbit-결과.md)
11. [예비시험에서 두 제품이 함께 놓친 문제](05-두제품이-놓친-문제.md)

## 예비시험 PR — 본시험 점수에는 넣지 않음

| 시험 | CodeRabbit | Qodo | 결과 |
|---|---:|---:|---|
| P01 | [#6](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6) | [#6174](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6174) | 둘 다 찾음 |
| P02 | [#7](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/7) | [#6175](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6175) | 둘 다 핵심 문제를 못 찾음 |
| P03 | [#8](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/8) | [#6176](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6176) | 둘 다 찾음 |
| P04 | [#9](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/9) | [#6177](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6177) | 둘 다 찾음 |
| C01 | [#10](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/10) | [#6178](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6178) | 둘 다 잘못된 경고 없음 |
| C02 | [#11](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/11) | [#6179](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6179) | 둘 다 잘못된 경고 없음 |

각 줄의 두 PR에는 똑같은 코드 변경이 들어 있어.

## 저장소 안의 폴더

```text
src/
+= Flask 실제 코드
+
+tests/
+= 두 제품도 볼 수 있는 기존 테스트
+
+.benchmark-private/
+= 리뷰가 끝나기 전까지 제품에 보여주지 않은 정답
+
+benchmark/
+= Flask의 과거 이슈·PR 자료와 실행 기록
+
+실험-케이스/
+= P01~P04와 C01~C02 설명
+
+실험-결과/
+= Qodo와 CodeRabbit의 실제 결과
```

## 이번 실행 상태

- 결함 4개와 정상 코드 2개의 쌍둥이 PR 12개 완료
- 제품별 리뷰 원문 저장 완료
- 숨은 확인과 적용 가능한 수정 코드 확인 완료
- 결과 문서 작성 완료

딱 기억해.

**이번 범위는 결함 4개와 정상 코드 2개, 쌍둥이 PR 12개까지야.**
