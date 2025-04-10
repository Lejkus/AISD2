class AVLNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.height = 1

# ------------------- Wysokość i balans -------------------
def getHeight(node):
    return node.height if node else 0

def getBalance(node):
    return getHeight(node.left) - getHeight(node.right) if node else 0

# ------------------- Rotacje AVL -------------------
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

# ------------------- Wstawianie do AVL -------------------
def insert(root, key):
    if not root:
        return AVLNode(key)
    elif key < root.data:
        root.left = insert(root.left, key)
    else:
        root.right = insert(root.right, key)

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

# ------------------- Tworzenie drzewa z posortowanej tablicy -------------------
def sortedArrayToAVL(arr):
    if not arr:
        return None

    mid = len(arr) // 2
    root = AVLNode(arr[mid])
    root.left = sortedArrayToAVL(arr[:mid])
    root.right = sortedArrayToAVL(arr[mid+1:])
    root.height = 1 + max(getHeight(root.left), getHeight(root.right))
    return root

# ------------------- Traversale -------------------
def inOrderTraversal(node):
    if node:
        inOrderTraversal(node.left)
        print(node.data, end=", ")
        inOrderTraversal(node.right)

def preOrderTraversal(node):
    if node:
        print(node.data, end=", ")
        preOrderTraversal(node.left)
        preOrderTraversal(node.right)

def postOrderTraversal(node):
    if node:
        postOrderTraversal(node.left)
        postOrderTraversal(node.right)
        print(node.data, end=", ")

# ------------------- Minimum i maksimum -------------------
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

# ------------------- Usuwanie węzła -------------------
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
        temp = findMinNode(root.right)
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

def findMinNode(node):
    current = node
    while current.left:
        current = current.left
    return current

# ------------------- Usuwanie drzewa post-order -------------------
def deleteTreePostOrder(node):
    if node:
        node.left = deleteTreePostOrder(node.left)
        node.right = deleteTreePostOrder(node.right)
        print(f"Usuwam: {node.data}")
        node = None
    return node

# ------------------- Równoważenie metodą DSW -------------------
def treeToVine(root):
    vine_tail = dummy = AVLNode(None)
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
    vine_root = AVLNode(None)
    vine_root.right = root
    vine_root.right = treeToVine(root)
    size = countNodes(vine_root.right)
    vineToTree(vine_root, size)
    return vine_root.right

# ------------------- Menu użytkownika -------------------
if __name__ == "__main__":
    root = None
    while True:
        print("\nDostępne operacje:")
        print("1. Wstaw element")
        print("2. Usuń element")
        print("3. In-order traversal")
        print("4. Pre-order traversal")
        print("5. Post-order traversal")
        print("6. Znajdź minimum")
        print("7. Znajdź maksimum")
        print("8. Równoważ metodą DSW")
        print("9. Usuń całe drzewo (post-order)")
        print("0. Wyjście")

        choice = input("Wybierz operację: ")

        match choice:
            case "1":
                val = int(input("Podaj wartość do wstawienia: "))
                root = insert(root, val)
            case "2":
                val = int(input("Podaj wartość do usunięcia: "))
                root = deleteNode(root, val)
            case "3":
                print("In-order:")
                inOrderTraversal(root)
                print()
            case "4":
                print("Pre-order:")
                preOrderTraversal(root)
                print()
            case "5":
                print("Post-order:")
                postOrderTraversal(root)
                print()
            case "6":
                if root:
                    print("Minimum:", findMin(root))
                else:
                    print("Drzewo jest puste.")
            case "7":
                if root:
                    print("Maksimum:", findMax(root))
                else:
                    print("Drzewo jest puste.")
            case "8":
                if root:
                    root = balanceDSW(root)
                    print("Zrównoważono drzewo metodą DSW.")
                else:
                    print("Drzewo jest puste.")
            case "9":
                root = deleteTreePostOrder(root)
                print("Drzewo usunięte.")
            case "0":
                print("Koniec programu.")
                break
            case _:
                print("Nieprawidłowy wybór. Spróbuj ponownie.")
