"""
한줄평:

소요 시간)
타임라인) 이해 및 구상 : 15 분 - 구현 : 분  - 디버깅 : 분
사용한 알고리즘)

[구현]
-) 자주 사용하던 자료구조가 아니면 왠만하면 X ...
-> 시간초과나는 문제 거의 안나올테니 잘 쓰던 리스트 플레이어 쓰자
-) 프린트 디버깅 코드 이젠 외울때도 되지 않았나...?

[디버깅] 현호님이랑 같이함
-) print 찍었다고 찍은 애들만 보고 디버거를 통해 다른 상태값 보는걸 하지 않는다 ex. v (이게 핵심인데)
-) 동작을 그냥 보는게 아니라, 지금 이러니까 이 함수 호출하면 이렇게 변화하겠지 예상하고 봐야함 (그냥 찍고, 맞나 틀리나 X)
-) 구상과 디버깅 준비에 오랜 시간을 들인 만큼, 디버깅 자체를 편하고 빠르게 해야함 .
-) 디버거로 찾는건 진짜 운이다. 무조건 논리에서 찾아내야함: 디버거 찍을 때도 디버거창만 보지말고 무조건 코드랑 같이 봐야함


(오류 내용)
1. defaultdict(int): 이거 int 로 초기화 안해주면 key error 남
=> 동일한 동작시키는데 어디선 에러나고 어디서 안남

1) "여기서, 이상한걸 알아챔! 근데 왜 디버거를 돌리지?"
> 디버거의 목적은 이상한걸 '발견'하기 위함
 : 이상함을 이미 발견했다면, 디버거가 아니라 코드를 보고 두 동작을 비교했어야함
=> remove()에서 초기화해줄 때 arr에 새로운 defaultdict() 넣어줄 때 int 로 초기화하지 않아 keyerror발생

2) 자료구조에서 문법 오류 났을 때, 자료구조 자체의 문제가 아닌 경우 훨씬 多 (유사: 스타트택시)
=> 보통, 전 단계 함수에서 처리를 잘못했을 가능성 큼 ***


2. remove()에서 삭제된 애들만 처리한다는 조건문 빠트림
- 'if len(arr[ri][rj]) >= 1' :
ㄴ 팩맨이 들렸던 곳이라도, 삭제할 몬스터가 있는 경우에만 시체가 남잖아 (논리적으로)
ㄴ 이거 빼먹고 v 배열 값 증가시켜줘서 오류 발생
=> 근데 이걸, 첫턴에서 발견했어야함 : 잡아먹은 몬스터 칸만 시체 남는게 아니라 이동 경로에 다 남잖아 ;;
    print 디버깅만 믿고 디버거 창 확인 안해서 생긴 문제
    ㄴ print 디버깅은 보기 힘든것만 보기 편하려고 하는 것, 실제로는 관련 자료구조를 모두 체크했어야함


3. move_packman()
1) sm을 무조건 갱신함:
왔던 칸을 다시 갈 수 있는데(재방문), 먹는 건 한번밖에 안된다는 당연한 문제 사실을 빠트림 (문제 사실: 명시적으로 주어져있지는 않지만, 논리적으로 당연한 조건)
 => 재방문이 아닌 경우만 sm에 합쳐주도록 분기 추가 : '방문한 루트에 현재 좌표가 있나?'

2) route 자료 구조 추가
각 반복문마다 route.append((i, j))
-> 백트래킹이랑 구조는 비슷하지만, 재귀가 아닌 반복문을 썼기 때문에 복원되지 않음 : LIST 에 계속 쌓임
=> 1) 좌표를 일단 다 구하고, 그 세 좌표로 루트를 만들어 반환
   2) 왔던 칸을 리스트 조회로 비교하는게 아닌, 3칸밖에 안되므로 각각 비교


4. move()에서 유효 턴수 오해함
: 문제를 잘못 읽어서 생긴 문제
-> '몬스터의 시체가 2턴 동안 유지된다' = 다음턴, 다다음턴 시체 유지 -> 이걸 이번턴, 다음턴이라고 오해함
=> 오해할 수 있음, but 나도 읽으면서 애매하다고 생각했던 부분
ㄴ 임의로 해석하고 그게 맞다고 생각하고 코드 짜지말고,
   일단 메모해놓고 두 경우 모두 오픈 TC랑 비교해서 어떤게 맞는지 확인했어야함




[시간/공간 복잡도]
- 예상한 복잡도)
- 실제 복잡도)

[EdgeCase]
- 고려한 Edge Case)
- 고려하지 못한 Edge Case)
"""


import copy
from collections import defaultdict

# [0]
M, T = map(int, input().split())
si, sj = map(int, input().split()) # 1-based
si, sj = si-1, sj-1 # 0-based

arr = [[defaultdict(int) for _ in range(4)] for _ in range(4)]
for _ in range(M) :
    i, j, d = map(int, input().split())
    arr[i-1][j-1][d-1] += 1

v = [[0]*4 for _ in range(4)]

delta = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]
ds = ['↑', '↖', '←', '↙', '↓', '↘', '→', '↗']

# print(len(arr[0][0]))
debug = 0

# [1]
def oob(ni, nj):
    return not (0 <= ni < 4 and 0 <= nj < 4)

def print_arr(arr):
    for i in range(4):
        for j in range(4) :
            if len(arr[i][j]) >= 1 :
                for dr, cnt in arr[i][j].items():
                    print("".join([ds[dr], str(cnt)]).rjust(4), end = '')
            else:
                print('_'.rjust(4), end = '')
        print()
    print()


def move(ci, cj, dr):
    for _ in range(8):
        ni, nj = ci + delta[dr][0], cj + delta[dr][1]
        # 조건 주의
        if oob(ni, nj) or v[ni][nj] >= turn or (ni, nj) == (si, sj) :
            dr = (dr + 1) % 8
        else:
            return ni, nj, dr
    else:
        return ci, cj, dr  # 갈수 있는칸 X


def move_players():
    global arr
    narr = [[defaultdict(int) for _ in range(4)] for _ in range(4)]

    for ci in range(4):
        for cj in range(4):
            if len(arr[ci][cj]) >= 1:
                for dr, cnt in arr[ci][cj].items():
                    ni, nj, nd = move(ci, cj, dr)
                    narr[ni][nj][nd] += cnt  # 여기서는 key 없어도 오류 X

    arr = narr


def move_packman():
    tmp_delta = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    # print(sum(arr[1][2].values())) # 2
    # 이동방향 3개 조합 (중복 순열)
    # mx = (-1, -1, -1)  # val, i, j -> Edge : 먹을 수 있는 몬스터가 없을 때, 좌표가 -1, -1로 잘못 참조됨
    mx = (-1, -1, -1) # but, 0개여도 무조건 갱신되도록 했기 때문에 ㄱㅊ을듯     (?)

    for d1 in range(4): # 방향 우선순위 자동 보장 (?) : oo 상좌하후*상좌하우*상좌하우 -> 클때만 갱신 : 우선순위 보장
        i1, j1 = si+tmp_delta[d1][0], sj+tmp_delta[d1][1]
        if oob(i1, j1): continue # break 절대 X..break는 진짜 조심해서 쓰자
        sm = sum(arr[i1][j1].values()) # 첫번째 칸은 무조건 시작칸이 아니므로 sm에 더해줌
        # route = [(i1, j1)]

        for d2 in range(4):
            i2, j2 = i1+tmp_delta[d2][0], j1+tmp_delta[d2][1]
            if oob(i2, j2): continue
            if (i2, j2) != (si, sj) and (i2, j2) != (i1, j1):
                sm2 = sm+sum(arr[i2][j2].values())
            else:
                sm2 = sm
            # route.append((i2, j2)) # 루트에는 들어갈 수 있음

            for d3 in range(4):
                i3, j3 = i2+tmp_delta[d3][0], j2+tmp_delta[d3][1]
                if oob(i3, j3): continue
                if (i3, j3) != (si, sj) and (i3, j3) != (i2, j2) and (i3, j3) != (i1, j1):
                    sm3 = sm2 + sum(arr[i3][j3].values())
                else:
                    sm3 = sm2
                # route.append((i3, j3))

                if mx[0] < sm3: # 0이어도 갱신 (mx[0] 초기값 : -1)
                    # mx = (sm, i, j)  # DEBUG!! 나 진짜 생각없이 i, j 그냥 쓴다...
                    mx = (sm3, i3, j3) # 최종 위치를 저장해줘야함!
                    mx_route = [(i1, j1), (i2, j2), (i3, j3)]
                    # mx_route = route

    return mx[1], mx[2], mx_route


def remove():
    # 여기서...초기 위치에 값을 지워주나...?
    for ri, rj in route :
        if len(arr[ri][rj]) >= 1 :
            arr[ri][rj] = defaultdict(int) # 이거 ... int 안쓰면 자동으로 안되는구나....
            v[ri][rj] = turn+2  # 이동 가능해지는 턴수


DEBUG = False
for turn in range(1, T+1) :
    if DEBUG:
        print("#### TURN :", turn, "####")
        print_arr(arr)
    debug = 0

    # 1. 몬스터 복제
    tarr = copy.deepcopy(arr)

    # 2. 몬스터 모두 이동
    move_players() # arr 변화
    if DEBUG:
        print_arr(arr)
    debug = 0

    # 3. 팩맨 이동
    si, sj, route = move_packman() # si, sj 변화
    debug = 1

    # 4. 몬스터 없애기 & 시체 남기기 : arr & v 변화
    remove()
    if DEBUG:
        print_arr(arr)
    debug = 2

    # 5. 복제 배열 합치기
    for i in range(4):
        for j in range(4):
            for dr, cnt in tarr[i][j].items():
                arr[i][j][dr] += cnt # 여기서는 왜 오류...?
    if DEBUG :
        print_arr(arr)
    debug = 3

# [2]
ans = 0
for i in range(4):
    for j in range(4):
        ans += sum(arr[i][j].values())

print(ans)

