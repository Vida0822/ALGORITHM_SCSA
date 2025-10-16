"""
[마법사 상어와 파이어스톰]
한줄평: 다시 풀어볼 문제 X

소요 시간) 2시간
타임라인) 이해 및 구상 : 10 분 - 구현 : 50분  - 디버깅 : 60 분
사용한 알고리즘) 구현(시뮬레이션) + BFS

[구상]
+) 빨랐다, 필요한 기능을 적절히 나눠 로직을 잘 구성한 것 같다. (각각의 알고리즘 적어줌)
+) 2^N 이라는 인덱스가 헷갈릴 것 같아 미리 어떤 변수로 표시할 지 적어두었다
-) 새로운 배열을 복사해서 반환할지, 그 복사 배열을 어느 범위에서 시용할 지 제대로 정해놓지 않아 구현 때 헷갈렸다.

[구현]
-) 2^L 로 나누는 부분의 인덱스 설정이 어려웠다.
-) 배열 돌리기는 이제 템플릿처럼 쳐질 때도 됐는데 아직도 고민한다.
-) 도형 문제가 긴장돼 도형 쪽만 구상을 신경쓰다보니 BFS 에서 실수가 많이 나왔다 .
-) 느리고... 중간중간 외출을 자주해 집중이 깨졌다.

[디버깅]
-) 이미 단위 테스트를 완료한 로직을 수정해 다시 문제가 발생함을 뒤늦게 알았다.
-) 문제를 내 맘대로 해석해서 조건을 반대로 체크했다.

(오류 내용)
- 서브 배열로 자르는 인덱스 설정을 계속 실수했고, 시간도 오래걸렸다
 => 관련 문제 풀어봐야겠음
- '얼음이 있는 칸 3개 또는 그 이상과 인접해있지 않은 칸은 얼음의 양이 1 줄어든다. '
    -> 이걸 그냥 얼음이 있는 칸을 1씩 증가시키고 cnt >= 3 인지 확인하면 되는데, 굳이 없는 칸으로 바꿔서 부등호 잘 못 사용
        (자동으로 범위 체크도 X)

[시간/공간 복잡도]
- 예상한 복잡도)
- 실제 복잡도) O(Q * 4^N)

[EdgeCase]
- 고려한 Edge Case)
- 고려하지 못한 Edge Case)
"""



from collections import deque

def oob(ni, nj) :
    return not (0 <= ni < 2**N and 0 <= nj < 2**N)

def devide(si, sj, ei, ej, arr):
    '''
    si, sj 로부터 arr의 (2**Lx2**L)만큼 추출하는 함수

    :param si, sj:  추출 시작 위치
    :param si, sj:  추출 완료 위치
    :param arr:  전체 arr
    :return: 추출한 sub_arr
    '''
    sub_arr = [[0]*(ej-sj) for _ in range(ei-si)]
    for i in range(n):
        for j in range(n): # arr내 위치
            sub_arr[i][j] = arr[si+i][sj+j]
    return sub_arr

def rotate(sub_arr):
    '''

    :param sub_arr: 추출한 sub_arr을 회전 시키는 함수
    :return: 회전된 sub_arr
    '''
    rot_arr = [lst[:] for lst in sub_arr]
    for i in range(n):
        for j in range(n):
            rot_arr[j][n-1-i] = sub_arr[i][j]
    return rot_arr


def attach(si, sj, ei, ej, rot_arr):
    '''
    기존 arr에 회전된 배열을 반영하는 함수
    :param si, sj: 반영 시작 위치
    :param rot_arr: 회전된 배열
    :return: 재배치한 배열
    '''

    for i in range(si, ei):
        for j in range(sj, ej):
            att_arr[i][j] = rot_arr[i%n][j%n]
    return att_arr

def chg_arr(arr):
    '''
    인접 4칸에 얼음이 2개 이하로 있으면 해당 칸 얼음 1 감소
    :param att_arr: 회전해서 붙인 얼음
    :return: 감소한 얼음 반영한 칸
    '''
    cp_arr = [lst[:] for lst in arr]
    for ci in range(2**N):
        for cj in range(2**N):
            cnt = 0
            for di, dj in ((-1 , 0), (0, -1), (0, 1), (1, 0)):
                ni, nj = ci+di, cj+dj

                if oob(ni, nj):
                    continue

                if arr[ni][nj] > 0 :
                    cnt += 1

            if cnt < 3 :
                cp_arr[ci][cj] -= 1

    return cp_arr

def bfs(si, sj) :
    global mem_cnt
    global mem_mx

    # [0] 자료형
    q = deque()
    mem = 0

    # [1] 첫방문
    q.append((si, sj))
    v[si][sj] = 1

    mem += 1
    mem_cnt += arr[i][j]

    # [2] 순회
    while q:
        ci, cj = q.popleft()

        for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            ni, nj = ci+di, cj+dj

            if oob(ni, nj):
                continue
            if v[ni][nj] :
                continue
            if arr[ni][nj] > 0 :
                mem_cnt += arr[ni][nj] # 얼음 합
                mem += 1 # 칸 수

                q.append((ni, nj))
                v[ni][nj] = 1

    mem_mx = max(mem_mx, mem)

# [0] 준비
N, Q = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(2**N)]
# t = 1
# for i in range(2**N):
#     for j in range(2**N):
#         arr[i][j] = t
#         t += 1

L_list = list(map(int, input().split()))
debug = 0

# [1] 실행
for i in range(Q):
    L = L_list[i]
    n = 2**L

    att_arr = [[0] * (2**N) for _ in range(2 ** N)]
    for si in range(0, 2**N, n) :  # 2**N+1: 정사각형 총 길이
        for sj in range(0, 2**N, n):
            ei, ej = si+n, sj+n

            # 1. 격자 나누기
            sub_arr = devide(si, sj, ei, ej, arr)
            debug = 1

            # 2. 회전 하기
            rot_arr = rotate(sub_arr)
            debug = 2

            # .3 붙이기
            att_arr = attach(si, sj, ei, ej, rot_arr)
            debug = 3

    arr = att_arr
    # 4. 얼음양 감소 (완탐, 인접 4칸)
    arr = chg_arr(arr)
    debug = 4


# [2] 정답
# ANS1 = 0
# for a in arr :
#     ANS1 += sum(a)

v = [[0]*(2**N) for _ in range(2**N)]
mem_cnt = 0
mem_mx = 0
for i in range(2**N):
    for j in range(2**N):
        if arr[i][j] > 0 and not v[i][j]:
            bfs(i, j)

print(mem_cnt)
print(mem_mx)