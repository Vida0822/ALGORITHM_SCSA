"""
한줄평:
1. 나 ni, nj, nd를 갱신해야할 때랑, try만 해서 갱신하면 안될 때 엄청 실수하는구나...
=> ni, nj 갱신 여부를, 각 격자 타입마다 어떻게 처리할지 미리 정리해야했음 (왜냐면 난 맨날 이부분을 실수하니까!)
2. 명심하자: 조건 체크는 무조건 다음 좌표 기준으로!!!****** 현재 좌표까지는 원활히 이동해왔다고 생각 (+방향값도 이전에 정해서 넘겨줌) 안그럼 머리 터짐
 ㄴ CI, CJ 조건체크는 종료조건만
 => 순회 자체는 BFS 처럼 생각해서 구조 가져갔으면 안헷갈렸을 듯
  : 종료 조건은 ci, cj 밑에서 등

소요 시간) 1시간
타임라인) 이해 및 구상 : 20 분 - 구현 : 15 분  - 디버깅 : 40분
사용한 알고리즘) 시뮬레이션

[구상]
+) 종료 조건 잘 적어둠
+) white_holl 딕셔너리로 쓴거 굿
-) triangels[idx] : 해당 삼각형으로 이동하는 방향에 따라 dr 값에 더해줄 값
 ㄴ 이거! 실수 항상 많이 하는데 항상 틀린다
  : 구현 때 그림보면서 다시 할거면 뭐하러 구상 때 숫자값 다 구해놓은거지 ...?
   차라리 1) 구상에서 구한 숫자를 더블 체크하고, 2) 구현 때는 옮겨적는게 good (왜냐하면 구현하면서 또 그림보고 적으면 무조건 실수하니까)
-) ni, nj 갱신 여부를, 각 격자 타입마다 어떻게 처리할지 미리 정리해야했음 (왜냐면 난 맨날 이부분을 실수하니까!)

[구현]
+) 글애도...분기를 처음에 좀 깔끔하게 잡은듯(구상 덜한 것 치고는...?)
+) 딕셔너리 리스트 index 활용하는거 유용하군
-) swea 형식에서 전처리 어떻게 해야할지...이제는 좀 확정해야하지 않을까?
1. 일단 코드트리 형식으로 [0] 전처리 [1] 로직 [2] 정답 순으로 짜기
2. 오픈 TC 하나씩 다 맞추고, 위치 이동
  - [0] 전처리 부분 : TC 돌리는 부분 아래로 (global로 사용하기 위함)
  - [1] main 은 solve()로 분리 / 함수는 그대로
  - [2] 정답은 return으로 변경 -> TC 부분에서 ans 받아서 출력
  - ~ 나머진 상황 따라 적절히 ~


[디버깅]
-) 오...swea 문제라고 또 구현하고 점검 안하고 디버거 돌리네..대박
  + 여기저기 손대기
-) 또 로직 안보고 디버거 돌리면서 고치네... ni, nj 갱신 이상한거 코드 한번 읽으면 바로 알았어야...

(오류 내용)
1. triangles : look_up 값 오류

2. oob 라면 다음 턴에서 이동하도록 처리
- 그렇게 하면 현재 좌표가 유지되는데, 현재 좌표가 블럭일 경우 방향이 바뀜
- 근데, 다음턴에선 블럭 여부를 현재 좌표가 아니라 ni, nj 로 검사하기 때문에 방향 전환 누락
=> 이게 문젠데... 코드 점검 안하고 급하게 고치느냐 삽질 오지게 함
 (삽질 :
 1. 갑자기 현재 좌표가 블럭이라면 방향 바꾸는걸로 로직 변경 => 바꿔도 방향을 바꿔줘야지...좌표를 바꾸는건 뭘까
  => 잘 끼워맞추면 됐겠지만...기존 로직과 너무 달라지잖아. indexing 해놓은거 왠만하면 바꾸지 말고 바꿀거면 무조건 재구상
 2. 갑자기 함수 추가 : oob 후 아래 이동 시도하려함 -> 간단한 문제를 복잡하게 가는 것 ) 그냥 oob 를 if~else 문에서 빼주고 별도의 if 문으로 처리하면 되는데 다급해져서 생각 이상해짐

3. whilteholl에서 문제인것처럼 보이지만, 사실은 block 쪽 문제였음
=> 근데 whiteholl만 계속 찍어봄

4. 갑자기 oob를 ci, cj 로 바꿈 ㅋㅋㅋㅋ
=> 명심하자: 조건 체크는 무조건 다음 좌표 기준으로!!!****** 현재 좌표까지는 원활히 이동해왔다고 생각 (+방향값도 이전에 정해서 넘겨줌) 안그럼 머리 터짐
 ㄴ CI, CJ 조건체크는 종료조건만
 => 순회 자체는 BFS 처럼 생각해서 구조 가져갔으면 안헷갈렸을 듯
  : 종료 조건은 ci, cj 밑에서 등

[시간/공간 복잡도]
- 예상한 복잡도)
- 실제 복잡도)

[EdgeCase]
- 고려한 Edge Case)
- 고려하지 못한 Edge Case)
"""


from collections import defaultdict

# [0] 전처리
delta = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # 나중에 옮기자
blocks = [  # 1-based
    [],
    [2, 2, -1, 1],
    [1, 2, 2, -1],
    [-1, 1, 2, 2],
    [2, -1, 1, 2],
    [2, 2, 2, 2]
]


# [1]
def oob(ni, nj):
    return not (0 <= ni < N and 0 <= nj < N)


def move(si, sj, dr): # *** MAIN
    # print(si, sj, dr)
    ci, cj = si, sj
    scr = 0

    while True :
        di, dj = delta[dr]
        ni, nj = ci+di, cj+dj  # new 좌표

        # 조건 검사
        # 1. oob
        if oob(ni, nj):
            scr += 1
            dr = (dr+2)%4  # ci, cj 는 변화

            ni, nj = ci, cj

        # 2. block
        if 1 <= arr[ni][nj] <= 5:
            scr += 1
            dr = (dr+blocks[arr[ni][nj]][dr])%4
            ci, cj = ni, nj # 일단 이동 : 갔다가 꺽는거라고 생각 (?)

        # 3. while holl
        elif 6 <= arr[ni][nj] <= 10:
            lst = white_holl[arr[ni][nj]]
            idx = lst.index((ni, nj))
            ci, cj = lst[(idx+1)%2]
            # 방향은 안바뀜

        # 4. black holl (종료조건 1)
        elif arr[ni][nj] == -1:
            return scr

        # 6. 빈칸
        else:
            # 5. 자신의 출발 위치 (종료조건 2)
            if (ni, nj) == (si, sj):
                return scr
            ci, cj = ni, nj  # 방향은 유지


def solve():
    mx = -1
    # 1. 모든 좌표, 모든 방향에 대해 완탐
    for si in range(N):
        for sj in range(N):
            if arr[si][sj] == 0 :

                # 2. 이동 시키기
                for sd in range(4):
                    if (si, sj) == (0, 9):
                        debug = 0
                    scr = move(si, sj, sd)
                    mx = max(mx, scr)

    return mx


TC = int(input())
for tc in range(1, TC+1):
    # [0]
    N = int(input())
    arr = [list(map(int, input().split())) for _ in range(N)]

    # 화이트홀
    white_holl = defaultdict(list)
    for i in range(N):
        for j in range(N):
            if 6 <= arr[i][j] <= 10 :
                white_holl[arr[i][j]].append((i, j))

    ans = solve()
    print(f"#{tc} {ans}")
