"""
한줄평:
- 다시 도전하기 전에 '배열 돌리기' 문제를 풀고 템플릿을 익히고 도전하니 잘 풀렸다
- 나 도형 문제 (특히 돌리고, 뒤집고, 밀고) 정말 못푼다. 주말에 무조건 브론즈/실버 도형문제 잔뜩 풀자

1차 시도: 실패 (1시간 40분)
2차 시도 : 성공

소요 시간) 1시간 20분
타임라인) 이해 및 구상 : 15분 - 구현 : 35분  - 디버깅 : 30분
사용한 알고리즘) 시뮬레이션 (도형)

[구상]
+) 실제로 오픈 TC를 시뮬레이션 해보며(특히 먼지퍼지기 부분) 잘못 구상한 것을 바로잡았다.
+) 배열 돌리기 부분을 상세히 그림을 그려놓고 좌표도 표시해 실수를 줄였다 (없진 않았다) 
-) 시뮬레이션이라 시간 복잡도를 덜 고려했다 (체크는 했어야했다. )

[구현]
+) (T초 동안 반복 + 각각의 함수 호출 ) 이라는 큰 틀을 코드상에서 미리 써놓으니  좋았다.
+) 함수의 기능과 리턴값을 구현하기 주석으로 명시하니 좋았다
-) 공기청정기에 먼지가 들어갔을 때의 상황을 미리 구상하지 않고 단순히 돌릴 때 좌표 변화만 집중했다

[디버깅]
+) 단위 테스트하는 방법을 주현님한테 배웠는데 너무너무너무 좋았다! (debug = 0, 1, 2.. 단위로 테스트)
    => 기능별로 테스트하니 오류도 빨리 발견하고, 이후 문제가 재발생했을 때도 해당 디버그 위치를 다시 참조하는 방식으로 이전보다는 체계적으로 디버깅
-) 인덱스를 잘못 사용했을 때 곰곰히 생각해보고 고치는게 아니라 이거 1 증가시켜보고, 1빼보고...하는 식으로 무분별하게 했다
    => 손코딩에 인덱스를 다시 표시하고 코드를 고치자

[시간/공간 복잡도]
- 예상한 복잡도) O(T*(N*M)*N) = O(T) : T초동안 반복 * O(N^2) : 전체좌표 완탐하며 미세먼지 확산 * O(4N) : 배열 shift
- 실제 복잡도) O(T)*(O(N*M)+O(4N) : 전체 좌표 탐색(O(N^2)과 가장자리 돌면서 배열 shift(O(4N)) 은 별도의 과정이므로 곱하기가 아닌 더하기

[EdgeCase]
- 고려한 Edge Case) X
- 고려하지 못한 Edge Case) 
"""

delta = [(-1, 0), (0, -1), (0, 1), (1, 0)]

def oob(ni, nj) :
    return not (0 <= ni < N and 0 <= nj < M)

def spread() :
    '''
    미세먼지 퍼지는 정도를 조건따라 계산해서 A 배열 변경
    :return: X
    '''
    cp = [[0]*M for _ in range(N)]

    # 1) 각 먼지의 증감값 도출
    for ci in range(N): # delta 적용할거면 무조건 ci, cj로 쓰자
        for cj in range(M):
            if A[ci][cj] == -1:
                continue

            t = A[ci][cj] // 5
            if t > 0:
                cnt = 0
                for di, dj in delta:
                    ni, nj = ci+di, cj+dj

                    # 범위 체크
                    if oob(ni, nj) or A[ni][nj] == -1:
                        continue

                    cp[ni][nj] += t
                    # A[ni][nj] += t
                    cnt += 1
                cp[ci][cj] -= cnt*t
                # A[ci][cj] -= cnt*t

    # 2) 증감값 A 배열에 반영
    for i in range(N):
        for j in range(M):
            if A[i][j] != -1 :
                A[i][j] += cp[i][j]


def refresh_up(si, sj, ei, ej) :
    '''
    위의 공기청정기로 A 배열 값들 가장자리만 <반시계> 회전 (A배열 변경)
    :param si, sj: 대상 직사각형 좌상단 좌표
    :param ei, ej: 대상 직사각형 우하단 좌표
    :return: X
    '''

    # 왼쪽 끝열 ↓
    for i in range(ei-1, si-1, -1):
        if A[i+1][sj] == -1 :
            continue
        A[i+1][sj] = A[i][sj]

    # 맨위 1열 ←
    for j in range(sj+1, ej+1) :
        A[si][j-1] = A[si][j]

    # 오른쪽 끝열 ↑
    for i in range(si+1, ei+1) :
        A[i-1][ej] = A[i][ej]

    # 맨아래 끝열 →
    for j in range(ej-1, sj-1, -1):
        if j == sj:
            A[ei][j] = 0
        A[ei][j+1] = A[ei][j]

    A[up[0]][up[1]] = -1


def refresh_dwn(si, sj, ei, ej):
    '''
    위의 공기청정기로 A 배열 값들 가장자리만 <시계> 회전 (A배열 변경)
    :param si, sj: 대상 직사각형 좌상단 좌표
    :param ei, ej: 대상 직사각형 우하단 좌표
    :return: X
    '''

    # 왼쪽 끝열 ↑
    for i in range(si+1, ei+1):
        if A[i-1][sj] == -1:
            continue
        A[i-1][sj] = A[i][sj]

    # 맨아래 끝열 ←
    for j in range(sj+1, ej+1):
        A[ei][j-1] = A[ei][j]

    # 오른쪽 끝열 ↓
    for i in range(ei-1, si-1, -1):
        A[i+1][ej] = A[i][ej]

    # 맨위 1열 →
    for j in range(ej-1, sj-1, -1):
        if j == sj:
            A[si][j] = 0
        A[si][j+1] = A[si][j]

    A[dwn[0]][dwn[1]] = -1

# [0] 시뮬레이션 준비
N, M, T = map(int, input().split())
A = [list(map(int, input().split())) for _ in range(N)]

# 공기 청정기 찾기
for i in range(N):
    if A[i][0] == -1:
        up = (i, 0)
        dwn = (i+1, 0)
        break
    # debug = 0

# [1] 시뮬레이션 실행
for _ in range(T):
    # 1) 미세먼지 확산
    spread()
    # debug = 1

    # 2) 공기 청정 (위, 반시계)
    refresh_up(0, 0, up[0], M-1)
    # debug = 2

    # 3) 공기 청정 (아래, 시계)
    refresh_dwn(dwn[0], 0, N-1, M-1)
    # debug = 3


# [2] 시뮬레이션 출력
ans = 0
for i in range(N):
    for j in range(M) :
        if A[i][j] != -1:
            ans += A[i][j]
# debug = 4
print(ans)