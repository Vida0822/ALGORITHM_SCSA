"""
한줄평:
-  '삭제' 로직은 생각없이 구현하다보면 꼬이기 때문에, 삭제 처리를 rm_set에 받을지, 아니면 진짜 없애줄지 등 구상에서 미리 정하는게 중요함을 알았다
- 중력에서 가장 중요한 것: 마지막 잔여 값 처리 !! (실수 多)
- 중력/달팽이는 템플릿이 있는데 이렇게 구현이 오래걸리면 안됐다... ㅠㅠ


소요 시간) 2시간
타임라인) 이해 및 구상 : 15분 - 구현 : 60분  - 디버깅 : 45분
사용한 알고리즘)

[구상]
+) 1차원에서 당기고, 변화시키는 로직을 nslt를 떠올려서 잘 활용한 것 같다
=> 중력이나 연속값 처리 등 한 리스트를 대상으로 값을 보는 로직은 나는 왠만하면 nlst 사용
+) '삭제' 로직은 생각없이 구현하다보면 꼬이기 때문에, 삭제 처리를 rm_set에 받을지, 아니면 진짜 없애줄지 등 구상에서 미리 정하는게 중요함을 알았다
-) 점수 계산에 대한 구상을 정확히 확인하지 않아 구현 때 해맸다 (구슬 넘버를 곱해야한다는 사실을 빼먹었고, 어디서 점수 처리할 지 정하지 X )

[구현]
+) 함수 호출 부분에 변화하는 자료구조를 미리 써놓으니 좋음
-) 달팽이 구현에 15분 걸림...언제 한번에 제대로 할래...매번 더듬더듬하지말고 좋은 템플릿 찾아서 확정+바로바로 칠 수 있도록 문제 몇개 풀면서 연습
-) 입력 1-based 로 주어지는거 구상 때 메모X
-) 중력쪽 포인터 사용 아직 불안불안하다... : cnt 관리, cur/nxt 관리 아직 헷갈림 ... + 마지막값 처리도 ...
-) ans 반영해주는 로직 이상하다...


[디버깅]
+) 아리까리한 open TC 무지성 디버거 돌리는게 아니라 동작 꼼꼼히 확인해줌 !!
 => 동작 단위로 잘 돌아가고 있는지 체크!

(오류 내용)
'구현 중 수정'
- 달팽이 : 매번 cnt 1부터 시작시켜주는거 까먹음
- 또 자료 구조 동기화 문제 : arr <-> vals
    => 길이 제한을 배열 입력 자체에만 적용하고 해당 자료구조 자체는 또 안잘라줌

'구현 후 점검 때 '
- ans 처리 : 1, 3과정에서 하는거 늦게 봄 + 번호 곱해주는거 까먹음 (쉬워 보인다고 문제 대충 읽지 말자)
- pull()에서 i를 lst 조회하는 idx 로 써놓고 좌표를 또 (i, j)로 받음 -> 오류 안났으면 디버깅 못했다... i, j 는 왠만하면 좌표에만 사용

'디버거 수정'
-  magic() : 이상하게 구슬 터짐 => delta 잘못 만들어줌
-  bomb() : *****
    - flag 실수 : 폭발 여부를 반대로 적용해서 무한루프
    - 중력 재적용할 때 초기화 적용 X : nvals 를 [] 로 안만들어줌 , 잔여값 안넣어줌,
- pull() : list index of range
 --> 여기서 오류 났지만 원인은 fill()에서  vals의 동기화를 제대로 처리해주지 않아 값이 남음


[시간/공간 복잡도]
- 예상한 복잡도)
- 실제 복잡도)

[EdgeCase]
- 고려한 Edge Case)
- 고려하지 못한 Edge Case)
"""


# [0]
N, M = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]

dal_del = [(0, -1), (1, 0), (0, 1), (-1, 0)]

# 전처리 : 달팽이 좌표 - 값

# 좌표
lst = [] # 불변
si, sj, sd = N // 2, N // 2, 0  # 0 based

cnt_mx = 1
flag = False
while (si, sj) != (0, 0):
    di, dj = dal_del[sd]
    for cnt in range(cnt_mx):
        si += di
        sj += dj
        lst.append((si, sj))

    sd = (sd + 1) % 4 # cnt == cnt_mx
    if flag:
        # if cnt_mx == N - 1: continue  # 마지막엔 갈 범위 증가시켜주지 X
        cnt_mx += 1
        flag = False
    else:
        flag = True

# 값
vals = [] # 변
for i, j in lst:
    if not arr[i][j]:
        break
    vals.append(arr[i][j])

# 입력은 미리 받아놓는게 better
orders = [list(map(int, input().split())) for _ in range(M)]

delta = [(0, 1), (1, 0), (0, -1), (-1, 0)]

debug = 0

# [1]
def oob(ni, nj):
    return not (0 <= ni < N and 0 <= nj < N)

def magic(d, s): # 1단계
    global ans1, ans2, ans3
    '''
    마법을 써 구슬을 파괴하는 함수
    :param d: 방향
    :param s: 범위
    :return:
    '''
    rm_set = set()

    di, dj = delta[d]
    for cnt in range(1, s+1):
        ni, nj = si+di*cnt, sj+dj*cnt

        if oob(ni, nj) :
            break
        rm_set.add((ni, nj))

        # 문제를 끝까지 1차로 읽고 구상 시작해야하는 이유...
        if arr[ni][nj] == 1: ans1+=1
        elif arr[ni][nj] == 2: ans2+=1
        elif arr[ni][nj] == 3: ans3+=1

    return rm_set

def pull(rm_set):
    '''
    없어진 빈칸을 채워주는 함수
    :param rm_set:
    :return: nvals
    '''
    global vals
    nvals = []
    for l in range(len(vals)):
        i, j = lst[l]
        if (i, j) in rm_set :
            arr[i][j] = 0
            continue
        else:
            nvals.append(arr[i][j])
    vals = nvals


def bomb(): # ******
    '''
    연속하는 4개의 구슬을 계속 터트리는 함수
    => two-pointer로 한번에 (이동 다시시키기 X )
    :return: X ) vals <- nvals
    '''
    global vals, ans1, ans2, ans3
    nvals = []

    i = 1
    cur = vals[0]
    cnt = 1
    flag = False # 폭발 여부
    while True:
        # 종료 조건
        if i == len(vals):
            # 마지막 값 주의
            if cnt < 4:
                nvals.extend(vals[i - cnt:i])
            else:
                # 정답 처리
                if cur == 1:
                    ans1 += cnt
                elif cur == 2:
                    ans2 += cnt
                elif cur == 3:
                    ans3 += cnt
            vals = nvals
            if not flag :
                break
            else : # 폭발했으면 재검사
                i = 1
                cur = vals[0]
                cnt = 1
                flag = False
                nvals = []


        # 반복 처리
        n = vals[i]
        if cur == n :
            cnt += 1
        else:
            if cnt >= 4 : # 폭발
                flag = True
                # 정답 처리
                if cur == 1:  ans1 += cnt
                elif cur == 2: ans2 += cnt
                elif cur == 3: ans3 += cnt
                # cur = vals[i-cnt] -> '모든 몬스터는 동시에 폭발한다'
            else:
                nvals.extend(vals[i-cnt:i]) # 이전값들 넣어주기
            cur = n
            cnt = 1

        i += 1




def change():
    '''
    1차원 대상으로 구슬을 (개수, number)로 바꿔주는 함수
    :return:
    '''
    global vals

    nvals = []
    cur = vals[0]
    cnt = 1

    for i in range(1, len(vals)) :
        if cur == vals[i] : # nxt
            cnt += 1
        else:
            nvals.append(cnt)
            nvals.append(cur)
            cnt = 1
        cur = vals[i]

    # 마지막 값 주의
    nvals.append(cnt)
    nvals.append(cur)

    vals = nvals


def fill():
    global arr, vals

    narr = [[0]*N for _ in range(N)]
    vals = vals[:min(len(lst), len(vals))]
    for l in range(len(vals)):
        i, j = lst[l]
        narr[i][j] = vals[l]

    arr = narr


## MAIN ##
DEBUG = True

si, sj = N//2, N//2
ans1, ans2, ans3 = 0, 0, 0
for turn in range(M):  # 최대값

    # 1. 몬스터 공격
    d, s = orders[turn]
    rm_set = magic(d, s) # 2차원 변화, ans 변화
    if DEBUG : debug = 0

    # 2. 몬스터 당기기 
    pull(rm_set)  # 1차원 변화
    if DEBUG: debug = 0

    # 3. 몬스터 폭발
    bomb() # 1차원 변화, ans 변화
    if DEBUG: debug = 0

    # 4. 구슬 변화
    change() # 1차원 변화
    if DEBUG: debug = 0

    # 5. 2차원 다시 채워주기
    fill() # 2차원 변화
    if DEBUG: debug = 0


# [2]
# print(1*ans1, 2*ans2, 3*ans3)

# DEBUG !! 이미 내부 로직에서 곱해서 더해줬으므로 여기선 그냥 출력해야함
# print(1*ans1+ 2*ans2+3*ans3)
print(ans1+2*ans2+3*ans3)
