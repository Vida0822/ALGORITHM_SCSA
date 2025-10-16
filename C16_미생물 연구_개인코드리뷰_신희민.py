"""
한줄평:
답이 중간 부터 틀림
=> 디버거: 답이 맞는데까진 동작이 잘 되는지 확인 + 답이 틀린 부분부터 원인 찾기


소요 시간) 2시간 20분
타임라인) 이해 및 구상 : 40분(화장실 5분) - 구현 : 60분 (~첫 실행)  - 디버깅 : 40 분
사용한 알고리즘)

[구상]
+) 자료 구조를 명확히 정의했다
-) 각 자료구조가 언제 변화하고, 언제 새로운걸로 만들어줄지 결정하는 부분을 제대로 정하지 않고 덕지덕지했고,
그거 때문에 오히려 나중에 손구상 보고 디버깅할 때 헷갈렸다.
=> 디버깅 할 때 큰 흐름 맞춰 로직 점검하는 단계에서는 ***손코딩이 아닌 문제랑 비교**
-) 미친...조건 빠트림 ('크기가 같다면 먼저 들어온 애들부터') : 이건 진짜 대실수... -> 이거 제대로 읽었으면 idx 관리했어야하는거 일찍 알았을 듯
-) 입력이 이상한걸 디버거 찍어봐야 알았다 : 오픈 TC를 고려 안했다는 얘기

[구현]
+) 불필요한 단위 테스트를 줄이고 빠르게 전체 구현
-> 이후 전체 점검하면서 수정하니까 오히려 로직도 안해치고 적절히 수정함
-) 문제 조건과 다르게 입력받고 임의로 문제 로직 수정 : 도저히 생각이 안나서 반전시켰지만...
  문제 설명과 그대로 구현할 수 있는 방법 有?
-) 생각하고 추가해야할 로직을 임의로 추가

-) 상대 좌표 템플릿을 아는게 아니었구나....

< '상대 좌표' = 시작 좌표 + new 좌표 - 기준 좌표 >
di, dj = grp[0]
for gi, gj in grp:
    ni, nj = si+gi-di, sj+dj-dj

-) narr, ngr oups 등 새로운걸 만들고 넣어주는 로직 처리가 서툴다
-) idx, turn 변수명을 혼용해서 사용 (헷갈리고, 전역으로 참조하기에 잘못 참조할수도 있었음)

*****
-) 중간에 로직을 한번 크게 수정해줬는데
   (그룹 인덱스를 계속 유지해야했기에 그룹을 삭제하지 않고 계속 갖고 있어주는걸로 수정)
    => 사이드 이펙트를 여기저기 간신히 고침 : put(), move(), score()에 모두 영향 주는데 이걸 정리 안하고 바로 손대다가 엄청 꼬임
    - 갑자기 range(key)로 정렬을 한다던가,,, append()해주던거를 빈 리스트를 준다던가... 잘못했으면 디버깅 못했음
    => 자료 구조 수정 필요시, 손 구상에 확실히 정리하고, 함수 순차적으로 수정

-) 고려 못한 함수 막 만듬 (move 쪽도)
-) 함수 하나를 쭉 짜는게 아니라 여기저기 왔다갔다거림

+) **** 구현하고 바로 실행 안하고 전체 코드 점검하는 time 잘 지킴(주석도 틈틈히) => 실제로 여기서 오류 몇개 잡음
    ㄴ 근데...문제랑 비교하는게 아니라 그냥 코드만 보는 느낌? 문제 순서대로 따라갔어야함

[디버깅]
-) 답 다르게 나왔을 때... 코드 전체 점검 또 안하고 그냥 딛버거 돌림

(오류 내용)
- 먹혀서 아예 격자에 존재하지 않는 경우 고려 X
  : 여전히 분기별 처리 누락하는 경우 多
  -> if 를 썼다면, else에 어떤 로직이 와야할지 항상 염두
- 상대 좌표 : 기준 좌표(좌상단)을 (0, 0)으로 맞췄어햐는데, 그냥 배열 돌리기처럼 (si, sj)를 더해줌


[시간/공간 복잡도]
- 예상한 복잡도)
- 실제 복잡도)

[EdgeCase]
- 고려한 Edge Case)
- 고려하지 못한 Edge Case)
"""




from collections import deque
from itertools import combinations

# [0]
N, Q = map(int, input().split())
arr = [[0]*N for _ in range(N)]
groups = [-1]  # 1 based index
removed = [False]*(Q+1) # 1 based index


# [1]
def oob(ni, nj):
    return not (0 <= ni < N and 0 <= nj < N)


def bfs(si, sj, colors, v):
    # [0]
    q = deque()
    grp = []

    # [1]
    v[si][sj] = 1
    q.append((si, sj))
    grp.append((si, sj))

    # [2]
    while q:
        ci, cj = q.popleft()

        for di, dj in ((0, -1), (-1, 0), (0, 1), (1, 0)) :
            ni, nj = ci+di, cj+dj

            if oob(ni, nj) or v[ni][nj] :
                continue

            if arr[ni][nj] in colors:
                v[ni][nj] = 1
                q.append((ni, nj))
                grp.append((ni, nj))

    return grp


def put(idx, si, sj, ei, ej):
    '''
    미생물 투입하는 함수 (그냥 행 반전됐다고 생각하고 그대로 넣어주기 -> 디버깅 할때만 반대로 print)
    :param si, sj: 시작점 (포함)
    :param ei, ej: 끝점 (포함)
    :return: X -> arr, groups 변경
    '''

    # 1. 1칸씩 완탐하면서
    ngrp = []
    eaten = []
    for i in range(si, ei):
        for j in range(sj, ej):
            if arr[i][j] != 0 :  # 다른 미생물이 있다면
                eaten.append(arr[i][j])  # 삭제 예정 (그루핑 check 대상)
            arr[i][j] = idx
            ngrp.append((i, j))
    groups.append(ngrp)

    # 2. 먹힌 애들 아직도 연결되어있는지 확인
    for fidx in eaten :
        fgrp = groups[fidx] # 기존 그룹 좌표들
        flag = False
        v = [[0]*N for _ in range(N)]
        for fi, fj in fgrp:
            if arr[fi][fj] == fidx and not v[fi][fj]:# 여전히 안먹히고 남아있다면
                if flag :  # 그루핑을 한번 했는데 또 그루핑을 해야하는 상황이라면
                    removed[fidx] = True
                    break
                else:
                    fgrp = bfs(fi, fj, {fidx}, v)
                    flag = True
        if not flag : # 한번도 그루핑이 안되었을 때 (격자에서 아예 사라짐)
            removed[fidx] = True
        groups[fidx] = fgrp  # 새로 구한 좌표 넣어주기 (좌표 일부 삭제됨)


def try_move(si, sj, grp, narr):
    '''
    새로운 배양 용기에 배치할 수 있는지 확인하는 함수
    :param si:
    :param sj:
    :param grp:
    :return:
    '''
    # 기준 좌표
    grp.sort()
    di, dj = grp[0]
    for gi, gj in grp:
        ni, nj = si+gi-di, sj+gj-dj
        if oob(ni, nj) or narr[ni][nj]:
            return False
    return True


def real_move(si, sj, grp, narr, idx):
    '''
    실제로 새로운 배양 용기에 배치하는 함수
    :param si:
    :param sj:
    :param grp:
    :return:
    '''
    ngrp = []
    di, dj = grp[0]
    for gi, gj in grp:
        ni, nj = si+gi-di, sj+gj-dj
        ngrp.append((ni, nj))
        narr[ni][nj] = idx
    return ngrp # 이동한 좌표 list


def move_all(turn):
    '''
    새로운 배양 용기로 옮기기 : 각 그룹 좌표 list 조회하면서
    => groups, arr <- ngroups, narr
    :return:
    '''
    global arr
    narr = [[0] * N for _ in range(N)]

    # 1. 영역 넓은 애들부터 차지하도록 정렬
    keys = list(range(1, turn+1))
    keys.sort(key=lambda key : (-len(groups[key]), key))

    # 2. 무리 하나씩 옮기기
    for idx in keys:

        # 상태 체크
        if removed[idx] :
            continue # 새 그룹에 포함 X (간접 삭제)

        grp = groups[idx]

        # 놓을 수 있는 시작 좌표 찾고
        flag = False
        for sj in range(N):
            if flag : break
            for si in range(N):
                if narr[si][sj] == 0: # 빈 칸이면

                    # 그 시작 좌표에서 놓았을때 형태 유지 가능?
                    if try_move(si, sj, grp, narr):
                        ngrp = real_move(si, sj, grp, narr, idx) # narr 변경
                        groups[idx] = ngrp
                        flag = True
                        break

        # 놓을 수 없으면 삭제 처리
        if not flag:
            removed[idx] = True

    arr = narr


def score(turn):
    # 두 그룹을 조합해 인접한지 확인하는 함수
    # => 점수 도출

    comb = list(combinations(range(1, turn + 1), 2))
    scr = 0

    # 1. 두 그룹 뽑고
    for a_idx, b_idx in comb:
        if removed[a_idx] or removed[b_idx] :
            continue

        a = groups[a_idx]
        b = groups[b_idx]

        # 2. 좌표하나 추출해서, 두 색깔로 그루핑
        v = [[0] * N for _ in range(N)]
        sgrp = bfs(a[0][0], a[0][1], {a_idx, b_idx}, v)

        # 3. 길이가 같으면 인접 => 점수 누적
        if len(sgrp) == len(a) + len(b) :
            scr += len(a)*len(b)

    return scr


## MAIN ##
for turn in range(1, Q+1):

    # 1. 투입하기
    sj, si, ej, ei = map(int, input().split())
    # si, sj, ei, ej = map(int, input().split())
    put(turn, si, sj, ei, ej)
    debug = 0

    # 2. 옮기기
    move_all(turn) # arr <- narr, groups <- ngroups
    debug = 1

    # 3. 실험 결과 추출
    scr = score(turn)
    debug = 2

    # 4.정답 출력
    print(scr)
    debug = 3