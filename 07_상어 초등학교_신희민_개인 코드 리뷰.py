"""
한줄평:

소요 시간)
타임라인) 이해 및 구상 :  분 - 구현 : 분  - 디버깅 : 분
사용한 알고리즘)

[구상]
+)
-)

[구현]
+)
-)

[디버깅]
+)
-)

[시간/공간 복잡도]
- 예상한 복잡도)
- 실제 복잡도)

[EdgeCase]
- 고려한 Edge Case)
- 고려하지 못한 Edge Case)
"""


# [0] 시뮬레이션 준비
N = int(input())
A = [[0]*(N+1) for _ in range(N+1)]
likes = {}
delta = ((-1, 0), (0, -1), (0, 1), (1, 0))
def check(ni, nj):
    return 1 <= ni <= N and 1 <= nj <= N
def func1(s):
    '''
    좋아하는 학생 수를 각 좌표별로 세고(4방향), 가장 많은 cnt를 가진 좌표 반환
    :param : 학생 idx
    :return: lst[좌표] --> 2개 이상 가능
    '''
    ans = []
    mx = 0
    for ci in range(1, N+1):
        for cj in range(1, N+1) :
            if A[ci][cj] :
                continue

            cnt = 0
            for di, dj in delta:
                ni, nj = ci+di, cj+dj

                # 범위
                if not check(ni, nj):
                    continue

                # 좋아하는 학생?
                like = likes[i]
                if A[ni][nj] in like:
                    cnt += 1
            if mx < cnt :
                ans = [(ci, cj)]
                mx = cnt
            elif mx == cnt :
                ans.append((ci, cj))
    return ans


def func2(lst):
    '''
    빈자리를 각 좌표별로 세고(4방향), 가장 많은 cnt를 가진 좌표 반환
    :param: lst (1번 조건 만족 좌표)
    :return: lst[좌표] --> 2개 이상 가능
    '''
    mx = 0
    ans = []
    # for ci in range(1, N+1):
    #     for cj in range(1, N+1):
    for ci, cj in lst :
            if A[ci][cj] :
                continue
            cnt = 0
            for di, dj in delta:
                ni, nj = ci+di, cj+dj

                # 범위
                if not check(ni, nj):
                    continue

                if A[ni][nj] == 0:
                    cnt += 1

            if mx < cnt :
                ans = [(ci, cj)]
                mx = cnt
            elif mx == cnt :
                ans.append((ci, cj))
    return ans

def func3():
    '''
    :return: 비어있는 유일한 좌표 반환
    '''
    for ci in range(1, N+1):
        for cj in range(1, N+1):
            if A[ci][cj] == 0 :
                return ci, cj

def satisfy(i, ci, cj):
    like = likes[i]
    cnt = 0
    for di, dj in delta:
        ni, nj = ci+di, cj+dj
        if check(ni, nj) and A[ni][nj] in like :
            cnt += 1
    return cnt

# [1] 시뮬레이션 실행
for _ in range(N**2):
    i, s1, s2, s3, s4 = map(int, input().split())
    likes[i] = [s1, s2, s3, s4]

    # [1] 실행
    lst = func1(i)
    # debug = 0

    if len(lst) > 1:
        lst = func2(lst)
    # debug = 1

    if not lst:
        ni, nj = func3()
    else:
        ni, nj = lst[0]
    # debug = 2

    A[ni][nj] = i

# [3] 정답 출력
ANS = 0
for i in range(1, N+1):
    for j in range(1, N+1):
        scr = satisfy(A[i][j], i, j)
        if scr == 2:
            scr = 10
        elif scr == 3 :
            scr = 100
        elif scr == 4 :
            scr = 1000
        ANS += scr
print(ANS)
