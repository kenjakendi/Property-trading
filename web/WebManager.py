from web3 import Web3
from configparser import ConfigParser
import json

class WebManager:
    cfg = ConfigParser()
    cfg.read("conf/cfg.conf")
    w3 = Web3(Web3.HTTPProvider(cfg.get('APP_CONF', 'ganache_url')))
    contract_address = cfg.get('APP_CONF', 'contract_address')
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

    # Modify Property
    def changeTitle(self, id, title):
        self.contract.functions.changeTitle(id, title).transact()

    def changeInfo(self, id, info):
        self.contract.functions.changeInfo(id, info).transact()

    def changePrice(self, id, price):
        self.contract.functions.changePrice(id, price).transact()

    def toggleForSale(self, id):
        self.contract.functions.toggleForSale(id).transact()

    def changePropertyParams(self, id, title, info, for_sale, price):
        id -= 1
        property = self.getAllProperties()[id]
        if property[1] != title:
            self.changeTitle(id, title)
        if property[2] != info:
            self.changeInfo(id, info)
        if property[3] != for_sale:
            self.toggleForSale(id)
        if property[4] != price:
            self.changePrice(id, price)

    # Using Contract
    def createProperty(self, title, info, is_for_sale, price):
        tx_hash = self.contract.functions.createProperty(title, info, is_for_sale, price).transact()
        self.w3.eth.wait_for_transaction_receipt(tx_hash)

    def buyProperty(self, id):
        id -= 1
        property = self.getAllProperties()[id]
        tx_hash = self.contract.functions.buyProperty(id).transact({'value': property[4]})
        self.w3.eth.wait_for_transaction_receipt(tx_hash)

    # Get from contract
    def getAllProperties(self):
        return self.contract.functions.getAllProperties().call()
    
    def getForSaleProperties(self):
        return self.contract.functions.getForSaleProperties().call()
    
    def getOwnerProperties(self, owner_address):
        try:
            return self.contract.functions.getOwnerProperties(owner_address).call()
        except Exception as e:
            print(e)
            return []
        
    def getMyProperties(self):
        return self.contract.functions.getMyProperties().call()
