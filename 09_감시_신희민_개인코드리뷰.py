"""
2차 도전
=> 수정 포인트 : 하나의 델타 배열로 관리하고 경우 따라 참조

소요 시간) 40분
타임라인) 이해 및 구상 : 15 분 - 구현 : 15분  - 디버깅 : 10분
사용한 알고리즘) 백트래킹 + 퍼져나가기 시뮬 (연구소와 유사)

한줄평:
1. 컨디션 안 좋을때나 압박받는 상황(시간 제한, 다른 사람과 함께 풀이)에서도 문제를 풀 수 있는 실력의 '저점'을 올려야 한다.
2. 문제에서 구상을 꼼꼼히 할 부분을 판단하는 시각이 필요할 것 같다 (연습만이 답..?)
3. 각 type 에 따른 델타 좌표가 달라지는 경우 look-up 테이블을 활용하는 것이 정석임을 알았다
    => 자주 나오는 유형인듯하니 템플릿처럼 익숙해지자 (유사 문제 : S1953 탈주범 검거)

[구상]
-) 1차 시도에서, 이 문제의 핵심은 델타배열(각 타입에 따른 델타값 관리)가 핵심인데,
    다른 부분만 과하게 손코딩하고 이부분은 구현하면서 생각하자...했던게 그대로 구현 실패로 드러났다.
    => 구상에서 꼼꼼하게 해야할 부분을 파악하는 시각...이 중요할 것 같은데 아직은 감이 잘 안온다 ㅠ
+) 2차 시도에서, 불필요한 손코딩을 줄이고 중요한 부분/주의할 점을 강조하니 훨씬 보기 편하고 실수도 줄었다 (아마 문제를 미리 알아서 그런듯..)
    => 손코딩...을 얼만큼 자세히 해야할지 감이 잘 안온다 ..
+) 각 기능별로 함수를 미리 정의해두어(+기능 주석 포함) 로직 흐름이 잘 잡혔다.

[구현]
-) 1차 시도에서, 구현 방향이 틀린 것같은데.. 를 알았지만 멈추지 못했다.
    => 싹 지우고 다시 구상한다는 판단을 빨리 해야하는데 좀처럼 안된다
-) 여전히 느리다. 너무너무 느리다.
+) 파이참 디버깅 기능을 활용해서 각 타입(cctv 1번~5번)의 구현 -> 테스트를 중간중간 진행해 디버깅 시간 감소
+) 범위 체크하는 'oob()'와 배열 상태를 출력하는 'test()' 매우 유용하다 : 왠만하면 필수 구현하자

[디버깅]
-) 계속 실수하는 부분을 틀린다.
    => 오답노트(자주 실수하는 부분)을 간단하게라도 얼른 만들어야겠다.

(오류 내용)
-  2차원 백트래킹에서 j 좌표를 설정하는 부분을 계속 틀린다. 암기하자!!
    for ci in range(i, N):
        for cj in range(M):
            if ci == i and cj < j :
                continue
- 델타 좌표 실수 : 상하좌우(90°회전) 순서로 구현해야하는데, 순서를 잘못하고 좌표 자체도 자잘하게 틀린다.
- cctv 1번처럼 한 방향만 참조하는 경우 iterable이 만들어지지 않아,
    방문할 방향(di, dj)를 뽑아낼 directions iterator가 아닌 int가 생성
    -> 한 방향도 튜플로 구현 (1,)
- v배열에 튜플이 표시된다... 문제는 풀렸지만 더 ㄴ나은 방향 고려
-) look-up -> delta -> di, dj 연결해 참조하는 방식이기에, 한줄로 한번에 코딩하려해 실수가 나왔다.
    => 지역 변수를 활용해 헷갈리지 않게 명시했다.
        ex) directions = look_up[A[ci][cj]], directions = v[ci][cj], di, dj = delta[idx]

[시간/공간 복잡도]
- 예상한 복잡도) O(완전탐색)*O(방향조합:4^CCTV 개수) * O(감시영역표시) :
            = O(N^2)*O(4^8)*O(N^2)
- 실제 복잡도) 개선한다면, O(4C⋅C⋅N2) --> CCTV 좌표를 저장해두고, 그거만 참조하면서

[EdgeCase]
- 고려한 Edge Case)
- 고려하지 못한 Edge Case)
"""
def test(cp_A):
    for a in cp_A:
        print(*a)
    print()

def oob(ni, nj):
    return not (0 <= ni < N and 0 <= nj < M)

def check(cp_A):
    '''

    :param cp_A: 감시영역 표시된 배열
    :return: 사각지대(0) 개수
    '''
    cnt = 0
    for i in range(N):
        for j in range(M):
            if cp_A[i][j] == 0:
                cnt += 1
    return cnt

def spread(cctv):
    '''
    감시 영역을 표시한 복사 배열을 반환
    :param cctv: cctv가 위치한 좌표
    :return: cp_A
    '''

    cp_A = [lst[:] for lst in A]
    for ci, cj in cctv:
        directions = v[ci][cj]
        for idx in directions:
            di, dj = delta[idx]
            ni, nj = ci, cj

            while True:
                # 감시 영역 표시
                ni, nj = ni+di, nj+dj

                if oob(ni, nj):
                    break
                if cp_A[ni][nj] == 6:
                    break
                if cp_A[ni][nj] == 0 :
                    cp_A[ni][nj] = '#'

    debug = 1
    return cp_A

def dfs(n, i, j) :
    '''
    각 cctv의 방향을 결정해 조합
    :param n: 방향을 정해준 cctv 개수
    :param i, j: 이전 검사 위치
    :return: X -> ANS 값만 갱신
    '''
    global ANS
    # [0] 종료 조건
    if n == cctv_cnt :
        cp_A = spread(cctv)
        cnt = check(cp_A)
        ANS = min(ANS, cnt)

        # test(cp_A)
        return

    # [1] 재귀 호출
    # 각 cctv 방향 결정
    for ci in range(i, N):
        for cj in range(M):
            if ci == i and cj < j :
                continue
            if v[ci][cj] :
                continue
            if 1 <= A[ci][cj] <= 5:
                directions = look_up[A[ci][cj]]
                for d in directions :
                    v[ci][cj] = d
                    dfs(n+1, ci, cj)
                    v[ci][cj] = 0

# [0] 시뮬레이션 준비
N, M = map(int, input().split())
A = [list(map(int, input().split())) for _ in range(N)]

# cctv 개수
cctv = []
for i in range(N):
    for j in range(M):
        if 1 <= A[i][j] <= 5:
            cctv.append((i, j))
cctv_cnt = len(cctv)

delta = {0:(-1, 0), 1:(0, -1), 2:(1, 0), 3:(0, 1)} # 상, 좌, 하, 우
look_up = {1:[(0,), (1,), (2,), (3,)],
           2:[(0, 2), (1, 3)],
           3:[(0, 1), (1, 2), (2, 3), (0, 3)],
           4:[(0, 1, 2), (1, 2, 3), (0, 1, 3), (0, 2, 3)],
           5:[(0, 1, 2, 3)]}

# [1] 시뮬레이션 실행
ANS = N*M+1
v = [[0]*M for _ in range(N)]
dfs(0, 0, 0)

# [2] 시뮬레이션 출력
print(ANS)
