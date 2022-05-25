# a warehouse demo including making classes (meant to be inside a products.py file), aggregating in a 
# warehouse.py file, testing in a testing file and using pickle for persistance 

from abc import ABC, abstractmethod

class Product(ABC):
# an internally generated id to assign a unique code
    __id = -1
	def __init__ (self,name,price):
		self._item_code = self.generate_id()
		self._name = name
		self._price = price

	def generate_id(self):
		Product.__id += 1
		return Product.__id

	@property
	def item_code(self):
		return self._item_code

	@property
	def name(self):
		return self._name

	@property
	def price(self):
		return self._price

	def __str__(self):
		return str(self.code) + ':' + self._name + ',' + self.price

class Clothing(Product):
	def __init__(self,name,price,size,color):
		super().__init__(name,price) #call the constructor in parent class to get name and price
		self._size = size
		self.color = color

	@property
	def size(self):
		return self._size

class Camping(Product):
	def __init__

class Shirt(Clothing):

#Put the super as the first thing under __init__
#If there are no attributes in parent class, there is no point in onvoking constructor in parent class (dont use super)

#You can do some quick testing with print statements
#Real testing: test_products ? test instansiation of every possible object instance you are creating using assert statements from pytest
#Import pytest
#From products import Shirt,Pant,ELEctrical

#Test:
#Def test_create_shirt():
#Make a shirt ? then assert s.name == name you made

#Implementing warehouse which composes all products
From products import *

class Warehouse:
	def __init__(self):
		#list of products
        self._items = []
        #list of mapping of id to product
        self._mapping = []
            
#returns list of items in the inventory
	def get_all_items(self):
		return self._items

def search_all(self,name):
	srch_items = []
	for item in self._items:
		if name.lower() in item._name.lower():
			srch_items.append(item)
	return srch_items

def add_item(self,item):
	self._items.append(item)
	self._mapping[item.code] = item

@classmethod
def load_data(cls): #creates mock data
	Inventory = Warehouse()
	#create a shirt
	Item = Shirt(attributes blah blah)
	#add the shirt to the warehouse
    Inventory.add_item(item)
    #Repeat for how many items you want to add
    return inventory

#EVENTUALLY:
#Load_data will be loading data from database or flat file
#But for now, it is fake data
	
#Now:
#Warehouse = Warehouse.load_data()
#All_items = warehouse.get_all_items()

For x in all_items


Testing: using pytest
Make a mock warehouse called warehouse_fixture ? returns a warehouse
Test the search use case using the warehouse_fixture

import pickle # allows persistence
Pickle.dump(self,file)
To load it back up-  pickle.load(file)
Now our data is persistanct 
