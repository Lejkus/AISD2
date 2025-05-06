import os
import time
import csv
from typing import List

# --- Struktury drzew i funkcje pomocnicze (identyczne jak wcześniej) ---

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

def insertBST(root, data):
    if root is None:
        return Node(data)
    if data < root.data:
        root.left = insertBST(root.left, data)
    else:
        root.right = insertBST(root.right, data)
    return root

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

def findMinAVL(node):
    # Minimalna wartość w AVL (po prostu jak w BST)
    current = node
    while current.left:
        current = current.left
    return current.data if current else None

def findMaxAVL(node):
    # Maksymalna wartość w AVL (po prostu jak w BST)
    current = node
    while current and current.right:
        current = current.right
    return current.data if current else None

def in_order_collect(node, result):
    if node:
        in_order_collect(node.left, result)
        result.append(node.data)
        in_order_collect(node.right, result)

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

def sortedArrayToAVL(arr):
    if not arr:
        return None
    mid = len(arr) // 2
    root = Node(arr[mid])
    root.left = sortedArrayToAVL(arr[:mid])
    root.right = sortedArrayToAVL(arr[mid + 1:])
    root.height = 1 + max(getHeight(root.left), getHeight(root.right))
    return root

# --- Pomiar ---

def read_numbers_from_file(file_path: str) -> List[int]:
    with open(file_path, 'r') as f:
        return list(map(int, f.read().split()))

def measure_time(func, *args, **kwargs):
    start = time.perf_counter()
    result = func(*args, **kwargs)
    end = time.perf_counter()
    return result, round(end - start, 6)

def extract_length_from_filename(filename: str) -> int:
    """Wyciąga liczbę z nazwy pliku np. 'constant_array_00000004.txt' -> 4"""
    base_name = filename.split('_')[-1].split('.')[0]  # np. '00000004'
    return int(base_name)  # Zwraca liczbę (np. 4)


def perform_measurements_for_file(filepath: str, metric: str):
    data = read_numbers_from_file(filepath)
    length = extract_length_from_filename(os.path.basename(filepath))  # np. 512
    result = {'length': length}

    def ms(t): return round(t * 1000, 3)  # sekundy → milisekundy

    if metric == "AVL_halfing_build":
        _, t = measure_time(lambda: sortedArrayToAVL(sorted(data)))
    elif metric == "BST_sequential_build":
        bst_root = None
        def build_bst():
            nonlocal bst_root
            bst_root = None
            for num in data:
                bst_root = insertBST(bst_root, num)
        _, t = measure_time(build_bst)
    elif metric == "BST_find_min":
        bst_root = None
        for num in data:
            bst_root = insertBST(bst_root, num)
        _, t = measure_time(findMin, bst_root)
    elif metric == "BST_find_max":
        bst_root = None
        for num in data:
            bst_root = insertBST(bst_root, num)
        _, t = measure_time(findMax, bst_root)
    elif metric == "AVL_find_min":
        avl_root = sortedArrayToAVL(sorted(data))
        _, t = measure_time(findMinAVL, avl_root)
    elif metric == "AVL_find_max":
        avl_root = sortedArrayToAVL(sorted(data))
        _, t = measure_time(findMaxAVL, avl_root)
    elif metric == "BST_inorder_traversal":
        bst_root = None
        for num in data:
            bst_root = insertBST(bst_root, num)
        _, t = measure_time(lambda: in_order_collect(bst_root, []))
    elif metric == "AVL_inorder_traversal":
        avl_root = sortedArrayToAVL(sorted(data))
        _, t = measure_time(lambda: in_order_collect(avl_root, []))
    elif metric == "DSW_rebalance":
        bst_root = None
        for num in data:
            bst_root = insertBST(bst_root, num)
        _, t = measure_time(lambda: balanceDSW(bst_root))
    else:
        raise ValueError(f"Nieznana metryka: {metric}")

    result['time'] = ms(t)
    return result


def process_metric_for_all_folders(base_folder: str, metric: str, output_folder: str):
    subfolders = [f.name for f in os.scandir(base_folder) if f.is_dir()]
    for sub in subfolders:
        results = []
        sub_path = os.path.join(base_folder, sub)
        for filename in sorted(os.listdir(sub_path)):
            if filename.endswith(".txt"):
                filepath = os.path.join(sub_path, filename)
                try:
                    full_result = perform_measurements_for_file(filepath, metric)
                    results.append({
                        'length': full_result['length'],
                        'time': full_result['time']
                    })
                    print(f"{metric} - {sub}/{filename}")
                except Exception as e:
                    print(f"Błąd w {filename}: {e}")

        out_path = os.path.join(output_folder, f"{metric}_{sub}.csv")
        with open(out_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['length', 'time'])
            writer.writeheader()
            for result in results:
                writer.writerow(result)


# --- Uruchomienie ---

if __name__ == "__main__":
    base = input("Podaj ścieżkę do folderu bazowego z danymi: ")
    metric = input("Podaj nazwę metryki (np. AVL_halfing_build): ")
    output = input("Podaj ścieżkę do folderu wyjściowego: ")
    os.makedirs(output, exist_ok=True)
    process_metric_for_all_folders(base, metric, output)
