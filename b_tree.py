class getNode:
    def __init__(self,m):
        self.n = 0
        self.K = [0 for i in range(m+1)]
        self.P = [None for i in range(m+1)]

class BT:
    def __init__(self):
        self.T = None

    def insertBT(self, m, newKey):

        # 루트 노드 생성
        if self.T == None:
            self.T = getNode(m) # T.n ← 0; T. Ki ← null; Pi ← null;
            self.T.K[1] = newKey
            self.T.n = 1
            return

        # newKey를 삽입할 노드의 경로를 탐색하며, 스택에 경로 저장
        found, stack = self.searchPath(self.T, m, newKey, None)
        if found == True: # newKey를 발견함. 삽입 불가.
            print('i', newKey, ': The key already exists')
            return

        # newKey가 없으므로, T에 삽입 (이제 x는 null)
        finished = False
        x = stack.pop()
        y = None # 새로 분할된 오른쪽 노드를 담을 변수

        while True:
            if x.n < m-1: # Overflow 발생 여부 검사
                # Overflow 발생 안함. newKey를 노드 x의 올바른 위치에 삽입
                self.insertKey(m, x, y, newKey)
                finished = True
            else: # Overflow 발생
                # x를 newKey을 기준으로 분할, 분할된 노드 반환
                left, newKey, y = self.splitNode(m, x, y, newKey)
                x.K = left.K
                x.P = left.P
                x.n = left.n

                if stack:
                    x = stack.pop()
                else: # 트리의 레벨이 하나 증가
                    self.T = getNode(m)
                    self.T.K[1] = newKey
                    self.T.n = 1 #새 노드의 키 1개
                    self.T.P[0] = x #새 노드의 왼쪽 부분
                    self.T.P[1] = y #새 노드의 오른쪽 부분
                    finished = True
            if not finished: continue
            break

    def searchPath(self, T, m, key, stack):
        if stack == None:
            stack = []

        x = T

        while True:
            i = 1
            while i <= x.n and key > x.K[i]:
                i += 1

            stack.append(x)

            # 삽입할 키를 발견함. 삽입 불가
            if i <= x.n and key == x.K[i]:
                return True, stack

            # for some i where K[i–1] < key < K[i], 삽입할 키를 아직 발견하지 못함.
            x = x.P[i-1]
            if x is not None: continue
            break

        return False, stack

    def insertKey(self, m, x, y, newKey):
        # newKey 보다 큰 키들을, 오른쪽으로 한 칸씩 이동
        i = x.n
        while i>=1 and newKey < x.K[i]:
            x.K[i+1] = x.K[i]
            x.P[i+1] = x.P[i]
            i = i-1

        while x.K[i] < newKey:
            i += 1
            if x.K[i] == 0: break

        # newKey를 삽입
        x.K[i] = newKey
        x.P[i] = y
        x.n = x.n + 1

    def splitNode(self, m, x, y, newKey):
        tempNode = x # 오버플로우를 위한 임시 노드(x와 newKey를 저장)
        self.insertKey(m, tempNode, y, newKey)
        centerKey = tempNode.K[round(m/2)] # 분할 기준인 중앙값

        left = getNode(m) # centerKey 이전 값을 노드 x로 복사
        i = 1
        while tempNode.K[i] < centerKey:
            left.K[i] = tempNode.K[i]
            left.P[i-1] = tempNode.P[i-1]
            i += 1
            left.n += 1
        left.P[i-1] = tempNode.P[i-1]

        newNode = getNode(m) # centerKey 이후 값을 노드 newNode로 복사

        i +=1
        newNode_i = 1 # newNode에 앞에서부터 centerKey 이후 값을 넣기 위한 체크용 변수
        while i <= tempNode.n:
            newNode.K[newNode_i] = tempNode.K[i]
            newNode.P[newNode_i-1] = tempNode.P[i-1]
            i += 1
            newNode_i += 1
            newNode.n += 1

        newNode.P[newNode_i-1] = tempNode.P[i-1]

        return left, centerKey, newNode

    def deleteBT(self, m, oldKey):
        # oldKey가 있된 노드의 경로를 탐색하며, 스택에 경로 저장
        found, stack = self.searchPath(self.T, m, oldKey, None)

        if not found:
            print('d', oldKey, ': The key does not exist')
            return

        for i in stack:
            print("&&&&&&&", i.K)

        x = stack.pop()
        y = None
        print("삭제를 찾은 노드: ", x.K, " 삭제할키: ", oldKey)

        leaf = True # 리프 노드인지 체크용

        for pointer in x.P:
            if pointer is not None:
                leaf = False
                break

        if not leaf:  # oldKey를 내부 노드에서 발견.
            print("리프노드아님")
            internalNode = x
            i = internalNode.K.index(oldKey)

            stack.append(x)
            # 후행키의 위치 탐색 (Ki와 일치하는 키는 찾지 못하나, 노드 경로는 검색)
            found2, stack = self.searchPath(x.P[i], m, x.K[i], stack)

            for wow in stack:
                print("~~~~~~~~",wow.K)

            # 후행키와 oldKey를 교환함.
            x = stack.pop()  # x는 후행키가 있는 단말노드
            print(internalNode.K)
            temp = internalNode.K[i]
            internalNode.K[i] = x.K[1]
            x.K[1] = temp  # 이제 x.K[1]이 oldKey임

        finished = False
        self.deleteKey(m, x, oldKey) # 노드 x에서 oldKey를 삭제

        if stack:
            y = stack.pop() # 노드 y는 x의 부모 노드

        while True:
            if x.K == self.T.K or x.n >= (round(m/2)-1): # underflow 발생하지 않음
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
        x.n -= 1

    def bestSibling(self, m, x, y):
        # y에서 x의 위치 i를 탐색
        i = 0
        while y.P[i] != x:
            i += 1

        # 바로 인접한 두 형제 중, 키의 개수가 많은 형제를 bestSibling으로 선택함.
        if i == 0:
            bestSibling = i + 1 # 왼쪽 형제가 없음
        elif i == y.n:
            bestSibling = i - 1 # 오른쪽 형제가 없음
        elif y.P[i].n >= y.P[i+1].n:
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
            lastKey = bestNode.K[bestNode.n]
            self.insertKey(m, x, None, y.K[i])
            x.P[1] = x.P[0]
            x.P[0] = bestNode.P[bestNode.n]
            bestNode.P[bestNode.n] = None
            self.deleteKey(m, bestNode, lastKey)
            y.K[i] = lastKey
        else: # bestSibling이 오른쪽 형제 노드
            firstKey = bestNode.K[1]
            self.insertKey(m, x, None, y.K[i + 1])
            x.P[x.n] = bestNode.P[0]
            bestNode.P[0] = bestNode.P[1]
            self.deleteKey(m, bestNode, firstKey)
            y.K[i + 1] = firstKey

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
        while j <= x.n:
            bestNode.K[bestNode.n + 1] = x.K[j]
            bestNode.P[bestNode.n] = x.P[j-1]
            bestNode.n = bestNode.n + 1
            j+=1
        bestNode.P[bestNode.n] = x.P[x.n]
        self.deleteKey(m, y, y.K[i])
        del x

    def inorderBT(self,T,m):
        i = 0
        while i < T.n:
            if T.P[i] is not None:
                self.inorderBT(T.P[i],m)
            print(T.K[i+1],end=' ')
            i += 1
        if T.P[i] is not None:
            self.inorderBT(T.P[i], m)


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
