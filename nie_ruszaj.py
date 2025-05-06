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
        if scanner and scanner.right:
            child = scanner.right
            scanner.right = child.right
            scanner = scanner.right
            child.right = scanner.left
            scanner.left = child


def vineToTree(root, size):
    leaves = size + 1 - 2 ** (size.bit_length() - 1)
    compress(root, leaves)
    size = size - leaves
    while size > 1:
        compress(root, size // 2)
        size = size // 2


def balanceDSW(root):
    if not root:
        return root
    vine_root = treeToVine(root)
    size = countNodes(vine_root)
    dummy = Node(None)
    dummy.right = vine_root
    vineToTree(dummy, size)
    return dummy.right


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
        print(node.data, end=" ")
        inOrderTraversal(node.right)


def preOrderTraversal(node):
    if node:
        print(node.data, end=" ")
        preOrderTraversal(node.left)
        preOrderTraversal(node.right)


def postOrderTraversal(node):
    if node:
        postOrderTraversal(node.left)
        postOrderTraversal(node.right)
        print(node.data, end=" ")


def findMinNode(node):
    current = node
    while current.left:
        current = current.left
    return current


def findMin(node):
    if node:
        return findMinNode(node).data
    return None


def findMax(node):
    current = node
    while current and current.right:
        current = current.right
    return current.data if current else None


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
    root.right = sortedArrayToAVL(arr[mid + 1:])
    root.height = 1 + max(getHeight(root.left), getHeight(root.right))
    return root


def export(node):
    if not node:
        return "child[missing]"
    if not node.left and not node.right:
        return f"node {node.data}"
    l_str = f"child {{{export(node.left)}}}" if node.left else "child[missing]"
    r_str = f"child {{{export(node.right)}}}" if node.right else "child[missing]"
    return f"node {node.data} {{{l_str} {r_str}}}"


def main(tree_root):
    return f"\\{export(tree_root)};"


def ozdoba():
    print("---*^*---")


def getHelp():
    ozdoba()
    print("Print - wypisuje drzewo używając in-order, post-order, pre-order")
    print("MinAndMax - wypisuje minimum i maximum w drzewie")
    print("Remove - usuwa wskazany element z drzewa")
    print("Delete - usuwa całe drzewo w post-order")
    print("Export - eksportuje do tikzpicture")
    print("Rebalance - równoważenie drzewa")
    print("Help - wypisuje komendy i ich opisy")
    print("Exit - kończy program")
    ozdoba()


def outPut(konstrukt, liczby, root):
    if konstrukt.lower() == 'bst':
        ozdoba()
        print("Inserting >> ", liczby)
        for num in liczby:
            root = insertBST(root, num)
        print()
        ozdoba()
    elif konstrukt.lower() == 'avl':
        ozdoba()
        print("Inserting >> ", liczby)
        for num in liczby:
            root = insertAVL(root, num)
        print()
        ozdoba()
    else:
        print("Nie ma takiej opcji.")
        exit()
    return root


if __name__ == "__main__":
    root = None
    l = []
    print("Dane mają być <<wpisane>>, <<wygenerowane>> czy z <<pliku>>.")
    ins = input("Wpisz słowo z nawiasów zamkniętych by wybrać opcje: ")

    if ins.lower() == 'wpisane':
        konstrukt = input("Wybierz AVL czy BST: ")
        liczby = list(map(int, input("Podaj liczby do skonstruowania drzewa (rozdzielaj je spacją): ").split()))
        root = outPut(konstrukt, liczby, root)
    elif ins.lower() == 'wygenerowane':
        konstrukt = input("Wybierz AVL czy BST: ")
        dlugosc = int(input("Podaj długość wygenerowanego ciągu: "))
        for i in range(dlugosc):
            l.append(i)
        root = outPut(konstrukt, l, root)
    elif ins.lower() == 'pliku':
        konstrukt = input("Wybierz AVL czy BST: ")
        name = input("Podaj nazwę pliku: ")
        try:
            with open(name, 'r') as plik:
                zawartosc = plik.read()
                liczby = list(map(int, zawartosc.split()))
            root = outPut(konstrukt, liczby, root)
        except FileNotFoundError:
            print("Plik nie istnieje.")
            exit()
        except ValueError:
            print("Plik zawiera nieprawidłowe dane.")
            exit()
    else:
        print("Nie ma takiej opcji wprowadzenia danych.")
        exit()

    while True:
        print("\nWybierz operacje: Print, MinAndMax, Remove, Delete, Export, Rebalance, Help, Exit")
        choice = input("Wybierz operację >> ").lower()

        if choice == "print":
            ozdoba()
            print("In-order: ", end=" ")
            inOrderTraversal(root)
            print("\nPost-order: ", end=" ")
            postOrderTraversal(root)
            print("\nPre-order: ", end=" ")
            preOrderTraversal(root)
            print()
            ozdoba()
        elif choice == "minandmax":
            ozdoba()
            min_val = findMin(root)
            max_val = findMax(root)
            if min_val is not None and max_val is not None:
                print("Minimum:", min_val)
                print("Maximum:", max_val)
            else:
                print("Drzewo jest puste.")
            ozdoba()
        elif choice == "delete":
            ozdoba()
            root = deleteTreePostOrder(root)
            print("Drzewo usunięte.")
            ozdoba()
        elif choice == "help":
            getHelp()
        elif choice == "remove":
            ozdoba()
            try:
                val = int(input("Podaj wartość do usunięcia: "))
                root = deleteNode(root, val)
                print(f"Usunięto wartość {val} z drzewa.")
            except ValueError:
                print("Nieprawidłowa wartość.")
            ozdoba()
        elif choice == "export":
            print(main(root))
        elif choice == "rebalance":
            ozdoba()
            if root:
                root = balanceDSW(root)
                print("Zrównoważono drzewo metodą DSW.")
                print("Nowe drzewo (in-order):", end=" ")
                inOrderTraversal(root)
                print()
            else:
                print("Drzewo jest puste.")
            ozdoba()
        elif choice == "exit":
            ozdoba()
            print("Koniec programu.")
            break
        else:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")