# Klasa reprezentująca węzeł drzewa AVL
class AVLNode:
    def __init__(self, data):
        self.data = data              # Wartość węzła
        self.left = None              # Lewy podwęzeł
        self.right = None             # Prawy podwęzeł
        self.height = 1               # Wysokość węzła (potrzebna do AVL, ale tutaj tylko do odczytu)

# Funkcja pomocnicza - zwraca wysokość węzła
def getHeight(node):
    if not node:
        return 0
    return node.height

# Główna funkcja budująca zbalansowane drzewo AVL z posortowanej tablicy
def sortedArrayToAVL(arr):
    if not arr:
        return None  # Jeśli lista pusta, nie tworzymy węzła

    mid = len(arr) // 2  # Wybieramy środkowy element jako korzeń
    print(f"Tworzenie węzła z elementu: {arr[mid]}")
    root = AVLNode(arr[mid])

    # Rekurencyjnie tworzymy lewe i prawe poddrzewo
    print(f"  -> Lewa część: {arr[:mid]}")
    root.left = sortedArrayToAVL(arr[:mid])

    print(f"  -> Prawa część: {arr[mid+1:]}")
    root.right = sortedArrayToAVL(arr[mid+1:])

    # Ustawiamy wysokość tego węzła
    root.height = 1 + max(getHeight(root.left), getHeight(root.right))
    print(f"  => Ustawiono wysokość dla {root.data}: {root.height}")
    return root

# Przechodzenie przez drzewo w kolejności in-order (lewe -> korzeń -> prawe)
def inOrderTraversal(node):
    if node:
        inOrderTraversal(node.left)
        print(node.data, end=", ")
        inOrderTraversal(node.right)

# Przykładowe dane
sorted_data = sorted([5, 4, 7, 2, 3, 5, 0])  # Najpierw sortujemy dane
print(f"Posortowane dane: {sorted_data}")

# Budujemy AVL z posortowanej listy
print("\nBudowanie drzewa AVL...")
avl_root = sortedArrayToAVL(sorted_data)

# Wyświetlamy dane w porządku in-order
print("\nAVL (z połowienia binarnego) - przejście in-order:")
inOrderTraversal(avl_root)
