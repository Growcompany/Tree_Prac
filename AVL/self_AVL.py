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

    def insertAVL(self, newKey):
        if self.T == None:
            y = getNode()
            y.key = newKey
            self.T = y
            print("NO", end=' ')
            return

        if not self.insertBST(newKey): #Step1 - BST 삽입 알고리즘 이용, 만약 존재할 시 리턴
            return

        rotationType, p, q = self.checkBalance(newKey) # Step2 - 균형검사 p는 불균형 위치, q는 p의 부모, 균형 트리면 "NO"리턴

        if rotationType != "NO":
            self.rotateTree(rotationType,p,q)
        else:
            print("NO", end=' ')
            return

    def checkBalance(self, newKey):
        f = None
        a = self.T
        p = self.T
        q = None
        x = None
        stack = []

        #Step1 - newKey의 삽입 위치 검색
        while p is not None:
            if p.bf != 0: #bf가 0이 아닐 때(즉, 위치를 찾기 직전 부모노드 저장용)
                a = p # newKey의 삽입위치
                f = q # newKey의 삽입위치 부모노드

            if newKey < p.key: # newKey가 현재 삽입위치보다 클 때
                q = p
                stack.append(q)
                p = p.left #p를 왼쪽으로 움긴다.
            elif newKey > p.key: # newKey가 현재 삽입위치보다 클 때
                q = p
                stack.append(q)
                p = p.right
            else:
                q = p # newKey가 현재p와 같을때 삽입위치 찾음으로 위치를 q로 지정
                stack.append(q)
                break

        unbalanced = False
        #Step2 - BF 계산
        while stack:
            q = stack.pop()
            q.height = 1 + max(self.height(q.left),self.height(q.right))
            q.bf = self.height(q.left)-self.height(q.right)
            #print("q:", q.key, "q.bf:", q.bf, "left_height:",self.height(q.left), "right_height",self.height(q.right))

            if 1 < q.bf or q.bf < -1:
                if x is None:
                    x = q
                unbalanced = True

        if unbalanced: #Step3 - 트리 균형 여부를 검사 #트리가 불균형이라 회전 유형을 결정
            if 1 < x.bf: #왼쪽이 불균형일 때
                if x.left.bf > 0:
                    rotateType = "LL"
                else:
                    rotateType = "LR"
            else:
                if x.right.bf < 0:
                    rotateType = "RR"
                else:
                    rotateType = "RL"
        else:
            rotateType = "NO"

        return rotateType,a,f

    def rotateTree(self,rotateType,p,q):
        if rotateType == "LL":
            print("LL", end = ' ')
            a = p
            b = p.left
            a.left = b.right
            b.right = a
            a.bf = 0
            b.bf = 0
        elif rotateType == "LR":
            print("LR", end=' ')
            a = p
            b = p.left
            c = b.right
            b.right = c.left
            a.left = c.right
            c.left = b
            c.right = a
            if c.bf == 0: #LR(A)
                b.bf = 0
                a.bf = 0
            elif c.bf == 1: #LR(B)
                a.bf = -1
                b.bf = 0
            elif c.bf == -1: #LR(C)
                b.bf = 1
                a.bf = 0
            c.bf = 0
            c.height = self.height(c)
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
            if c.bf == 0: #RL(A)
                b.bf = 0
                a.bf = 0
            elif c.bf == 1: #RL(B)
                a.bf = 0
                b.bf = -1
            elif c.bf == -1: #RL(C)
                b.bf = 0
                a.bf = 1
            c.bf = 0
            c.height = self.height(c)
            b = c

        a.height = self.height(a)
        b.height = self.height(b)

        if q is None:
            self.T = b
        elif a == q.left:
            q.left = b
        elif a == q.right:
            q.right = b

        self.T.height = 1 + max(self.height(self.T.left), self.height(self.T.right))
        self.T.bf = self.height(self.T.left) - self.height(self.T.right)
        #print("T:",self.T.key,"T.bf:",self.T.bf,"T.left.height:",self.height(self.T.left),"T.right.height:",self.height(self.T.right))

    #deleteBST(T, deleteKey)

    def height(self,node):
        if node is None:
            return 0
        left = self.height(node.left)
        right = self.height(node.right)

        return max(left, right) + 1

    def inorderAVL(self,node):
        if node is not None:
            self.inorderAVL(node.left)
            print("({0}, {1})".format(node.key,node.bf),end=' ')
            #print("({0}, {1}, {2})".format(T.key,T.bf, T.height),end=' ')
            self.inorderAVL(node.right)

f = open('AVL-input.txt', 'r')

AVL_tree = AVL()

for line in f:
    cmd, key = line.split()
    if cmd == 'i':
        AVL_tree.insertAVL(int(key))
    elif cmd == 'd':
        print()
        #AVL_tree.deleteAVL(int(key))
    AVL_tree.inorderAVL(AVL_tree.T)
    print()