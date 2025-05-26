from datetime import datetime
from hashlib import sha256
from typing import List, Optional
from pydantic import BaseModel
import rsa


class create_request (BaseModel):
    lender: str = "Femi"
    borrower: str
    amount: int
    
class balance (BaseModel):
    lender: str
    
# create lending group
# name, totalAmount, splitRate
class create_group (BaseModel):
    name: str
    totalAmount: float
    splitRate_inPercent: float 
    
# add lender to group
class add_lender (BaseModel):
    lender: str
    group: str
    

# Lending request transactions   
class LendingRequestM(BaseModel):
    lender: str = None
    borrower: str
    amount: int
    requestDate: Optional[datetime] = datetime.now()
    requestHash: Optional[str]
    
class AccountM(BaseModel):
    lendingRequest: LendingRequestM
    lastAccount: str = None
    creationDate: datetime = datetime.now()   
    hashState: Optional[str]
    
class Lender(BaseModel):
    name: str
    amount: float
    proof_of_participation_key: Optional[str]

class GroupLenderM(BaseModel):
    name: str
    totalAmount: float
    splitRate_inPercent: float
    lenders: List[Lender] = []
    groupCreationDate: datetime = datetime.now()
    groupHash: Optional[str]

class LendingRequest:        
    def __init__(self, lenderRequest: LendingRequestM):
        self.lender = lenderRequest.lender
        self.borrower = lenderRequest.borrower
        self.amount = lenderRequest.amount
        self.requestDate = lenderRequest.requestDate
        
    def calculate_request_hash(self):
        return sha256((str(self.lender) + str(self.borrower) + str(self.amount) + str(self.requestDate)).encode()).hexdigest()
    
# blocks  
class Account:
    def __init__(self, account: AccountM):
        self.lendingRequest = account.lendingRequest
        self.lastAccount = account.lastAccount
        self.creationDate = account.creationDate        
        self.counter = 0
        self.hashState = self.calculate_hash_state()
        self.miningWork()
        
    def calculate_hash_state(self):
        hash_object = sha256((str(self.lendingRequest) + str(self.lastAccount) + str(self.creationDate) + str(self.counter)).encode())
        return hash_object.hexdigest()
    
    def miningWork(self, difficulty=3):
        start_time = datetime.now()
        while True:
            if self.hashState[0:difficulty] == ''.join(['0'] * difficulty):
                print("\n Mining Work Completed in %s seconds" % (datetime.now() - start_time))
                break
            else:
                # increment the counter
                self.counter += 1
                self.hashState = self.calculate_hash_state()
                
                
class GroupLender:
    def __init__(self, groupLender: GroupLenderM):
        self.name = groupLender.name
        self.lenders = groupLender.lenders
        self.totalAmount = groupLender.totalAmount
        self.splitRate = groupLender.splitRate_inPercent
        self.groupCreationDate = datetime.now()
        
    def calculate_hash(self):
        return sha256((str(self.totalAmount) + str(self.splitRate) + str(self.groupCreationDate)).encode()).hexdigest()
        
    def calculate_total_lended(self):
        total_lended = 0
        for lender in self.lenders:
            total_lended += lender.amount
        return total_lended
    
    def process_lender_stake(self, groupHash):
        # sign the group and give proof of participation to each lender
        (public_key, priv_key) = rsa.newkeys(512)  
        signature = rsa.sign(groupHash.encode(), priv_key, 'SHA-256')
       
        # print('verify: ', rsa.verify(self.ash.encode(), signature, public_key))
        
        for lender in self.lenders:
            lender.proof_of_participation_key = str(public_key)
            
        return self.lenders