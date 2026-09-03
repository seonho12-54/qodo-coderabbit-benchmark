# 2026-09-03 파일럿 정답과 실행 기록

여기는 **두 제품의 리뷰가 모두 끝난 뒤 공개한 재현 증거**야.

`test_pilot_oracle.py`는 실행 전에 봉인했던 원래 정답 6개야. `test_posthoc_p04.py`는 Qodo의 추가 finding을 확인하려고 리뷰 후 만든 보조 테스트라서 원래 점수에는 넣지 않아.

## 원본 연결

| 케이스 | 원본 | commit | 깨진 동작 |
|---|---|---|---|
| P01 | [Flask #6096](https://github.com/pallets/flask/pull/6096), [이슈 #6093](https://github.com/pallets/flask/issues/6093) | `05e9c6bd630ecf4ec0ec884b1fc7901663737bc7` | IPv6 host와 port 파싱 |
| P02 | [Flask #5928](https://github.com/pallets/flask/pull/5928) | `c34d6e81fd8e405e6d4178bf24b364918811ef17` | 오류 뒤 callback·signal 실행 |
| P03 | [Flask #5917](https://github.com/pallets/flask/pull/5917), [이슈 #5916](https://github.com/pallets/flask/issues/5916) | `12e95c93b488725f80753f34b2e0d24838ca4646` | 명시한 OPTIONS 설정 우선순위 |
| P04 | [Flask #6013](https://github.com/pallets/flask/pull/6013) | `dcbede0cb00df32e7f1895e19e37d5f40a75d1f6` | autoescape 확장자 대소문자 |

## 실행 환경

```text
날짜: 2026-09-03
Python: CPython 3.12.13
실행기: uv
base: 98f129ed5bf1c73175739a8adccdc0806ef4e901
공개 전체 테스트: 493개
봉인 정답 테스트: 6개
```

## 기준 브랜치

```bash
uv run --python 3.12 --group tests pytest -q \
  benchmark/oracles/pilot-2026-09-03/test_pilot_oracle.py

uv run --python 3.12 --group tests pytest -q
```

결과:

```text
봉인 정답 6 passed
전체 공개 테스트 493 passed
```

## 결함과 대조군 검증

| 브랜치 | 공개 테스트 | 원래 정답 테스트 |
|---|---|---|
| `case/pilot/p01` | `tests/test_basic.py`: 133 passed | P01 실패 |
| `case/pilot/p02` | appctx·signals: 22 passed | P02 실패 |
| `case/pilot/p03` | `tests/test_basic.py`: 133 passed | P03 실패 |
| `case/pilot/p04` | `tests/test_templating.py`: 32 passed | P04 3개 실패 |
| `control/pilot/c01` | `tests/test_templating.py`: 32 passed | 6 passed |
| `control/pilot/c02` | `tests/test_basic.py`: 133 passed | 6 passed |

## CodeRabbit 최초 patch 검증

P03 patch:

```text
봉인 P03 테스트 1 passed
전체 공개 테스트 493 passed
최종 판정: 수정 성공
```

P04 patch:

```text
봉인 P04 테스트 3 passed
전체 공개 테스트 493 passed
사후 점파일 테스트 failed
최종 판정: 원래 주 결함 수정, 전체 회귀 기준 부분 수정
```

## 재사용 금지

이 정답은 이미 공개됐으므로 같은 PR을 다음 블라인드 실험에 다시 쓰면 안 돼. 후속 실험은 원리는 같되 코드 모양과 입력을 바꾼 새 비공개 정답을 사용해야 해.

딱 기억해.

**원래 정답과 리뷰 후 발견한 보조 정답을 분리해야 결과를 보고 점수를 바꾸는 일을 막을 수 있어.**
