"""
한줄평:
1. 자료구조 싹 바꿨지만 성공한 문제
 => 솔직히 아슬아슬하긴 했지만, 아예 망하지는 않는다...자신감을 갖자 !
2. 쓸데없이 효율성 추구하지 말고, 크기가 크지 않다면 완탐하자...

소요 시간)
타임라인) 이해 및 구상 : 20 분 - 구현 : 25 분  - 디버깅 : 50 분
사용한 알고리즘)

[구상]
+) 단계 구분이 잘 되어있지 않은 문제지만, 적절히 분리한 듯
+) 각 자료구조를 idx로 관리한 건 잘한 선택: 애초에 map에 index로 구분해서 주어진다는 말 봤으면 idx 사용했을 생각 바로 하긴했어야...
-) 오픈 TC 보기 힘들다고 제대로 확인 X ...

[구현]
+) 0-based, 1-based 잘 적어주니 실수 안함

[디버깅]
+) 중간에 자료 구조 바꿔야함을 알았을 때, 급하게 여기저기 손대지 않고 조금이라도 손으로 재구상 하고 구현한거 good (그나마 덜 실수하고 당황한듯)
+) 문제 꼬였을 때 급하게 코드 손대지 않고 리프레쉬 한 것
-) 근데 결국 정신없이 여기저기 바꾸긴 함...
-) 튜플을 2차원 배열에 넣었을 때 값 참조 계속 실수
+) move() 조건 리펙토링하면서 디버깅하기 쉬워지고 명료해짐
+) 그나마 디버거 디버깅을 늦게해서 빨리 잡은것 같기도...
-) 급해지니까 또 여기저기 손대기...


(실행 전 발견)
- 우선 순위 자료구조 잘못된

(실행 후 발견)
- 종료조건 빼먹음
- 자료구조 잘못된걸 알았다:
냄새와 사람 이동을 arr에서 동시에 처리해줬는데 사람 이동처럼 narr을 만들어서 사람 이동은 구현이 됐지만 '냄새가 표시되어있어야한다' 가 구현 X
=> 즉, 실제 사람이 위치했는지와 남아있는 냄새가 있는지가 구분이 안됨
=> 떠올린 생각
1. arr에는 냄새만 표시, 플레이어는 리스트로만 관리
2. 냄새 표시하는 v 배열(2차원), 사람 표시하는 arr 배열(3차원), player 리스트 따로 관리
=> BAD : 어차피 새로 이동한 애들 완탐해서 조건 처리해줄거면 players 를 애초에 list로 관리할 필요 X .... 완탐해서 바로바로 이동시켰어야...

- v 배열에 음수값 들어감 : 0이면 없애주는 로직을 해야하는데, 그냥 값만 감소시키고 아직 냄새가 남아있는걸로 처리해 이동도 제대로 X
 => 0되면 튜플을 없애는 로직으로 수정 (값만 빼주는게 아니라)

- i, j 실수 : move() 함수 안에서 ni, nj 를 써야하는데 i, j 를 썼고, 이걸 main에서 쓰고있기에 전역 참조해서 오류 발생 X



[시간/공간 복잡도]
- 예상한 복잡도)
- 실제 복잡도)

[EdgeCase]
- 고려한 Edge Case)
- 고려하지 못한 Edge Case)
"""



# [0]
N, M, K = map(int, input().split())
ipt_v = [list(map(int, input().split())) for _ in range(N)]  # idx 저장
dd = list(map(int, input().split())) # 0-based ※
delta = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)] # 1-based

# 플레이어
players = [-1]*(M+1) # 1-based: 인덱스가 순차적으로 주어지지 않을 때는 미리 크기만큼 만들어 놓아야함
v = [[0]*N for _ in range(N)]
arr = [[[] for _ in range(N)] for _ in range(N)]
for i in range(N):
    for j in range(N):
        if ipt_v[i][j] > 0 :
            idx = ipt_v[i][j]
            players[idx] = (i, j, dd[idx-1])
            v[i][j] = (idx, K)
            arr[i][j].append(idx)

# 우선 순위
priorities = [[0] for _ in range(M+1)] # 1-based idx, 1-based delta (5칸)
for idx in range(1, M+1):
    priority = priorities[idx] # 해당 사람의 우선순위 테이블
    for _ in range(4):
        priority.append(list(map(int, input().split())))

removed = [False]*(M+1) # 1-based idx


# [1]
def oob(ni, nj):
    return not (0 <= ni < N and 0 <= nj < N)


def move(idx): # ******
    '''
    각 플레이어를 조건/우선순위에 맞게 이동할 수 있는 좌표+갱신된 방향을 반환하는 함수
    :return: ni, nj, nd
    '''

    ci, cj, cd = players[idx]
    dirs = priorities[idx][cd]

    # print(turn, idx)

    # 1. 계약 X 칸 찾기
    for d in dirs:
        ni, nj = ci+delta[d][0], cj+delta[d][1]

        if oob(ni, nj):
            continue
        if v[ni][nj] == 0: # DEBUG!! ㄹㅈㄷ...ni, nj 를 i, j 로 적음...
            return ni, nj, d

    # 2. 자기 칸 찾기
    for d in dirs:
        ni, nj = ci+delta[d][0], cj+delta[d][1]

        if oob(ni, nj):
            continue
        if v[ni][nj] and v[ni][nj][0] == idx:
            return ni, nj, d


def move_all(turn):
    '''
    모든 플레이어를 이동시키는 함수: 상태 체크 및 자료 구조 변경
    :return:
    '''

    global arr
    narr = [[[] for _ in range(N)] for _ in range(N)]
    for idx in range(1, M+1):
        if removed[idx]:
            continue
        ni, nj, nd = move(idx)  # 좌표만 반환, check는 여기서
        players[idx] = (ni, nj, nd)  # info
        narr[ni][nj].append(idx)  # map
    arr = narr


def eat():
    for i in range(N):
        for j in range(N):
            if v[i][j] :
                if v[i][j][1]-1 == 0 :
                    v[i][j] = 0
                else:
                    v[i][j] = (v[i][j][0], v[i][j][1]-1)
            if arr[i][j] :
                if len(arr[i][j]) > 1 :
                    mn = min(arr[i][j])

                    for idx in arr[i][j] :
                        if mn < idx :
                            removed[idx] = True
                    arr[i][j] = [mn]
                v[i][j] = (arr[i][j][0], K)




## MAIN ##
debug = 0
for turn in range(1, 1001):

    # 1. 각 player 이동
    move_all(turn)  # players, arr 변경
    debug = 0

    # 2. 중첩 player 한명만 남기기
    eat() # players, arr, v, removed 변경
    debug = 1

    # 3. 종료 조건
    if removed[1:].count(True) == M-1:
        break

# [2]
print(turn if turn < 1000 else -1)


