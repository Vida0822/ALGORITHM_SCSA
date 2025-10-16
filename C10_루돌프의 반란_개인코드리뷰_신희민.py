"""
한줄평:
마음이 조급한게 문제 : 무조건 디버깅 쪽은 루틴 빡시게 만들고 지켜야겠다.........
히든 테케 틀렸을 때 점검 루틴+확인해야할 포인트 리스트 만들기
무지성 고치기 절대 X -> DEBUG : '이유' 무조건 적어야 수정

소요 시간) 3시간 40분 (FAIL)
타임라인) 이해 및 구상 : 40분 - 구현 : 1시간 20분  - 디버깅 : 2시간
사용한 알고리즘)

[구상]
-) 너무 느긋하게 한다.. 꼼꼼히 하되 정신 차리고 빠릿빠릿하게 할 생각...

[구현]
+) 조심해야할 부분을 미리 주석으로 써 그나마 실수가 줄었다...
-) 제약 조건 실수 (최대/최소값 설정 오류) **********
-) 격자 내 이동 구현할 때 각 분기별로 지우고 쓰고 하다보니 빠트리는 실수
   => 무조건 지우고, 쓰더라도 다시 덮어쓰는 로직 적용
-) 동일한 코드를 함수화하지 않고 중복으로 쓰고 각각 고쳐줘 로직 이상해짐
-) 좌표 정보 저장해주는 양식을 통일해주지 않음: 어디서는 튜플, 어디서는 리스트...

[디버깅]
-) '틀렸습니다' 뜨면 당황함 => 무지성 디버거 + 여기저기 고치고 제출 하다가 망함
-) 마음이 급해 로직 및 문제 점검을 하지 않고 무지성 디버거 돌리기
 => 제대로 생각 안하고 부분부분 고치다가 코드 산으로 감
 => 나 진짜진짜 코드/문제 중간 정독을 안하는구나.............
    : 틀렸습니다 한번 나오면 무조건 쿨타임 20분 있다고 생각
     => 키보드 손 떼기 + 문제 정독 + 문제 & 코드 정독 : 고칠 부분 메모 (하나 고치고 내기 절대 금지) => 로직 따라가면서 고칠 부분 수정하기
-) 디버거 돌려놓고 제대로 안봄
-) 덕지덕지 조건문

(오류 내용)
- 'cannot access local variable rd' : 무조건 갱신되어야하는 변수인데 이 값이 나오지 않음
=> 단순히 지역변수로 해결할게 아니라, 정렬 조건에서 왜 갱신되지 않는지 확인했어야
=> 오류 부분과 원인이 동떨어져있을 때 그걸 찾아가는게 어렵다 (유사: 오늘 아침 문제 'nxt' 변수 이상함)
-) ni, nj 실수 원래 잘 안하는데..이번엔 했다..


[시간/공간 복잡도]
- 예상한 복잡도)
- 실제 복잡도)

[EdgeCase]
- 고려한 Edge Case)
- 고려하지 못한 Edge Case)
"""
"""
- 구상 : 40분
- 유의: 자료구조 동기화 / 상태체크(out/기절) / 방향값 저장 여부

[오답]
- 거리 최대값을 잘못봐서 생긴 문제........ 50*50 은 2500이라 가장 큰 값을 2500을 해줬어야함
    => 크기가 큰 테케에서는 무조건 의심
- 이 오류는 돌려보면서 발견한게 아니라 문제(입출력 제한조건 포함) 정독하면서 발견한 부분
    => 크기 큰 테케 or 히든 테케 틀린다면 무조건 문제 정독 및 코드 한줄한줄 로직 점검 (키보드에서 무조건 손 때기!!!!!!!!!!!!!!!!!!!!!!!!!)
"""
# [0]
N, M, P, C, D = map(int, input().split())
ri, rj = map(int, input().split())

# 산타 정보
# 전부 one-based index 하자 (패딩: 벽처리)
arr = [[-1]*(N+2)]+[[-1]+[0]*N+[-1] for _ in range(N)]+[[-1]*(N+2)] # 산타 표시할 격자
santa_info = [0]*(P+1) # 각 idx 산타의 '현재' 좌표
for _ in range(P):
    idx, si, sj = map(int, input().split())
    santa_info[idx] = (si, sj)
    arr[si][sj] = idx

alive = [True]*(P+1)
wakeup = [0]*(P+1)
ans = [0]*(P+1)

delta = [(-1, 0), (0, 1), (1, 0), (0, -1)] # 상우하좌
delta2 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

debug = 0

# [1]
def oob(ni, nj):
    return not (1 <= ni <= N and 1 <= nj <= N)

def deer_move():
    global ri, rj
    # 1. 각 산타로의 거리 계산 => 가장 가까운 산타 반환
    # mn = (500, -1, -1, -1)  # 거리, 산타 위치, 산타 idx
    mn = (2500, -1, -1, -1)  # 거리, 산타 위치, 산타 idx
    # DEBUG!!!!! 미친 .... 거리 최대값을 잘못봐서 생긴 문제........ 50*50 은 2500이라 가장 큰 값을 2500을 해줬어야함
    for idx in range(1, P + 1):  # one-based index
        # 상태 체크
        if not alive[idx]:
            continue

        # 거리 작고, 행 크고, 열 크고
        si, sj = santa_info[idx]  # 해당 산타의 현재 위치
        dist = (ri - si) ** 2 + (rj - sj) ** 2

        if mn[0] > dist:
            mn = (dist, si, sj, idx)
        elif mn[0] == dist:
            if mn[1] < si:
                mn = (dist, si, sj, idx)
            elif mn[1] == si:
                if mn[2] < sj:
                    mn = (dist, si, sj, idx)


    # 2. 인접 8방향 중 해당 산타와 가장 가까운 위치로 이동
    min_d, si, sj, idx = mn
    ci, cj = ri, rj
    rd = -1
    for nd in range(8):
        di, dj = delta2[nd]
        ni, nj = ci+di, cj+dj

        if oob(ni, nj): # oob
            continue

        cur_d = (ni - si) ** 2 + (nj - sj) ** 2
        if min_d > cur_d:
            min_d = cur_d
            ri, rj, rd = ni, nj, nd
    # print(ri, rj)
    return ri, rj, rd


def deer_crush(ri, rj, rd):
    '''
    여기 맵 변경 주의 -> santa_info, arr
    :param ri:
    :param rj:
    :param rd: 산타가 이동해온 방향
    :return:
    '''
    global arr

    # 0. 산타 점수 추가
    idx = arr[ri][rj]
    ans[idx] += C

    # 1. 산타 밀려나기
    # 1) 좌표 구하기
    si, sj = ri, rj
    di, dj = delta2[rd] # 루돌프가 이동해온 방향
    ni, nj = si+di*C, sj+dj*C

    # 2) 조건 확인
    # 탈락 ?
    if not (1 <= ni <= N and 1 <= nj <= N):
        alive[idx] = False
        arr[si][sj] = 0

    else:
        # 빈칸 ?
        if arr[ni][nj] == 0 :
            santa_info[idx] = [ni, nj] # 1) info
            arr[ni][nj] = idx  # 2) arr
            arr[si][sj] = 0

        # 다른 산타?
        else:
            interact(idx, ni, nj, di, dj)

        # 산타 기절
        wakeup[idx] = turn+1 # 잠들어 있는 timeline


def move_all_santas():
    '''
    info & arr 동기화 주의
    :return:
    '''
    # 1번 ~ P번 산타까지 순서대로
    for i in range(1, P+1):
        # 상태 체크 : 탈락 or 기절 ?
        if not alive[i] or wakeup[i] >= turn:
            continue

        # 이동 시도
        si, sj = santa_info[i]
        ni, nj, nd = move_santa(si, sj, ri, rj)

        # 이동 X
        if (ni, nj) == (si, sj):
            continue
        # 이동 가능 시
        else :
            # 충돌 X
            if (ni, nj) != (ri, rj):
                santa_info[i] = [ni, nj]  # 1) info
                arr[ni][nj] = arr[si][sj]  # 2) arr
                arr[si][sj] = 0
            # 충돌 O
            else:
                # 일단 이동 후
                santa_info[i] = [ni, nj]  # 1) info
                arr[ni][nj] = arr[si][sj]  # 2) arr
                arr[si][sj] = 0

                # 충돌 처리
                santa_crush(ni, nj, nd)


def move_santa(si, sj, ri, rj):
    '''
    개별 산타를 이동시키는 함수 (우선 순ㄴ위, 조건 주의)
    :return:
    '''
    mn_d = (ri - si) ** 2 + (rj - sj) ** 2 # 현자 위치와의 거리
    mn = (mn_d, si, sj, -1)

    # 각 4방향 조사하면서 루돌프와의 거리 가까운 곳 구하기
    for d in range(len(delta)):
        di, dj = delta[d]
        ni, nj = si+di, sj+dj

        dist = (ni - ri) ** 2 + (nj - rj) ** 2

        # 조건 체크
        if oob(ni, nj) or arr[ni][nj] > 0 :
            continue

        if mn[0] > dist: # 우선순위는 보장되므로 작기만하면 갱신
            mn = (dist, ni, nj, d)

    return mn[1], mn[2], mn[3]


def santa_crush(si, sj, sd):
    global arr

    # 0. 산타 점수 추가
    idx = arr[si][sj]
    ans[idx] += D

    # 1. 산타 밀려나기
    # 1) 방향 반대로
    sd = (sd+2)%4

    # 2) 좌표 구하기
    di, dj = delta[sd]  # 산타가 이동해온 방향
    ni, nj = si + di*D, sj + dj*D

    # 3) 조건 확인
    # 탈락 ?
    if not (1 <= ni <= N and 1 <= nj <= N):
        alive[idx] = False
        arr[si][sj] = 0

    else:
        # 빈칸 ?
        if arr[ni][nj] == 0:
            santa_info[idx] = [ni, nj]  # 1) info
            arr[ni][nj] = idx  # 2) arr
            arr[si][sj] = 0

        # 다른 산타?
        else:
            interact(idx, ni, nj, di, dj)

        # 산타 기절
        wakeup[idx] = turn + 1  # 잠들어 있는 timeline


def interact(idx, ni, nj, di, dj):

    global arr
    narr = [lst[:] for lst in arr]

    # 본인 이동
    # ni, nj = si+di, sj+dj
    si, sj = santa_info[idx]
    santa_info[idx] = [ni, nj]  # 1) info
    narr[ni][nj] = idx          # 2) arr
    narr[si][sj] = 0

    while True:
        if arr[ni][nj] <= 0:
            break
        nidx = arr[ni][nj]
        ni, nj = ni + di, nj + dj
        if oob(ni, nj) : #  DEBUG !!!
            alive[nidx] = False
            break
        santa_info[nidx] = [ni, nj]  # 1) info
        narr[ni][nj] = nidx  # 2) arr
    arr = narr


### MAIN ###
for turn in range(1, M+1):

    # 1. 루돌프 이동 : 이동
    ri, rj, rd = deer_move()
    debug = 0

    # 2. 루돌프 충돌
    if arr[ri][rj] > 0 : # 산타가 있으면
        deer_crush(ri, rj, rd)
    debug = 1

    # 3. 산타 이동 : 이동 & 충돌
    move_all_santas()
    debug = 2

    # 3. 점수 처리 : 생존 산타 +1
    for idx in range(1, P+1):
        if alive[idx]:
            ans[idx] += 1
    debug = 5

    # 4. 종료 조건
    if alive[1:].count(False) == P:
        break

# [2]
debug = 6
print(*ans[1:])



