class ShippingContainer:
    # class attribute
    next_serial = 1337
    # object attributes

   # def _generate_serial(self): # leading underscore to indicate will be used internally
   #     result = ShippingContainer.next_serial
   #     ShippingContainer.next_serial += 1
   #     return result

    @staticmethod        # and remove the self    this terminilogy comes from C and C++
    def _generate_serial():  # leading underscore to indicate will be used internally
        result = ShippingContainer.next_serial
        ShippingContainer.next_serial += 1
        return result

    def __init__(self,owner_code,contents):
        self.owner_code = owner_code
        self.contents = contents
        self.serial= ShippingContainer._generate_serial()     #we can remove the self using static

