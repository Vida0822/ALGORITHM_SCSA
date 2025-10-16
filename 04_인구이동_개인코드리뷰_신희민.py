"""
[개인 코드 리뷰]
한줄평:
1. 디버깅 및 테스트의 체계를 갖춰야한다.
2. 함수의 매개변수와 리턴값을 손코딩 당시 사전에 적어두자. 

소요 시간: 40분
타임라인 : 구상-20분, 구현:10분, 디버깅: 10분

[구상]
+) '컨베이너 벨트 위의 로봇' 문젱에서 언급했던대로 코드 로직(필요한 자료형)과 오픈 TC 시뮬레이션 부분을 손코딩에 포함
    => 로직의 구멍이 나지 않았고, 문제를 다시 읽을 필요 없이 손코딩 만으로 구현 가능
-) 엣지케이스를 미리 고려하지 않음

[구현]
+) 주의해야할 부분을 미리 적어두어 구현 시 실수를 최소화
-) 변수명이 모호함
-) 리턴값이 (리스트, 정수) 형태로 일반적이지 않아 헷갈림
    => 여유가 된다면 함수 인자/리턴값부터 먼저 정해두기
-) 리스트 등을 global 표시 없이 그냥 사용 (기능은 정상 동작하지만, 가독성 측면에서 global 사용하는게 better)

[디버깅]
-) 여전히 기능(단위)별 테스트에 어려움을 느낌 : 그냥 코드 전반에 여기저기 print 찍고 확인하는 느낌 
    => 디버깅 잘하는 다른 팀원들 방식을 참고할 필요성

"""

from collections import deque

# BFS
def bfs(si, sj):
    # [0] 필요한 자료형
    ans = []
    sm = 0
    q = deque()

    # [1] 첫방문
    sm += A[si][sj]
    ans.append((si, sj))
    v[si][sj] = 1
    q.append((si, sj))

    # [2] 순회
    while q:
        ci, cj = q.popleft()

        # 인접 조회
        for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            ni, nj = ci + di, cj + dj

            # 범위
            if not (0 <= ni < N and 0 <= nj < N):
                continue

            # 미방문 & 조건
            if not v[ni][nj] and (L <= abs(A[ci][cj] - A[ni][nj]) <= R):
                # 정답 처리
                sm += A[ni][nj]
                ans.append((ni, nj))

                # 다음 방문 준비
                v[ni][nj] = 1
                q.append((ni, nj))
    return ans, sm


# MOVE
def move():
    for union in unions:
        members = union[0]
        sm = union[1]
        cnt = len(members)
        for ci, cj in members:
            # print(members)
            A[ci][cj] = int(sm / cnt)


# MAIN
# [0] 필요한 자료형
N, L, R = map(int, input().split())
A = [list(map(int, input().split())) for _ in range(N)]
ans = 0
while True:
    v = [[0] * N for _ in range(N)]
    unions = []

    # 1. 국경선 open (연합 만들기)
    for i in range(N):
        for j in range(N):
            if not v[i][j]:
                union = bfs(i, j)
                if len(union[0]) > 1:
                    unions.append(union)

    # 2. 인구 이동
    if unions:
        # print(unions)
        move()
    else:
        break
    #
    # for a in A:
    #     print(*a)
    # print()
    ans += 1

# 3. 정답 출력
print(ans)


