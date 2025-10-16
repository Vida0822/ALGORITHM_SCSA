"""
한줄평:
구상은 진짜 꼼꼼히 하되(메이즈러너, 왕실의 기사들, 민트 초코 우유처럼 코드 전개도 무조건 적어놓고)
=> 즉, 시나리오 로직과 코드 로직 각각 적는 것 ! 1시간 정도 잡고


소요 시간) 4시간 + a ... 디버깅 실패
=> 풀지 못한데는 원인이 있을 것! 영상 보면서 확인

타임라인) 이해 및 구상 : 40분 - 구현 : 1시간 20분  - 디버깅 : 3시간
사용한 알고리즘) BFS

[구상]
-) 코드 로직 꼼꼼히 안짬 : 특히 BFS는 템플릿 안다고 조건/상태값 처리 어떻게 해줄지 고민 안했다가 구현 때 엄청 오래걸리고 덕지덕지 수정 하게됨
=> 템플릿화 되어있는 거라도 무조건 코드 로직 작성 : 어떤 값을 저장하고, 어떤 조건을 체크해야하는지


[구현]
-) 구상을 겁나 오래 해놓고 구현을 다시 고민하는건 뭐하는 거지...?
=> 꼼꼼하게 구상한 것이므로 내 코드 로직을 믿고 기세 있게, 자신감 있게 와다다 쳐야함
(불필요한 단위 테스트 및 중간 디버깅 최소화)
-) 구현도 다 안했는데 단위 테스트 및 디버깅 과함 : 구현 흐름 끊기고 속도 루즈해짐 (어차피 후반에 전체 디버깅 다시 해야하는데)
-) 코드 로직

[디버깅]
-) 로직 점검 안하고 디버거 의존 + 오픈 TC 맞추려고 여기저기 손댐

(오류 내용)
-
-

[시간/공간 복잡도]
- 예상한 복잡도)
- 실제 복잡도)

[EdgeCase]
- 고려한 Edge Case)
- 고려하지 못한 Edge Case)
"""

"""
- 골렘에서 내릴 때에는 정해진 출구를 통해서만 내릴 수 있습니다.
- (동쪽/서쪽) 방향으로 한 칸 이동을 한 뒤 내려가기 때문에 (동쪽/서쪽) 한 칸이 모두 비어 있어야 함에 유의합니다.
- 골렘이 최대한 남쪽으로 이동했지만 골렘의 몸 일부가 여전히 숲을 벗어난 상태라면,

<정령이 도착하는 최종 위치를 답에 포함시키지 않습니다.>
<(1) 의 방법으로 이동할 수 없으면 서쪽 방향으로 회전하면서 내려갑니다.> 

"""
from collections import deque

# [0]
R, C, K = map(int, input().split())
delta = [(-1, 0), (0, 1), (1, 0), (0, -1)]

# 지도
arr = [[0]*(C+2) for _ in range(R+4)]  # 1-based-index

# 골렘 정보
gol_info = [(-1, -1, -1)]
for _ in range(K):
    sj, sd = map(int, input().split())
    gol_info.append((1, sj, sd)) # 시작 위치, 출구 방향


# [1]
def print_arr(arr):
    print("".join(map(lambda x: str(x).replace('-1', ' ').rjust(5), [str(j) for j in range(-1, C+2)])))
    i = 0
    for row in arr :
        print(str(i).rjust(5), end='')
        print("".join(map(lambda x: str(x).replace('0', '_').rjust(5), row)))
        i += 1
    print()


def oob(i, j):
    return not (0 <= i <= R+2 and 1 <= j <= C)


def try_dwn(i, j) :
    if not (oob(i + 1, j - 1) or oob(i + 2, j) or oob(i + 1, j + 1)):
        if arr[i + 1][j - 1] == 0 and arr[i + 2][j] == 0 and arr[i + 1][j + 1] == 0:
            return True
    return False


def test(arr, i, j, d, sj):
    test_arr = [lst[:] for lst in arr]
    test_arr[i][j] = idx
    for dd in range(4):
        di, dj = delta[dd]
        if oob(i + di, j + dj):
            continue
        if d == dd:
            test_arr[i + di][j + dj] = -idx
        else:
            test_arr[i + di][j + dj] = idx
    test_arr[0][sj] = 'S' + str(idx)
    return test_arr


def gol_move(idx):
    global arr
    q = deque()

    # 초기 위치
    si, sj, sd = gol_info[idx]
    q.append((si, sj, sd))

    while True:
        i, j, d = q.popleft()

        # 1. 남쪽 이동 시도
        if not (oob(i+1, j-1) or oob(i+2, j) or oob(i+1, j+1)) :
            if arr[i+1][j-1] == 0 and arr[i+2][j] == 0 and arr[i+1][j+1] == 0:
                gol_info[idx] = (i+1, j, d)
                q.append((i+1, j, d))
                continue

        # 2. 서쪽 이동 시도
        if not (oob(i-1, j-1) or oob(i, j-2) or oob(i+1, j-1)) :
            if arr[i-1][j-1] == 0 and arr[i][j-2] == 0 and arr[i+1][j-1] == 0:
                if try_dwn(i, j-1) :
                    d = (d-1)%4
                    gol_info[idx] = (i, j-1, d)
                    q.append((i, j-1, d))
                    continue

        # 3. 동쪽 이동 시도
        if not (oob(i-1, j+1) or oob(i, j+2) or oob(i+1, j+1)) :
            if arr[i-1][j+1] == 0 and arr[i][j+2] == 0 and arr[i+1][j+1] == 0:
                if try_dwn(i, j+1) :
                    d = (d+1)%4
                    gol_info[idx] = (i, j+1, d)
                    q.append((i, j+1, d))
                    continue

        # 종료 조건 : 이동 불가능 (맨 밑이라/ oob)
        # 튀어나옴
        if i <= 3:  # not (2 <= i <= R-1 and 2 <= j <= C-1) :
            arr = [[0] * (C + 2) for _ in range(R + 4)]
            return -1
        else:
            arr[i][j] = idx
            for dd in range(4) :
                di, dj = delta[dd]
                ni, nj = i+di, j+dj
                if d == dd :
                    arr[ni][nj] = -idx
                else :
                    arr[ni][nj] = idx
            return 0


def bfs(si, sj, idx) :
    # [0]
    q = deque()
    v = [[0]*(C+2) for _ in range(R+4)]
    r = -1

    # [1]
    q.append((si, sj, idx))
    v[si][sj] = 1

    # [2]
    while q:
        ci, cj, color = q.popleft()

        # 정답 처리
        r = max(r, ci)

        for di, dj in delta:
            ni, nj = ci+di, cj+dj

            # 범위밖, 방문, 빈칸
            if oob(ni, nj) or v[ni][nj] or arr[ni][nj] == 0:
                continue

            # 같은 블럭일때 (출구 or 일반 블럭)
            if abs(arr[ni][nj]) == color :
                v[ni][nj] = 1
                q.append((ni, nj, arr[ni][nj]))

            # 다른 블럭일 때
            else:
                if color < 0:  # 내가 출구라면
                    v[ni][nj] = 1
                    q.append((ni, nj, arr[ni][nj]))
    debug = 4
    return r-2


## MAIN ##
ANS = 0
for idx in range(1, K+1) :
    # 1. 골렘 이동
    ret = gol_move(idx)  # gol_info 변경됨 -> 최종 arr 반영
    # print_arr(arr)
    debug = 1

    # 2. 정령 이동
    if ret != -1:
        si, sj, sd = gol_info[idx]
        ANS += bfs(si, sj, idx)
        debug = 2

# [2]
print(ANS)