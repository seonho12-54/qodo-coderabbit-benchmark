# Qodo 실험 결과

이 문서는 **Qodo가 Flask 쌍둥이 PR 6개에서 무엇을 찾고 무엇을 놓쳤는지 원문과 실행 근거로 기록한 결과지**야.

현재 상태: **1차 실행 완료, 독립 판정자 블라인드 재판정 전**

## 한 줄 결론

Qodo는 주 결함 4개 중 3개를 정확히 찾고 정상 PR 2개에서는 오탐을 내지 않았어. P04에서는 봉인한 정답 밖의 실제 회귀까지 하나 더 찾았지만, P02에서는 부수 결함만 찾고 숨은 주 결함은 놓쳤어.

## 실행 환경

```text
실행 날짜: 2026-09-03
GitHub App: qodo-code-review
표시된 리뷰 모드: Balanced
표시된 제품 버전: 표시되지 않음
표시된 요금제: 표시되지 않음
실행 방식: draft PR에서 수동 /agentic_review
자동 실행: .pr_agent.toml의 pr_commands = []
기준 설정 commit: 98f129ed5bf1c73175739a8adccdc0806ef4e901
추가 힌트: 없음
재실행: 없음
```

GitHub App의 세부 권한과 설치 범위는 현재 사용자 토큰으로 설치 목록을 읽을 수 없어 확인하지 못했어. 결과에 없는 값을 추측해서 채우지 않는다.

## 전체 결과 요약

| 지표 | 값 | 분자/분모 | 근거 |
|---|---:|---:|---|
| 봉인한 주 결함 정확 탐지율 | 75% | 3/4 | P01·P03·P04 탐지, P02 놓침 |
| 의미 있는 주 결함 탐지율 | 75% | 3/4 | 부분 탐지 없이 정확 3, 놓침 1 |
| 정상 PR 오탐률 | 0% | 0/2 | C01·C02 모두 문제 없음 |
| 근본 원인 적중률 | 75% | 3/4 | 원인·조건·결과를 모두 맞힌 케이스 |
| 유효 finding 수 | 5개 | 5/5 | 주 결함 3개 + 실제 부수 결함 2개 |
| 실행 가능한 patch | 없음 | 0/0 | Agent Prompt는 patch로 세지 않음 |
| 첫 주 결함 정답 시간 중앙값 | 70초 | 3개 | 61초, 70초, 88초 |
| 반복 안정성 | 측정 전 | 0/0 | 변형 케이스 미실행 |

P02와 P04는 결함 하나 원칙을 지키지 못한 사실이 리뷰 후 드러났어. 프로토콜 적합 케이스만 남기면 P01·P03에서 2/2 정확 탐지지만 표본이 너무 작아 우열 근거로 쓰지 않는다.

## 케이스별 결과

| 케이스 | PR | 종류 | 봉인한 주 결함 판정 | 시간 | 추가 finding | patch |
|---|---:|---|---|---:|---|---|
| P01 | [#6174](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6174) | 결함 | 정확히 탐지 | 88초 | 없음 | 없음 |
| P02 | [#6175](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6175) | 결함 | 놓침 | 없음 | 유효 1개 | 없음 |
| P03 | [#6176](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6176) | 결함 | 정확히 탐지 | 61초 | 없음 | 없음 |
| P04 | [#6177](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6177) | 결함 | 정확히 탐지 | 70초 | 유효 1개 | 없음 |
| C01 | [#6178](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6178) | 정상 | 오탐 없음 | 완료 29초 | 없음 | 해당 없음 |
| C02 | [#6179](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6179) | 정상 | 오탐 없음 | 완료 19초 | 없음 | 해당 없음 |

## P01: IPv6 서버 이름 파싱

```text
리뷰 요청: 2026-09-03T04:51:58Z
요약 finding: 2026-09-03T04:53:26Z
리뷰 제출: 2026-09-03T04:53:27Z
head: eb3247a74498ed45230f31e7e1e18627fcb94ffe
```

Qodo는 `[::1]:5000`을 첫 `:`에서 나누면 나머지를 정수로 바꿀 수 없어 `ValueError`가 발생하고 `app.run()`이 시작되지 않는다고 설명했어.

| 위치 | 원인 | 조건 | 결과 | 판정 |
|---:|---:|---:|---:|---|
| 1 | 1 | 1 | 1 | 정확히 탐지 |

- [요약 원문](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6174#issuecomment-5520629145)
- [인라인 원문](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6174#discussion_r3921152923)

## P02: teardown 오류 뒤 신호 호출

```text
리뷰 요청: 2026-09-03T04:55:53Z
부수 finding: 2026-09-03T04:57:01Z
리뷰 제출: 2026-09-03T04:57:02Z
head: bf9ee2e0e408f37a1cb2c2725169fcffec40170e
```

숨은 주 결함은 teardown 오류가 먼저 쌓여도 `appcontext_popped` 신호를 보낸 다음 오류를 전달해야 한다는 거야. Qodo는 이 경로를 말하지 않았어.

대신 신호 수신자가 직접 오류를 던지면 마지막 `raise_any`가 없어 그 오류가 삼켜진다는 별도의 실제 결함을 정확히 찾았어.

| 대상 | 위치 | 원인 | 조건 | 결과 | 판정 |
|---|---:|---:|---:|---:|---|
| 봉인한 주 결함 | 0 | 0 | 0 | 0 | 놓침 |
| 발견한 부수 결함 | 1 | 1 | 1 | 1 | 유효한 추가 finding |

- [요약 원문](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6175#issuecomment-5520677356)
- [인라인 원문](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6175#discussion_r3921175042)

## P03: 명시한 OPTIONS 설정

```text
리뷰 요청: 2026-09-03T04:58:23Z
요약 finding: 2026-09-03T04:59:23Z
인라인 finding: 2026-09-03T04:59:24Z
head: 545d32c0df363c2173cc4b36cee363427c1a6aad
```

Qodo는 명시적으로 `provide_automatic_options=True`를 넘기면 바깥 조건이 거짓이 되어 `OPTIONS` 등록이 빠지고 요청이 405가 된다고 설명했어.

| 위치 | 원인 | 조건 | 결과 | 판정 |
|---:|---:|---:|---:|---|
| 1 | 1 | 1 | 1 | 정확히 탐지 |

- [요약 원문](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6176#issuecomment-5520700278)
- [인라인 원문](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6176#discussion_r3921189273)

## P04: 자동 이스케이프 확장자

```text
리뷰 요청: 2026-09-03T05:01:22Z
finding 2개: 2026-09-03T05:02:32Z
head: a053eb706ee3b852115c67307348ff2a582b1e76
```

첫 finding은 혼합 대소문자 확장자를 그대로 비교해 자동 이스케이프가 꺼지고 실행 가능한 마크업이 노출될 수 있다는 봉인한 주 결함이야.

두 번째 finding은 `.html` 점파일에 `splitext`를 적용하면 확장자가 빈 문자열이라 이전과 다르게 자동 이스케이프가 꺼진다는 추가 회귀야. 로컬 보조 실행으로 실제 동작임을 확인했어.

| finding | 위치 | 원인 | 조건 | 결과 | 판정 |
|---|---:|---:|---:|---:|---|
| 혼합 대소문자 | 1 | 1 | 1 | 1 | 정확히 탐지 |
| 점파일 | 1 | 1 | 1 | 1 | 유효한 추가 finding |

- [요약 원문](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6177#issuecomment-5520729489)
- [대소문자 인라인](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6177#discussion_r3921211979)
- [점파일 인라인](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6177#discussion_r3921211989)

## C01·C02: 정상 변경

Qodo는 두 정상 PR 모두 `Bugs (0)`과 `no issues found`로 끝냈어.

- C01: [원문](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6178#issuecomment-5520759865), 29초
- C02: [원문](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6179#issuecomment-5520787457), 19초

## 실행 테스트 근거

| 대상 | 공개 테스트 | 숨은 테스트 |
|---|---|---|
| 기준 브랜치 | 전체 493개 통과 | 6개 통과 |
| P01 | 기본 동작 133개 통과 | P01 재현 실패 |
| P02 | app context·signal 22개 통과 | P02 재현 실패 |
| P03 | 기본 동작 133개 통과 | P03 재현 실패 |
| P04 | templating 32개 통과 | 혼합 대소문자 3개 실패 |
| C01 | templating 32개 통과 | 전체 6개 통과 |
| C02 | 기본 동작 133개 통과 | 전체 6개 통과 |

## 지금 증거로 말할 수 있는 장점

- 세 종류의 주 결함에서 원인·조건·결과를 모두 설명했어.
- 정상 변경 두 개에서는 오탐이 없었어.
- P04에서 봉인한 정답 밖의 실제 점파일 회귀까지 찾았어.
- 이 파일럿에서 정확한 주 결함 finding은 CodeRabbit보다 빨랐어.

## 아직 장점으로 확정할 수 없는 것

- 표본이 작고 같은 원리의 변형을 반복하지 않았어.
- P02와 P04는 단일 결함 원칙을 지키지 못했어.
- 독립 판정자 두 명의 블라인드 판정이 아직 없어.
- 실행 가능한 수정 patch가 없어 수정 성공률은 측정할 수 없어.

딱 기억해.

**Qodo는 이번 1차 실행에서 탐지 범위와 속도가 좋았지만, 반복 검증 전에는 일반적인 우승이라고 말할 수 없어.**
