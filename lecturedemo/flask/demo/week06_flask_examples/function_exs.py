#Example1: Assigning a function to a variable

def hello_world(name):
        return "Hello World!" + name

my_function = hello_world
print(my_function("Sam"))

#Example2: Nesting functions inside functions

def nested_hello_world(name):
        def greet():
                return "Hello World! "
        return greet() + " " + name

print(nested_hello_world("Jack"))


#Example3: Passing functions as parameters to other functions

def greet(name, lang):
        if lang == "French":
                return "Bonjour " + name
        else:
                return "Hello World!"+ name        

def another_hello_world(func):
        my_name = "Jack"
        my_lang = "French"
        return func(my_name,my_lang)

print(another_hello_world(greet))


#Example4: Functions can return other functions
def another_hello_world():
        def greeting(name):
                return "Hello there! " + name
        return greeting

my_function=another_hello_world()
print(my_function("Maya"))

#Example5: Passing functions as parameters to other functions
def increase(x):
        return x+1

def decrease(x):
        return x-1

def square(x):
        return x * x

def apply_func_list(func_list,number):
        if len(func_list) == 0:
                return number
        else:
                return apply_func_list(func_list[1:],func_list[0](number))

print("Result: {0}".format(apply_func_list([increase, decrease,square],10)))

#Applying the above ideas, we build a function decorator
#Using Python's neat decorator syntax
def my_decorator(func):
        def wrapper():
            name = "jack"
            return func() + name
        return wrapper

@my_decorator
def say_hello():
        return "Hello World! "

#There are two ways of decorating the function
# Assign to a variable as follows
# decorated_func = my_decorator(say_hello)
# print(decorated_func())
# OR simply use Python's nice decorator syntax

print(say_hello())
