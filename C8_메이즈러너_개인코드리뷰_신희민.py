"""
한줄평:

<좌표 회전> (시작 좌표: si, sj/ 길이: K)
- 시계 : i, j = si+(j-sj), sj+(K-1)-(i-si)
- 반시계 : i, j = si+(K-1)-(j-sj), sj+(i-si)

ㄴ 도형이랑 달리, 시계는 뒤쪽에 길이 반영/반시계는 앞쪽에 길이 반영


<3차원 배열 복사>
narr = [[lst[:] for lst in row] for row in player_arr]



소요 시간) 1시간 30분
타임라인) 이해 및 구상 : 20 분 - 구현 : 아마 40 분  - 디버깅 : 30분
사용한 알고리즘)

[구상]
+) 참가자들이 있는 격자를 회전 시키기 때문에 info 사용 안하고 격자만 활용한 거 good (안그랬으면 회전 -> info 동기화 했어야...)
+) 확실히 move_all(), move()나누는거 굿
-) 좌표 회전 제대로 모르면서...또 생각 안함 => 나중에 급하게 로직 바꾸느냐 여기저기 구멍 (갱신 위치도 헷갈림)
-) 구상하지 않은 함수화(분리)가 많았다.. 필요한 과정이었지만 왠만하면 구상 때..! 실수 나오기 쉬움


[구현]
-) 좌표 회전 어떻게 하더라...
-) 3차원 배열 복사 어떻게 하더라...
 -> 암기 : narr = [[lst[:] for lst in row] for row in player_arr]


[디버깅]
+)
-)

(오류 내용)
- 좌표 회전이 잘못되어 뒤의 로직에 계속 영향 (출구 좌표가 이동에 영향을 주므로: 거리측정기준 )
 (move() 좌표 이상, rotate() : local variable 오류 ->  무조건 갱신되어야하는 값임을 미리 적어주니, 당황해서 그부분 급하게 수정하지 않고 로직 점검)

1. move()
- 'return ni, nj'
: 계속 반환할 때 최소값(mn)을 반환해야하는데 그냥 ni, nj 를 반환해줌 -> 이거 몇번 실수했다(이건 오류도 안남), 주의


2. rotate()
- 최소 정사각형 잡는 부분 : 정사각형 찾으면 모든 반복문 종료해야하는데, 그냥 break 만 해줘서 다음 행 탐색
 => find_min_square() 함수로 분리 + return 문으로 바꿔줌
ㄴ  나 2차원 배열에서 검사 종료 조건 많이 틀린다 (특히 백트래킹) :  답 안나오면 여기 의심


3. find_min_square()
- 정사각형 길이 설정 오류 : 'for K in range(1, N-1)'
=> swea-서비스영역 문제도 그렇고, 나 한변 길이 체크를 계속 대충하고 넘어가네...?
 ㄴ check()에서 검사 조건을 si<= i <=si+K-1 (**) 까지 했기 때문에,
    K 크기 자체는 N-1(4: 끝좌표)까지 해줘야 끝좌표 (0+N-1)까지 포함
 ==> 반복문 끝변수로는 N을 써줘야함
ㄴ 이거 진짜 조심 : 찾기도 힘들다(불안하면 그냥 oob+조금 크게 주기)


4. 정답 출력
: 1-based 로 입력받아서 내 로직에서 0-based 로 처리하고,
출력을 1-based로 다시하는거 까먹음 (동작 전체 확인하느냐 추가 15분 소요)
=> 출력값이 좌표일 땐 0-based, 1-based 다시 한번 체크

[시간/공간 복잡도]
- 예상한 복잡도)
- 실제 복잡도)

[EdgeCase]
- 고려한 Edge Case)
- 고려하지 못한 Edge Case)
"""
# [0]
N, M, K = map(int, input().split())

# 벽
wall_arr = [list(map(int, input().split())) for _ in range(N)]

# 사람
player_arr = [[[] for _ in range(N)] for _ in range(N)]
for idx in range(M): # 0-based
    i, j = map(int, input().split())
    player_arr[i-1][j-1].append(idx) # 0-based

escaped = [False]*M

# 출구
ei, ej = map(int, input().split())
ei -= 1
ej -= 1

# (급한대로...)
wall_arr[ei][ej] = -1


# [1]
def oob(ni, nj):
    return not (0 <= ni < N and 0 <= nj < N)


def move(ci, cj):
    '''
    조건에 따라 이동/이동X 등 new 좌표 반환하는 함수
    :param ci:
    :param cj:
    :param idx:
    :return:
    '''
    cdist = abs(ei-ci)+abs(ej-cj)
    mn = (cdist, ci, cj)

    # (?) 움직일 수 있는 칸이 2개 이상이라면, 상하로 움직이는 것을 우선시
    # -> 상하가 거리가 똑같으면 어떡해? 그럴수는 없나...
    for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)) : # 방향 우선순위 보장(?)
        ni, nj = ci+di, cj+dj

        # 범위 밖 or 벽
        if oob(ni, nj) or wall_arr[ni][nj] > 0 :
            continue

        ndist = abs(ei-ni)+abs(ej-nj)
        if mn[0] > ndist: # 현재 위치보다 작을때만 이동, 좌/우가 상/하보다 작을때만 이동
            mn = (ndist, ni, nj)

    # return ni, nj
    return mn[1], mn[2]


def move_all():
    global ans, player_arr # 이동 거리 합

    '''
    전체 좌표 완탐해서 사람 이동
    :return:
    '''
    narr = [[[] for _ in range(N)] for _ in range(N)]
    for ci in range(N):
        for cj in range(N):
            if len(player_arr[ci][cj]) >= 1:
                for idx in player_arr[ci][cj] :
                    # 상태 체크
                    if escaped[idx] :
                        continue # break 아님 주의

                    ni, nj = move(ci, cj) # 이동 안해도 넣어줌
                    ans += abs(ni-ci)+abs(nj-cj)

                    # 출구 ?
                    # if (ni, nj) == (ei, ej) :
                    if wall_arr[ni][nj] == -1:
                        escaped[idx] = True
                    else:
                        narr[ni][nj].append(idx)

    player_arr = narr


def rotate_wall(si, sj, K):
    global wall_arr
    narr = [lst[:] for lst in wall_arr]

    for i in range(K):
        for j in range(K):
            narr[si+i][sj+j] = wall_arr[si+K-1-j][sj+i]

            # 내구도 처리
            if narr[si+i][sj+j] > 0 :
                narr[si + i][sj + j] -= 1

    wall_arr = narr


def rotate_player(si, sj, K):
    global player_arr
    narr = [[lst[:] for lst in row] for row in player_arr]
    # 이거 맞나...? row : 2차원, lst: 1차원 -> lst[:] 1차원
    debug = 0

    for i in range(K):
        for j in range(K):
            narr[si+i][sj+j] = player_arr[si+K-1-j][sj+i]

    player_arr = narr


def check(si, sj, K):
    flag1 = flag2 = False  # 참가자, 출구
    for i in range(si, si+K):
        for j in range(sj, sj+K):
            if oob(i, j):
                return False # 애초에 안되는 정사각형
            if len(player_arr[i][j]) >= 1 :
                flag1 = True
            # if (i, j) == (ei, ej) :
            if (i, j) == (ei, ej):
                flag2 = True

    return flag1 and flag2


def find_min_square():
    for K in range(1, N):
        for si in range(N):
            for sj in range(N):
                if check(si, sj, K):
                    return si, sj, K # 무조건 1번은 갱신돼야함

    return -1 # 나올리 없음


# def find_exit():
#     for i in range(N):
#         for j in range(N):
#             if wall_arr[i][j] == -1:
#                 return i, j

def rotate() :
    global ei, ej

    # 1. 정사각형 잡기
    si, sj, K = find_min_square()

    # 2. 회전하기 -> wall_arr, player_arr, (ei, ej) 변화
    rotate_wall(si, sj, K) # 2차원
    rotate_player(si, sj, K) # 3차원 ... => 그냥 따로따로
    # ei, ej = si+ej, sj+K-1-ei
    # ei, ej = find_exit()
    ei, ej = si+(ej-sj), sj+(K-1)-(ei-si)

ans = 0
for turn in range(1, K+1):

    # 1. 이동하기
    move_all() # player_arr 변화, escaped 변화

    # 종료 조건
    if escaped.count(True) == M:
        break

    # 2. 회전하기
    rotate() # wall_arr, player_arr, (ei, ej) 변화
    debug = 1


# [2]
print(ans)
# ei, ej = find_exit()
print(ei+1, ej+1)
