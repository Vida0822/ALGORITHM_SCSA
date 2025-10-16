"""
한줄평:
1. 틀려도 괜찮아! 디버깅하면되지!
2. 구상을 꼼꼼히 한 대신, 그거 믿고 기세있게, 빠르게 구현하자 (그리고 디버깅 하면 됨!)
3. 디버거를 볼거면 그림이랑 비교하면서 꼼꼼히 보기 (절대 눈에 띄는 부분만 보지X)
4. 확실하지 않으면 이건가..? 하고 수정하는거 절대 금지: 근거를 가져라



소요 시간) 1시간 10분
타임라인) 이해 및 구상 :20 분 - 구현 : 25 분  - 디버깅 : 25분
사용한 알고리즘)

[구상]
+) 패딩 미리 그려두니까 덜 헷갈림 (그래도 틀렸지만...)
+) 정령 BFS 쪽 조건 분기 해놓으니 덜 헷갈림 (그래도 틀렸지만...)
-) 골렘 이동 lookup 자료구조만 써놓고 로직 구상 X -> 구현할 때 당황 + 재구상
+) 구현 안헷갈리는 부분은 수도 코드 굳이 작성 안하고 로직만 간단히 적어도 괜찮은 듯? (그정도 구현력은 올라왔으니까!)
 ex) 골렘 이동 中 else : 이동 중지 / 색칠하기 or 비우기 / return
+) lookup 좌표 : 구상때 두어번 보니 실수를 덜했다 (그래도 틀렸지만...이건 언제 한번에 제대로 짤까... )
+) 1-based, 0-based 미리 써놓는거 중요**
+) 색칠하는 부분 괜히 반복문 안쓰고 좌표 바로 참조한거 굿
[구현]
-) 자료구조는 왠만하면 정의하는데 옆에 이게 무슨 자료구조인지 주석 달아주자 (안그러면 헷갈림)
ex. lookup: 중앙에서 해당 방향을 이동할 때 참조하는 상대 좌표

[디버깅]
+)
-) 확실히, 실행 후 디버깅 할 때 엄청 다급해하는게 느껴진다. 시험때는 쿨타임 갖기 : 5분

(오류 내용)
1. 입력값 잘못봄 (이럴거면 왜적니..아 안적었구나...)
: 출구 방향인데 무의식적으로 이동 방향...이라고 생각

2. forest[][] : 패딩 오류 ****
1) '답이 0 나옴' : 북쪽 숲 (i : 0 ~ 2) 를 -1로 칠해서 이동 시작도 못하게 함
-> 위쪽 0으로 바꾸도록 함
-> 차원 오류 [  [[-2]*[0]*M+[-2]]   for _ in range(N+3)] : 요러면 3차원..
   -> [  [-2]*[0]*M+[-2]]   for _ in range(N+3)]
3) 2번째 골렘 이동 불가(출구인데도)
: 못가는데를 -1, -2로 표시하고(bfs 조건)... 출구를 -idx로 저장해주면.. 오류가 생기지 ...
 ㄴ 근데 -1에서 -2 로 바꾸는건 뭐지..? idx 도 2 쓰자나
 => 결국 index 2부터 받도록 바꿔주긴함
4) 초기화 오류 : 복붙한 코드는 수정하면 항상 같이 수정해줘야함 => 주석으로 써두기
5) 패딩을 했으면 정답 처리는 다시 패딩 미반영 값으로 바꿔줘야함

3. down 내 좌표 순서
: [(2, ), (1,), (1, )
-> 마지막 열(패딩 바로위)에선 2칸 밑 참조하면 오류난다.

4. gol_move()
- 디버거를 돌렸으면 제대로 봐야지.. 출구 방향만 눈에 띈다고 보지 말고
 -> 출구가 잘못 돌아간게 아니라, 회전을 멈췄어야하는데 회전을 한번 더한거잖아
 : 또 쓸다리없이 출구쪽 로직, check로직.... 손대려 했지...
 -> 오류 원인 left(lookup) 마지막 좌표: 2, -1 이어야하는데 (2, -1)해줌
ㄴ 디버거를 볼거면 그림이랑 비교하면서 꼼꼼히 보기 (절대 눈에 띄는 부분만 보지X)


[시간/공간 복잡도]
- 예상한 복잡도)
- 실제 복잡도)

[EdgeCase]
- 고려한 Edge Case)
- 고려하지 못한 Edge Case)
"""

from collections import deque


# 이동 lookup
down = [(1, 1), (1, -1), (2, 0)] # 다 중앙에 적용시켜줄거임
left = [(-1, -1), (0, -2), (1, -1), (1, -2), (2, -1)]
right = [(-1, 1), (0, 2), (1, 1), (1, 2), (2, 1)]

delta = [(-1, 0), (0, 1), (1, 0), (0, -1)]

debug = 0

# [1]
def check(ci, cj, look):
    for di, dj in look:
        ni, nj = ci+di, cj+dj
        if forest[ni][nj] != 0 : # 범위밖 or 다른 골렘
            return False
    else:
        return True


def move_gol(sj, ex, idx): # ex_dr: 색칠할때만 필요, 그 전에는 회전만
    global forest

    ci, cj = 1, sj
    while True :
        # 남쪽 이동 시도
        if check(ci, cj, down):
            ci, cj = ci+1, cj
        # 서쪽 이동 시도
        elif check(ci, cj, left):
            ci, cj = ci+1, cj-1
            ex = (ex-1)%4  # 출구: 반시계
        # 동쪽 이동 시도
        elif check(ci, cj, right):
            ci, cj = ci+1, cj+1
            ex = (ex+1)%4  # 출구: 시계
        # 이동 중지
        else:
            # 조건 체크: 벗어남?
            if ci < 4:
                # 초기화
                forest = [[-1] + [0] * M + [-1] for _ in range(N + 3)] + [[-1] * (M + 2)]
                return -1, -1
            else:
                # 색칠하기
                forest[ci][cj] = forest[ci-1][cj] = forest[ci+1][cj] = forest[ci][cj-1] = forest[ci][cj+1] = idx

                # 출구는 - 표시
                di, dj = delta[ex]
                forest[ci+di][cj+dj] = -idx

                return ci, cj


def move_fairy(si, sj): # BFS
    # [0]
    q = deque()
    v = [[0]*(M+2) for _ in range(N+4)]

    # [1]
    q.append((si, sj))
    v[si][sj] = 1

    # [2]
    mx = si
    while q:
        ci, cj = q.popleft()

        # 정답 처리
        mx = max(mx, ci)

        for di, dj in ((-1, 0), (0, 1), (1, 0), (0, -1)):
            ni, nj = ci+di, cj+dj

            # 범위밖(패딩), 미방문
            if forest[ni][nj] == -1 or v[ni][nj] != 0:
                continue

            # 다른 골렘이 있을 때
            if forest[ni][nj] != 0:
                # 내가 출구임
                if forest[ci][cj] < 0 :
                    q.append((ni, nj))
                    v[ni][nj] = 1
                # 아니면
                else:
                    # 같은 골렘 내에서만 이동
                    if forest[ni][nj] in (forest[ci][cj], -forest[ci][cj]) :
                        q.append((ni, nj))
                        v[ni][nj] = 1

    return mx-2


## MAIN ##
def solve():
    ans = 0
    for turn in range(2, K+2) :
        sj, ex = orders[turn-2]

        # 1. 골렘 이동
        ci, cj = move_gol(sj, ex, turn) # forest 변화 -> 중앙위치 (정령 위치 반환)

        if (ci, cj) == (-1, -1):
            continue

        # 2. 정령 이동
        mx = move_fairy(ci, cj) # ans 변화 (global)
        ans += mx

    return ans


# TC = int(input())
TC = 1
for tc in range(1, TC+1):
    # [0]

    N, M, K = map(int, input().split())
    orders = [list(map(int, input().split())) for _ in range(K)]  # j는 1-based, d 는 0-based

    # 숲
    forest = [[-1] + [0] * M + [-1] for _ in range(N + 3)] + [[-1] * (M + 2)]

    ans = solve()

    # [2]
    print(ans)
