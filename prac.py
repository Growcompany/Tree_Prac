class node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class binarytree:
    def __init__(self):
        self.root = None

    def insert(self, newKey):
        p = self.root
        q = None
        stack = []

        # find position to insert newKey while storing parent node on stack
        while not p == None:
            if newKey == p.key:
                print('i', newKey, ': The key already exists')
                return

            q = p
            stack.append(q)

            if newKey < p.key:
                p = p.left
            elif newKey > p.key:
                p = p.right

        # create new node
        newNode = node(newKey)
        newNode.key = newKey

        # insert newNode as a child of q
        if self.root == None:
            self.root = newNode
        elif newKey < q.key:
            q.left = newNode
        else:
            q.right = newNode

        # update height while popping parent node from stack
        while stack:
            q = stack.pop()
            # q.height = 1+max(q.left.height, q.right.height)

    # REMOVE

    def remove(self, data):
        if self.root != None:
            self._remove(data, self.root)

    def _remove(self, data, cur_node):
        if cur_node == None:
            return cur_node
        if data < cur_node.data:
            cur_node.left = self._remove(data, cur_node.left)
        elif data > cur_node.data:
            cur_node.right = self._remove(data, cur_node.right)
        else:
            if cur_node.left is None and cur_node.right is None:
                print('Removing Leaf Node')
                if cur_node == self.root:
                    self.root = None
                del cur_node
                return None
            if cur_node.left is None:
                print('Removing None with Right Child')
                if cur_node == self.root:
                    self.root = cur_node.right
                tempnode = cur_node.right
                del cur_node
                return tempnode
            elif cur_node.right is None:
                print('Removing None with Left Child')
                if cur_node == self.root:
                    self.root = cur_node.left
                tempnode = cur_node.left
                del cur_node
                return tempnode
            print('Removing Node with 2 Children')
            tempnode = self.getpred(cur_node.left)
            cur_node.data = tempnode.data
            cur_node.left = self._remove(cur_node.data, cur_node.left)
        return cur_node

    def getpred(self, cur_node):
        if cur_node.right != None:
            return self.getpred(cur_node.right)
        return cur_node

    # INORDER TRAVERSAL

    def inorder(self):
        if self.root != None:
            self._inorder(self.root)

    def _inorder(self, cur_node):
        if cur_node != None:
            self._inorder(cur_node.left)
            print(cur_node.data,end=' ')
            self._inorder(cur_node.right)

    # MINIMUM VALUE

    def minval(self):
        if self.root != None:
            return self._minval(self.root)

    def _minval(self, cur_node):
        if cur_node.left != None:
            return self._minval(cur_node.left)
        return cur_node.data

    # MAXIMUM VALUE

    def maxval(self):
        if self.root != None:
            return self._maxval(self.root)

    def _maxval(self, cur_node):
        if cur_node.right != None:
            return self._maxval(cur_node.right)
        return cur_node.data


tree = binarytree()

f = open('BST-input.txt','r')

for line in f:
    cmd, key = line.split()
    if cmd == 'i':
        tree.insert(int(key))
        tree.inorder()
    elif cmd == 'd':
        tree.remove(int(key))
    print()

tree.insert(100)
tree.insert(90)  # 100
tree.insert(110)  # /	\
tree.insert(95)  # 90   110
tree.insert(30)  # /  \
#		30    95
tree.remove(110)
tree.remove(90)

tree.inorder()

print(tree.minval())
print(tree.maxval())
