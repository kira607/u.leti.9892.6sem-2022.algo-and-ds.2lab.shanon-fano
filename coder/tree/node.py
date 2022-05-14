class ShanonFanoTreeNode:
    def __init__(self, id, symbol=None, parent=None):
        self.id = id
        self.symbol = symbol

        self.parent = parent
        self.left = None
        self.right = None

    @property
    def is_leaf(self):
        return self.symbol is not None

    @property
    def is_left(self):
        if not self.parent:
            return False
        return self == self.parent.left

    @property
    def is_right(self):
        if not self.parent:
            return False
        return self == self.parent.right

    def get_dot_string(self):
        s = self.id
        l = self.left.id if self.left else "NULL"
        r = self.right.id if self.right else "NULL"
        l = f'{s} -- {l} [label="1"]\n' if self.left else ''
        r = f'{s} -- {r} [label="0"]\n' if self.left else ''
        return l + r
