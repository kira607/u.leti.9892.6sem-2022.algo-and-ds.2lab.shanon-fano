from .builder import TreeBuilderCodes, TreeBuilderProbs


class ShanonFanoTree:
    _builder = None

    def __init__(self, data):
        self._root = self._builder.build(data)
        self._symbols = self._get_symbols(self._root)

    @classmethod
    def from_counter_table(cls, counter_table: dict):
        cls._builder = TreeBuilderProbs()
        return cls(counter_table)

    @classmethod
    def from_codes_table(cls, codes_table: dict) -> None:
        cls._builder = TreeBuilderCodes()
        return cls(codes_table)

    def get_codes_table(self) -> dict:
        return {k: self.get_code(k) for k in self._symbols}

    def separate(self, code: str):
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
