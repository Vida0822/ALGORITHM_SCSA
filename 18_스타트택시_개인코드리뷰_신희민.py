"""
한줄평: BFS 관련 테크닉을 많이 얻어갈 수 있는 문제 

[start_arr & end_lst]
- start_arr[i][j] = idx : 승객들간 출발지가 겹치지 않아, 삭제해도 서로 영향을 주지 않음
- end_lst[idx] = (i, j) : 승객들간 목적지가 겹칠 수 있어 배열에 표시하면 값이 중첩갱신되는 경우, 각 idx 별로 관리

[일반 BFS vs q/nq 사용]
1. 방향 우선 순위
- 도착지가 하나 일 때: 일반 BFS 가능! delta 만 잘 주면 경로 내 방향 우선순위는 자동 보장됨 (첫방문 방향 우선순위도 마찬가지)
    => 단, 만나자마자 종료해야함
- 도착지가 여러개일 때, 우선 순위 보장 X => q/nq에 후보군 받아서 비교해줘야 함

2. 행/열 등 기타 우선 순위 조건
- 도착지 하나 일 때: q/nq 로 후보군 받아서 비교해줘야함 (경로 내 행, 열 정렬 순서는 보장 X)
- 도착지 여러개일 때:  q/nq 로 후보군 받아서 비교해줘야함


소요 시간) 40분
타임라인) 이해 및 구상 : 20 분 - 구현 : 분  - 디버깅 : 분
사용한 알고리즘)

[구상]
+) 일반 BFS를 사용해야하는지, 특수 BFS를 사용해야하는지 확실히 정의하고 들어가 구현에서 실수가 없었다
-) **** 숨어있는(?) 두번째 종료 조건을 구상때 고려하지 못함 ('이동 불가능 (벽 등 때문에)')

+) 제한조건에서 엣지 케이스를 미리 고려해서 자료 구조 정의

* start_arr 이 사용 가능했던 이유
: "'삭제'를 염두했을 때, 다른 승객 정보가 지워지지 않나?" 더블 체크
1. 한 승객의 출발지 != 목적지
 -> 출발지 지워줘도 목적지 영향 X
2. 각 승객의 출발지는 다른 승객의 목적지와

[구현]
+) 0-based, 1-based index 드디어 안틀림
-) 리턴값 처리 애매했다: 고민되면 효율성 생각하지 말고 필요 정보 그냥 다 넘겨 주기
-) q/nq 로직 종료조건 계속 까먹음('if not nq') : 'nq가 비었을 때' == '목적지 도착 안했는데, 더 이상 이동할 수 있는 칸이 없을 때'
    ㄴ 위치 주의 : candi 검사 아래에 써줘야함 : 탐색 종료와 동시에 찾았을수도 있으므로

[디버깅]
+) 구현 후 한번 점검하는거 역시 굿
+) 이번에 디버깅 진짜 안했다! 자료구조를 중간에 안바꾸니 한번에 정확히 구현한 듯

(오류 내용)
- 사전 종료 조건 만족 시 최종 정답 출력을 하면 안되는데 사전 종료 flag & 정답 모두 출력
-

[시간/공간 복잡도]
- 예상한 복잡도)
- 실제 복잡도)

[EdgeCase]
- 고려한 Edge Case)
- 고려하지 못한 Edge Case)
"""


from collections import deque

# [0]
N, M, C = map(int, input().split())
wall_arr = [list(map(int, input().split())) for _ in range(N)]

# 택시 정보
ti, tj = map(int, input().split())
ti, tj = ti-1, tj-1 # 0-based

# 승객 정보
start_arr = [[0]*N for _ in range(N)]
end_lst = [0]*(M+1)
arrived = [False]*(M+1)

for idx in range(1, M+1):
    si, sj, ei, ej = map(int, input().split())
    start_arr[si-1][sj-1] = idx # 1-based
    end_lst[idx] = (ei-1, ej-1)


# [1]
def oob(ni, nj):
    return not (0 <= ni < N and 0 <= nj < N)


def bfs_special(si, sj):
    # [0]
    q = deque()
    v = [[-1]*N for _ in range(N)]

    # [1]
    q.append((si, sj))
    v[si][sj] = 0

    # [2]
    while True :
        nq = deque()
        candi = []
        while q:
            ci, cj = q.popleft()

            # 종료 조건
            if start_arr[ci][cj] != 0 :
                candi.append((-v[ci][cj], ci, cj))

            for di, dj in ((-1, 0), (0, -1), (1, 0), (0, 1)):
                ni, nj = ci+di, cj+dj

                # 범위밖, 방문
                if oob(ni, nj) or v[ni][nj] != -1:
                    continue

                # 조건
                if wall_arr[ni][nj] == 0:
                    nq.append((ni, nj))
                    v[ni][nj] = v[ci][cj]+1

        if candi:
            dist, ni, nj = min(candi)
            return -dist, ni, nj, start_arr[ni][nj]
        else:
            q = nq

        # 손남 못찾았는데 이동 불가능한 경우 (위치 주의: 탐색 종료와 동시에 찾았을수도 있으므로 candi 검사 아래에 써줘야함)
        if not nq :
            return -1, si, sj, -1


def bfs_normal(si, sj, ei, ej) :
    # [0]
    q = deque()
    v = [[-1]*N for _ in range(N)]

    # [1]
    q.append((si, sj))
    v[si][sj] = 0

    # [2]
    while q:
        ci, cj = q.popleft()

        # 종료 조건
        if (ci, cj) == (ei, ej):
            return v[ci][cj], ei, ej

        for di, dj in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            ni, nj = ci+di, cj+dj

            # 범위밖, 미방문
            if oob(ni, nj) or v[ni][nj] != -1:
                continue

            # 조건 : 벽?
            if wall_arr[ni][nj] == 0:
                q.append((ni, nj))
                v[ni][nj] = v[ci][cj]+1
    else:
        return -1, si, sj

## MAIN ##
for turn in range(1, M+1):

    # 1. 승객 찾기 -> 이동
    dist, ni, nj, idx = bfs_special(ti, tj)

    # 종료 조건 1, 2 : 연료 떨어짐, 이동 불가(벽 등 때문에)
    if C < dist or dist == -1:
        print(-1)
        break

    ti, tj = ni, nj
    start_arr[ti][tj] = 0 # ※ 삭제는 신중히
    C -= dist

    # 2. 목적지 찾기 -> 이동
    ei, ej = end_lst[idx]
    dist, ni, nj = bfs_normal(ti, tj, ei, ej)

    # 종료 조건
    if C < dist or dist == -1:
        print(-1)
        break

    ti, tj = ni, nj
    arrived[idx] = True
    C += dist

else:
    print(C)






