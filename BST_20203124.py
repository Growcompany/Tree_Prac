class getNode:
    def __init__(self):
        self.key = None
        self.left = None
        self.right = None
        self.height = 1

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

    global tree
    tree = T

def deleteBst(T,deleteKey):
    p = T
    q = None
    stack = []

    # 삭제할 노드 위치 찾기, stack에는 q(부모노드)저장
    while p is not None and not deleteKey == p.key:
        q = p
        stack.append(q)

        if deleteKey < p.key:
            p = p.left
        else:
            p = p.right

    if p is None: #삭제할 키가 없을 때
        print('d', deleteKey, ': The key does not exists')
        return

    # 삭제할 노드의 차수가 2일때
    if p.left is not None and p.right is not None:
        stack.append(p)
        tempNode = p

        if p.left.height > p.right.height:
            p,temp_stack = maxNode(p.left)
            stack += temp_stack
        elif p.left.height < p.right.height:
            p,temp_stack = minNode(p.right)
            stack += temp_stack
        else:
            if noNodes(p.left) >= noNodes(p.right):
                p, temp_stack = maxNode(p.left)
                stack += temp_stack
            else:
                p, temp_stack = minNode(p.right)
                stack += temp_stack

        tempNode.key = p.key
        q = stack[-1]

    # 삭제할 노드의 차수가 1이나 0일때
    if p.left is None and p.right is None: # 노드의 차수가 0일때
        if q is None:
            T = None
        elif q.left == p:
            q.left = None
        else:
            q.right = None
    else:
        if not p.left is None: # 노드의 차수가 1일때
            if q is None:
                T = T.left
            elif q.left == p:
                q.left = p.left
            else:
                q.right = p.left
        else:
            if q is None:
                T = T.right
            elif q.left == p:
                q.left = p.right
            else:
                q.right = p.right

    del p

    # stack에있는 노드 높이 업데이트
    while stack:
        q =stack.pop()
        q.height =height(q)

def height(T):
    if T is None:
        return 0
    left = height(T.left)
    right = height(T.right)

    return max(left, right) + 1

def noNodes(T):
    cnt = 0
    if T is not None:
        cnt = 1+noNodes(T.left)+noNodes(T.right)
    return cnt

def maxNode(T):
    temp_T = T
    temp_stack = []
    while temp_T.right is not None: # right 자식노드가 없을 때까지 탐색 = 제일 오른쪽(큰) 노드
        temp_stack.append(temp_T)
        temp_T = temp_T.right
    return temp_T,temp_stack

def minNode(T):
    temp_T = T
    temp_stack = []
    while temp_T.left is not None: # left 자식노드가 없을 때까지 탐색 = 제일 왼쪽(큰) 노드
        temp_stack.append(temp_T)
        temp_T = temp_T.left
    return temp_T,temp_stack

def inorderBST(T):
    if T is not None:
        inorderBST(T.left)
        print(T.key,end=' ')
        inorderBST(T.right)

f = open('BST-input.txt', 'r')

global tree
tree = None

for line in f:
    cmd, key = line.split()
    if cmd == 'i':
        insertBST(tree,int(key))
    elif cmd == 'd':
        deleteBst(tree,int(key))
    inorderBST(tree)
    print()