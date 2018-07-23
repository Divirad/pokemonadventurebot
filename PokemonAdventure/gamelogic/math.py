class Array2d:
    """Describes a 2-Dimensional Array"""

    def __init__(self, x, y, length = None, val = None):
        """
        Initializes and creates the array.
        :param x:   width of the 2D array
        :param y:   width of the 2D array
        :param val: var to fill in the array. Standard: None
        :param length: a list of elements
        """

        self.width = x
        self.heigth = y

        if length is None:
            self.array = list()
            for i in range(0, self.width*self.heigth):
                self.array.append(val)
        else:
            self.array = list

    def get(self, x, y):
        """
        gets an element of the 2D-array
        :param x: x-location
        :param y: y-location
        :return: returns the element at coordinate x, y
        """
        n = (y*self.width) + x
        return self.array[n]

    def set(self, x, y, val):
        """
        sets a value at a specific location
        :param x:   x-location where to set the data
        :param y:   y-location where to set the data
        :param val: Element to overwrite the existing element
        :return: True
        """
        n = (y * self.width) + x
        self.array[n] = val
        return True

    def returnall(self):
        """
        returns the complete 2D-array as string
        :return: array as string
        """

        lines = ""
        for y in range(0, self.heigth):
            s = str("%03d" % y) + " | "
            for x in range(0, self.width):
                n = (y * self.width) + x

                if self.array[n] is not None:
                    s += str(self.array[n])  # + "\t"
                else:
                    s += "None"

            lines += s + "\n"
        return lines

    def retall(self):
        """
        returns the complete 2D-array as string
        :return: array as string
        """
        lines = ""
        for y in range(0, self.heigth):
            s = ""
            for x in range(0, self.width):
                n = y * self.width
                if self.array[n] is not None:
                    s += str(self.array[n])
                else:
                    s += "None"

            lines += s
        return lines

    def returnlist(self):
        """

        :return:
        """
        return self.array

    def printall(self):
        """
        prints the complete 2D-array
        :return: True
        """

        s = self.returnall()
        print(s + "\n")
        return True


class Vector2d(object):
    """
    A 2D Vector
    """
    def __init__(self, _x, _y):
        """
        A 2 Dimensional Vector
        :param _x:
        :param _y:
        """
        self.x = _x
        self.y = _y

    def set_x(self, x):
        """
        Sets X-coordinate
        :param x: new X-coordinate
        """
        self.x = x

    def set_y(self, y):
        """
        Sets Y-coordinate
        :param y: new Y-coordinate
        """
        self.y = y

    def set(self, x, y):
        """
        Sets X and Y Coordinate
        :param x: new X-coordinate
        :param y: new Y-coordinate
        :return:
        """
        self.x = x
        self.y = y

    @classmethod
    def scalar(cls, vector1, vector2):
        """
        Vector2d Scalar
        :param vector1: Vector2d
        :param vector2: Vector2d
        :return: Vector2d
        """
        return vector1.x * vector2.x + vector1.y * vector2.y

    @classmethod
    def addition(cls, vector1, vector2):
        """
        Vector2d Addition
        :param vector1: Vector2d
        :param vector2: Vector2d
        :return: Vector2d
        """
        return Vector2d(vector1.x + vector2.x, vector1.y + vector2.y)

    @classmethod
    def substraction(cls, vector1, vector2):
        """
        Vector2d Substraction
        :type vector1: Vector2d
        :type vector2: Vector2d
        :return: Vector2d
        """
        return Vector2d(vector1.x - vector2.y, vector1.y - vector2.y)

    @classmethod
    def multiplication(cls, vector1, vector2):
        """
        Vector2d Multiplication
        :type vector1: Vector2d
        :type vector2: Vector2d
        :return: Vector2d
        """
        return Vector2d(vector1.x * vector2.x, vector1.y * vector2.y)
