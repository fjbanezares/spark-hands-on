# help(math.factorial)
# import module_name
# from module_name import factorial
# import this
# if bool:
#    do this
#else:
#    do that
#while explicitly converted to bool:
#    do this
#break goes out of the look into next line
#input() to request text form usset
# be consistent with String literals
pepito="""multiline
string"""
juanito='''another
multiline
string'''
ramoncito="also\n we can do the multiline the old way\n"
#windows \r\n, mac, univ \r en python pones |n y te traduce pep0278 about universal new line support
# backslash also used to escape
path= r'this is a raw string where nothing escapa what you see is that you get \f\f\f\f\\f\f\f\\\\'
#str is Unicode source encodinfg is UTF8
#bytes are sequences of bytes
# convert between bytes and strings ... norsl.encode(utf8)

#list of objects, types can be heterogenous
# dictionariers, k v sets from python 37 insertion order is kept
#     line_words = line.decode('utf-8').split()
# values only assigned to names
# arguments transferred pass-by-object-reference, reference to the object are copied not the objects, same the return!
# arguments with defaults fo after
# default relies on same reference even if you called a million times the f, never use mutable objects as default
# if a function pass as default executed only once
# again only use immutables as default, particualrly None. the rest in code
# Type System
# when run as is dynamic
# type declare unnecesary
# where binging to names are stored? Scopes
# Loca, inside current f; enclosing, inside enclosing f, global at top level, Bult-In, in specual built in modure
# rebind global name into a local scope: global count... and then count = whatever
# (a,b,c) tuples are immutable combination of random objects
# t + t concatenate
# 3 * t repeat 3 times
# (a,) single element tuple

import iso6346exit()
class ShippingContainer:
    # class attribute
    next_serial = 1337
    # object attributes

   # def _generate_serial(self): # leading underscore to indicate will be used internally
   #     result = ShippingContainer.next_serial
   #     ShippingContainer.next_serial += 1
   #     return result

    @classmethod        # and remove the self    this terminilogy comes from C and C++
    def _generate_serial(cls):  # leading underscore to indicate will be used internally
        result = cls.next_serial
        cls.next_serial += 1
        return result

    @classmethod
    def create_empty(cls, owner_code):
        return cls(owner_code, contents=[])

    @classmethod
    def create_with_items(cls, owner_code, items):
        return cls(owner_code, contents=list(items))

    def __init__(self,owner_code,contents):
        self.owner_code = owner_code
        self.contents = contents
        self.serial= ShippingContainer._generate_serial()

        #quite similar to staticmethod decorator
        # what we do?, In Java, In C#, C++
        # class method if access to the class to call other methods or the constructor
        # static if no needed access to the class or other instance objects
        # stqtic will be an implementation of a detail of the class
        # static mey be subject to stop being statica and become a global scope function in the module out of the class
        # class can be a named constructor, a factory


