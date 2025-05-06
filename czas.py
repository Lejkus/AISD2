import os
import time
import csv
from typing import List
import sys
sys.setrecursionlimit(40000)
import re

# --- Algorytmy i struktury drzew ---
def extract_number(filename):
    match = re.search(r'_(\d+)\.txt$', filename)
    return int(match.group(1)) if match else float('inf')

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

# --- Pomiar czasu ---

def read_numbers_from_file(file_path: str) -> List[int]:
    with open(file_path, 'r') as f:
        return list(map(int, f.read().split()))

def measure_time(func, *args, **kwargs):
    start = time.perf_counter()
    result = func(*args, **kwargs)
    end = time.perf_counter()
    return result, round((end - start) * 1000, 3)  # Mnożymy przez 1000, żeby otrzymać czas w milisekundach


def perform_measurements_for_file(filepath: str):
    data = read_numbers_from_file(filepath)
    result = {'filename': os.path.basename(filepath)}

    # (a) AVL z połowienia
    _, t_avl = measure_time(lambda: sortedArrayToAVL(sorted(data)))
    result['AVL_halfing_build'] = round(t_avl, 3)  # Zapisz do 3 miejsc po przecinku

    # (b) BST degenerowane (kolejno)
    bst_root = None
    def build_bst():
        nonlocal bst_root
        bst_root = None
        for num in data:
            bst_root = insertBST(bst_root, num)
    _, t_bst = measure_time(build_bst)
    result['BST_sequential_build'] = round(t_bst, 3)  # Zapisz do 3 miejsc po przecinku

    # (c) min & max
    _, t_min = measure_time(findMin, bst_root)
    _, t_max = measure_time(findMax, bst_root)
    result['Find_min'] = round(t_min, 3)  # Zapisz do 3 miejsc po przecinku
    result['Find_max'] = round(t_max, 3)  # Zapisz do 3 miejsc po przecinku

    # (d) in-order
    _, t_inorder = measure_time(lambda: in_order_collect(bst_root, []))
    result['Inorder_traversal'] = round(t_inorder, 3)  # Zapisz do 3 miejsc po przecinku

    # (e) DSW balance
    _, t_dsw = measure_time(lambda: balanceDSW(bst_root))
    result['DSW_rebalance'] = round(t_dsw, 3)  # Zapisz do 3 miejsc po przecinku

    return result


def process_all_files_in_folder(folder_path: str, output_csv: str):
    all_results = []
    for filename in sorted(os.listdir(folder_path), key=extract_number):

        if filename.endswith('.txt'):
            full_path = os.path.join(folder_path, filename)
            try:
                result = perform_measurements_for_file(full_path)
                all_results.append(result)
                print(f"Przetworzono: {filename}")
            except Exception as e:
                print(f"Błąd przy przetwarzaniu {filename}: {e}")

    if all_results:
        keys = all_results[0].keys()
        with open(output_csv, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(all_results)

if __name__ == "__main__":
    folder = input("Podaj ścieżkę do folderu z plikami .txt: ")
    output = input("Podaj nazwę pliku wyjściowego CSV: ")
    process_all_files_in_folder(folder,output)
