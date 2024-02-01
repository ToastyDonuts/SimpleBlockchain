from node.utility import Cryptographic_SHA256_Hash
import math
class Node:
    def __init__(self,value: int, left_child=None, right_child=None):
        self.value=value
        self.left_child=left_child
        self.right_child=right_child
class MerkleTree():
    def build_tree(self, node_data):
        transaction_set = [Cryptographic_SHA256_Hash(tx) for tx in node_data]
        tree_depth = math.ceil(math.log2(len(transaction_set)))
        root = self._build_tree_recursive(transaction_set, 0, len(transaction_set) - 1, 0)
        return root.value

    def _build_tree_recursive(self, transaction_set, start, end, depth):
        if start == end:
            return Node(transaction_set[start])

        mid = (start + end) // 2
        left_child = self._build_tree_recursive(transaction_set, start, mid, depth + 1)
        right_child = self._build_tree_recursive(transaction_set, mid + 1, end, depth + 1)

        combined_hash = Cryptographic_SHA256_Hash(left_child.value + right_child.value)
        return Node(combined_hash, left_child, right_child)


    
