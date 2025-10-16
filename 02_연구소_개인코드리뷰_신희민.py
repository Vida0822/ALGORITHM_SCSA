"""
[개인 코드 리뷰]
소요 시간: 60분
타임라인 : 이해 및 구상 : 10분 - 구현 : 20분  - 디버깅 : 30분
한줄평: 당연히 알고있다고 생각한 개념(백트래킹 index 관리)을 확실히 아는게 아니구나.

[구상]
(good)
- 문제를 꽤 빨리 이해해, 백트래킹 -> BFS -> Brute Force 의 구조를 꽤 빠른 시간에 구상했다
- 자주 실수하는 부분 또는 주의할만한 요소를 미리 적어두어 실수를 방지했다.

(bad)
- 오픈 테스트케이스를 귀찮다고 시뮬레이션 해보지 않아 도중에 잘못 이해한 조건이 있는걸 뒤늦게 알아챘다.
- 자주 실수하는 백트래킹 인덱스 같은 경우 손코딩 때 미리 적어두는게 좋을 것 같다.

[구현]
(good)
- 주석으로 탬플릿/구현할 부분을 미리 적어두니 가독성이 좋았고 영역 구분이 잘 되었다.
- 긴 로직을 함수를 사용해 적절히 분리한 것 같다.

(bad)
- 변수명을 중간중간 자주 바꿨다. 손코딩 당시 미리 정해두고 안바꾸는게 좋을 것 같다.
- 정말 정말 느리다 
- 잘 알고있다고 생각한 백트래킹 탬플릿을 잘못 활용했다
    : 다시 개념 복습하면서 정확히 이해하고 특히 2차원 배열 형태의 백트래킹을 항상 어려워하니 이 부분의 대표 코드를 자세히 봐야겠다.

[디버깅]
- 시뮬레이션은 코드가 길어 디버깅을 어느 부분부터 시작하고, 어떻게 해야하는지 막막하다
- 단계적으로, 기능별로 디버깅을 해야하는데 냅다 하는 느낌이라 오래걸리고, 어느 부분이 잘못되었는지 찾기 어렵다
 => 함수별, 기능별 테스트 하는 연습이 필요할 것 같고, 손코딩 할 때 미리 어떤 방식으로 테스트할지 정하고 시작하는 것도 좋을 것 같다.


"""
import copy
from collections import deque

def virus(lab): # BFS
    # [0] 필요한 자료형
    q = deque()
    v = [[0]*M for _ in range(N)]
    copy_lab = copy.deepcopy(lab)

    # [1] 첫방문
    for si in range(N):
        for sj in range(M):
            if copy_lab[si][sj] == 2:
                q.append((si, sj))
                v[si][sj] = 1

    # [2] 순회
    while q:
        ci, cj = q.popleft()

        for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            ni, nj = ci+di, cj+dj

            if not (0 <= ni < N and 0 <= nj < M):
                continue
            if v[ni][nj] == 0 and copy_lab[ni][nj] == 0:
                v[ni][nj] = 1
                copy_lab[ni][nj] = 2
                q.append((ni, nj))

    return copy_lab


def cnt(copy_lab) : # Brute-Force
    cnt = 0
    for i in range(N):
        for j in range(M):
            if copy_lab[i][j] == 0:
                cnt += 1
    return cnt

def build_walls(n, si, sj): # Backtracking
    global ANS

    # [0] 종료 조건
    if n == 3:
        copy_lab = virus(lab)
        ANS = max(ANS, cnt(copy_lab))
        return

    # [1] 재귀 호출
    for i in range(N):
        for j in range(M):
            if lab[i][j] == 0:
                lab[i][j] = 1
                build_walls(n+1, i, j)
                lab[i][j] = 0


N, M = map(int, input().split())
lab = [list(map(int, input().split())) for _ in range(N)]
ANS = 0

build_walls(0, 0, 0)
print(ANS)