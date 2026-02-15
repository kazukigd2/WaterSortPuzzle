class ColorMap:
    """
    Mapea colores a números y viceversa para Water Sort Puzzle.
    """
    def __init__(self, colors: list[str]):
        self.color_to_num = {color: i + 1 for i, color in enumerate(colors)}  # 0 reservado para vacío
        self.num_to_color = {i + 1: color for i, color in enumerate(colors)}
        self.num_to_color[0] = "Empty"  # opcional, para representar 0

    def encode(self, color_name: str) -> int:
        """Devuelve el número correspondiente a un color."""
        return self.color_to_num.get(color_name, 0)

    def decode(self, num: int) -> str:
        """Devuelve el nombre del color correspondiente al número."""
        return self.num_to_color.get(num, "Unknown")

    def encode_list(self, color_list: list[str]) -> list[int]:
        """Codifica una lista de nombres de colores a números."""
        return [self.encode(c) for c in color_list]

    def decode_list(self, num_list: list[int]) -> list[str]:
        """Decodifica una lista de números a nombres de colores."""
        return [self.decode(n) for n in num_list]