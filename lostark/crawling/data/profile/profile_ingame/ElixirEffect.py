class ElixirEffect:
    def __init__(self):
        self.name = None
        self.total = None

    def add(self, total):
        if self.total is None:
            self.total = total
        elif self.total < total:
            self.total = total

    def set_name(self, name):
        self.name = name

    def __str__(self):
        return f"{self.name}, {self.total}"
