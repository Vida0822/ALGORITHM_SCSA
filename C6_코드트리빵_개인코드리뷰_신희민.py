"""
한줄평:

소요 시간) 1시간 30분
타임라인) 이해 및 구상 : 20 분 - 구현 : 40분  - 디버깅 : 40분
사용한 알고리즘)

[구상]
+) 불필요한 자료구조를 미리 삭제
-) 이 구상이 다른 우선순위 문제에도 적용할 수 있는 방식인가?

[구현]
+) main 잘 짰다.
+) 자료 구조를 한번 바꿨는데 덜 당황했다. ('바꾸면 바꾸는거지!' )
+) append 방식 대신 idx 만큼 미리 만들어놓은거 good
-) turn & idx 혼용하는거...조금 안좋은 듯
-) 왜케 왔다리갔다리 하면서 짜지...? 함수 하나 구현할 때는 그것만 쭉 하자.


[디버깅]
-) 제출 전 코드 전체 검토 안함... 컴파일 체크 전에도 한번 해주기 (빨간색 뜨면 멘탈 나가니까...)
-) 또 원인 분석 안하고 무지성 디버거+막 고치기.. 제발 침착하고 코드를 읽어1!!
-) 동일/유사한 로직은 동시에 수정해줘야함 (그게 싫으면 함수화)

(오류 내용)
- 'Unindentent does not match any outer indentation level' :
- v 배열 값이랑 실제 거리와 차이 있음 : 최단거리 관련 v 배열 처리는 왠만하면 초기값 -1 주자
- 못가는 경우 (v[i][j] == -1) 고려 X : 최단 거리와 못가는 값을 구분하지 않음
    : 못가는 곳으로 배치 or 이동 -> 다음 턴에 이동 못함 (ex. 인접이 -1) -> 영원히 탈출 못해서 무한 루프 
- v 배열 관련 처리를 거리 구할 때만 적용하고, 동일한 로직인 베이스 캠프 배치에서는 사용 X 


[시간/공간 복잡도]
- 예상한 복잡도)
- 실제 복잡도)

[EdgeCase]
- 고려한 Edge Case)
- 고려하지 못한 Edge Case)
"""


from collections import defaultdict, deque

# [0]
N, M = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]

# map 정보
start_lst = []
for i in range(N):
    for j in range(N):
        if arr[i][j] == 1:
            start_lst.append((i, j))
            arr[i][j] = 0

# 플레이어
end_map = defaultdict()
for idx in range(M): # 0-based
    ii, jj = map(int, input().split())
    end_map[idx] = (ii-1, jj-1)

players = [[] for _ in range(M)]
escaped = [False]*M

delta = [(-1, 0), (0, -1), (0, 1), (1, 0)]

# [1]
def oob(ni, nj):
    return not (0 <= ni < N and 0<= nj < N)


def bfs(si, sj) :
    # [0]
    q = deque()
    v = [[-1]*N for _ in range(N)]

    # [1]
    q.append((si, sj))
    v[si][sj] = 0

    # [2]
    while q:
        ci, cj = q.popleft()

        for d in range(4):
            ni, nj = ci+delta[d][0],  cj+delta[d][1]

            if oob(ni, nj) or v[ni][nj] != -1 :
                continue

            if arr[ni][nj] == 0:
                q.append((ni, nj))
                v[ni][nj] = v[ci][cj]+1

    return v


def move_all(turn):
    '''
    모든 플레이어를 이동시키는 함수
    :return:
    '''
    rm_lst = []

    L = min(turn, M)
    for idx in range(L):
        if escaped[idx]:
            continue

        ci, cj = players[idx]
        ei, ej = end_map[idx]

        v = bfs(ei, ej) # 목적지에서 모든 좌표로의 최단 거리

        # 방향 우선순위
        tmp = []
        for d in range(4):
            ti, tj = ci+delta[d][0], cj+delta[d][1]
            if oob(ti, tj) or v[ti][tj] == -1:
                continue
            # if arr[ti][tj] == -1:
            #     continue
            tmp.append((v[ti][tj], d))
        debug = 3
        # print(ci, cj,'->', ei, ej)
        # for vv in v:
        #     print(*vv)
        # print()
        _, d = min(tmp)
        ni, nj = ci+delta[d][0], cj+delta[d][1]

        # 탈출구라면
        if (ni, nj) == (ei, ej):
            rm_lst.append((ni, nj))
            escaped[idx] = True

        # info 갱신
        players[idx] = [ni, nj]

    # Block 처리
    for bi, bj in rm_lst:
        arr[bi][bj] = -1


def put(idx) :
    rm_lst = []
    ei, ej = end_map[idx]
    v = bfs(ei, ej)

    # 행, 열 우선순위
    tmp = []
    for si, sj in start_lst:
        if v[si][sj] == -1 :
            continue
        tmp.append((v[si][sj] , si, sj))

    _, ni, nj = min(tmp)

    players[idx] = [ni, nj]

    # Block 처리
    arr[ni][nj] = -1


## MAIN ##
turn = 0
while True :
    # 1. 모든 플레이어 이동 (+후 블락 처리)
    move_all(turn)
    debug = 0

    # 2. 베이스 캠프 배치 (+후 블락 처리)
    if turn < M :
        # idx = turn
        put(turn) # turn 수이자 idx
        debug = 1

    # 3. 종료 조건
    turn += 1
    if sum(escaped) == M :
        break


# [2]
print(turn)
