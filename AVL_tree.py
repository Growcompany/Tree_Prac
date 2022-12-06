class getNode:
    def __init__(self):
        self.key = None
        self.left = None
        self.right = None
        self.height = 1
        self.bf = 0

class AVL:
    def __init__(self):
        self.T = None

    def insertBST(self, newKey):
        p = self.T
        q = None
        stack = []

        # 새로운 키를 넣을 공간 찾기, stack에는 q(부모노드)저장
        while p is not None:
            if newKey == p.key: #키가 이미 노드에 존재
                print('i', newKey, ': The key already exists')
                return False

            q = p
            stack.append(q)
            if newKey < p.key:
                p = p.left
            else:
                p = p.right

        # 노드 생성(newkey를 key로 가진)
        newNode = getNode()
        newNode.key = newKey

        # q의 자식노드로 newNode 삽입
        if self.T is None:
            self.T = newNode
        elif newKey < q.key:
            q.left = newNode
        else:
            q.right = newNode

        # stack에있는 노드높이 업데이트
        while stack:
            q = stack.pop()
            q.height = self.height(q)

        return True

    def deleteBST(self, deleteKey):
        p = self.T
        q = None
        f = None
        stack = []
        x = None

        # 삭제할 노드 위치 찾기, stack에는 q(조상인 노드)저장
        while p is not None and deleteKey != p.key:
            q = p
            stack.append(q)

            if deleteKey < p.key:
                p = p.left
            else:
                p = p.right

            f = q  # newKey의 삽입위치 부모노드

        if p is None:  # 삭제할 키가 없을 때
            print('d', deleteKey, ': The key does not exist')
            f = None
            return f, False, x

        # 삭제할 노드의 차수가 2일때
        if p.left is not None and p.right is not None:
            stack.append(p)
            tempNode = p

            if p.left.height <= p.right.height:
                p = p.right
                while p.left is not None:
                    stack.append(p)
                    p = p.left
            else:
                p = p.left
                while p.right is not None:
                    stack.append(p)
                    p = p.right

            tempNode.key = p.key
            q = stack[-1]

        # 삭제할 노드의 차수가 1이나 0일때
        if p.left is None and p.right is None:  # 노드의 차수가 0일때
            if q is None:
                self.T = None
            elif q.left == p:
                q.left = None
            else:
                q.right = None
        else:
            if not p.left is None:  # 노드의 차수가 1일때
                if q is None:
                    self.T = self.T.left
                elif q.left == p:
                    q.left = p.left
                else:
                    q.right = p.left
            else:
                if q is None:
                    self.T = self.T.right
                elif q.left == p:
                    q.left = p.right
                else:
                    q.right = p.right

        del p

        # stack에있는 노드 높이,bf 업데이트
        while stack:
            q = stack.pop()
            q.height = self.height(q)
            q.bf = self.height(q.left) - self.height(q.right)
            if 1 < q.bf or q.bf < -1:  # bf가 불균형일 때
                if x is None:
                    x = q  # 불균형 저장

        return f, True, x

    def noNodes(self,T): # w자식 노드의 갯수 체크
        cnt = 0
        if T is not None:
            cnt = 1 + self.noNodes(T.left) + self.noNodes(T.right) #재귀로 왼쪽 오른쪽 다 돌면서 하나씩 추가
        return cnt

    def maxNode(self,T): #최대노드의 값 구하기
        temp_T = T #가장 큰 노드로 이용할 변수
        temp_stack = [] #가장 큰 노드까지 있는 노드들 저장
        while temp_T.right is not None:  # right 자식노드가 없을 때까지 탐색 = 제일 오른쪽(큰) 노드
            temp_stack.append(temp_T)
            temp_T = temp_T.right
        return temp_T, temp_stack

    def minNode(self,T):#최소노드의 값 구하기
        temp_T = T #가장 작은 노드로 이용할 변수
        temp_stack = [] #가장 작은 노드까지 있는 노드들 저장
        while temp_T.left is not None:  # left 자식노드가 없을 때까지 탐색 = 제일 왼쪽(큰) 노드
            temp_stack.append(temp_T)
            temp_T = temp_T.left
        return temp_T, temp_stack

    def insertAVL(self, newKey):
        if self.T == None: #처음 아무것도 없을 때 새로 getNode()로 새로 생성
            y = getNode()
            y.key = newKey
            self.T = y
            print("NO", end=' ')
            return

        if not self.insertBST(newKey): #Step1 - BST 삽입 알고리즘 이용, 만약 이미 존재하는 키일시 리턴
            return

        rotationType, p, q = self.checkBalance(newKey) # Step2 - 균형검사 p는 불균형 위치, q는 p의 부모, 균형 트리면 "NO"리턴

        if rotationType != "NO":
            self.rotateTree(rotationType,p,q) #재균형이 필요할 시 재균형 실시
        else:
            print("NO", end=' ')
            return

    def deleteAVL(self, deleteKey):

        #Step 1 - BST삭제 알고리즘 실행
        q,found,x = self.deleteBST(deleteKey) # q: 삭제한노드의 부모노드, found: 삭제가능여부, x: 불균형노드
        x_has = False
        if x is not None:
            x_has = True
            # Step2 - 균형검사 p는 불균형 위치, q는 p의 부모, 균형 트리면 "NO"리턴
            rotationType, p, q = self.checkBalance(x.key)

            if rotationType != "NO":
                self.rotateTree(rotationType, p, q)
            else:
                print("NO", end=' ')
                return

        if found: #삭제성공
            if q == None: #삭제한 키의 부모노드가 없을 때
                if not x_has:
                    print("NO", end=' ')
                return
        else: # 삭제할 키를 못 찾았을 때
            return

        # Step2 - 균형검사 p는 불균형 위치, q는 p의 부모, 균형 트리면 "NO"리턴
        rotationType, p, q = self.checkBalance(q.key)

        if not x_has:
            if rotationType != "NO":
                self.rotateTree(rotationType,p,q)
            else:
                print("NO", end=' ')

    def checkBalance(self, newKey):
        f = None # 삽입위치의 부모노드 저장용
        a = self.T  # 삽입위치 저장용
        p = self.T  # 위치 탐색용
        q = None # 스택저장용
        x = None # 불균형발견 시 저장용
        stack = [] # newKey까지 부모노드들 스택

        #Step1 - newKey의 삽입 위치 검색
        while p is not None:
            if p.bf != 0: #bf가 0이 아닐 때(즉, 위치를 찾기 직전 부모노드 저장용), 새로 추가하는 노드는 bf가 0
                a = p # newKey의 삽입위치
                f = q # newKey의 삽입위치 부모노드

            if newKey < p.key: # newKey가 현재 삽입위치보다 클 때
                q = p
                stack.append(q)
                p = p.left #p를 왼쪽 갱신
            elif newKey > p.key: # newKey가 현재 삽입위치보다 클 때
                q = p
                stack.append(q)
                p = p.right #p를 오른쪽 갱신
            else:
                q = p # newKey가 현재p와 같을때 삽입위치 찾음으로 위치를 q로 지정
                stack.append(q)
                break

        unbalanced = False
        #Step2 - BF 계산
        while stack: #스택에 있는 부모노드들 높이 및 bf 업데이트
            q = stack.pop()
            q.height = 1 + max(self.height(q.left),self.height(q.right))
            q.bf = self.height(q.left)-self.height(q.right)

            if 1 < q.bf or q.bf < -1: # bf가 불균형일 때
                if x is None:
                    x = q # 불균형 저장
                unbalanced = True # 불균형 발생

        if unbalanced: #Step3 - 트리 균형 여부를 검사 #트리가 불균형이라 회전 유형을 결정
            if 1 < x.bf: #왼쪽이 불균형일 때
                if x.left.bf > 0: #왼쪽에서 왼쪽노드의 bf가 양수면 LL형태
                    rotateType = "LL"
                else:
                    rotateType = "LR"
            else: #오른쪽 불균형 일 때
                if x.right.bf < 0: #오른쪽의 오른쪽노드의 bf가 음수면 RR형태
                    rotateType = "RR"
                else:
                    rotateType = "RL"
        else:
            rotateType = "NO"

        return rotateType,a,f

    def rotateTree(self,rotateType,p,q):
        if rotateType == "LL":
            print("LL", end = ' ')
            a = p # 불균형위치를 a로 지정
            b = p.left # 불균형위치에서 왼쪽 부분을 b로 지정
            a.left = b.right # a의 왼쪽을 b의 오른쪽 부분으로 지정
            b.right = a # b의 오른쪽 부분을 a로 지정
            a.bf = 0 # a의 균형은 0
            b.bf = 0 # b의 균형은 0
        elif rotateType == "LR":
            print("LR", end=' ')
            a = p
            b = p.left
            c = b.right
            b.right = c.left
            a.left = c.right
            c.left = b
            c.right = a
            if c.bf == 0: #LR c의 균형이 0이면 a랑 b도 0
                b.bf = 0
                a.bf = 0
            elif c.bf == 1: #LR c의 균형이 1이면 a는 -1 b는 0
                a.bf = -1
                b.bf = 0
            elif c.bf == -1: #LR c의 균형이 -1이면 a는 0 b는 1
                b.bf = 1
                a.bf = 0
            c.bf = 0
            c.height = self.height(c) #높이
            b = c
        elif rotateType == "RR":
            print("RR", end = ' ')
            a = p
            b = p.right
            a.right = b.left
            b.left = a
            a.bf = 0
            b.bf = 0
        elif rotateType == "RL":
            print("RL", end=' ')
            a = p
            b = p.right
            c = b.left
            b.left = c.right
            a.right = c.left
            c.right = b
            c.left = a
            if c.bf == 0: #RL
                b.bf = 0
                a.bf = 0
            elif c.bf == 1: #RL
                a.bf = 0
                b.bf = -1
            elif c.bf == -1: #RL
                b.bf = 0
                a.bf = 1
            c.bf = 0
            c.height = self.height(c)
            b = c

        #a와 b의 높이 업데이트
        a.height = self.height(a)
        b.height = self.height(b)

        if q is None: #부모 노드가 없으면 바로 넣기
            self.T = b
        elif a == q.left: #부모노드의 왼쪽이 a면 서브트리를 부모노드의 왼쪽에 삽입
            q.left = b
        elif a == q.right: #부모노드의 오른쪽이 a면 서브트리를 부모노드의 왼쪽에 삽입
            q.right = b

        # 루트노드 높이랑 bf 업데이트
        self.T.height = 1 + max(self.height(self.T.left), self.height(self.T.right))
        self.T.bf = self.height(self.T.left) - self.height(self.T.right)

    def height(self,node): # 높이 구하기
        if node is None:
            return 0
        left = self.height(node.left)
        right = self.height(node.right)

        return max(left, right) + 1

    def inorderAVL(self,node):
        if node is not None:
            self.inorderAVL(node.left)
            print("({0}, {1})".format(node.key,node.bf),end=' ')
            self.inorderAVL(node.right)

f = open('AVL-input.txt', 'r')

AVL_tree = AVL()

for line in f:
    cmd, key = line.split()
    if cmd == 'i':
        AVL_tree.insertAVL(int(key))
    elif cmd == 'd':
        AVL_tree.deleteAVL(int(key))
    AVL_tree.inorderAVL(AVL_tree.T)
    print()
