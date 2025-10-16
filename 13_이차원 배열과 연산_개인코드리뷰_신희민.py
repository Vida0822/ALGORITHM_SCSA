"""
한줄평: 다시 풀어볼 문제 (2차원 배열 연습)
1시간 이상 디버깅 했는데 안보이면 진짜 밀어야겠다.
정말 간단한 조건 하나를 놓쳤는데 2시간 내내 안보였다.

1차시도 : 실패
2차시도 : 성공
소요 시간) 50분
타임라인) 이해 및 구상 : 10 분 - 구현 : 20분  - 디버깅 : 20분
사용한 알고리즘) 구현 (도형)

[구상]
+) 대략적인 흐름을 정해놓고, 오픈 TC 를 시물레이션하며 구상을 구체화했다.
-) 정렬 기준이 까다로웠고, 초반에 좌표로 접근하니 행, 열 길이 변화를 잘 구현하지 못했다.

[구현]
-) 시뮬레이션 중간 중간 조건에 따른 '상태값 변경'을 정말 잘 놓치는 것 같다.
-) 2차원 배열 회전 정도는 이제 바로바로 나올때가 됐는데... 아직도 느리고 생각하면서 한다.

[디버깅]
-) 구현에 구멍이 많아 오픈 TC 맞추는데도 굉장한 시간이 소요됐다.
-) 문제 및 구상을 점검하지 않고 디버거 배웠다고 계속 디버거만 돌린다 (문제를 오해한거라 동작은 맞게 하는데도!) 

(오류 내용)
- 시간 조건 :  time >= 100 (X) ->  time > 100
    => 이런 시간, 카운트 소진으로 인한 종료 조건에서 항상 1씩 틀리고 맞는다
    (DEBUG)
- N, M 이 회전시에 원래 새로 갱신되는데, 이 경우 새로운 list를 만들어 append 하는 형식이기 때문에
  N, M을 바꾸면 안됐는데 계속 바꿨다...

"""

'''
조건
- 3x3
- 1초당 연산

- R : N <= M
- C : M > M
- time <= 100 (DEBUG)

'''


def sort_lst(lst):
    '''
    문제 규칙에 따라 리스트를 정렬하는 함수

    :param lst: 정렬할 행 또는 열
    :return: 정렬된 행 또는 열
    '''
    v = dict()
    for a in lst : # O(N)
        v[a] = v.get(a, 0)+1

    num_set = list(v.items())
    num_set.sort(key=lambda x: (x[1], x[0]))

    ret = []
    for n, c in num_set:
        if n == 0 :
            continue
        ret.extend((n, c))
    debug = 1
    return ret
    # print(num_set)



def rotate(new_A):
    '''
    C연산을 했을 때 행기준으로 채워준 배열을 좌 90도 돌리기
    :param new_A:
    :return:
    '''

    # 1행을 뽑아서 1열로 넣어주기
    rot_A = [[0]*M for _ in range(N)]
    for j in range(M):
        lst = new_A[j]
        for i in range(N):
            if i >= len(lst): # 아직 0을 안채워줬기 때문에 실제 N보다 더 작을 수 있다.
                rot_A[i][j] = 0
            else:
                rot_A[i][j] = lst[i]
    debug =1
    return rot_A

# [0] 시뮬 준비
r, c, k = map(int, input().split())
A = [list(map(int, input().split())) for _ in range(3)]
# A = [[1]*105 for _ in range(105)]
N, M = 3, 3

# for a in A:
#     print(*a)
# [1] 시뮬 실행
time = 0
while True:
    # 종료 조건
    if time > 100 :
        break
    if 0 <= r-1 < N and 0 <= c-1 < M and A[r-1][c-1] == k:
        break
    new_A = [] # 수정 염두

    # R 연산
    if N >= M :
        new_M = 0
        for i in range(N):
            # 0. 행 추출
            lst = A[i]

            # 1. 규칙 따라 정렬
            lst = sort_lst(lst)

            # 2. 정렬된 lst 모으고
            new_A.append(lst)

            # 3. N, M 값 갱신
            new_M = max(new_M, len(lst))
        M = min(new_M, 100)
    # C 연산
    else :
        new_N = 0
        for j in range(M) :

            # 0. 열 추출
            lst = []
            for i in range(N) :
                lst.append(A[i][j])

            # 1. 규칙 따라 정렬
            lst = sort_lst(lst)

            # 2. 정렬된 lst 알맞게 배치
            new_A.append(lst)

            # 3. N, M 값 갱신
            new_N = max(new_N, len(lst))

        # 4. 행<-> 열 치환
        N = min(new_N, 100)
        new_A = rotate(new_A)

    # 4. 새로운 A 배열 생성
    for i in range(N) :
        lst = new_A[i]
        if len(lst) < M :
            lst.extend([0]*(M-len(lst)))
    A = new_A
    time += 1

# [2] 시뮬 정답
print(time if time <= 100 else -1)