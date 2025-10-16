"""
한줄평:

소요 시간)
타임라인) 이해 및 구상 : 20분 - 구현 : 30 분  - 디버깅 : 15 분
사용한 알고리즘)

[구상]
+) 드디어 종료조건을 고려했구나...
+) 문제 자체가 단계가 나누어져 있어 함수화하기 좋았다
+) 불필요한 자료구조 없이 잘 사용한듯
+) v 배열의 좋은 활용법을 알았다!
+) 구상 때 함수 리턴값 정해주면 편하긴 편하다...! (근데 항상 할수있는건 X...) 
-) 아리까리 했던 점: 경로 중 방향 우선순위는 일반 bfs에서도 보장된다? 그렇다면 일반 bfs가 아니라 q/nq 사용해서 우선 순위 비교해줘야하는건 뭐지...?

[일반 BFS vs q/nq]
1. 방향 우선 순위
 - 일반 BFS : 도착지가 하나 일 때, 경로의 방향 우선순위는 보장됨(첫방문 방향 우선순위도 마찬가지) : 단, 만나자마자 종료해야함
 ※ 도착지가 여러개인 경우, 방향 우선 순위 보장 X => q/nq에 후보군 받아서 비교해줘야 함

2. 행/열 등 기타 우선 순위
 - q/nq 로 후보군 받아서 비교해줘야함

[구현]
+) 값만 신중하게 넣어준다면, list에 양수/음수값 넣어주고 min/max 뽑는게 실수도 훨씬 줄고 구현 시간도 줄어든다!
+) 동일한 로직을 두 군데 이상에서 사용했을 때, 이걸 변경하면 어디도 변경해줘야하는지 주석으로 달아주니 good
+) 값이 음수로 안떨어지도록 max 사용한거 굿
-) 후보군 리스트에 양수/음수 넣는거 아직도 헷갈린다... 여기 진짜 신중히 짜기
-) 만나면 종료하는 BFS 에선 최단 거리가 보장되기 때문에 굳이 거리 정보를 저장해줄 필요 없다!
+) 유사한 로직은 형식도 어느정도 통일해주니까 가독성 good

[디버깅]
+) 조금은...코드를 보면서 디버깅하는...것 같다....
+) 마음 급하게 먹지 않고, 제출 전 코드 검토 지킴!! => 오류 꽤 많이 발견했다.
-) min, max 로 뽑아낸 값을 계속 좌표로 착각한다... 정렬 기준임!!!
-) 답 다르게 나왔을 때 제발 침착해! (엄청 왔다갔다거리며 디버거 찍는다) : 차분히 코드 순서대로 읽으면서 디버그 포인트 잡기 (겸사 겸사 코드 점검)
+) 답 맞게 나왔어도 디버거로 동작 확인 후 제출 


(오류 내용)
- Index Error : 나 이제 N, M 실수도 하네...가지가지... 그래도 급하게 oob 추가 안하고 '나면 안나는데 왜 나지...?' 하고 생각한건 칭찬...
    => N, M 은 제출 전 꼭 한번더 검토
- delta 는 꼭 한번씩 잘못쓰네...
- BFS 분기 처리: 목적지 도착 못했어도 v return 했어야함
- razor의 v 배열은 실제로 공격 관련 외에도 방문 조사했던 곳도 표시되어있음 -> nv 만들어서 경로내 좌표만 v 표시해줌
*** 공격자는 공격받지 않는다는 조건 razor(), bomb()에서 모두 빠트림 (1차때도 했던 실수)
    : '시작점 별도 처리' 실수

[시간/공간 복잡도]
- 예상한 복잡도)
- 실제 복잡도)

[EdgeCase]
- 고려한 Edge Case)
- 고려하지 못한 Edge Case)
"""


from collections import deque

# [0]
N, M, K = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
did = [[0]*M for _ in range(N)]

# [1]
def select_weak():  # 변경하면 strong도 같이 변경해줘야함
    tmp = []
    for i in range(N):
        for j in range(M):
            if arr[i][j] > 0 :
                tmp.append((arr[i][j], -did[i][j], -(i+j), -j, i, j)) # 공격력, 공격 turn

    ret = min(tmp)
    return ret[-2], ret[-1]




def select_strong(): # 변경하면 weak도 같이 변경해줘야함
    tmp = []
    for i in range(N):
        for j in range(M):
            if arr[i][j] > 0 :
                tmp.append((arr[i][j], -did[i][j], -(i+j), -j, i, j)) # 공격력, 공격 turn

    ret = max(tmp)
    return ret[-2], ret[-1]


def razor(si, sj, ei, ej): # BFS
    # [0]
    q = deque()
    v = [[-1]*M for _ in range(N)]

    # [1]
    q.append((si, sj))
    v[si][sj] = (si, sj)

    # [2]
    while q:
        ci, cj = q.popleft()

        # 종료 조건 : 만나면 바로 종료 (방향은 보장됨) (?)
        if (ci, cj) == (ei, ej) :
            return v

        for di, dj in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            ni, nj = (ci+di)%N, (cj+dj)%M

            # 방문
            if v[ni][nj] != -1:
                continue

            # 부서진 포탑
            if arr[ni][nj] == 0 :
                continue

            q.append((ni, nj))
            v[ni][nj] = (ci, cj) # 역추적 위함

    return v


def bomb(si, sj, ei, ej):
    v = [[-1]*M for _ in range(N)]

    for di, dj in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
        ni, nj = (ei+di)%N, (ej+dj)%M

        if (ni, nj) == (si, sj):
            continue
        if arr[ni][nj] > 0 :
            v[ni][nj] = 1
    return v


def ready():
    for i in range(N):
        for j in range(M):
            if arr[i][j] > 0 and v[i][j] == -1:
                arr[i][j] += 1

debug = 0
for turn in range(1, K+1):

    # 1. 공격자 선정
    si, sj = select_weak()

    # 2. 대상자 선정
    ei, ej = select_strong()

    # 종료 조건
    if (si, sj) == (ei, ej):
        break
    debug = 0

    # 3. 공격 (레이저/폭탄)
    did[si][sj] = turn
    arr[si][sj] += (M+N)
    val = arr[si][sj]

    v = razor(si, sj, ei, ej)
    nv = [[-1]*M for _ in range(N)]
    if v[ei][ej] != -1 :
        arr[ei][ej] = max(0, arr[ei][ej]-val)
        ci, cj = ei, ej
        while True :
            ci, cj = v[ci][cj]
            if (ci, cj) == (si, sj):
                break
            nv[ci][cj] = 1
            arr[ci][cj] = max(0, arr[ci][cj]-val//2)
        v = nv
        debug = 1
    else:
        v = bomb(si, sj, ei, ej)
        arr[ei][ej] = max(0, arr[ei][ej] - val)

        for ci in range(N):
            for cj in range(M):
                if arr[ci][cj] > 0 and v[ci][cj] == 1:
                    arr[ci][cj] = max(0, arr[ci][cj]-val//2)
        debug = 2

    v[si][sj] = 1 # 공격자는 유관
    v[ei][ej] = 1 # 대상자도 유관

    # 4. 정비
    ready()
    debug = 3


# [2]
# ans = -1
# for i in range(N):
#     for j in range(M):
#         if arr[i][j] > ans :
#             ans = arr[i][j]
# # print(max(list(map(max, arr))))
# print(ans)
print(max(map(max, arr)))
# print(min(map(min, arr)))
# print(sum(map(sum, arr)))
# [1] arr의 각 행의 max 값을 구해서
# [2] (Iterable을 만들고)
# [3] 해당 Iterable의 최대값
#   => 전체 격자 중 최대값
