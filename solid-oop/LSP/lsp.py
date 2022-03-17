class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw(self):
        print(f"Rectangle({self.width}, {self.height})")


class Square:
    def __init__(self, size):
        self.size = size
        self._rect = Rectangle(size, size)

    def draw(self):
        self._rect.draw()


if __name__ == "__main__":
    rect = Rectangle(100, 200)
    rect.draw()

    square = Square(50)
    square.draw()
