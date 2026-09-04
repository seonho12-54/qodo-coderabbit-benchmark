# SEP 50개 PR 수정안 검증

적용 가능한 제품 코드 patch는 **CodeRabbit SEP-012 한 개**였고, 실제 적용 뒤 완전히 고쳐졌다.

## 무엇을 patch로 셌나

현재 코드에 그대로 적용할 수 있는 `diff` 또는 GitHub suggestion만 셌다. ‘이 순서를 바꿔라’ 같은 설명과 다른 AI에 줄 프롬프트는 patch가 아니다.

## SEP-012 검증 흐름

```text
CodeRabbit이 OSError 전체를 숨기는 문제와 diff를 제안
↓
PR head와 같은 별도 Git worktree 생성
↓
제품 diff를 그대로 적용
↓
숨은 정답 테스트 3번 실행: 3/3 통과
↓
Flask 공개 전체 테스트 실행: 494/494 통과
↓
완전 수정
```

| 제품 | 적용 가능한 patch | 적용 성공 | 숨은 테스트 통과 | 공개 테스트 통과 | 완전 수정 |
|---|---:|---:|---:|---:|---:|
| Qodo | 0 | 해당 없음 | 해당 없음 | 해당 없음 | 0/0 |
| CodeRabbit | 1 | 1/1 | 1/1 | 1/1 | 1/1 |

근거는 [CodeRabbit SEP-012 PR](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6226)과 [저장한 원본](원본/sep-50pr/coderabbit/SEP-012/)에 있다.

표본이 한 개뿐이므로 ‘CodeRabbit patch는 항상 맞다’거나 제품 간 patch 능력의 우열을 결론내리지 않는다.
