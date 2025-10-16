"""
한줄평:
- 전처리가 Main 만큼이나 중요한 문제 => 반드시 손구상 꼼꼼히 (새로운 페이지 활용)
- 인덱스로 객체 관리할 때는 삭제하기보다는 removed[idx] 사용!! (유사 : 미생물 연구)

소요 시간) 1시간 30분
타임라인) 이해 및 구상 : 20분 (풀었던 문제니까...) - 구현 : 분  - 디버깅 : 분
사용한 알고리즘)

[구상]
+) 조건 및 분기 체크를 move_all()과 move() 각각으로 적절히 나누어주니 실수도 줄고 가독성 굿
-) 전처리가 중요한 문제인데, 자료구조 칸에 맞추려고 그 만드는 과정 자세히 안써줌
 => 전처리가 하나의 기능만큼 복잡하거나 어려우면 무조건 페이지 넘겨서 별지에 따로 로직+그림 그리기

[구현]
+) 자료구조 동기화 자주 실수하니까 각 함수마다 적어주고, 주석도 틈틈히 달아줌
-) 1-based index/0-based index 할거면 모든 자료구조에 해줘야지...일부에만 하면 어떡해..
-) 3차원 리스트 만드는거 아직도 헷갈리는거 실화냐..
   [ [  [] for N ] for _ N   ]
-) 달팽이 전처리 엄청엄청 오래걸리고 실수 多 : 손구상 꼼꼼히 안해서!


[디버깅]
+)
-)

(실행 전 발견)
- 정방향 리스트의 참조값 si, sj -> lst[-1] 로 수정
- arr <- narr
- players[idx] 해야하는데 입력 또받음

(실행 후 발견)
- 마지막 line에서 flag 처리 해줘야함 ...
- 점수에 turn 안곱해줌

(디버거 발견)
- 달팽이 list : 경계값들 확인이 어렵... 결국 디버거 돌려서 꾸역꾸역 맞춤 (다음엔 경계값을 미리 메모하고 시작)
 => 전처리 로직을 점검하고 메모+한번에 수정 햇어야하는데 (찔끔 수정 -> 디버거 -> 찔끔 수정 -> 디버거 ...) 반복
- tree_map : 1-based index 실수...
- ******************* 도망자 -> 술래 이동인데 아예 문제를 잘못 읽음 : 진짜 대박이다 ㄷㄷ 


[시간/공간 복잡도]
- 예상한 복잡도)
- 실제 복잡도)

[EdgeCase]
- 고려한 Edge Case)
- 고려하지 못한 Edge Case)
"""


# [0]
N, M, H, K = map(int, input().split())

delta = [(0, -1), (-1, 0), (0, 1), (1, 0)] # ←, ↑, →, ↓

# 도망자
players = [] # info
arr = [[[] for _ in range(N)] for _ in range(N)] # map : idx 저장
for idx in range(M): # 0 based
    i, j, d = map(int, input().split())

    if d == 1 :  # 좌우
        players.append((i-1, j-1, 2)) # 0 based
        arr[i-1][j-1].append(idx) # 0 based

    else: # 상하
        players.append((i-1, j-1, 3)) # 0 based
        arr[i-1][j-1].append(idx)

removed = [False]*M

# 나무
tree_map = [[False]*N for _ in range(N)]  # 불변
for _ in range(H) :
    i, j = map(int, input().split())
    tree_map[i-1][j-1] = True # 0 based


# 술래 (** 달팽이 좌표 전처리)
si, sj, sd = N//2, N//2, 1
lst = []
rev_lst = [] # 방향 반전되서 저장됨 주의

cnt_mx = 1
flag = False
while (si, sj) != (0, 0):
    di, dj = delta[sd]
    for cnt in range(1, cnt_mx+1):
        si += di
        sj += dj

        lst.append((si, sj, sd))
        rev_lst.append((si, sj, (sd+2)%4)) # 정방향으로 조회하고 넣기를 반대로 넣어주기

    # # 유의 : cnt_mx 끝에서 방향 회전
    lst[-1] = (lst[-1][0], lst[-1][1], (lst[-1][2]+1)%4) # 시계
    # rev_lst[0] = (rev_lst[0][0], rev_lst[0][1], (lst[-1][2]-1)%4) # 반시계
    # rev_lst[0] = (rev_lst[0][0], rev_lst[0][1], (rev_lst[0][2]-1)%4) # 반시계

    sd = (sd+1)%4
    if flag :
        if cnt_mx == N-1 : continue
        cnt_mx += 1
        flag = False
    else:
        flag = True

# print(lst)
# print(rev_lst)
# 시작좌표, 끝좌표 중복으로 담김: 시작좌표는 lst 방향거(따로 추가 X: 모듈러 사용), 끝좌표는 rev_lst 방향거 사용해야함
lst = lst[:-1] + rev_lst[::-1]+[(N//2, N//2, 1)]
debug = 0

# [1]
def oob(ni, nj):
    return not (0 <= ni < N and 0 <= nj < N)


def move(pi, pj, pd):
    '''
    해당 도망자를 조건/규칙에 맞게 이동/이동X 하는 함수
    :param pi:
    :param pj:
    :param pd:
    :return:
    '''

    ni, nj = pi+delta[pd][0], pj+delta[pd][1]

    if not oob(ni, nj):
        if (ni, nj) == (si, sj) :
            return pi, pj, pd
        else:
            return ni, nj, pd
    else:
        nd = (pd+2)%4
        ni, nj = pi + delta[nd][0], pj + delta[nd][1]

        if (ni, nj) == (si, sj):
            return pi, pj, nd # *********** pd 아님 주의 : 방향 전환은 확정된 조건임
        else:
            return ni, nj, nd


def move_all(si, sj):
    '''
    술래와의 거리가 3 이하인 도망자를 이동시키는 함수
    :param si, sj: 술래 위치
    :return: X
    '''
    global arr

    narr = [[[] for _ in range(N)] for _ in range(N)]
    for idx in range(M):
        if removed[idx] :
            continue
        pi, pj, pd = players[idx]

        if abs(si-pi) + abs(sj-pj) <= 3:
            ni, nj, nd = move(pi, pj, pd)

            players[idx] = (ni, nj, nd) # info
            narr[ni][nj].append(idx) # map

    arr = narr


def catch(si, sj, sd):
    '''
    도망자를 잡는 함수
    :return:
    '''
    scr = 0
    di, dj = delta[sd]
    for cnt in range(3):
        ni, nj = si+di*cnt, sj+dj*cnt

        if oob(ni, nj):
            break
        if tree_map[ni][nj] :
            continue

        if arr[ni][nj] :
            scr += len(arr[ni][nj])
            for idx in arr[ni][nj]: # info
                removed[idx] = True
            arr[ni][nj] = [] # map

    return scr

## MAIN ##
ANS = 0
L = len(lst)
si, sj, sd = N//2, N//2, 1
for turn in range(1, K+1):

    # 1. 도망자 이동
    move_all(si, sj) # players, arr 변화
    debug = 1

    # 2. 술래 이동
    si, sj, sd = lst[(turn-1)%L]
    debug = 0

    # 3. 도망자 잡기
    scr = catch(si, sj, sd)
    ANS += turn*scr # removed, arr 변화
    debug = 2


# [2]
print(ANS)
