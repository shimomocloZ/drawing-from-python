import dataclasses


@dataclasses.dataclass
class Product:
    id: int = 0
    name: str = ''

    def __post_init__(self):
        self.id = int(self.id)
