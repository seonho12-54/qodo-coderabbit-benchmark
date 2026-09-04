# SEP 50개 PR 본시험 결과

이번 Flask 시험에서는 **Qodo가 새 결함을 더 많이 정확히 찾았다.** 다만 이 결과는 Flask 한 저장소의 25개 문제에만 해당하며, 모든 언어와 프로젝트의 우열을 뜻하지 않는다.

## 한눈에 보는 답

```text
실제 Flask 결함·정상 변경을 문제 25개로 만듦
↓
문제마다 코드가 같은 쌍둥이 PR 2개를 만듦
↓
Qodo와 CodeRabbit을 서로 다른 PR에서 실행함
↓
봉인한 정답과 대조해 위치·원인·조건·결과를 채점함
```

| 결과 | Qodo | CodeRabbit |
|---|---:|---:|
| 새 결함 정확 탐지 | 14/16 | 9/16 |
| 반복 문제까지 포함한 정확 탐지 | 18/20 | 11/20 |
| 반복 포함 정확 또는 일부 탐지 | 18/20 | 12/20 |
| 정상 변경의 오탐 | 0/5 | 0/5 |
| 바로 적용 가능한 코드 patch | 0개 | 1개 |

CodeRabbit은 SEP-012에서 적용 가능한 diff 하나를 줬다. 별도 worktree에 그대로 적용하자 숨은 정답 테스트 3/3과 공개 테스트 494개를 모두 통과해 **완전 수정 1/1**로 판정했다. 나머지 글 설명과 다른 AI용 프롬프트는 제품 patch로 세지 않았다.

## 문제 25개의 정답과 두 제품 판정

### SEP-001. 명시 환경 파일 우선순위

- 종류: 새 결함 · 설정·기본값 · 사전 분류 작음 / 어려움 · 실제 변경 1파일 6줄
- 정답: 기본 .flaskenv·.env를 먼저 합치고 사용자가 고른 파일을 마지막에 합쳐야 한다.
- 실제 사례 근거: [Flask PR #5630](https://github.com/pallets/flask/pull/5630)
- Qodo: **정확(4/4)** — [PR #6204](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6204) · [원본](원본/sep-50pr/qodo/SEP-001/)
- CodeRabbit: **정확(4/4)** — [PR #6205](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6205) · [원본](원본/sep-50pr/coderabbit/SEP-001/)

### SEP-002. 대문자 템플릿 자동 이스케이프

- 종류: 새 결함 · 입출력 안전 · 사전 분류 작음 / 쉬움 · 실제 변경 1파일 2줄
- 정답: 파일명을 소문자로 바꾼 뒤 HTML·SVG 등 자동 이스케이프 대상 확장자를 비교해야 한다.
- 실제 사례 근거: [Flask PR #6013](https://github.com/pallets/flask/pull/6013)
- Qodo: **정확(4/4)** — [PR #6206](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6206) · [원본](원본/sep-50pr/qodo/SEP-002/)
- CodeRabbit: **정확(4/4)** — [PR #6207](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6207) · [원본](원본/sep-50pr/coderabbit/SEP-002/)

### SEP-003. IPv6 호스트와 포트 분리

- 종류: 새 결함 · 요청·입력 · 사전 분류 작음 / 어려움 · 실제 변경 2파일 11줄
- 정답: 첫 콜론으로 자르지 말고 URL 파서로 IPv6 hostname과 port를 읽어야 한다.
- 실제 사례 근거: [Flask PR #6096](https://github.com/pallets/flask/pull/6096)
- Qodo: **정확(4/4)** — [PR #6208](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6208) · [원본](원본/sep-50pr/qodo/SEP-003/)
- CodeRabbit: **정확(4/4)** — [PR #6209](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6209) · [원본](원본/sep-50pr/coderabbit/SEP-003/)

### SEP-004. 빈 세션의 Vary: Cookie

- 종류: 새 결함 · 상태·캐시 · 사전 분류 작음 / 중간 · 실제 변경 1파일 8줄
- 정답: 읽힌 빈 세션도 조기 반환 전에 Vary: Cookie를 응답에 넣어야 한다.
- 실제 사례 근거: [Flask PR #5109](https://github.com/pallets/flask/pull/5109)
- Qodo: **정확(4/4)** — [PR #6210](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6210) · [원본](원본/sep-50pr/qodo/SEP-004/)
- CodeRabbit: **정확(4/4)** — [PR #6211](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6211) · [원본](원본/sep-50pr/coderabbit/SEP-004/)

### SEP-005. defaultdict 등록 코드 단순화

- 종류: 정상 변경 · 내부 정리 · 사전 분류 작음 / 중간 · 실제 변경 2파일 18줄
- 정답: 정상 변경이다. defaultdict(list)는 직접 인덱싱해도 빈 목록을 만들므로 동작이 보존된다.
- 실제 사례 근거: [Flask PR #3918](https://github.com/pallets/flask/pull/3918)
- Qodo: **오탐 없음** — [PR #6212](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6212) · [원본](원본/sep-50pr/qodo/SEP-005/)
- CodeRabbit: **오탐 없음** — [PR #6213](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6213) · [원본](원본/sep-50pr/coderabbit/SEP-005/)

### SEP-006. 중첩 Blueprint subdomain

- 종류: 새 결함 · 설정·기본값 · 사전 분류 중간 / 중간 · 실제 변경 1파일 12줄
- 정답: 자식 옵션·자식 기본값·부모 상태의 우선순위를 지키며 부모와 자식 subdomain을 합쳐야 한다.
- 실제 사례 근거: [Flask PR #4935](https://github.com/pallets/flask/pull/4935)
- Qodo: **정확(4/4)** — [PR #6215](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6215) · [원본](원본/sep-50pr/qodo/SEP-006/)
- CodeRabbit: **못 찾음(0/4)** — [PR #6214](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6214) · [원본](원본/sep-50pr/coderabbit/SEP-006/)

### SEP-007. 중첩 Blueprint 콜백 순서

- 종류: 새 결함 · 실행 순서 · 사전 분류 큼 / 어려움 · 실제 변경 2파일 6줄
- 정답: 요청 전·문맥·URL 기본값 콜백은 app→부모→자식 순서여야 한다.
- 실제 사례 근거: [Flask PR #4230](https://github.com/pallets/flask/pull/4230)
- Qodo: **정확(4/4)** — [PR #6216](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6216) · [원본](원본/sep-50pr/qodo/SEP-007/)
- CodeRabbit: **정확(4/4)** — [PR #6217](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6217) · [원본](원본/sep-50pr/coderabbit/SEP-007/)

### SEP-008. redirect 기본 상태 코드

- 종류: 새 결함 · 요청·기본 응답 · 사전 분류 작음 / 쉬움 · 실제 변경 2파일 4줄
- 정답: 호출자가 코드를 생략하면 helpers.redirect와 Flask.redirect 모두 303을 기본값으로 써야 한다.
- 실제 사례 근거: [Flask PR #5898](https://github.com/pallets/flask/pull/5898)
- Qodo: **못 찾음(0/4)** — [PR #6219](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6219) · [원본](원본/sep-50pr/qodo/SEP-008/)
- CodeRabbit: **못 찾음(0/4)** — [PR #6218](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6218) · [원본](원본/sep-50pr/coderabbit/SEP-008/)

### SEP-009. redirect 뒤 보존 문맥 순서

- 종류: 새 결함 · 상태·문맥 · 사전 분류 중간 / 중간 · 실제 변경 1파일 6줄
- 정답: 보존한 요청 문맥을 수집 순서대로 다시 넣어 마지막 응답 문맥이 현재 상태가 되게 해야 한다.
- 실제 사례 근거: [Flask PR #5797](https://github.com/pallets/flask/pull/5797)
- Qodo: **정확(4/4)** — [PR #6220](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6220) · [원본](원본/sep-50pr/qodo/SEP-009/)
- CodeRabbit: **정확(4/4)** — [PR #6221](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6221) · [원본](원본/sep-50pr/coderabbit/SEP-009/)

### SEP-010. Pyright ignore 범위 축소

- 종류: 정상 변경 · 타입 표시 · 사전 분류 중간 / 중간 · 실제 변경 5파일 20줄
- 정답: 정상 변경이다. ignore 코드를 좁혀도 런타임 동작은 바뀌지 않고 Pyright 오류도 없다.
- 실제 사례 근거: [Flask PR #5620](https://github.com/pallets/flask/pull/5620)
- Qodo: **오탐 없음** — [PR #6223](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6223) · [원본](원본/sep-50pr/qodo/SEP-010/)
- CodeRabbit: **오탐 없음** — [PR #6222](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6222) · [원본](원본/sep-50pr/coderabbit/SEP-010/)

### SEP-011. 세션 삭제 쿠키 HttpOnly

- 종류: 새 결함 · 쿠키 설정 · 사전 분류 중간 / 쉬움 · 실제 변경 1파일 1줄
- 정답: delete_cookie에도 계산한 httponly 설정을 전달해야 한다.
- 실제 사례 근거: [Flask PR #4486](https://github.com/pallets/flask/pull/4486)
- Qodo: **정확(4/4)** — [PR #6224](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6224) · [원본](원본/sep-50pr/qodo/SEP-011/)
- CodeRabbit: **못 찾음(0/4)** — [PR #6225](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6225) · [원본](원본/sep-50pr/coderabbit/SEP-011/)

### SEP-012. instance 폴더 오류 은폐

- 종류: 새 결함 · 예외 처리 · 사전 분류 중간 / 중간 · 실제 변경 1파일 5줄
- 정답: makedirs(exist_ok=True)로 기존 폴더만 허용하고 권한 오류 같은 다른 OSError는 전파해야 한다.
- 실제 사례 근거: [Flask PR #5903](https://github.com/pallets/flask/pull/5903)
- Qodo: **정확(4/4)** — [PR #6227](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6227) · [원본](원본/sep-50pr/qodo/SEP-012/)
- CodeRabbit: **정확(4/4)** — [PR #6226](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6226) · [원본](원본/sep-50pr/coderabbit/SEP-012/)
- 수정안 검증: CodeRabbit diff 적용 성공 · 숨은 테스트 3/3 · 공개 테스트 494/494 · 완전 수정

### SEP-013. flask --help 사용자 명령

- 종류: 새 결함 · CLI·앱 로딩 · 사전 분류 작음 / 쉬움 · 실제 변경 1파일 4줄
- 정답: help 옵션 하나만 있어도 환경 파일과 앱 옵션을 먼저 처리해 사용자 명령을 도움말에 넣어야 한다.
- 실제 사례 근거: [Flask PR #5674](https://github.com/pallets/flask/pull/5674)
- Qodo: **정확(4/4)** — [PR #6228](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6228) · [원본](원본/sep-50pr/qodo/SEP-013/)
- CodeRabbit: **못 찾음(0/4)** — [PR #6229](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6229) · [원본](원본/sep-50pr/coderabbit/SEP-013/)

### SEP-014. Response 기본 MIME 타입

- 종류: 새 결함 · 타입 호환 · 사전 분류 작음 / 쉬움 · 실제 변경 1파일 2줄
- 정답: default_mimetype를 str | None으로 명시해 하위 클래스가 None으로 지울 수 있게 해야 한다.
- 실제 사례 근거: [Flask PR #5034](https://github.com/pallets/flask/pull/5034)
- Qodo: **못 찾음(0/4)** — [PR #6231](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6231) · [원본](원본/sep-50pr/qodo/SEP-014/)
- CodeRabbit: **못 찾음(0/4)** — [PR #6230](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6230) · [원본](원본/sep-50pr/coderabbit/SEP-014/)

### SEP-015. dotenv 환경변수 공용 정리

- 종류: 정상 변경 · 테스트 정리 · 사전 분류 중간 / 중간 · 실제 변경 2파일 13줄
- 정답: 정상 변경이다. autouse fixture가 각 테스트 전에 환경변수를 지우므로 누수가 없다.
- 실제 사례 근거: [Flask PR #6095](https://github.com/pallets/flask/pull/6095)
- Qodo: **오탐 없음** — [PR #6232](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6232) · [원본](원본/sep-50pr/qodo/SEP-015/)
- CodeRabbit: **오탐 없음** — [PR #6233](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6233) · [원본](원본/sep-50pr/coderabbit/SEP-015/)

### SEP-016. 명시적 자동 OPTIONS

- 종류: 새 결함 · 설정·기본값 · 사전 분류 큼 / 어려움 · 실제 변경 1파일 14줄
- 정답: 기본값 결정과 분리해 최종 provide_automatic_options가 참이면 항상 OPTIONS를 필수 메서드에 넣어야 한다.
- 실제 사례 근거: [Flask PR #5917](https://github.com/pallets/flask/pull/5917)
- Qodo: **정확(4/4)** — [PR #6235](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6235) · [원본](원본/sep-50pr/qodo/SEP-016/)
- CodeRabbit: **정확(4/4)** — [PR #6234](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6234) · [원본](원본/sep-50pr/coderabbit/SEP-016/)

### SEP-017. 비동기 signal 수신 함수

- 종류: 새 결함 · 비동기 실행 · 사전 분류 중간 / 중간 · 실제 변경 4파일 36줄
- 정답: 모든 signal send에 같은 앱의 ensure_sync를 _async_wrapper로 전달해야 한다.
- 실제 사례 근거: [Flask PR #5049](https://github.com/pallets/flask/pull/5049)
- Qodo: **정확(4/4)** — [PR #6236](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6236) · [원본](원본/sep-50pr/qodo/SEP-017/)
- CodeRabbit: **정확(4/4)** — [PR #6237](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6237) · [원본](원본/sep-50pr/coderabbit/SEP-017/)

### SEP-018. 사용자 JSON provider 역직렬화

- 종류: 새 결함 · JSON 호환 · 사전 분류 중간 / 중간 · 실제 변경 1파일 14줄
- 정답: provider에는 값만 넘기고 읽힌 dict·list를 TaggedJSONSerializer가 재귀적으로 untag해야 한다.
- 실제 사례 근거: [Flask PR #5382](https://github.com/pallets/flask/pull/5382)
- Qodo: **정확(4/4)** — [PR #6239](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6239) · [원본](원본/sep-50pr/qodo/SEP-018/)
- CodeRabbit: **못 찾음(0/4)** — [PR #6238](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6238) · [원본](원본/sep-50pr/coderabbit/SEP-018/)

### SEP-019. 옛 Flask 하위 클래스 override

- 종류: 새 결함 · 이전 API 호환 · 사전 분류 큼 / 어려움 · 실제 변경 1파일 87줄
- 정답: 옛 override 서명을 감지해 ctx 인자 전후 호출을 호환 wrapper로 연결해야 한다.
- 실제 사례 근거: [Flask PR #5818](https://github.com/pallets/flask/pull/5818)
- Qodo: **정확(4/4)** — [PR #6240](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6240) · [원본](원본/sep-50pr/qodo/SEP-019/)
- CodeRabbit: **못 찾음(0/4)** — [PR #6241](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6241) · [원본](원본/sep-50pr/coderabbit/SEP-019/)

### SEP-020. 예외 전파 설정 한 번 읽기

- 종류: 정상 변경 · 성능 정리 · 사전 분류 중간 / 쉬움 · 실제 변경 1파일 4줄
- 정답: 정상 변경이다. walrus 결과를 is None으로 검사하므로 False를 None처럼 다루지 않는다.
- 실제 사례 근거: [Flask PR #2914](https://github.com/pallets/flask/pull/2914)
- Qodo: **오탐 없음** — [PR #6243](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6243) · [원본](원본/sep-50pr/qodo/SEP-020/)
- CodeRabbit: **오탐 없음** — [PR #6242](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6242) · [원본](원본/sep-50pr/coderabbit/SEP-020/)

### SEP-021. 보조 함수 안 환경 파일 우선순위

- 종류: 반복 문제 · 설정·기본값 · 사전 분류 큼 / 어려움 · 실제 변경 1파일 11줄
- 정답: SEP-001과 같다. 보조 함수로 감싸도 기본 파일 뒤에 명시 파일을 합쳐야 한다.
- 실제 사례 근거: [Flask PR #5630](https://github.com/pallets/flask/pull/5630)
- Qodo: **정확(4/4)** — [PR #6244](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6244) · [원본](원본/sep-50pr/qodo/SEP-021/)
- CodeRabbit: **정확(4/4)** — [PR #6245](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6245) · [원본](원본/sep-50pr/coderabbit/SEP-021/)

### SEP-022. 보조 함수 안 콜백 순서

- 종류: 반복 문제 · 실행 순서 · 사전 분류 큼 / 어려움 · 실제 변경 1파일 13줄
- 정답: SEP-007과 같다. 보조 함수가 app→부모→자식 순서를 반환해야 한다.
- 실제 사례 근거: [Flask PR #4230](https://github.com/pallets/flask/pull/4230)
- Qodo: **정확(4/4)** — [PR #6247](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6247) · [원본](원본/sep-50pr/qodo/SEP-022/)
- CodeRabbit: **못 찾음(0/4)** — [PR #6246](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6246) · [원본](원본/sep-50pr/coderabbit/SEP-022/)

### SEP-023. 보조 함수 안 IPv6 분리

- 종류: 반복 문제 · 요청·입력 · 사전 분류 중간 / 중간 · 실제 변경 2파일 16줄
- 정답: SEP-003과 같다. 보조 함수 안에서도 표준 URL 파서로 hostname과 port를 읽어야 한다.
- 실제 사례 근거: [Flask PR #6096](https://github.com/pallets/flask/pull/6096)
- Qodo: **정확(4/4)** — [PR #6248](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6248) · [원본](원본/sep-50pr/qodo/SEP-023/)
- CodeRabbit: **정확(4/4)** — [PR #6249](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6249) · [원본](원본/sep-50pr/coderabbit/SEP-023/)

### SEP-024. 옛 override 서명 오판

- 종류: 반복 문제 · 이전 API 호환 · 사전 분류 큼 / 어려움 · 실제 변경 1파일 15줄
- 정답: 두 번째 인자의 존재만 보지 말고 이름 또는 AppContext annotation으로 새 서명인지 판정해야 한다.
- 실제 사례 근거: [Flask PR #5818](https://github.com/pallets/flask/pull/5818)
- Qodo: **정확(4/4)** — [PR #6251](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6251) · [원본](원본/sep-50pr/qodo/SEP-024/)
- CodeRabbit: **일부(3/4)** — [PR #6250](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6250) · [원본](원본/sep-50pr/coderabbit/SEP-024/)
- 일부 판정 이유: CodeRabbit은 판정이 너무 넓어 TypeError가 난다는 점은 맞혔지만 `**kwargs` 경우만 고쳐, 일반 옛 위치 인자 서명은 계속 깨진다.

### SEP-025. routes 표 domain 열 정리

- 종류: 정상 변경 · CLI 표시 정리 · 사전 분류 큼 / 중간 · 실제 변경 1파일 10줄
- 정답: 정상 변경이다. 앱 설정으로 속성 이름을 한 번 고정해 host·subdomain 표시와 정렬을 보존한다.
- 실제 사례 근거: [Flask PR #5063](https://github.com/pallets/flask/pull/5063)
- Qodo: **오탐 없음** — [PR #6252](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6252) · [원본](원본/sep-50pr/qodo/SEP-025/)
- CodeRabbit: **오탐 없음** — [PR #6253](https://github.com/seonho12-54/qodo-coderabbit-benchmark/pull/6253) · [원본](원본/sep-50pr/coderabbit/SEP-025/)

## 판정 방법

코드 리뷰의 실행 가능한 지적에서 위치·원인·발생 조건·사용자 결과를 각각 1점으로 셌다. 네 가지를 모두 맞히면 정확, 원인을 맞히고 2~3점이면 일부, 원인을 못 맞히거나 0~1점이면 못 찾음이다. 단순 walkthrough와 release-note 요약은 결함 경고로 세지 않았다. 정상 변경은 실제로 없는 중대한 문제를 주장했을 때만 오탐으로 셌다.

## 결론의 경계

- RETRO 12개 PR은 이 점수에 넣지 않았다.
- Qodo PR에 자동으로 달린 CodeRabbit의 ‘자동 리뷰 꺼짐’ 안내와 모든 PR의 Copilot 사용량 초과 안내는 코드 판단이 아니므로 점수에 넣지 않았다.
- CodeRabbit 제한 응답은 실패로 세지 않고 같은 PR에서 다시 요청해 실제 리뷰가 끝난 결과만 채점했다.
- CodeRabbit이 자기 PR 본문에 자동 요약을 붙였으므로 결과는 기본 제품 흐름의 비교이지, 두 리뷰 모델만 격리한 비교가 아니다.
- 이 저장소 이름과 과거 Git 기록 때문에 완전한 외부 블라인드 시험은 아니다. 정답 테스트와 원본 이슈 번호는 PR에서 제거했다.
- 같은 작업자가 문제 구성과 판정을 맡았다. 제품 출력을 먼저 JSON으로 고정한 뒤 정답과 대조했지만 독립 심사자 블라인드 판정은 아니다.
- 두 제품이 공개 Flask 과거 자료를 검색해 원본 PR·이슈를 언급한 사례가 각각 1개 있었다. 인터넷 검색을 막은 추론-only 시험이 아니다.

자세한 수치와 불확실성은 [통계 문서](SEP-50개PR-통계.md), 실험이 깨지지 않았는지는 [공정성 검사](SEP-50개PR-공정성.md)에서 확인할 수 있다.
