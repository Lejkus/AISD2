


# AISD2


def export():
    ifnotnode.leftandnotnode.right:
    returnf"node{node.value}"
    l_str=f"child{export(node.l)}"ifnode.lelse"child[missing]"
    r_str=f"child{export(node.r)}"ifnode.relse"child[missing]"
    returnf"node{node.value}\{{l_str}\}\{{r_str}\}\"
def main():
    returnf"\\{export(tree_root)}"