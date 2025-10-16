"""
한줄평:
1. 처음으로 히든 테케 틀렸을 때 디버깅했다!!
2. 급하게 추가한 조건 분기는 히든 테케에 취약하다 !!
3. 집중하니까 히든 테케 틀린거 5분만에 찾았자나(물론 그 사이에 급하게 2번 제출한건 문제가 있다...)!!
 => 히든 테케 틀려도 침착하고, 차분히 로직 점검하자 (자신감!)


소요 시간) 1시간 30분
타임라인) 이해 및 구상 : 20 분 - 구현 : 30분  - 디버깅 : 50분 (제출 3회)
사용한 알고리즘)

[구상]
+) 각 단계에서 갱신되는 자료 구조를 적어주니 확실히 실수가 준다. 
+) 항상 헷갈리는 끝 좌표 포함 여부를 미리 적어두어 실수 x
-) 예상치 못한 완팀이 많았고, 이동 시도를 하지 않는 조건(상태 체크)을 손 구상에 적지 X -> 그대로 실수로
   => 상태 관련 자료구조 (ex. removed) 는 언제 어디서 체크해야하는지 항상 손구상엥 적어두어야함
     (상태 관련 자료구조가 있다면, 반드시 어디선가 이거로 상태 확인 로직이 들어가야함)
     => 삭제를 하지 않는 대신 idx 관련 처리 모든 곳에서 그냥 맘편히 상태 체크 로직 넣어도 나쁘지 X
-) 또... BFS 템플릿이라고 구조 제대로 안짬... 밀릴 때 이어져있는 애들 다같이 밀려버림... (실제 그 방향이 없더라도)
 => 이 문제는 '연쇄'라는 핵심 로직을 BFS로 응용해서 구현하는 것이 관건인 문제인데, 그 핵심 로직인 BFS를 대충 구상해서 생긴 문제
-) 리턴값 좀 애매하게 정해서 많이 바꿨다.
-) 무조건 중간에 리턴되어야 하는 로직은 아래 절대 닿지않는 return 문 추가해서 디버깅 쉽게 하자

[구현]
+) 확실히 info 는 list로 관리하는게 굿 (슬라이싱으로 정보 갱신 가능)
+) 형식적이어도 리턴 형식은 통일해주는거 good
-) players.append()는 개수가 정해져있지 않을 때만 사용하자 -> 왠만하면 players[idx] = [~info~] 형태
    ㄴ 기껏 갯수만큼 만들어놓고, append하면 오류남
-) 패딩 오랜만에 하니까 실수 : 행쪽 붙여줄 때 열 크기만큼 만들어줘야함
-) 안전하게 하려고한건 맞지만... 완탐을 너무 많이 하는 느낌... 그렇게 하더라도 시간 복잡도 정도는 체크했어야


[디버깅]
+) 구현 후 실행 안하고 코드 전체 점검하는거 너무 좋다! 중간 중간 주석도 달면서 이해 up & 로직 이상한거 잡기
+) 현호님 말씀대로 하나만 보지 않고, 전체 자료구조를 오픈 TC와 비교하면서 동작확인 (arr만 보기, info 만 보기 절대 X)
 => 무조건 자료구조 다 봐야함 (***)

(오류 내용)
* 실행 전 발견
- 체력 '이상' 함정 설치시 removed 처리인데 초과로 처리 ㄷㄷ  (이거 진짜 위험했다 : 나는 turn, cnt 이상 이하 많이 틀리니까 히든 때 이부분 염두)
- 'energy[idx] -= cnt' 빠트림: 실제로 체력 깎였으면 다음 턴을 위해 enerny[idx]에서도 감소시켜줬어야함

* 실행 후 발견
1. real_move() - 'cannot unpack non-iterable int object'
  -> 오류는 여기서 났지만 try_move()가 문제!! 실제로 int 가 들어있는 0 가 set에 들어감
    : player_arr[ci][cj] 가 idx 적혀있는 위치인데, idx로 player_arr[ni][nj]를 넣어줌

2. player_arr
- 전처리: 직사각형 표시해줘야하는데 시작점만 표시
- 지우고 쓰기(****) : 해당 위치에 다른 player의 idx가 적혀있을 수 있는데 기존 위치라는 이유로 지워버림 (지우는건 진짜 왠만하면 내 레벨에선 하지말자...)
 ㄴ 근데 어디봐...? 값이 이동 안하는게 문제면 try_move()가 아니라 실제로 arr을 변경하는 real_move(), get_damage() 봐야지
   : 변경되는 자료 구조 써놓는 이유는 구현 때 실수 안하려는 것도 있지만, 디버깅 때 갱신되는 위치 파악하는 용도도 있다 **
 ㄴ 그리고.. 운을 바라고 이거저거 손대면서 실행하지 말고...구상 다시했어야지...

3. bfs(): 핵심 로직 구상 오류
- 무조건 인접해야 밀리는걸로 처리함 ... 실제 밀리는 방향이 겹치지 않으면 인접해도 밀리지 않는다!!
=> 다른 인덱스일때는, 인접한거 조회 방향이 일치할 때만 재검사 대상으로 포함시켜줌 (같은 인덱스는 바로 추가)
 ㄴ 요거 좀 급하게 해서 애매했다... 그래도 분기 리펙토링한건 good

4. get_damage()
- 조건 빠트림 *******: '명령을 받은 기사는 데미지를 받지 않는다' (와 문제 조건 빠트린건 치명적이다..)
=> 명령받은 idx 매개변수로 전달해줌

5.  ****** real_move() : 'if removed[idx] : continue' ********
- 전체 인덱스 완탐하면서, 모든 인덱스에 대해 좌표에 새로 그려줌 (arr 삭제에서 narr 표시로 구상 변경함에 따라 변경된 로직) 
=> 이렇게 하면, 이미 삭제된 애들도 info에 남아있기 때문에 arr에 다시 추가됨!!
 ㄴ 구상을 바꾼 부분은 구멍이 나오기 마련이다: 특히 idx 조회하는 로직에서 **상태 체크**는 무조건 염두 (안전하게 여기저기 추가하고, 히든 TC 틀리면 무조건 이거 먼저 체크하자)

6. main : '# if removed.count(True) == M :'
-> 안시킨 가지치기 절대 NO!!!!!!!!!! 오류의 원인은 아니었지만 엄청 위험했다 (문제에서 시킬때만 고) 

[시간/공간 복잡도]
- 예상한 복잡도) O(K)*O(N^2 + N^2 + N^2)  = O(100) * O(40^2) = O(160000) -> 여유 ! (근데 이거 미리 계산했어야지...)
- 실제 복잡도)

[EdgeCase]
- 고려한 Edge Case)
- 고려하지 못한 Edge Case)
"""


from collections import deque

# [0]
N, M, K = map(int, input().split())

# 벽, 함정 (1-based)
wall_arr = [[2]*(N+2)]+[[2]+list(map(int, input().split()))+[2] for _ in range(N)]+[[2]*(N+2)]

# 플레이어 (1-based)
players = [0]*(M+1)
player_arr = [[0]*(N+2) for _ in range(N+2)]

energy = [0]*(M+1)
damaged = [0]*(M+1)
removed = [False]*(M+1)
for idx in range(1, M+1):
    i, j, h, w, k = map(int, input().split()) # 1-based

    players[idx] = [i, j, h, w]
    energy[idx] = k
    for r in range(i, i+h):
        for c in range(j, j+w):
            player_arr[r][c] = idx


# 명령 (1-based)
orders = [[-1]]+[list(map(int, input().split())) for _ in range(K)]

delta = [(-1, 0), (0, 1), (1, 0), (0, -1)]

# [1]
def bfs(si, sj, dr):
    # [0]
    q = deque()
    v = [[0]*(N+2) for _ in range(N+2)]
    grp = []

    # [1]
    q.append((si, sj))
    v[si][sj] = 1
    grp.append((si, sj))

    # [2]
    while q:
        ci, cj = q.popleft()

        for di, dj in ((-1, 0), (0, 1), (1, 0), (0, -1)):
            ni, nj = ci+di, cj+dj

            # 범위 체크 (벽으로 대신) , 미방문
            if wall_arr[ni][nj] == 2 or v[ni][nj] != 0 :
                continue

            # 조건
            if player_arr[ni][nj] != 0 :
                if player_arr[ni][nj] != player_arr[ci][cj] :
                    if (di, dj) == delta[dr]:  # 다른 인덱스고, 같은 방향이면 밀림 (다른 방향이면 영향 X)
                        q.append((ni, nj))
                        v[ni][nj] = 1
                        grp.append((ni, nj))
                else:
                    q.append((ni, nj))
                    v[ni][nj] = 1
                    grp.append((ni, nj))

    return grp


def try_move(idx, dr):
    '''
    해당 기사와 인접해있는 기사들 모두 이동시키는게 가능한지 확인
    :param idx:
    :param dr:
    :return:
    '''

    # 1. 이어져있는 좌표 반환
    si, sj = players[idx][:2]
    grp = bfs(si, sj, dr)

    # 2. 각 좌표에 dr 적용
    mvd_set = set()  # 영향받은 idx
    for ci, cj in grp:
        ni, nj = ci+delta[dr][0] , cj+delta[dr][1]

        # 벽 or 범위 밖
        if wall_arr[ni][nj] == 2 :
            return {} # 형식적이어도 리턴 형식은 통일해주는거 good

        mvd_set.add(player_arr[ci][cj])  # 영향받은 idx

    else:
        return mvd_set


def real_move(mvd_set, dr):
    '''
    영향받은 기사들을 실제로 이동시키는 함수
    => players, player_arr 변화
    :param mvd_set:
    :return:
    '''
    global player_arr

    di, dj = delta[dr]
    narr = [[0]*(N+2) for _ in range(N+2)]

    for idx in range(1, M+1) :
        if idx in mvd_set:
            si, sj, h, w = players[idx]
            ei, ej = si+h, sj+w

            for ci in range(si, ei):
                for cj in range(sj, ej):
                    ni, nj = ci+di, cj+dj # 조건 체크 X (에러나면 안됨)
                    # player_arr[ci][cj] = 0 # 새로 써준애도 지워버림
                    narr[ni][nj] = idx

            players[idx][:2] = [si+di, sj+dj]

        else:
            if removed[idx] : # DEBUG: 삭제된 기사인데 다시 그리기
                continue
            si, sj, h, w = players[idx]
            ei, ej = si + h, sj + w

            for ci in range(si, ei):
                for cj in range(sj, ej):
                    narr[ci][cj] = idx

    player_arr = narr


def get_damage(mvd_set, sidx):
    '''
    영향받은 기사들의 데미지를 누적하는 함수
    =>  # energy, removed, damaged, player_arr 변화
    :param mvd_set:
    :return:
    '''
    global ans

    for idx in mvd_set:
        if idx == sidx:
            continue
        si, sj, h, w = players[idx]
        ei, ej = si + h, sj + w

        cnt = 0
        for ci in range(si, ei):
            for cj in range(sj, ej):
                if wall_arr[ci][cj] == 1 : # 함정
                    cnt += 1

        if energy[idx] <= cnt: # '체력 이상의 데미지'
            removed[idx] = True
            for ci in range(si, ei):
                for cj in range(sj, ej):
                    player_arr[ci][cj] = 0
        else:
            damaged[idx] += cnt
            energy[idx] -= cnt


## MAIN ##
for turn in range(1, K+1): # 사전 종료 O => 기사가 모두 없어짐
    # 1. 이동 시도
    idx, dr = orders[turn]

    # 상태 체크
    if removed[idx]:
        continue

    # 밀림 체크
    mvd_set = try_move(idx, dr) # 변화 X
    debug = 0

    if not mvd_set: # 이동 불가
        continue # 다음 명령

    # 2. 실제 이동
    real_move(mvd_set, dr) # players, player_arr 변화

    # 3. 데미지 처리 ('기사들은 모두 밀린 이후에 데미지를 입게 됩니다')
    get_damage(mvd_set, idx) #  energy, removed, damaged, player_arr 변화

    # # 4. 종료 조건 : 전부 사라졌을 때
    # if removed.count(True) == M : # 1개 남았어도, 계속 명령을 받아서 이동하다가, 함정 때문에
    #     break

# [2]
ans = 0
for idx in range(1, M+1) :
    if not removed[idx] :
        ans += damaged[idx]

print(ans)