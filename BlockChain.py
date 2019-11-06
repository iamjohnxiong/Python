
"""
Code based from: https://towardsdatascience.com/building-a-minimal-blockchain-in-python-4f2e9934101d

messing around with blockchain structure
"""

import datetime
import hashlib
import copy

class Customer():
	def __init__(self, first_name, last_name, age):
		self.first_name = first_name
		self.last_name = last_name
		self.age = age

class Block():
	def __init__(self, previous_hash, customer, index):
		self.previous_hash = previous_hash
		self.customer = customer
		self.index = index
		self.hash = self.do_hash()

	def do_hash(self):
		hash = hashlib.sha3_256()
		hash.update(str(self.index).encode('utf-8'))
		hash.update(str(self.customer.first_name).encode('utf-8'))
		hash.update(str(self.customer.last_name).encode('utf-8'))
		hash.update(str(self.previous_hash).encode('utf-8'))
		return hash.hexdigest()		
		
class Chain():
	def __init__(self):
		self.blocks = [self.get_genesis_block()]

	def get_genesis_block(self):
		return Block('none', Customer("Genesis", "Block", 0), 0)

	def append_block(self, customer):
		self.blocks.append(Block(self.blocks[len(self.blocks) - 1].hash, customer, len(self.blocks)))

	def verify(self, verbose = True):
		flag = True
		for i in range (1, len(self.blocks)):
			block = self.blocks[i]
			if block.index != i:
				flag = False
				print(f'Block index {i} is incorrect!')
			if block.hash != block.do_hash():
				flag = False
				print(f'Hash for block index {i} is incorrect: ' + block.customer.first_name + ' ' + block.customer.last_name + ' ' + block.hash)
			if block.previous_hash != self.blocks[i - 1].hash:
				flag = False
				print(f'Previous hash for block {i} does not match for previous block!')
		return flag

chain = Chain()
customer1 = Customer('Bill', 'Clinton', 20)
customer2 = Customer('Barack', 'Obama', 30)
chain.append_block(customer1)
chain.append_block(customer2)

for i in range (0, len(chain.blocks)):
	block = chain.blocks[i]
	print(str(block.index) + ' ' + block.customer.first_name + ' ' + block.customer.last_name + ': ' + block.hash)

chain.blocks[1].customer.first_name = "Hill"
print("Blockchain Verified") if chain.verify() else print("Blockchain Invalid")