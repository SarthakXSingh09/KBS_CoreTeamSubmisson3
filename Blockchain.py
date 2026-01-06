import hashlib
import time

class Block:
    def __init__(self, index, timestamp, data, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.cal_hash()

    def cal_hash(self):
        block_string = (
            str(self.index)
            + str(self.timestamp)
            + str(self.data)
            + str(self.previous_hash)
            + str(self.nonce)
        )
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2  # number of leading zeros

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def mine_block(self, block):
        while not block.hash.startswith("0" * self.difficulty):
            block.nonce += 1
            block.hash = block.cal_hash()

    def add_block(self, data):
        latest_block = self.get_latest_block()
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            data=data,
            previous_hash=latest_block.hash
        )
        self.mine_block(new_block)
        self.chain.append(new_block)

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.cal_hash():
                return False

            if current.previous_hash != previous.hash:
                return False

        return True


# Example usage
if __name__ == "__main__":
    blockchain = Blockchain()

    blockchain.add_block("First transaction")
    blockchain.add_block("Second transaction")
    blockchain.add_block("Third transaction")

    for block in blockchain.chain:
        print("Index:", block.index)
        print("Timestamp:", block.timestamp)
        print("Data:", block.data)
        print("Previous Hash:", block.previous_hash)
        print("Hash:", block.hash)
        print("Nonce:", block.nonce)
        print("-" * 30)

    print("Blockchain valid?", blockchain.is_valid())
