class getNode:
    def __init__(self,m):
        self.height = 1
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
        found, stack = self.searchPath(m, newKey, None)
        if found == True: # newKey를 발견함. 삽입 불가.
            print('i', newKey, ': The key already exists')
            return

        # newKey가 없으므로, T에 삽입 (이제 x는 null)
        finished = False
        print("stack(len):",len(stack))
        x = stack.pop()
        print("now_x:",x.K,"now_x.n:",x.n)
        left = None # 새로 분할된 왼쪽 노드를 담을 변수
        y = None # 새로 분할된 오른쪽 노드를 담을 변수

        while True:
            if x.n < m-1: # Overflow 발생 여부 검사
                # Overflow 발생 안함. newKey를 노드 x의 올바른 위치에 삽입
                self.insertKey(m, x,left, y, newKey)
                finished = True
            else: # Overflow 발생
                # x를 newKey을 기준으로 분할, 분할된 노드 반환
                left, newKey, y = self.splitNode(m, x, left, y, newKey)
                print("111231x:", x.K, "1231123123x.n:", x.n)
                
                if stack:
                    x = stack.pop()
                else: # 트리의 레벨이 하나 증가
                    self.T = getNode(m)
                    self.T.K[1] = newKey
                    self.T.n = 1
                    self.T.P[0] = left
                    self.T.P[1] = y
                    print("*****************************************T.K:,T.n",self.T.K,self.T.n)
                    print("T.P[0]:,T.P[0].n:", self.T.P[0].K,self.T.P[0].n)
                    print("T.P[1]:,T.P[0].n:", self.T.P[1].K,self.T.P[1].n)
                    finished = True
            if not finished: continue
            break

    def searchPath(self, m, key, stack):
        if stack == None:
            stack = []

        x = self.T

        while True:
            i = 1
            while i <= x.n and key > x.K[i]:
                i += 1

            # 삽입할 키를 발견함. 삽입 불가
            if i <= x.n and key == x.K[i]:
                return True, stack

            # for some i where K[i–1] < key < K[i], 삽입할 키를 아직 발견하지 못함.
            stack.append(x)
            x = x.P[i-1]
            if x is not None: continue
            break

        return False, stack

    def insertKey(self, m, x,left, y, newKey):
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
        x.P[i-1] = left
        x.P[i] = y
        x.n = x.n + 1


    def splitNode(self, m, x,left, y, newKey):
        tempNode = x # 오버플로우를 위한 임시 노드(x와 newKey를 저장)
        print("전tempNode:", tempNode.K)
        self.insertKey(m, tempNode,left, y, newKey)
        print("tempNode:",tempNode.K)
        centerKey = tempNode.K[int(m/2)+1] # 분할 기준인 중앙값

        left = getNode(m) # centerKey 이전 값을 노드 x로 복사
        i = 1
        while tempNode.K[i] < centerKey:
            left.K[i] = tempNode.K[i]
            left.P[i-1] = tempNode.P[i-1]
            i += 1
            left.n += 1
        left.P[i-1] = tempNode.P[i-1]
        print("left:",left.K,"left.n:",left.n)

        newNode = getNode(m) # centerKey 이후 값을 노드 newNode로 복사

        i +=1
        print("i",i,'tempNode.n:',tempNode.n)
        while i <= tempNode.n:
            newNode.K[i-m+1] = tempNode.K[i]
            newNode.P[i-m] = tempNode.P[i-1]
            i += 1
            newNode.n += 1

        newNode.P[i-1] = tempNode.P[i-1]

        print("newNode:",newNode.K)
        return left, centerKey, newNode

    def height(self,node): # 높이 구하기
        if node is None:
            return 0
        left = self.height(node.left)
        right = self.height(node.right)

        return max(left, right) + 1

    def inorderBT(self,node):
        if node is not None:
            print(node.K)
            for x in node.P:
                if x != 0:
                    self.inorderBT(x)
            #print(node.K)

        #for x in node.P:
        #    print(x.K)
        #    self.inorderBT(x)
        #    for i in x.K:
        #        print("{0}".format(i), end=' ')

f = open('BT-input.txt', 'r')

BT_tree = BT()

for line in f:
    cmd, key = line.split()
    if cmd == 'i':
        BT_tree.insertBT(3,int(key))
    elif cmd == 'd':
        continue
        # BT_tree.deleteBT(int(key))
    BT_tree.inorderBT(BT_tree.T)
    print()

''' for line in f:
    cmd, key = line.split()
    if cmd == 'i':
        BT_tree.insertBT(4,int(key))
    elif cmd == 'd':
        continue
        # BT_tree.deleteBT(int(key))
    BT_tree.inorderBT(BT_tree.T)
    print()
    '''
