class getNode:
    def __init__(self,m):
        self.n = 0
        self.K = [float('-inf') for i in range(m+1)] # 노드의 m에 따른 길이의 키 리스트 생성
        self.P = [None for i in range(m+1)] # 노드의 m에 따른 길이의 포인터 리스트 생성

class BT:
    def __init__(self):
        self.T = None

    def insertBT(self, m, newKey):

        # 루트 노드가 없을 시 생성
        if self.T == None:
            self.T = getNode(m) # 기본 노드 생성
            self.T.K[1] = newKey # 첫 번째 키로 설정
            self.T.n = 1 # 개수 설정
            return

        # newKey를 삽입하기 위한 노드 경로 탐색, 경로를 스택에 저장
        found, stack = self.searchPath(self.T, m, newKey, None)
        if found == True: # newKey가 이미 있는지 found로 체크, 발견 시 삽입 불가
            print('i', newKey, ': The key already exists')
            return

        finished = False
        x = stack.pop() # x는 마지막 경로, newKey가 들어가야 될 노드
        y = None # 새로 분할된 오른쪽 노드를 담을 변수

        while True:
            if x.n < m-1: # Overflow 발생 여부 체크(발생 안함)
                # newKey를 노드 x에 삽입
                self.insertKey(m, x, y, newKey)
                finished = True # 오버플로우 발생안하고 삽입하면 성공
            else: # Overflow 발생
                # x를 newKey을 기준으로 분할, 분할된 노드 반환
                left, newKey, y = self.splitNode(m, x, y, newKey)
                x.K = left.K #left는 x노드를 임시로 담은 노드
                x.P = left.P
                x.n = left.n

                if stack: #오버플로우 발생 시 경로에 있는 선조 노드에 삽입하기 위함
                    x = stack.pop()
                else: # 트리 레벨 하나 증가, 모든 경로를 탐색해도 오버플로우면 새로 만듦
                    self.T = getNode(m)
                    self.T.K[1] = newKey
                    self.T.n = 1 #새 노드의 키 1개
                    self.T.P[0] = x #newKey 왼쪽 포인터 설정
                    self.T.P[1] = y #newKey 오른쪽 포인터 설정
                    finished = True
            if not finished: continue
            break

    def searchPath(self, T, m, key, stack):
        if stack == None: # 넘겨받은 stack이 없으면 새로 만들어주기
            stack = []

        x = T

        while True:
            i = 1
            while i <= x.n and key > x.K[i]: # i를 1 더해주며 위치 탐색
                i += 1

            stack.append(x) #현재 노드 stack에 경로 추가

            # 삽입할 키를 발견, 삽입 불가
            if i <= x.n and key == x.K[i]:
                return True, stack

            # 삽입할 키를 아직 발견하지 못함, 다음 포인터로 노드 이동
            x = x.P[i-1]
            if x is not None: continue
            break

        return False, stack

    def insertKey(self, m, x, y, newKey):
        i = x.n
        while i>=1 and newKey < x.K[i]: # newKey 보다 큰 키들을, 오른쪽으로 한 칸씩 이동
            x.K[i+1] = x.K[i]
            x.P[i+1] = x.P[i]
            i = i-1

        while x.K[i] < newKey: # newKey가 들어갈 위치 탐색
            i += 1
            if x.K[i] == float('-inf'): break

        # newKey를 삽입
        x.K[i] = newKey
        x.P[i] = y
        x.n = x.n + 1

    def splitNode(self, m, x, y, newKey):
        tempNode = x # 오버플로우를 위한 임시 노드(x와 newKey 저장)
        self.insertKey(m, tempNode, y, newKey)
        centerKey = tempNode.K[round(m/2)] # 분할 기준인 중앙 키

        left = getNode(m) # centerKey 왼쪽 값을 노드 left로 복사
        i = 1
        while tempNode.K[i] < centerKey:
            left.K[i] = tempNode.K[i]
            left.P[i-1] = tempNode.P[i-1]
            i += 1
            left.n += 1
        left.P[i-1] = tempNode.P[i-1]

        newNode = getNode(m) # centerKey 이후 값을 노드 newNode로 복사

        i +=1
        newNode_i = 1 # newNode의 앞에서부터 centerKey 이후 값을 넣기 위한 체크 변수
        while i <= tempNode.n:
            newNode.K[newNode_i] = tempNode.K[i]
            newNode.P[newNode_i-1] = tempNode.P[i-1]
            i += 1
            newNode_i += 1
            newNode.n += 1

        newNode.P[newNode_i-1] = tempNode.P[i-1]

        return left, centerKey, newNode

    def deleteBT(self, m, oldKey):
        # oldKey가 있는 노드의 경로를 탐색, 스택에 경로 저장
        found, stack = self.searchPath(self.T, m, oldKey, None)

        if not found:
            print('d', oldKey, ': The key does not exist')
            return

        x = stack.pop() # 삭제할 키가 있는 노드
        y = None # 노드 y는 x의 부모 노드

        leaf = True # 리프 노드인지 체크용

        for pointer in x.P: # 포인터가 없으면 말단 노드
            if pointer is not None:
                leaf = False
                break

        if not leaf:  # oldKey를 내부 노드에서 발견.
            internalNode = x
            i = internalNode.K.index(oldKey)

            stack.append(x)
            # 후행키의 위치 탐색 (Ki의 오른쪽 포인터에서 가장 가까운 키 탐색, 노드 경로 검색)
            found2, stack = self.searchPath(x.P[i], m, x.K[i], stack)

            # 후행키와 oldKey를 교환함.
            x = stack.pop()  # x는 후행키가 있는 단말노드
            temp = internalNode.K[i]
            internalNode.K[i] = x.K[1]
            x.K[1] = temp  # x.K[1]는 oldKey

        finished = False
        self.deleteKey(m, x, oldKey) # 노드 x에서 oldKey 삭제

        if stack:
            y = stack.pop() # 노드 y는 x의 부모 노드

        while True:
            if x.K == self.T.K or x.n >= (round(m/2)-1): # 루트노드거나 최소 키 수 유지되면 underflow 발생하지 않음
                finished = True
            else: # underflow 발생
                # 키 재분배 또는 노드 합병을 위한 형제 노드를 결정
                bestSibling = self.bestSibling(m, x, y)

                if y.P[bestSibling].n > (round(m/2)- 1): # bestSibling에서 재분배
                    self.redistributeKeys(m, x, y, bestSibling)
                    finished = True
                else: # bestSibling과 노드 합병
                    self.mergeNode(m, x, y, bestSibling)
                    x = y
                    if stack:
                        y = stack.pop()
                    else:
                        finished = True
            if not finished:
                continue
            break

        if y is not None and y.n == 0: # y에 키가 없음.(비어 있음)
            self.T = y.P[0]
            del y
            #discard y node # old root를 삭제, 트리 높이가 하나 줄어듬.

    def deleteKey(self, m, x, oldKey):
        # oldKey의 위치 i를 탐색
        i = 1
        while oldKey > x.K[i]:
            i += 1

        # oldKey 보다 큰 키들을 왼쪽으로 한 칸씩 이동
        while i <= x.n:
            x.K[i] = x.K[i+1]
            x.P[i] = x.P[i+1]
            i += 1
        x.n -= 1 # 키 하나 삭제했기에 개수 하나 감소

    def bestSibling(self, m, x, y):
        # y에서 x의 위치 i 탐색
        i = 0
        while y.P[i] != x:
            i += 1

        # 바로 인접한 두 형제 중, 키의 개수가 많은 형제를 bestSibling으로 선택
        if i == 0:
            bestSibling = i + 1 # 왼쪽 형제가 없음
        elif i == y.n:
            bestSibling = i - 1 # 오른쪽 형제가 없음
        elif y.P[i].n >= y.P[i+1].n: # y 포인터 왼쪽꺼가 오른쪽보다 개수가 많은 지에 따라 bestSibling 선택
            bestSibling = i - 1
        else:
            bestSibling = i + 1
        return bestSibling

    def redistributeKeys(self, m, x, y, bestSibling):
        # y에서 x의 위치 i를 탐색
        i = 0
        while y.P[i] != x:
            i += 1

        bestNode = y.P[bestSibling]
        if bestSibling < i: # bestSibling이 왼쪽 형제 노드
            lastKey = bestNode.K[bestNode.n] # lastKey는 왼쪽 형제노드에서 차출한 키
            self.insertKey(m, x, None, y.K[i])
            x.P[1] = x.P[0]
            x.P[0] = bestNode.P[bestNode.n]
            bestNode.P[bestNode.n] = None
            self.deleteKey(m, bestNode, lastKey) # 왼쪽 형제노드에서 lastKey 삭제
            y.K[i] = lastKey # 부모노드에 차출한 키를 올림
        else: # bestSibling이 오른쪽 형제 노드
            firstKey = bestNode.K[1] # firstKey는 오른쪽 형제노드에서 차출한 키
            self.insertKey(m, x, None, y.K[i + 1])
            x.P[x.n] = bestNode.P[0]
            bestNode.P[0] = bestNode.P[1] # 오른쪽 형제노드 포인터가 한칸 왼쪽으로
            self.deleteKey(m, bestNode, firstKey) # 오른쪽 형제노드에서  firstKey삭제
            y.K[i + 1] = firstKey # 부모노드에 차출한 키를 올림

    def mergeNode(self, m, x, y, bestSibling):
        i = 0 # y에서 x의 위치 i를 탐색
        while y.P[i] != x:
            i += 1

        bestNode = y.P[bestSibling]
        # 왼쪽 형제 노드로의 병합만 고려할 수 있도록 swap
        if bestSibling > i:
            bestSibling, i = i, bestSibling
            bestNode, x = x, bestNode

        # 왼쪽 형제 노드와 병합
        bestNode.K[bestNode.n + 1] = y.K[i]
        bestNode.n += 1
        j = 1
        while j <= x.n: # x.n개까지 x를 bestNode에 병합
            bestNode.K[bestNode.n + 1] = x.K[j]
            bestNode.P[bestNode.n] = x.P[j-1]
            bestNode.n = bestNode.n + 1
            j+=1
        bestNode.P[bestNode.n] = x.P[x.n]
        self.deleteKey(m, y, y.K[i])
        del x

    def inorderBT(self,T,m):
        i = 0
        while i < T.n: # 현재 노드의 개수만큼 반복
            if T.P[i] is not None:
                self.inorderBT(T.P[i],m) # 왼쪽 포인터부분부터 탐색
            print(T.K[i+1],end=' ') # 중간에 출력
            i += 1
        if T.P[i] is not None:
            self.inorderBT(T.P[i], m) # 마지막에 오른쪽 포인터부분 탐색


f = open('BT-input.txt', 'r')
BT_tree = BT()

for line in f:
    cmd, key = line.split()
    if cmd == 'i':
        BT_tree.insertBT(3,int(key))
    elif cmd == 'd':
        BT_tree.deleteBT(3,int(key))
    BT_tree.inorderBT(BT_tree.T,3)
    print()

f = open('BT-input.txt', 'r')
BT_tree = BT()

for line in f:
    cmd, key = line.split()
    if cmd == 'i':
        BT_tree.insertBT(4,int(key))
    elif cmd == 'd':
        BT_tree.deleteBT(4,int(key))
    BT_tree.inorderBT(BT_tree.T,4)
    print()
