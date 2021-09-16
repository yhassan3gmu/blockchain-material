from hashlib import sha256
import json
import time

from flask import Flask, request
import request

class Block:
    def __init__(self, index, timestamp, transactions, backhash):
        self.index = index
        self.timestamp = ts
        self.transactions = transactions
        #self.mydata = mydata
        self.backhash = backhash
        #self.hash = self.hashop()
    def compute_hash():
        """
        Returns the hash of the block instance by first converting it
        into JSON string.
        """
        block_string = json.dumps(self.__dict__, sort_keys = True)
        return sha256(block_string.encode()).hexdigest()
    
    '''
    def hashop(self):
       
        shahash = hasher.sha256()
        shahash.update(str(self.idx).encode('utf-8') + str(self.ts).encode('utf-8') + str(self.mydata).encode('utf-8') + str(self.backhash).encode('utf-8'))
        return shahash.hexdigest()
        '''
class Blockchain:
	# difficulty of PoW algorithm
	difficulty = 2
    def __init__(self):
        """
        Constructor for the `Blockchain` class.
        """
		self.unconfirmed_transactions = [] #data yet to get into blockchain
        self.chain = []
        self.create_genesis_block()
    def create_genesis_block():
        #return Block(0, date.datetime.now(), 'Genesis Block', '0')
		genesis_block = Block(0, [], time.time(), "0")
		genesis_block.hash = genesis_block.compute_hash()
		self.chain.append(genesis_block)
	#@property
	def last_block(self):
		"""
        A quick pythonic way to retrieve the most recent block in the chain. Note that
        the chain will always consist of at least one block (i.e., genesis block)
        """
		return self.chain[-1]
	def proof_of_work(self, block):
		"""Function that tries different values of the nonce to get a hash that satifies our difficulty criteria."""
		block.nonce = 0
		
		computed_hash = block.compute_hash()
		while not computed_hash.startswith('0' * Blochchain.difficulty):
			block.nonce+=1
			computed_hash = block.compute_hash()
		return computed_hash
	def add_block(self, block, proof):
		"""this_idx = last_block.idx + 1
    	this_ts = date.datetime.now()
    	this_mydata = 'Block' + str(this_idx)
    	this_hash = last_block.hash
    	return Block(this_idx, this_ts, this_mydata, this_hash)"""
		previous_hash = self.last_block.hash
		if previous_hash != block.previous_hash:
			return False
		if not Blockchain.is_valid_proof(block, proof):
			return False
		block.hash = proof
		self.chain.append(block)
		return True
	def is_valid_proof(self, block, block_hash):
		"""
        Check if block_hash is valid hash of block and satisfies
        the difficulty criteria.
        """
		#this returns the nonce
		return (block_hash.startswith('0' * Blockchain.difficulty) and block_hash = block.compute_hash())
	def mine(self):
		"""adds pending transactions to blockchain by adding them to block and doing the proof of work"""
		if not self.unconfirmed_transactions:
			return False
		
		last_block = self.last_block
		
		new_block = Block(index = last_block.index + 1, transactions = self.unconfirmed_transactions,
						 timestamp = time.time(), previous_hash = last_block.hash)
		proof = self.proof_of_work(new_block)
		self.add_block(new_block, proof)
		self.unconfirmed_transactions = [] #why is  self unconfirmed_transactions an empty list again?
		return new_block.index
	
#initialize flask application
app = Flask(__name__)

#initialize blockchain object
blockchain = Blockchain()

#allows other members to participate
peers = set()

#Flask's way of declaring end points
@app.route('/new_transaction', methods = ['POST'])
def new_transaction():
	tx_data = request.get_json()
	required_fields = ["author", "content"]
	
	for field in required_fields:
		if not tx_data.get(field):
			return "Invalid transaction data", 404
	
	tx_data["timestamp"] = time.time()
	
	blockchain.add_new_transactions(tx_data)
	
	return "Success", 201
@app.route('/chain', methods = ['GET'])
def get_chain():
	chain_data = []
	for block in blockchain.chain:
		chain_data.append(block.__dict__)
	return json.dumps({"length": len(chain_data), "chain": chain_data})
@app.route('/mine', methods = ['GET'])
def mine_unconfirmed_transactions():
	result = blockchain.mine()
	if not result:
		return "No transactions to mine"
	return "Block {} is mined.".format(result)
@app.route('/pending_tx')
def get_pending_tx():
	return json.dumps(blockchain.unconfirmed_transactions)
#Endpoint to add new peers to the network
@app.route('/register_node', methods = ['POST'])
def register_new_peers():
	#host address to peer node
	node_address = request.get_json()["node_address"]
	if not node_address:
		return "Invalid Data", 400
	#Add the node to the peer list
	peers.add(node_address)