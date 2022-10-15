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

    # find position to insert newKey while storing parent node on stack
    while p is not None:
        if newKey == p.key:
            print('i', newKey, ': The key already exists')
            return

        q = p
        stack.append(q)

        if newKey < p.key:
            p = p.left
        else:
            p = p.right

    # create new node
    newNode = getNode()
    newNode.key = newKey

    # insert newNode as a child of q
    if T is None:
        T = newNode
    elif newKey < q.key:
        q.left = newNode
    else:
        q.right = newNode

    # update height while popping parent node from stack
    while stack:
        q = stack.pop()
        q.height = height(q)

    global tree
    tree = T

def deleteBst(T,deleteKey):
    p = T
    q = None
    stack = []

    #find position of deleteKey while storing parent node on stack
    while p is not None and not deleteKey == p.key:
        q = p
        stack.append(q)

        if deleteKey < p.key:
            p = p.left
        else:
            p = p.right

    if p is None: #deleteKey was not found
        print('d', deleteKey, ': The key does not exists')
        return

    #case of degree 2 is reduced to case of degree 0 or case of degree 1
    '''if p.left is not None and p.right is not None:
        if p.left.height > p.right.height:
            r = maxNode(p.left)
            flag = "LEFT"
        elif p.left.height < p.right.height:
            r = minNode(p.right)
            flag = "RIGHT"
        else:
            if noNodes(p.left) >= noNodes(p.right):
                r = maxNode(p.left)
                flag = "LEFT"
            else:
                r = minNode(p.right)
                flag = "RIGHT"
            p = p.right
            while p.left is not None:
                stack.append(p)
                p = p.left
        p.key = r.key
        if flag == "LEFT":
            deleteBst(p.left,r.key)
        else:
            deleteBst(p.right,r.key)'''
    if p.left is not None and p.right is not None:
        stack.append(p)
        tempNode = p

        if p.left.height <= p.right.height:
            p,temp_stack = minNode(p.right)
            stack += temp_stack
        else:
            p,temp_stack = maxNode(p.left)
            stack += temp_stack

        tempNode.key = p.key
        q = stack[-1]

    #now degree of p is 0 or 1
    #delete p from T
    if p.left is None and p.right is None:
        if q is None:
            T = None
        elif q.left == p:
            q.left = None
        else:
            q.right = None
    else:
        if not p.left is None: #case of degree 1
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

    #update height while popping parent node from stack
    while stack:
        q =stack.pop()
        q.height =height(q)

def inorderBST(T):
    if T is not None:
        inorderBST(T.left)
        print(T.key,end=' ')
        inorderBST(T.right)

def height(T):
    if T is None:
        return 0
    left = height(T.left)
    right = height(T.right)

    return max(left, right) + 1

def minNode(T):
    temp_T = T
    temp_stack = []
    while temp_T.left is not None:
        temp_stack.append(temp_T)
        temp_T = temp_T.left
    return temp_T,temp_stack

def maxNode(T):
    temp_T = T
    temp_stack = []
    while temp_T.right is not None:
        temp_stack.append(temp_T)
        temp_T = temp_T.right
    return temp_T,temp_stack

def noNodes(T):
    cnt = 0
    if T is not None:
        cnt = 1+noNodes(T.left)+noNodes(T.right)
    return cnt

f = open('BST-input.txt','r')

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
