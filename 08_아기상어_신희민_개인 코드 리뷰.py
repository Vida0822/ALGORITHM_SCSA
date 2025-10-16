"""
한줄평:
1. 시뮬레이션이라고 무조건 문제에서 step을 주지 않는다 => 해석해서 로직 재구상해야하는 경우도 有
2. 문제가 제대로 이해가 안됐다면....제발 오픈 TC좀 돌려봐

1차 시도 : 2시간 => 실패
2차 시도 :
소요 시간) 30분
타임 라인) 이해 및 구상 : 15 분 - 구현 : 10 분  - 디버깅 : 5 분
사용한 알고리즘) BFS + 시뮬레이션

[구상]
+) 오픈 TC를 직접 시뮬레이션하니 오해하고 있던 부분을 바로 찾았다.
+) 과한 함수화를 하지 않았다. => 함수에서 할 부분과 Main에서 할 부분을 잘 구분한 것 같다.

[구현]
+) 타자 속도가 조금 빨라졌다.

[디버깅]
+) 전부 다 하고 돌려보는게 아닌 단위별로 구현 -> 테스트하는 방식으로 진행해 오류 탐색 범위를 줄였다. (debug = 0, 1, 2 미리 찍어두는거 매우 효과적! )
-) 함수의 리턴값을 명확히 하지 않아 정렬 등을 재구상해야했다.

(오류 내용)
- 문제 이해를 완전 잘못했다!! 자신의 크기만큼 물고기를 새로 먹어야 크기 += 1이라 먹은 개수를 초기화해야하는데 하지 않았다 => 오픈 TC 시뮬 필수
- 정렬 실수 : cnt오름차순, i오름차순, j오름차순 -> 맨 앞 빼야하는데 i를 내림차순으로 정렬하고..또 마지막걸 빼고
    => 여러 기준으로 정렬할 경우 손코딩에 명시

[시간/공간 복잡도]
- 예상한 복잡도) O(N^2): 이동 * O(NlogN): 정렬
- 실제 복잡도) while 루프 고려안했다...
O(while 루프) × (BFS + 정렬)
= O(N²) × (O(N²) + O(N² log N))
= O(N⁴ + N⁴ log N)
= O(N⁴ log N)

[EdgeCase]
- 고려한 Edge Case) X
- 고려하지 못한 Edge Case) X
"""



from collections import deque
delta = [(-1, 0), (0, -1), (0, 1), (1, 0)]

def oob(ni, nj) :
    return not (0 <= ni < N and 0 <= nj < N)

def bfs(si, sj, cw) :
    '''
    :param si, sj: 상어의 좌표
    :param cw: 상어의 무게
    :return: 먹을 수 있는 물고기 (최소만 X, 일단 전부 넣는다)
    '''

    # [0] 필요한 자료형
    q = deque()
    v = [[0]*N for _ in range(N)]
    ret = []

    # [1] 첫 방문
    q.append((si, sj))
    v[si][sj] = 1

    # [2] 순회
    while q:
        ci, cj = q.popleft()

        if 0 < A[ci][cj] < cw:
            ret.append((ci, cj, v[ci][cj]-1))

        for di, dj in delta:
            ni, nj = ci+di, cj+dj

            # 범위
            if oob(ni, nj):
                continue

            # 미방문
            if v[ni][nj] :
                continue

            if A[ni][nj] <= cw:
                v[ni][nj] = v[ci][cj] + 1
                q.append((ni, nj))
    return ret



# [0] 시뮬레이션 준비
N = int(input())
A = [list(map(int, input().split())) for _ in range(N)]

# 상어 찾기
for i in range(N): # O(N^2)
    for j in range(N):
        if A[i][j] == 9:
            A[i][j] = 0
            ci, cj = i, j
            break
cw = 2

# [1] 시뮬레이션 실행
time = 0 # ans
eat = 0
while True:
    # 1. 먹을 수 있는 물고기 : 이동 가능 + 크기 작음
    fishes = bfs(ci, cj, cw)
    # debug = 0

    # 2. 종료 조건
    if not fishes:
        break

    fishes.sort(key=(lambda x : (x[2], x[0], x[1])))
    ni, nj, cnt = fishes.pop(0)
    # debug = 1


    # 3. 물고기 먹기
    A[ni][nj] = 0
    eat += 1
    # debug = 2

    # 4. 이동 시간 누적
    time += cnt
    # debug = 3

    # 5. 크기 비교
    if eat == cw:
        cw += 1
        eat = 0

    # 6. 이동 : 좌표 변환
    ci, cj = ni, nj



# [2] 시뮬레이션 출력
print(time)


