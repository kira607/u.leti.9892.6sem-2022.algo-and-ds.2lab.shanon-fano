from typing import List
from operator import sub

from .node import ShanonFanoTreeNode


def _sort_probs(probs):
    return dict(
        sorted(
            list(probs.items()), 
            key=lambda x: x[1], 
        )
    )


def _split_probs(probs):
    left_sum = sum(probs.values())
    right_sum = 0
    cached_pair = (left_sum, right_sum)
    lprobs = list(probs.items())

    for i, (_, v) in enumerate(lprobs):
        right_sum += v
        left_sum -= v

        if left_sum <= right_sum:
            if abs(left_sum - right_sum) > abs(sub(*cached_pair)):
                split_point = i
            else:
                split_point = i + 1
            l, r =  dict(lprobs[:split_point]), dict(lprobs[split_point:])
            return _sort_probs(l), _sort_probs(r)
        else:
            cached_pair = (left_sum, right_sum)


class ShanonFanoTree:
    _gen_node_id = None
    _build = None
    _split = None

    def __init__(self, data):
        self._root = None
        self._build(data)
        self._symbols = self._get_symbols(self._root)

    @classmethod
    def from_counter_table(cls, counter_table: dict):
        cls._gen_node_id = cls._gen_node_id_from_probs
        cls._build = cls._build_from_counter_table
        return cls(counter_table)

    @classmethod
    def from_codes_table(cls, codes_table: dict) -> None:
        cls._gen_node_id = cls._gen_node_id_from_codes
        cls._build = cls._build_from_codes_table
        return cls(codes_table)

    def get_codes_table(self) -> dict:
        return {k: self.get_code(k) for k in self._symbols}

    def separate(self, code: str) -> List[str]:
        input_code = code
        separated = []
        while code:
            _, code = self._get_leaf(code)
            if code:
                separated.append(input_code[:-len(code)])
            else:
                separated.append(input_code)
            input_code = input_code[len(separated[-1]):]
        return separated

    def get_symbol(self, code: str):
        n, _ = self._get_leaf(code)
        return n.symbol

    def get_code(self, symbol: str):
        node = self._symbols.get(symbol)
        if not node:
            raise ValueError(symbol)
        code = ''
        while node.parent:
            code += '1' if node.is_left else '0'
            node = node.parent
        return code[::-1]

    def get_dot_string(self) -> str:
        graphviz_string = 'graph {\n'
        for node in self._traverse(self._root):
            graphviz_string += node.get_dot_string()
        graphviz_string += '}'
        return graphviz_string

    def _get_leaf(self, code):
        node = self._root
        print(node.id)
        while not node.is_leaf:
            c = code[0]
            if c == '1':
                node = node.left
            elif c == '0':
                node = node.right
            else:
                raise ValueError(code)
            code = code[1:]
        return node, code

    def _traverse(self, node=None):
        if node:
            yield node
            yield from self._traverse(node.left)
            yield from self._traverse(node.right)

    def _get_symbols(self, node):
        if not node:
            return {}
        if node.is_leaf:
            return {node.symbol: node}

        ls = self._get_symbols(node.left)
        rs = self._get_symbols(node.right)
        return {**ls, **rs}

    def _build_from_counter_table(self, ct):
        self._root = ShanonFanoTreeNode(self._gen_node_id(ct))
        ct = _sort_probs(ct)
        q = [(ct, self._root)]
        while q:
            counts, node = q.pop(0)
            if not node.is_leaf:
                l, r = _split_probs(counts)

                lsymbol = None
                if l and len(l) == 1:
                    lsymbol = list(l)[0][0]

                rsymbol = None
                if r and len(r) == 1:
                    rsymbol = list(r)[0][0]
                
                node.left  = ShanonFanoTreeNode(self._gen_node_id(l), lsymbol, parent=node)
                node.right = ShanonFanoTreeNode(self._gen_node_id(r), rsymbol, parent=node)

                q.extend(((l, node.left), (r, node.right)))

    def _build_from_codes_table(self, ct):
        self._root = ShanonFanoTreeNode(self._gen_node_id(ct))
        ct = dict(sorted(list(ct.items()), key=lambda x: len(x[1]), reverse=True))
        q = [(ct, self._root)]
        while q:
            c, n = q.pop(0)

            to_left = {}
            to_right = {}

            for symbol, code in c.items():
                if code.startswith('0'):
                    to_right[symbol] = code[1:]
                elif code.startswith('1'):
                    to_left[symbol] = code[1:]
                elif code == '':
                    n.symbol = symbol
                else:
                    raise ValueError(ct)

            if to_left:
                new_node = ShanonFanoTreeNode(self._gen_node_id(to_left), parent=n)
                n.left = new_node
                q.append((to_left, new_node))
                print(f'left: {to_left}')
            if to_right:
                new_node = ShanonFanoTreeNode(self._gen_node_id(to_right), parent=n)
                n.right = new_node
                q.append((to_right, new_node))
                print(f'right: {to_right}')

    def _gen_node_id_from_probs(self, c):
        s = f'({sum(c.values())}) -- '
        for k, v in c.items():
            s += f'{repr(k)}: {v}, '
        s = s[:-2]
        s = f'"{s}"'
        return s

    def _gen_node_id_from_codes(self, c):
        i = ', '.join(repr(k) for k in c)
        if len(c) == 1:
            i += ' (s)'
        return f'"{i}"'
