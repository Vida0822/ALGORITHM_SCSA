"""
한줄평:

소요 시간) 2시간 10분
타임라인) 이해 및 구상 : 20분(너무 짧..) - 구현 :60분 (개오바 너무 김)  - 디버깅 : 60 분
사용한 알고리즘)

[구상]
+) 솔직히 집중 안되서 대충했다 -> 구현 때 훨씬 시간 오래 걸린듯
+) 메두사 시야 로직 생각하면서 player_arr 만드는걸로 구상 변경한거 굿
-) 보는걸 시도하는 로직과 실제로 보는 로직이 거의 차이나지 않기 때문에 이런 경우 하나의 함수로 통일하고,
  갱신된 배열을 사용하냐/마냐 & 개수 따로 세기로 로직 구상을 미리 했어야 했음
   ㄴ TRY/REAL 을 구분하는 건 두 로직 및 정답 처리가 많이 차이날 때
-) 이동 때 '동시 이동 -> narr 필요' 미리 체크 X : 구현 때 버벅
-) 전사 쪽 가림 처리가 핵심인 문제인데, 그쪽 로직을 제대로 구상 X -> dirs 설정에 디버깅 엄청 소요했고, 결국 그림 하나하나 재구상함
=> 문제를 읽으며 어디를 main으로 했는지, 어디가 출제자의 핵심 의도가 담겨져 있는지 파악하고, 그 부분은 구현이 까다롭기 때문에 손구상 꼼꼼히
-) 사전 종료 조건 구상 대충 : 사전 종료는, 어디서 체크하고 어디서 종료시키는지가 가장 중요하다.

[구현]
+) map, info 동기화는 이제 어느정도 하는 듯..!
+) 왠일로 look_up 안틀렸지... delta&lookup은 오래 걸리더라도 일일히 (화살표 그리기 + 숫자표시 + 구현때는 생각하지 말고 바로 옮기기)하는게 굿

[디버깅]
-) 답을 각각 출력하는거는 오히려 어디가 잘못됐는지 디버깅하기 쉽다 : 전부 보려하지 말고 이상한 결과값 나오는 함수부터 확인
-) 또 하나 고치고 실행하네...
-) 나 v 배열을 진짜 안보네... 가림 처리 이상한데 눈치 못채는거 ㄹㅈㄷ
-) 문제 함수를 특정한다기보단, 문제 발생하면 막 여기저기 보는 느낌? 각각 실행하면서 어디가 문제일지 좁혀야지 계속 전체를 보면 X
-) 확실하게 확인하고, 맞고 틀리고 확신하고 다음 함수봐야지 왜 같은 함수를 계속 다시 보지..?

(오류 내용)
1. move_medusa() :
1) route에 추가할 때 튜플 형태가 아니라 [i, j] 형태로 넣어줌 (이거 실수 多)
2) 이동 루트에 시작점 포함 (ans 개수 다름)

2. move_all()
1) 상태 체크 빼먹음: 기절? -> 상태값은 손구상 때 반드시 어디서 체크하는지 mapping
2) if v[ci][cj] == 1: continue -> 계속 실수하는거: 이동하지 않는 객체를 narr에 넣어주지 않음


[시간/공간 복잡도]
- 예상한 복잡도)
- 실제 복잡도)

[EdgeCase]
- 고려한 Edge Case) 메두사 시작 위치가 도착 위치 ?
- 고려하지 못한 Edge Case)
"""


from collections import deque

# [0]
N, M = map(int, input().split())

# 메두사 정보
si, sj, ei, ej = map(int, input().split())

# 전사 정보
inpts = list(map(int, input().split()))
players = []
player_arr = [[[] for _ in range(N)] for _ in range(N)]

idx = 0
for t in range(0, 2*M-1, 2):
    i, j = inpts[t], inpts[t+1]
    players.append((i, j))
    player_arr[i][j].append(idx)
    idx += 1

removed = [False]*M

# 마을 지도
wall_arr = [list(map(int, input().split())) for _ in range(N)]

delta = [(-1, 0), (1, 0), (0, -1), (0, 1)]
delta2 = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

dir_map = [(7, 0, 1), (5, 4, 3), (7, 6, 5), (1, 2, 3)]  # lookup

debug = 0

# [1]
def oob(ni, nj):
    return not (0 <= ni < N and 0 <= nj < N)


def move_medusa(si, sj, ei, ej):
    '''
    메두사 이동 경로 반환
    '''
    # [0]
    q = deque()
    v = [[0]*N for _ in range(N)]

    # [1]
    q.append((si, sj, []))
    v[si][sj] = 1

    while q:
        ci, cj, route = q.popleft()

        # 종료 조건
        if (ci, cj) == (ei, ej):
            return route

        for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            ni, nj = ci+di, cj+dj

            # 범위밖, 미방문
            if oob(ni, nj) or v[ni][nj] != 0 :
                continue

            # 조건 : 벽? (벽은 메두사때만 활용)
            if wall_arr[ni][nj] == 0 :
                q.append((ni, nj, route+[(ni, nj)]))
                v[ni][nj] = 1
    else:
        return []


def warrior_see(mi, mj, wi, wj, v, dr):
    # delta2 = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

    # [0]
    q = deque()

    # 방향lst 결정 : 메두사와 전사 상대 위치 (delta2 기준)
    # delta2 = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    dirs = []
    if dr == 0 : # 상
        dirs.append(0)
        if wj < mj:
            dirs.append(7)
        elif wj > mj:
            dirs.append(1)
    elif dr == 1:  # 하
        dirs.append(4)
        if wj < mj :
            dirs.append(5)
        elif wj > mj:
            dirs.append(3)
    elif dr == 2 : # 좌
        dirs.append(6)
        if wi < mi:
            dirs.append(7)
        elif wi > mi:
            dirs.append(5)
    else:  # 우
        dirs.append(2)
        if wi < mi:
            dirs.append(1)
        elif wi > mi:
            dirs.append(3)

    # [1]
    q.append((wi, wj))
    v[wi][wj] = 2 # 처음 전사는 메두사 시야 o

    while q:
        ci, cj = q.popleft()

        for dr in dirs:
            di, dj = delta2[dr]
            ni, nj = ci+di, cj+dj

            # 범위밖, 미방문
            if oob(ni, nj) or v[ni][nj] == 2 :
                continue

            v[ni][nj] = 2
            q.append((ni, nj))


def medusa_see(d, mi, mj):

    # BFS : 메두사 시야 표시
    # [0]
    q = deque()
    v = [[0]*N for _ in range(N)]
    dirs = dir_map[d]

    # [1]
    q.append((mi, mj))
    v[mi][mj] = 1

    # [2]
    while q:
        ci, cj = q.popleft()

        for dr in dirs:
            di, dj = delta2[dr]
            ni, nj = ci+di, cj+dj

            # 범위밖 or 미방문
            if oob(ni, nj) or v[ni][nj] != 0 :
                continue

            # 조건: 전사 O ?
            if len(player_arr[ni][nj]) >= 1:
                warrior_see(mi, mj, ni, nj, v, d) # v 배열 변경

            v[ni][nj] = 1
            q.append((ni, nj))

    v[mi][mj] = 0
    return v


def check(v):
    cnt = 0
    for i in range(N):
        for j in range(N):
            if len(player_arr[i][j]) >= 1 and v[i][j] == 1:
                cnt += len(player_arr[i][j])

    return cnt


def move(ci, cj):
    '''
    조건에 따라 전사 1명을 이동시키는 함수
    :param ci:
    :param cj:
    :return:
    '''
    # try1
    cdist = abs(mi-ci)+abs(mj-cj)
    mn = (-1, -1)
    for dr in range(4):
        di, dj = delta[dr]
        ni, nj = ci+di, cj+dj

        if oob(ni, nj) or v[ni][nj] == 1 :
            continue

        ndist = abs(mi-ni)+abs(mj-nj)

        if cdist > ndist: # 더 가까워지면
            mn = (ni, nj)
            cdist = ndist

    if mn == (-1, -1):
        return ci, cj
    else:
        ci, cj = mn

    # TRY 2
    mn == (-1, -1)
    cdist = abs(mi - ci) + abs(mj - cj)
    for dr in ((2, 3, 0, 1)):
        di, dj = delta[dr]
        ni, nj = ci + di, cj + dj

        if oob(ni, nj) or v[ni][nj] == 1:
            continue

        ndist = abs(mi - ni) + abs(mj - nj)

        if cdist > ndist:
            mn = (ni, nj)
            cdist = ndist

    if mn == (-1, -1):
        return ci, cj
    else:
        return mn[0], mn[1]


def move_all(mi, mj):
    '''
    모든 전사들을 이동시키는 함수 (상태체크, 자료구조 변경, 정답 처리 여기서)
    :return:
    '''
    global player_arr

    dist = 0
    att = 0
    narr = [[[] for _ in range(N)] for _ in range(N)]

    for idx in range(M):
        # 상태 체크 1: 없어진 기사?
        if removed[idx] :
            continue

        ci, cj = players[idx]

        # 상태 체크 2: 시야 내 기사?
        if v[ci][cj] == 1 :
            narr[ci][cj].append(idx)
            continue

        ni, nj = move(ci, cj)

        # 정답 처리1 : 거리 갱신
        dist += abs(ni-ci)+abs(nj-cj)

        # 상태 체크 2: 메두사 공격?
        if (ni, nj) == (mi, mj):
            att += 1
            removed[idx] = True
        else:
            players[idx] = (ni, nj)  # info
            narr[ni][nj].append(idx)  # map

    player_arr = narr
    return dist, att


## MAIN ##
route = move_medusa(si, sj, ei, ej)
if not route :
    print(-1)
else:
    # MAIN
    # 1. 메두사 이동
    for mi, mj in route :

        # 종료 조건(도착하면 즉시 종료)
        if (mi, mj) == (ei, ej):
            print(0)
            break

        # 전사 공격
        if len(player_arr[mi][mj]) >= 1 :
            for idx in player_arr[mi][mj]:
                removed[idx] = True
            player_arr[mi][mj] = [] # map 변경

        # 2. 메두사 시야
        mx = (-1, -1)
        for d in range(4): # 상하좌우
            v = medusa_see(d, mi, mj)

            cnt = check(v)
            if cnt > mx[0] :
                mx = (cnt, d)

        ans2 = mx[0]
        v = medusa_see(mx[1], mi, mj)

        # 3. 전사 이동 & 공격
        ans1, ans3 = move_all(mi, mj)

        # 4. 정답 출력
        print(ans1, ans2, ans3)


