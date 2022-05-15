from abc import ABC, abstractmethod
from operator import sub

from .node import ShanonFanoTreeNode


class TreeBuilder(ABC):
    def build(self, table):
        root = ShanonFanoTreeNode(self._node_id(table))
        table = self._sort(table)
        q = [(table, root)]
        while q:
            table, node = q.pop(0)

            if node.is_leaf:
                continue

            l, r = self._split(table)

            lsymbol, rsymbol = self._mksymbols(l, r)
            
            node.left  = ShanonFanoTreeNode(self._node_id(l), lsymbol, node)
            node.right = ShanonFanoTreeNode(self._node_id(r), rsymbol, node)

            q.extend(((l, node.left), (r, node.right)))
        return root

    @abstractmethod
    def _node_id(self, table):
        raise NotImplementedError()

    @abstractmethod
    def _sort(self, table):
        raise NotImplementedError()
    
    @abstractmethod
    def _split(self, table):
        raise NotImplementedError()

    def _mksymbols(self, l, r):
        lsymbol = None
        if l and len(l) == 1:
            lsymbol = list(l)[0][0]

        rsymbol = None
        if r and len(r) == 1:
            rsymbol = list(r)[0][0]

        return lsymbol, rsymbol


class TreeBuilderProbs(TreeBuilder):
    def _node_id(self, table):
        s = f'({sum(table.values())}) -- '
        for k, v in table.items():
            s += f'{repr(k)}: {v}, '
        s = s[:-2]
        s = f'"{s}"'
        return s

    def _sort(self, table):
        return dict(
            sorted(
                table.items(), 
                key=lambda x: x[1],
            )
        )
    
    def _split(self, table):
        left_sum = sum(table.values())
        right_sum = 0
        cached_pair = (left_sum, right_sum)
        lprobs = list(table.items())

        for i, (_, v) in enumerate(lprobs):
            right_sum += v
            left_sum -= v

            if left_sum <= right_sum:
                if abs(left_sum - right_sum) > abs(sub(*cached_pair)):
                    split_point = i
                else:
                    split_point = i + 1
                l, r =  dict(lprobs[:split_point]), dict(lprobs[split_point:])
                return self._sort(l), self._sort(r)
            else:
                cached_pair = (left_sum, right_sum)


class TreeBuilderCodes(TreeBuilder):
    def _node_id(self, table):
        i = ', '.join(repr(k) for k in table)
        if len(table) == 1:
            i += ' (s)'
        return f'"{i}"'

    def _sort(self, table):
        return dict(
            sorted(
                table.items(), 
                key=lambda x: len(x[1]), 
                reverse=True,
            )
        )

    def _split(self, table):
        l, r = {}, {}
        for symbol, code in table.items():
            if code.startswith('1'):
                l[symbol] = code[1:]
            elif code.startswith('0'):
                r[symbol] = code[1:]
            else:
                raise ValueError(table)
        return l, r