from web3 import Web3
import json

class WebManager:
    w3 = Web3(Web3.HTTPProvider('HTTP://172.31.240.1:7455'))
    contract_address = '0x7B326740D5b4c08a8f8019FC6906F38a6a14847A'
    contract_abi_file = 'web/contract_abi.json'

    def __init__(self, address):
        self.contract = self.getContract()
        self.setAccount(address)

    def getContract(self):
        file = open(self.contract_abi_file)
        contract_abi = json.load(file)
        file.close()
        return self.w3.eth.contract(address = self.contract_address, abi = contract_abi)

    def setAccount(self, account_address):
        self.w3.eth.default_account = account_address

    # Using Contract
    def createProperty(self, title, info, is_for_sale, price):
        tx_hash = self.contract.functions.createProperty(title, info, is_for_sale, price).transact()
        self.w3.eth.wait_for_transaction_receipt(tx_hash)


    # Get from contract
    def getAllProperties(self):
        return self.contract.functions.getAllProperties().call()
    
    def getForSaleProperties(self):
        return self.contract.functions.getForSaleProperties().call()
    
    def getOwnerProperties(self, owner_address):
        try:
            return self.contract.functions.getOwnerProperties(owner_address).call()
        except:
            return []
        
    def getMyProperties(self):
        return self.contract.functions.getMyProperties().call()


    
test = WebManager('0x7076e6CFf8b0D541CEb0F7229521756d8Af380A6')
print(test.getMyProperties())
