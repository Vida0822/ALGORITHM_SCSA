"""
한줄평: 오래 걸리더라도 코드 로직을 써놓는게 중요하다/문제 1회독때는 처음부터 끝까지 빠르게 읽자

소요 시간) 55분
타임라인) 이해 및 구상 : 20분 - 구현 : 20분  - 디버깅 : 15분
사용한 알고리즘) 시뮬레이션 (delta)

[구상]
+) 정말 오래, 꼼꼼히 했다 (코드 로직까지 다 적음)
    --> 로직 구멍을 빠르게 발견할 수 있었고 필요한 자료형을 명확히 정해둘 수 있었다
-) 문제를 처음 정독할 때 입출력 부분까지만 읽고 그 아래 오픈 TC를 시뮬레이션 해준 부분을 읽지 않았다
    : 굉장한 힌트를 놓침 & 스스로 이해하느냐 시간 소요
    => 처음 읽을 때는 무조건 처음부터 끝까지 빠르게 보고 문제의 구성 파악 필요
-) 구름 이동/물복사버그는 상수시간인걸 놓쳐 괜히 효율적으로 짜려다가 실수

[구현]
+) 손코딩에 미리 코드 로직과 필요한 자료형을 정해두니 구현 시 고민없이 빠르게 할 수 있었다.
-) 중간중간 테스트를 하지 않고 전부 다 짜고 테스트를 시작했다 (버그 발견 곤란)

[디버깅]
+) 오픈 TC 배열 변화 과정이 문제에 잘 나와있어서 그걸 기준으로 print하며 디버깅 하니 용이했다
=> 앞으로도 (내가 시뮬레이션한) 오픈 TC를 기준으로 디버깅을 해야겠다고 감을 잡았다
-) 물의 양을 1 증가시키는 부분을 이동 당시가 아닌 구름이 이동한 좌표를 다 모으고 하나씩 꺼내며 증가시켜줬는데
답이 다르게 나왔다. 이동 즉시 1 증가하는 것으로 고쳐 답은 맞았지만, 전자와 후자의 차이를 모르겠다

[시간/공간 복잡도]
- 예상한 복잡도) O(M)*O(N^2)*O(N^2) = 명령횟수*전체좌표완탐*구름이동 =  O(625000000) = O(10^9)
- 실제 복잡도) O(M)*O(N^2) = O(M) : 명령횟수
                        * (O(N^2) : 구름이 N^2개 일 때 --> 구름 이동/물복사버그는 상수시간)
                            + O(N^2) : 구름 생성하느냐고 완탐)

[EdgeCase]
- 고려한 Edge Case) 물복사버그 수행 시 해당 회차의 다른 칸 물복사버그의 변화를 해당 칸에 반영? 미반영?
                => TC 확인하니 반영!
- 고려하지 못한 Edge Case) X

"""

from collections import deque

# [0] 시뮬레이션 준비
N, M = map(int, input().split())
A = [[0] * (N + 1)] + [[0] + list(map(int, input().split())) for _ in range(N)]

q = deque([(N, 1), (N, 2), (N - 1, 1), (N - 1, 2)])
#  ←, ↖, ↑, ↗, →, ↘, ↓, ↙
delta = {1: (0, -1), 2: (-1, -1), 3: (-1, 0), 4: (-1, 1),
         5: (0, 1), 6: (1, 1), 7: (1, 0), 8: (1, -1)}

# [1] 시뮬레이션 실행
for _ in range(M):
    d, s = map(int, input().split())
    di, dj = delta[d][0] * s, delta[d][1] * s

    # step1. 구름 이동
    nq = deque()
    while q:
        ci, cj = q.popleft()
        ni = (ci + di) % N if (ci + di) % N != 0 else N
        nj = (cj + dj) % N if (cj + dj) % N != 0 else N
        nq.append((ni, nj))

        # step2 : 물의 양 1증가
        A[ni][nj] += 1

    # 2. 물 증가
    v = set()
    while nq:
        ci, cj = nq.popleft()

        # step3 구름 사라짐 (있었음은 표시)
        v.add((ci, cj))

        # step4: 물복사버그
        cnt = 0
        # cp_A = [lst[:] for lst in A]
        for di, dj in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
            ni, nj = ci + di, cj + dj

            # 범위 체크
            if not (1 <= ni <= N and 1 <= nj <= N):
                continue
            if A[ni][nj] > 0:
                cnt += 1

        A[ci][cj] += cnt
        # print(ci, cj, cnt)

    # step 5. 새로운 구름 생성
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            if A[i][j] >= 2 and (i, j) not in v:
                A[i][j] -= 2
                q.append((i, j))

    # test
    # for a in A[1:]:
    #     print(*a[1:])
    # print()

# [3] 시뮬레이션 정답
ans = 0
for i in range(1, N + 1):
    for j in range(N + 1):
        ans += A[i][j]
print(ans)


