"""
한줄평:
- 확실히 잠깐 쉬고 다시 차근히 보니 오류가 잘 보인다! (화장실 갔다오고 5분만에 잡음)
- 분기가 많이 되는 시뮬레이션은 수형도를 그리면 함수화도 보이고 실수가 줄어든다
- 디버깅 할때는 여기저기 보기보다 전체 순서 or 함수 흐름 대로 보는게 좋을 듯
- 고치고 바로 실행 X -> 최소 3개는 찾는다는 생각으로 쭉 읽기
- 찜찜한 부분, 의심가는 부분을 더 집중해서 보자 (같은데 계속 다시보기보다는)


소요 시간) 1시간 20분
타임라인) 이해 및 구상 : 15 분 - 구현 : 45분  - 디버깅 : 20분
사용한 알고리즘)

[구상]
+) 분기가 많이 되는 시뮬레이션은 수형도를 그리면 실수가 줄어든다
-) 이번거 함수화가 깔끔히 떨어지지 않아 구현 도중 수정 많았다 (억지로라도 함수화는 구분해놓는게 좋을듯)

[구현]
+) arr 이름을 gun_arr, player_arr로 쓰니 안헷갈리고 좋았다
  => arr이 진짜 딱 하나만 있는 문제 아닌 이상 변수명 저런식으로 짓자
+) 리스트로 info 관리하니까 확실히 수정이 편하다..
-) 2차 풀이인데 구현 시간이 45분이면.... 정말 느린거다... ㅠㅠ
-) 함수화 구상을 꼼꼼히 하지 않아 여기저기 수정이 많았다.
-) 컴파일 에러가 많다


[디버깅]
+) 확실히 잠깐 쉬고 다시 차근히 보니 오류가 잘 보인다!
+) 그나마...디버거 덜돌리고 찾은 오류가 많다..
-) 나 i, j 실수 엄청 하는 편이었구나... 앞으로 검증 루틴에는 i, j 유의해서 보도록 하자
 => 특히 ci, cj / ni, nj 는 여기저기 사용되기 때문에 왠만하면 한 함수 내에서 중복해서 사용하지 말자

(오류 내용)
- 3차원 배열 사용할 때 '좌표 내' 리스트에 값을 넣어줘야함을 계속 까먹음 (디버거 돌리고 알았음...)
  ex) arr.append(idx) (x) -> arr[i][j].append(idx)
 => 전처리는 동작 확인 전 디버거로 미리 확인해봐도 좋을 듯 (시간 절약)
- 총이 없는걸 공격력이 0인 총을 가지고 있다고 처리 => 조건 추가 : if pe > 0 --> 여기저기에...
- 'item not in list' : 자료구조 동기화 부분 확인 필요 (이건 보통 다른 함수 로직 문제임)
- 1-based 하면서 자료구조 전체에 적용 까먹는 경우 多 : info, arr 모두 적용 했어야

[시간/공간 복잡도]
- 예상한 복잡도) O(K*M) = O(K*N**2) = 500*400 = 200000
- 실제 복잡도)

[EdgeCase]
- 고려한 Edge Case) winner 또는 loser가 삭제처리 됨
  => 일단 배열에 중복해서 넣어놓고, 길이 2 이상일 때 처리해두독 하여 자료구조 동기화 편하게
- 고려하지 못한 Edge Case)
"""


# [0]
N, M, K = map(int, input().split())
ipt_arr = [list(map(int, input().split())) for _ in range(N)]

delta = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # ↑, →, ↓, ←
ds = ['↑', '→', '↓', '←']

# 총 정보
gun_arr = [[[] for _ in range(N)] for _ in range(N)]
for i in range(N):
    for j in range(N):
        if ipt_arr[i][j] > 0 :
            gun_arr[i][j].append(ipt_arr[i][j])

# 플레이어 정보 (0-based)
players = []
player_arr = [[[] for _ in range(N)] for _ in range(N)]

for idx in range(M):
    i, j, d, s = map(int, input().split())
    player_arr[i-1][j-1].append(idx)
    players.append([i-1, j-1, d, s, 0])

debug = 0

# [1]
def oob(ni, nj):
    return not (0 <= ni < N and 0 <= nj < N)



def move(ci, cj, cd):
    # TRY1
    ni, nj = ci+delta[cd][0], cj+delta[cd][1]
    if not oob(ni, nj) :
        return ni, nj, cd
    else:
        nd = (cd+2)%4
        ni, nj = ci+delta[nd][0], cj+delta[nd][1]
        return ni, nj, nd


def get_gun(idx, ni, nj) :
    # gun_arr, players 변화
    if not gun_arr[ni][nj] :
        return

    pe = players[idx][-1]
    if pe > 0 :  # DEBUG ! 공격력이 0인건데 총으로 들어감
        gun_arr[ni][nj].append(pe)

    gun_arr[ni][nj].sort()

    pe = gun_arr[ni][nj].pop() # map
    players[idx][-1] = pe  # info


def fight(ni, nj):
    # gun_arr, player_arr, players 변화

    # 1. 승/패 가리기 및 점수 처리
    # gun_arr, player_arr, players 변화
    player_arr[ni][nj].sort(
        key = lambda idx: (sum(players[idx][-2:]), players[idx][-2])
    )

    win_idx = player_arr[ni][nj][1]
    lose_idx = player_arr[ni][nj][0]  # 두명이 최대

    ans[win_idx] += sum(players[win_idx][-2:]) - sum(players[lose_idx][-2:])

    # 2. 진 플레이어 처리
    # 총 내려놓기
    pe = players[lose_idx][-1]
    if pe > 0 :
        gun_arr[ni][nj].append(pe)
    players[lose_idx][-1] = 0

    # 이동하기
    ci, cj, cd = players[lose_idx][:3]
    while True :
        ni, nj = ci+delta[cd][0], cj+delta[cd][1]

        if oob(ni, nj) or len(player_arr[ni][nj]) >= 1 :
            cd = (cd+1)%4
        else:
            # players[idx][:3] = [ni, nj, cd]  # info
            players[lose_idx][:3] = [ni, nj, cd]  # info
            player_arr[ci][cj].remove(lose_idx) # map
            player_arr[ni][nj].append(lose_idx)
            break

    # 총 줍기
    li, lj = players[lose_idx][:2] # 여기서 진 플레이어 index로 바꿔버려서 밑의 이긴 사람 위치가 이상함
    get_gun(lose_idx, li, lj)

    # 3. 이긴 플레이어 처리
    wi, wj = players[win_idx][:2]
    get_gun(win_idx, wi, wj)


## MAIN ##
ans = [0]*M
for turn in range(1, K+1):
    for idx in range(M):

        # 1. 이동 시키기
        ci, cj, cd, _, _ = players[idx]
        player_arr[ci][cj].remove(idx) # 지우고 시작

        ni, nj, nd = move(ci, cj, cd)
        players[idx][:3] = [ni, nj, nd]  # info
        player_arr[ni][nj].append(idx)  # map (겹쳐도 넣어주기)
        debug = 0

        # 2. 플레이어 여부 확인
        # 플레이어 없으면
        if len(player_arr[ni][nj]) < 2:
            get_gun(idx, ni, nj)  # gun_arr, players 변화

        # 3. 있으면 대결 및 상태 변경
        else:
            fight(ni, nj)  # gun_arr, player_arr, players 변화
        debug = 1

print(*ans)

