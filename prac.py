class getNode:
    def __init__(self):
        self.key = None
        self.left = None
        self.right = None
        self.height = 1

def insert(T, newKey):
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

def inorder(T):
    if T is not None:
        inorder(T.left)
        print(T.key,end=' ')
        inorder(T.right)

def height(T):
    if T is None:
        return 0
    left = height(T.left)
    right = height(T.right)

    return max(left, right) + 1

global tree
tree = None

f = open('BST-input.txt','r')

for line in f:
    cmd, key = line.split()
    if cmd == 'i':
        insert(tree,int(key))
        inorder(tree)
    print()
