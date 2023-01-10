def  generate_power(exponent: int):
    def power(base: int):
        return base ** exponent
    return power


raise_two = generate_power(2.5)  # elevar al cuadrado
raise_three = generate_power(3)

raise_two(4)  # 16
print (raise_two(5))  # 25 always remember exponent is 2 (the environment snapshot)


raise_three(4)  # 64
raise_three(5)  # 125

square = lambda x: x**2
product = lambda f, n: lambda x: f(x)*n

ans = product(square, 2)(10)
print(ans)

# how to get the element of an entry on a list
# https://pythonexamples.org/python-find-index-of-item-in-list/

mylist = [21, 5, 8, 52, 21, 87, 52]
item = 67

try:
    #search for the item
    index = mylist.index(item)
    print('The index of', item, 'in the list is:', index)
except ValueError:
    print('item not present')



# In Scala we could deal failure if there is no element with an Option
# ls.indexOf(elem) returns a -1 if there is no such element
# But Python crashes, we need to treat the exception
# There are tries to make Python more Monadic
# https://stackoverflow.com/questions/22992433/is-there-a-python-equivalent-for-scalas-option-or-either
# But nothing relevant, better use Python in a Python way or switch to Scala

def f():
    python_list = ["mouse", [8, 4, 6], ['a']]
    print(python_list[1][2])  # 6
    #item=[8, 4, 6]
    item=6
    try:
        #search for the item
        index = python_list.index(item)
        print('The index of', item,'in the list is:', index)
        return 3.14
    except ValueError:
        print('item',item,'not present')
        return 12
print(f()) # encapsulate exception treatment in a function best, the best way
# print(python_list[1][3])  # IndexError Python Exception stops the process contrary to bash eg
# https://www.programiz.com/python-programming/list

odd = [1, 3, 5]

print(odd + [9, 7, 5])

print(["re"] * 3)

odd = [1, 9]
odd.insert(1,3)

print(odd)

odd[2:2] = [5, 7]

print(odd)

my_list = ['p', 'r', 'o', 'b', 'l', 'e', 'm']

# delete one item
del my_list[2]

print(my_list)

# delete multiple items
del my_list[1:5] # borra el 1, 2, 3 y 4
print(my_list)


pepe=(10,20)[False]
print(pepe)





pepe=(0,int("10")) ["124124".isnumeric()]
print(pepe)


# using Python functional way (can be done)

def greet_bob(greeter_f):
    return greeter_f("Boob")


def say_hello(who):
    print(f"hello {who}")


def say_ey(who):
    print(f"ey {who}!!")


greet_bob(say_ey)
greet_bob(say_hello)



def parent(num):
    def first_child():
        return "Hi, I am Emma"

    def second_child():
        return "Call me Liam"

    if num == 1:
        return first_child
    else:
        return second_child

first = parent(1)
second = parent(2)

print(first)
print(parent(99))
print(first())
print(parent(99)())

def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

def say_whee():
    print("Whee!")

say_whee = my_decorator(say_whee)

say_whee()

# decorators wrap a function, modifying its behavior.

from datetime import datetime

def not_during_the_night(func):
    def wrapper():
        if 7 <= datetime.now().hour < 21:
            func()
        else:
            pass  # Hush, the neighbors are asleep
    return wrapper

def say_whee():
    print("Whee!")

say_whee = not_during_the_night(say_whee)

say_whee()


def my_decorator_for_pie (func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper


@my_decorator_for_pie
def say_whee():
    print("Whooooe!")


say_whee()
# Con la anotacion le digo que la funcion que defino es la que la paso al decorator
# Como siempre más directo si lo conoces pero hay que entender bien lo que implica poner la anotacion

