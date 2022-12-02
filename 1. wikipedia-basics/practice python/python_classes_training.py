class ShippingContainer:
    # class attribute
    next_serial = 1337
    # object attributes
    def __init__(self, owner_code, contents):
        self.owner_code = owner_code
        self.contents = contents
        self.serial= ShippingContainer.next_serial # with self would work but not good practice
        ShippingContainer.next_serial+=1 # with self would't work would generate a new attribite hiding the external

        # self is instance reference
        # class attributes acceses by Class object reference in this case ShippingContainer
        # instance attribites takes preference over class attributes when accessed through self
        # There is no class scope in Python, jjust LEGB Local Enclosing Global Built-In
