def deleteBT(self, m, oldKey):
    # oldKey가 있된 노드의 경로를 탐색하며, 스택에 경로 저장
    found, stack = self.searchPath(self.T, m, oldKey, None)
    if found == False:
        return  # oldKey를 발견 못함. 삭제 불가.

    x = stack.pop()

    if oldKey is not in terminal node:  # oldKey를 내부 노드에서 발견.
        internalNode = x
        i = index of oldKey in internalNode

        # 후행키의 위치 탐색 (Ki와 일치하는 키는 찾지 못하나, 노드 경로는 검색)
        found2, stack = self.searchPath(x.P[i], m, x.K[i], stack)

        # 후행키와 oldKey를 교환함.
        x = stack.pop()  # x는 후행키가 있는 단말노드
        temp = internalNode.K[i]
        internalNode.K[i] = x.K[1]
        x.K[1] = temp  # 이제 x.K[1]이 oldKey임

    finished = False
    self.deleteKey(self, m, x, oldKey) # 노드 x에서 oldKey를 삭제

    if stack:
        y = stack.pop() # 노드 y는 x의 부모 노드

    while True:
        if isRoot(x) or x.n >= (round(m/2)-1): # underflow 발생하지 않음
            finished = True
        else: # underflow 발생
            # 키 재분배 또는 노드 합병을 위한 형제 노드를 결정
            bestSibling = self.bestSibling(T, m, x, y)

            if y.P[bestSibling].n > (round(m/2)- 1): # bestSibling에서 재분배
                redistributeKeys(T, m, x, y, bestSibling)
                finished = True
            else: # bestSibling과 노드 합병
                mergeNode(T, m, x, y, bestSibling)
                x = y
                if stack:
                    y = stack.pop()
                else:
                    finished = True
        if not finished:
            continue
        break

    if y.n == 0: # y에 키가 없음.(비어 있음)
        T = y.P[0]
        discard y node # old root를 삭제, 트리 높이가 하나 줄어듬.

    def deleteKey(self, m, x, oldKey):
        # oldKey의 위치 i를 탐색
        i = 1
        while oldKey > x.K[i]:
            i = i + 1

        # oldKey 보다 큰 키들을 왼쪽으로 한 칸씩 이동
        while i <= x.n:
            x.K[i] = x.K[i+1]
            x.P[i] = x.P[i+1]
            i = i + 1
        x.n = x.n - 1

    def bestSibling(self, m, x, y):
        # y에서 x의 위치 i를 탐색
        i = 0
        while y.P[i] != x:
            i += 1

        # 바로 인접한 두 형제 중, 키의 개수가 많은 형제를 bestSibling으로 선택함.
        if I == 0:
            bestSibling = i + 1 # 왼쪽 형제가 없음
        elif i == y.n:
            bestSibling = i – 1 # 오른쪽 형제가 없음
        elif y.P[i–1].n >= y.P[i+1].n:
            bestSibling = i – 1
        else:
            bestSibling = i + 1
        return bestSibling

    def redistributeKeys(T, m, x, y, bestSibling):
        # y에서 x의 위치 i를 탐색
        i = 0
        while y.P[i] != x:
            i += 1

        bestNode = y.P[bestSibling]
        if bestSibling < i: # bestSibling이 왼쪽 형제 노드
            lastKey = bestNode.K[bestNode.n]
            self.insertKey(T, m, x, null, y.K[i])
            self.deleteKey(T, m, bestNode, lastKey)
            y.K[i] = lastKey
        else: # bestSibling이 오른쪽 형제 노드
            firstKey = bestNode.K[1]
            self.insertKey(T, m, x, null, y.K[i + 1])
            self.deleteKey(T, m, bestNode, firstKey)
            y.K[i + 1] = firstKey

    def mergeNode(T, m, x, y, bestSibling):
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
        bestNode.n = bestNode.n + 1
        j = 1
        while j <= x.n:
            bestNode.K[bestNode.n + 1] = x.K[j]
            bestNode.P[bestNode.n] = x.P[j–1]
            bestNode.n = bestNode.n + 1

        bestNode.P[bestNode.n] = x.P[x.n]
        self.deleteKey(m, y, y.K[i])
        discard x node

