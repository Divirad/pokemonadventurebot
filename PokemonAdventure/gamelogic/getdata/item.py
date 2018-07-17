from database.DBIdObject import DBIdObject


class Item(DBIdObject):
    """
    Super cool Wrapper to get Data from the MySQL-database
    """

    table = "shop"
    name: str
    price: int
    discount: int
    productdescription: str

    def __init__(self, id):
        DBIdObject.__init__(self, id)

    def get_attribute(self, name):
        """
        gets the Attributes ofthe Object.
        :param name: name of the attribute
        :return:
        """

        if name == "id":
            return self.id
        elif name == "name":
            return self.name
        elif name == "price":
            return self.price
        elif name == "discount":
            return self.discount
        elif name == "productdescription":
            return self.productdescription
        else:
            return getattr(self, name)

    def set_attribute(self, name, value):
        # TODO implement
        pass

    def buy_item(self, database, id, user):
        # TODO implement
        pass

    def give_item(self, database, id, user):
        # TODO implement
        pass
