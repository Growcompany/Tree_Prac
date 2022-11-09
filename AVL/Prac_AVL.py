class getNode:
    def __init__(self):
        self.key = None
        self.left = None
        self.right = None
        self.height = 1
        self.bf = 0

def insertBST(T, newKey):
    p = T
    q = None
    stack = []

    # 새로운 키를 넣을 공간 찾기, stack에는 q(부모노드)저장
    while p is not None:
        if newKey == p.key: #키가 이미 노드에 존재
            print('i', newKey, ': The key already exists')
            return

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
    if T is None:
        T = newNode
    elif newKey < q.key:
        q.left = newNode
    else:
        q.right = newNode

    # stack에있는 노드높이 업데이트
    while stack:
        q = stack.pop()
        q.height = height(q)

    return T

def insertAVL(T, newKey):
    T = insertBST(T,newKey) #Step1 - BST 삽입 알고리즘 이용

    global AVL_tree
    AVL_tree = T
    rotationType, p, q = checkBalance(T,newKey) # Step2 - 균형검사 p는 불균형 위치, q는 p의 부모, 균형 트리면 "NO"리턴

    if rotationType != "NO":
        rotateTree(T,rotationType,p,q)
    else:
        print("NO", end=' ')
        return

    AVL_tree = T

def checkBalance(T, newKey):
    f = None
    a = T
    p = T
    q = None

    #Step1 - newKey의 삽입 위치 q를 찾음
    while p is not None:
        if p.bf != 0:
            a = p
            f = q
        if newKey < p.key:
            q = p
            p = p.left
        elif newKey > p.key:
            q = p
            p = p.right
        else:
            q = p
            break

    #Step2 - BF 계산
    if a is not None:
        if newKey < a.key:
            p = a.right
            b = q
            d = -1
        else:
            p = a.left
            b = p
            d = 1

    while p != q:
        if p == None:
            break
        if newKey < p.key:
            p.bf = 1
            p = p.left
        else:
            p.bf = -1
            p = p.right

    #Step3 - 트리 균형 여부를 검사
    unbalanced = True
    if a is not None:
        if a.bf != 0 or (a.bf+d) != 0: #트리가 균형일 때
            a.bf = a.bf+d
            unbalanced = False
    rotateType = "NO"

    if unbalanced == True: #트리가 불균형이라 회전 유형을 결정
        if d == 1: #왼쪽 불균형일 때
            if b.bf == 1:
                rotateType = "LL"
            else:
                rotateType = "LR"
        else:
            if b.bf == -1:
                rotateType = "RR"
            else:
                rotateType = "RL"
    return rotateType,a,f

def rotateTree(T,rotateType,p,q):
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
        b = c

    if q is not None:
        T = b
    elif a == q.left:
        q.left = b
    elif a == q.right:
        q.right = b

def bf(T):
    p = None
    if T is None:
        return 0
    left = bf(T.left)
    right = bf(T.right)
    T.bf = left-right

    return p

def height(T):
    if T is None:
        return 0
    left = height(T.left)
    right = height(T.right)

    return max(left, right) + 1

#rotateTree(T, rotationType, p, q)

#deleteBST(T, deleteKey)

def r_rotate(T): #오른쪽 회전
    x = T.left
    print("x.key:",x.key)
    if x.right == None:
        T.left = None
    else:
        T.left = x.right
    T.left = None if x.right == None else x.right
    x.right = T
    T.height = 1 + max(0 if T.left == None else T.left.height, 0 if T.right == None else T.right.height)
    x.height = 1 + max(0 if x.left == None else x.left.height, 0 if x.right == None else x.right.height)
    return x

def l_rotate(T): #왼쪽 회전
    x = T.right
    T.right = None if x.left == None else x.left
    x.left = T
    T.height = 1 + max(0 if T.left == None else T.left.height, 0 if T.right == None else T.right.height)
    x.height = 1 + max(0 if x.left == None else x.left.height, 0 if x.right == None else x.right.height)
    return x

def inorderAVL(T):
    if T is not None:
        inorderAVL(T.left)
        print("({0}, {1}, {2})".format(T.key,T.bf, T.height),end=' ')
        inorderAVL(T.right)


f = open('AVL-input.txt', 'r')

global AVL_tree
AVL_tree = None

for line in f:
    cmd, key = line.split()
    if cmd == 'i':
        insertAVL(AVL_tree,int(key))
    elif cmd == 'd':
        print()
        #deleteAVL(AVL_tree,int(key))
    inorderAVL(AVL_tree)
    print()