class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.height = 1

def getHeight(node):
    return node.height if node else 0

def getBalance(node):
    return getHeight(node.left) - getHeight(node.right) if node else 0

def rightRotate(y):
    x = y.left
    T2 = x.right
    x.right = y
    y.left = T2
    y.height = 1 + max(getHeight(y.left), getHeight(y.right))
    x.height = 1 + max(getHeight(x.left), getHeight(x.right))
    return x

def leftRotate(x):
    y = x.right
    T2 = y.left
    y.left = x
    x.right = T2
    x.height = 1 + max(getHeight(x.left), getHeight(x.right))
    y.height = 1 + max(getHeight(y.left), getHeight(y.right))
    return y

def deleteNode(root, key):
    if not root:
        return root
    if key < root.data:
        root.left = deleteNode(root.left, key)
    elif key > root.data:
        root.right = deleteNode(root.right, key)
    else:
        if not root.left:
            return root.right
        elif not root.right:
            return root.left
        temp = findMin(root.right)
        root.data = temp.data
        root.right = deleteNode(root.right, temp.data)
    root.height = 1 + max(getHeight(root.left), getHeight(root.right))
    balance = getBalance(root)
    if balance > 1 and getBalance(root.left) >= 0:
        return rightRotate(root)
    if balance > 1 and getBalance(root.left) < 0:
        root.left = leftRotate(root.left)
        return rightRotate(root)
    if balance < -1 and getBalance(root.right) <= 0:
        return leftRotate(root)
    if balance < -1 and getBalance(root.right) > 0:
        root.right = rightRotate(root.right)
        return leftRotate(root)
    return root

def treeToVine(root):
    vine_tail = dummy = Node(None)
    dummy.right = root
    current = dummy.right

    while current:
        if current.left:
            rotated = rightRotate(current)
            vine_tail.right = rotated
            current = rotated
        else:
            vine_tail = current
            current = current.right

    return dummy.right

def countNodes(root):
    count = 0
    current = root
    while current:
        count += 1
        current = current.right
    return count

def compress(root, count):
    scanner = root
    for _ in range(count):
        if scanner.right:
            rotated = leftRotate(scanner.right)
            scanner.right = rotated
            scanner = rotated


def vineToTree(root, size):
    leaves = size + 1 - 2 ** (size.bit_length() - 1)
    compress(root, leaves)
    size = size - leaves
    while size > 1:
        compress(root, size // 2)
        size //= 2

def balanceDSW(root):
    vine_root = Node(None)
    vine_root.right = root
    vine_root.right = treeToVine(root)
    size = countNodes(vine_root.right)
    vineToTree(vine_root, size)
    return vine_root.right

def insertBST(root, data):
    if root is None:
        return Node(data)
    if data < root.data:
        root.left = insertBST(root.left, data)
    else:
        root.right = insertBST(root.right, data)
    return root

def inOrderTraversal(node):
    if node:
        inOrderTraversal(node.left)
        print(node.data, end=", ")
        inOrderTraversal(node.right)

def preOrderTraversal(node):
    if node:
        print(node.data, end=", ")
        inOrderTraversal(node.left)
        inOrderTraversal(node.right)

def postOrderTraversal(node):
    if node:
        inOrderTraversal(node.left)
        inOrderTraversal(node.right)
        print(node.data, end=", ")

def findMin(node):
    current = node
    while current.left:
        current = current.left
    return current.data

def findMax(node):
    current = node
    while current.right:
        current = current.right
    return current.data

def insertAVL(root, key):
    if not root:
        return Node(key)
    elif key < root.data:
        root.left = insertAVL(root.left, key)
    else:
        root.right = insertAVL(root.right, key)

    root.height = 1 + max(getHeight(root.left), getHeight(root.right))
    balance = getBalance(root)

    if balance > 1 and key < root.left.data:
        return rightRotate(root)
    if balance < -1 and key > root.right.data:
        return leftRotate(root)
    if balance > 1 and key > root.left.data:
        root.left = leftRotate(root.left)
        return rightRotate(root)
    if balance < -1 and key < root.right.data:
        root.right = rightRotate(root.right)
        return leftRotate(root)
    return root

def insertBST(root, data):
    if root is None:
        return Node(data)
    if data < root.data:
        root.left = insertBST(root.left, data)
    else:
        root.right = insertBST(root.right, data)
    return root

def deleteTreePostOrder(node):
    if node:
        node.left = deleteTreePostOrder(node.left)
        node.right = deleteTreePostOrder(node.right)
        print(f"Usuwam: {node.data}")
        node = None
    return node

def sortedArrayToAVL(arr):
    if not arr:
        return None
    mid = len(arr) // 2
    root = Node(arr[mid])
    root.left = sortedArrayToAVL(arr[:mid])
    root.right = sortedArrayToAVL(arr[mid+1:])
    root.height = 1 + max(getHeight(root.left), getHeight(root.right))
    return root
def export(node):
    if not node.left and not node.right:
        return f"node {node.data}"
    l_str = f"child {{{export(node.left)}}}" if node.left else "child[missing]"
    r_str = f"child {{{export(node.right)}}}" if node.right else "child[missing]"
    return f"node {node.data} {{{l_str} {r_str}}}"

def main(tree_root):
    return f"\\{export(tree_root)};"
def getHelp():
    print("Print - wypisuje drzewo używając in-order, post-order, pre-order\n")
    print("MinAndMax - wypisuje minimun i maximum w drzewie\n")
    print("Remove - *\n")
    print("Delete - usuwa całe drzewo w post-order\n")
    print("Export - *\n")
    print("Rebalance - *\n")
    print("Help - wypisuje komendy i ich opisy\n")
    print("Exit - kończy program\n")
def getTree(k,l):
    k = input("Wybierz AVL czy BST: ")
    l = list(map(int, input("Podaj liczby do skostruktowania drzewa (rozdzielaj je spacją): ").split()))
if __name__ == "__main__":
    root = None
    konstrukt = input("Wybierz AVL czy BST: ")
    liczby = list(map(int, input("Podaj liczby do skostruktowania drzewa (rozdzielaj je spacją): ").split()))
    if konstrukt.lower()=='bst':
        print("Inserting >> ",liczby)
        for num in liczby:
            root = insertBST(root, num)
    elif konstrukt.lower()=='avl':
        print("Inserting >> ", liczby)
        for num in liczby:
            root = insertAVL(root, num)
        #print(sortedArrayToAVL(root))
        print("Mediana >> ")
    while True:
        print("Wybierz operacje: Print, MinAndMax, Remove, Delete, Export, Rebalance, Help, Exit")
        choice = input("Wybierz operację >> ")
        choice=choice.lower()
        match choice:
            case "print":
                print("In-order: ", preOrderTraversal(root))
                print("Post-order: ", postOrderTraversal(root))
                print("Pre-order: ", preOrderTraversal(root))
            case "minandmax":
                if root:
                    print("Minimum:", findMin(root))
                    print("Maximum:", findMax(root))
                else:
                    print("Drzewo jest puste.")
            case "delete":
                root = deleteTreePostOrder(root)
                print("Drzewo usunięte.")
            case "help":
                getHelp()
            case "remove":
                val = int(input("Podaj wartość do usunięcia: "))
                root = deleteNode(root, val)
            case "export":
                print(main(root))
            case "rebalance":
                if root:
                    root = balanceDSW(root)
                    print("Zrównoważono drzewo metodą DSW.")
                else:
                    print("Drzewo jest puste.")
            case "exit":
                print("Koniec programu.")
                break
            case _:
                print("Nieprawidłowy wybór. Spróbuj ponownie.")