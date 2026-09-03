# CodeRabbit 실험 결과

이 문서는 **CodeRabbit이 Flask 쌍둥이 PR 6개에서 무엇을 찾고 무엇을 놓쳤는지 원문과 실행 근거로 기록한 결과지**야.

현재 상태: **1차 실행 완료, 독립 판정자 블라인드 재판정 전**

## 한 줄 결론

CodeRabbit은 주 결함 4개 중 3개를 정확히 찾고 정상 PR 2개에서는 오탐을 내지 않았어. P03과 P04에는 바로 적용 가능한 patch를 줬지만, P04 patch는 Qodo가 발견한 점파일 회귀를 고치지 못했어.

## 실행 환경

```text
실행 날짜: 2026-09-03
GitHub App: coderabbitai
표시된 리뷰 프로필: CHILL
표시된 요금제: Advanced
표시된 제품 버전: 표시되지 않음
실행 방식: draft PR에서 수동 @coderabbitai full review
자동 실행: .coderabbit.yaml의 reviews.auto_review.enabled = false
기준 설정 commit: 98f129ed5bf1c73175739a8adccdc0806ef4e901
추가 힌트: 없음
재실행: 없음
```

GitHub App의 세부 권한과 설치 범위는 현재 사용자 토큰으로 설치 목록을 읽을 수 없어 확인하지 못했어.

## 전체 결과 요약

| 지표 | 값 | 분자/분모 | 근거 |
|---|---:|---:|---|
| 봉인한 주 결함 정확 탐지율 | 75% | 3/4 | P01·P03·P04 탐지, P02 놓침 |
| 의미 있는 주 결함 탐지율 | 75% | 3/4 | 부분 탐지 없이 정확 3, 놓침 1 |
| 정상 PR 오탐률 | 0% | 0/2 | C01·C02 모두 actionable comment 없음 |
| 근본 원인 적중률 | 75% | 3/4 | 원인·조건·결과를 모두 맞힌 케이스 |
| 유효 finding 수 | 4개 | 4/4 | 주 결함 3개 + 실제 부수 결함 1개 |
| 원래 정답 patch 성공률 | 100% | 2/2 | P03·P04 봉인 테스트와 전체 테스트 통과 |
| 모든 발견 회귀 기준 patch 성공률 | 50% | 1/2 | P04 점파일 보조 테스트 실패 |
| 첫 주 결함 정답 시간 중앙값 | 142초 | 3개 | 118초, 142초, 219초 |
| 반복 안정성 | 측정 전 | 0/0 | 변형 케이스 미실행 |

프로토콜 적합 케이스만 남기면 P01·P03에서 2/2 정확 탐지지만 표본이 너무 작아 우열 근거로 쓰지 않는다.

## 케이스별 결과

| 케이스 | PR | 종류 | 봉인한 주 결함 판정 | 시간 | 추가 finding | 최초 patch |
|---|---:|---|---|---:|---|---|
| P01 | [#6](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6) | 결함 | 정확히 탐지 | 219초 | 없음 | 없음 |
| P02 | [#7](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/7) | 결함 | 놓침 | 없음 | 유효 1개 | 없음 |
| P03 | [#8](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/8) | 결함 | 정확히 탐지 | 118초 | 없음 | 수정 성공 |
| P04 | [#9](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/9) | 결함 | 정확히 탐지 | 142초 | 없음 | 부분 수정 |
| C01 | [#10](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/10) | 정상 | 오탐 없음 | 완료 86초 | 없음 | 해당 없음 |
| C02 | [#11](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/11) | 정상 | 오탐 없음 | 완료 310초 | 없음 | 해당 없음 |

## P01: IPv6 서버 이름 파싱

```text
리뷰 요청: 2026-09-03T04:51:58Z
인라인 finding: 2026-09-03T04:55:37Z
리뷰 제출: 2026-09-03T04:55:38Z
완료 표시: 2026-09-03T04:55:41Z
head: eb3247a74498ed45230f31e7e1e18627fcb94ffe
run ID: bd0729b0-68ee-4e1f-a3ce-acf369ea005d
```

CodeRabbit은 `[::1]:8080`을 첫 `:`에서 나누면 `int()`가 실패해 `run_simple` 전에 중단된다고 설명했어.

| 위치 | 원인 | 조건 | 결과 | 판정 |
|---:|---:|---:|---:|---|
| 1 | 1 | 1 | 1 | 정확히 탐지 |

- [리뷰 원문](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6#pullrequestreview-5097901713)
- [인라인 원문](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6#discussion_r3921166594)

## P02: teardown 오류 뒤 신호 호출

```text
리뷰 요청: 2026-09-03T04:55:53Z
부수 finding: 2026-09-03T04:57:43Z
리뷰 제출: 2026-09-03T04:57:44Z
완료 표시: 2026-09-03T04:57:47Z
head: bf9ee2e0e408f37a1cb2c2725169fcffec40170e
run ID: a5cadb42-7b46-4a2b-a764-7ecc52cdc2b8
```

CodeRabbit도 teardown 오류 때문에 `appcontext_popped` 호출 자체가 건너뛰어지는 숨은 주 결함은 말하지 않았어. Qodo와 똑같이 신호 수신자가 던진 오류가 삼켜지는 부수 결함을 찾았어.

| 대상 | 위치 | 원인 | 조건 | 결과 | 판정 |
|---|---:|---:|---:|---:|---|
| 봉인한 주 결함 | 0 | 0 | 0 | 0 | 놓침 |
| 발견한 부수 결함 | 1 | 1 | 1 | 1 | 유효한 추가 finding |

- [리뷰 원문](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/7#pullrequestreview-5097915556)
- [인라인 원문](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/7#discussion_r3921178460)

## P03: 명시한 OPTIONS 설정

```text
리뷰 요청: 2026-09-03T04:58:23Z
인라인 finding: 2026-09-03T05:00:21Z
리뷰 제출: 2026-09-03T05:00:23Z
head: 545d32c0df363c2173cc4b36cee363427c1a6aad
run ID: c35dddeb-1070-4394-ac4c-af0cdbe60e38
```

CodeRabbit은 명시한 `True`일 때 조건 분기를 건너뛰어 `OPTIONS`가 등록되지 않고 405가 된다고 설명하고, 두 줄을 바깥으로 옮기는 committable suggestion을 제공했어.

| 위치 | 원인 | 조건 | 결과 | 판정 |
|---:|---:|---:|---:|---|
| 1 | 1 | 1 | 1 | 정확히 탐지 |

최초 patch 검증:

```text
patch 적용 성공
숨은 P03 테스트 1개 통과
Flask 전체 공개 테스트 493개 통과
새 회귀 없음
```

- [리뷰 원문](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/8#pullrequestreview-5097937896)
- [인라인과 patch](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/8#discussion_r3921195653)

## P04: 자동 이스케이프 확장자

```text
리뷰 요청: 2026-09-03T05:01:22Z
인라인 finding: 2026-09-03T05:03:44Z
리뷰 제출: 2026-09-03T05:03:45Z
head: a053eb706ee3b852115c67307348ff2a582b1e76
run ID: c633e291-89d0-4db7-a348-f2238ef28c79
```

CodeRabbit은 혼합 대소문자 확장자가 자동 이스케이프를 우회해 XSS로 이어질 수 있다고 설명하고 확장자에 `.lower()`를 적용하는 patch를 줬어.

| 위치 | 원인 | 조건 | 결과 | 판정 |
|---:|---:|---:|---:|---|
| 1 | 1 | 1 | 1 | 정확히 탐지 |

최초 patch 검증:

```text
봉인한 혼합 대소문자 테스트 3개 통과
Flask 전체 공개 테스트 493개 통과
사후 점파일 보조 테스트 실패
```

원래 정답만 보면 수정 성공이지만, Qodo가 발견한 `.html` 점파일 회귀까지 포함하면 부분 수정이야.

- [리뷰 원문](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/9#pullrequestreview-5097968617)
- [인라인과 patch](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/9#discussion_r3921222648)

## C01·C02: 정상 변경

CodeRabbit은 두 정상 PR 모두 `No actionable comments`로 끝냈어.

- C01: [원문](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/10#issuecomment-5519021848), 완료 86초, run ID `cf4e1dbe-8c23-45ff-b231-002d29963ad3`
- C02: [원문](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/11#issuecomment-5519021748), 완료 310초, run ID `4510a678-e947-4f5d-8b55-c2a53770553e`

C02는 실패하지 않았지만 다른 실행보다 대기 시간이 크게 길었어. 한 번의 지연이므로 반복 전에는 일반적인 성능 단점으로 확정하지 않는다.

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
- P03과 P04에 바로 적용할 수 있는 patch를 제공했어.
- P03 patch는 숨은 테스트와 전체 공개 테스트를 모두 통과했어.

## 지금 증거로 말할 수 있는 약점

- P02의 주 실패 경로를 놓치고 두 제품이 같은 부수 경로에 집중했어.
- P04 patch는 자신이 지적한 대소문자 문제는 고쳤지만 같은 변경의 점파일 회귀는 남겼어.
- 정확한 주 결함 finding의 중앙 시간은 Qodo보다 느렸어.
- 정상 C02는 완료에 310초가 걸렸어. 단, 반복 전에는 일시적 지연 가능성을 배제할 수 없어.

## 아직 결론 낼 수 없는 것

- 케이스 수가 6개뿐이야.
- 독립 블라인드 판정과 변형 재시험이 없어.
- P02와 P04는 단일 결함 원칙을 지키지 못했어.
- 일반적인 저장소와 언어 전체로 결과를 확대할 수 없어.

딱 기억해.

**CodeRabbit은 실행 가능한 patch가 강점이었지만, patch가 PR의 모든 실제 회귀를 고쳤는지는 별도 테스트가 필요했어.**
