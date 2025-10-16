"""
한줄평: 꼭! 다시 풀어볼 문제
- 구현/시뮬레이션 문제도 시간 복잡도를 잘 고려해야함을 실감

1차 시도 => 실패
2차 시도
소요 시간) 2시간 20분
타임라인) 이해 및 구상 : 15 분 - 구현 : 15 분  - 디버깅 : 120 분
사용한 알고리즘) Bactracking

[구상]
-) 사다리 자체를 구현하기가 어려워 문제를 따르지 않고 배열 크기를 늘려, 세로선과 가로선을 따로 구현했다.
    => 문제와 맞지 않는 입력, 인덱스 체크 등 실수가 많이 나왔다.
-) 시간 복잡도를 생각하지 않아 시간 초과 문제가 많이 발생했다.

[구현]
-) 사다리의 세로선을 따라 내려갈 수 있는지를 처음에 BFS로 어렵게 접근해 구현에 실패했다.
-) 종료 개수가 정해져있지 않는 문제이기에 구현을 어떻게해야할지 감이 안왔다 => 주현님 코드 참고하니 반복문으로 1씩 증가하며 DFS 돌림

[디버깅]
-) 2차원 백트래킹이라 마음을 먹고 들어갔는데도 실수가 많았다.

(오류 내용)
- 2차원 백트래킹의 종료 조건을 '마지막 좌표로 도달했을 떼'로 잡아
 마지막 사다리가 있는 경우 종료 조건을 만족하지 못함

-

[시간/공간 복잡도]
- 예상한 복잡도)
- 실제 복잡도)

[EdgeCase]
- 고려한 Edge Case)
- 고려하지 못한 Edge Case)
"""
import sys
input = sys.stdin.readline

def check():
    '''
    각 세로선의 j 좌표가 바뀌지 않고 모두 내려가는지 확인하는 함수

    :return: True/False
    '''
    for j in range(N): # O(N*H)
        cur = j

        for i in range(H):
            if cur > 0 and arr[i][cur-1]:
                cur -= 1
            elif arr[i][cur] :
                cur += 1
        if j != cur :
            return False
    return True



def dfs(n, si, sj):
    '''

    :param n: 지금까지 놓은 new 가로선 개수
    :param si, sj: 이전 검사 위치 (놓았을수도, 안놓았을수도 있음)
    :return: X -> ANS 값 갱신
    '''
    global ANS

    # 가지치기
    if n >= ANS or n > 3:
        return

    # [0] 종료 조건
    if check():
        if n < ANS :
            ANS = n
        return

    # [1] 재귀 호출
    for i in range(si, H):
        for j in range(N-1):
            if i == si and j < sj :
                continue
            if arr[i][j] or arr[i][j+1] :
                continue
            if j > 0 and arr[i][j-1]:
                continue
            arr[i][j] = 1
            dfs(n+1, i, j+2)
            arr[i][j] = 0


# [0] 준비
N, M, H = map(int, input().split())
arr = [[0]*N for _ in range(H)]
# arr[i][j] : j와 j+1열을 잇는 가로선 (오른쪽으로 나있다)
# 'b번 세로선과 b+1번 세로선을 a번 점선 위치에서 연결했다는 의미' --> 문제를 그대로 구현하자...

for _ in range(M):
    r, c = map(int, input().split())
    arr[r-1][c-1] = 1 # 기존에 있는 가로 사다리 :


# [1] 실행
# 1. 사다리 놓기
ANS = 4
dfs(0, 0, 0)

# [2] 정답
print(ANS if ANS < 4 else -1)
