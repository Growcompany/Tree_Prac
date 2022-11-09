def insertAVL(T, newKey):
    p = T;
    q = None;
    x = None;
    f = None;
    stack = [];

    # find position to insert newKey while storing parent node on stack
    while p is not None:
        if newKey == p.key:
            return

        q = p;
        stack.append(q)

    if newKey < p.key:
        p = p.left
    else:
        p = p.right;

    # create new node
    y = getAVLNode();
    y.key = newKey;

    # insert y as a child of q
    if T is None:
        T = y
    elif newKey < q.key:
        q.left = y
    else:
        q.right = y

    # update height and balancing factor while popping parent node from stack
    while stack:
        q = stack.pop()
        q.height = 1 + max(q.left.height, q.right.height)
        q.bf = q.left.height - q.right.height

        if 1 < q.bf or q.bf < -1:
            if x is None:
                x = q
                f = stack[-1]

    # if there's no problem, return
    if x is None:
        return;

    # rebalance tree
    if 1 < x.bf:
        if x.left.bf < 0:
            rotate
            LR
        else:
            rotate
            LL;
    else:
        if x.right.bf > 0:
            rotate
            RL;
        else:
            rotate
            RR;


def deleteAVL(T, deleteKey):
    p = T;
    q = None;
    x = None;
    f = None;
    stack = [];

    # perform standard BST deletion
    # find position of deleteKey while storing parent node on stack
    while p is not None and deleteKey != p.key:
        q = p;
        stack.append(q)

        if deleteKey < p.key:
            p = p.left;
        else:
            p = p.right;

    if p is None:
        return  # deleteKey was not found

    # case of degree 2 is reduced to case of degree 0 or case of degree
    if p.left is not None and p.right is not None:
        stack.append(p)
        tempNode = p

        if p.left.height <= p.right.height:
            p = p.right
            while p.left is not None:
                stack.append(p)
                p = p.left
        else:
            p = p.left;
            while p.right is not None:
                stack.append(p)
                p = p.right

        tempNode.key = p.key;
        q = stack[-1]

    # now degree of p is 0 or 1
    # delete p from T
    if p.left is None and p.right is None:  # case of degree 0
        if q is None:
            T = None  # case of root
        elif q.left == p:
            q.left = None
        else:
            q.right = None
    else:  # case of degree 1
        if p.left is not None:
            if q is None:
                T = T.left  # case of root
            elif q.left == p:
                q.left = p.left
            else:
                q.right = p.left;
        else:
            if q is None:
                T = T.right  # case of root
            elif q.left == p:
                q.left = p.right
            else:
                q.right = p.right

    del p

    # update height and balancing factor while popping parent node from stack
    while not stack:
        q = stack.pop()
        q.height = 1 + max(q.left.height, q.right.height)
        q.bf = q.left.height - q.right.height

        if 1 < q.bf or q.bf < -1:
            if x is None:
                x = q
                f = stack[-1]

    # if there's no problem, return
    if x is None:
        return

    # rebalance tree
    if 1 < x.bf:
        if x.left.bf < 0:
            rotate
            LR;
        else:
            rotate
            LL;
    else:
        if x.right.bf > 0:
            rotate
            RL;
        else:
            rotate
            RR;