class CoderNode:
    def __init__(self, char: str, code: str, frequency: float) -> None:
        self.char: str = char
        self.code: str = code
        self.frequency: float = frequency


class CodeTable:
    def __init__(self) -> None:
        self.table: list[CoderNode] = list()
        self.crc_gen: str

    def toDict(self) -> dict:
        return dict([(i.char, i.code) for i in self.table])