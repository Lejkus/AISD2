class BSTNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

def insertBST(root, data):
    if root is None:
        return BSTNode(data)
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

# Przykład użycia:
sequence = [5, 4, 7, 2, 3, 5, 0]
bst_root = None
for num in sequence:
    bst_root = insertBST(bst_root, num)

print("\nBST (z ciągu liczb):")
inOrderTraversal(bst_root)
