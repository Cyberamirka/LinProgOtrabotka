class LinProgContainer:
    def __init__(self, z_func: list, a: list, constraint: list, ismax: bool):
        self.z = z_func
        self.a = a
        self.constraint = constraint
        self.ismax = ismax


class Global:
    current_equation: LinProgContainer = None
