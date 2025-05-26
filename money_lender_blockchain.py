from lending_requests import LendingRequest, Account, GroupLender, AccountM, LendingRequestM, GroupLenderM, Lender
from flask import jsonify

class MoneyLenderBlockChain:
    def __init__(self):
        self.pendingRequests = []
        self.groupLenders = []
        self.maxAmountMinable = 100
        self.miningOutputOwner = "Femi"
        self.miningDifficulty = 3
        self.AccountChain = []
        self.create_initial_account()
        
    def create_initial_account(self):
        lastAccount = None
        
        # generate a mined lending request
        request = LendingRequestM(borrower = self.miningOutputOwner, amount = self.maxAmountMinable)
        request.requestHash = LendingRequest(request).calculate_request_hash()
        
        # add the mined lending request an account
        account = AccountM(lendingRequest = request, lastAccount = lastAccount)
        account.hashState = Account(account).calculate_hash_state()
        
        # append to the chain
        self.AccountChain.append(account)
        
    def return_last_account(self):
        return self.AccountChain[-1]
    
    def create_new_account(self, account):
        self.AccountChain.append(account)
    
    def is_the_blockchain_valid(self):
        for i in range(len(self.AccountChain) - 1):
            
            # compare hashes between the last account and the current account
            if self.AccountChain[i].hashState != self.AccountChain[i+1].lastAccount:
                return False
            
            # compare stored hash and calculated hash state
            if self.AccountChain[i].hashState != self.AccountChain[i].calculate_hash_state():
                return False
            
            # latest accounts should have the most recent creation date
            if self.AccountChain[i].creationDate > self.return_last_account().creationDate:
                return False           
            
        return True
        
    def create_new_lending_request(self, lender: str, borrower: str, amount: float):
        
        # the lender cannot be the borrower
        if(lender.lower() == borrower.lower()):
            return jsonify({"message": "The lender cannot be the borrower"}), 400
        
        # the lender cannot lend more than the max amount
        if amount > self.maxAmountMinable:
            return jsonify({"message": "The lender cannot lend more than the max amount"}), 400
        
        # the lender cannot lend more than the amount he has
        if amount > self.calculate_lender_balance(lender):
            return jsonify({"message": "The lender cannot lend more than the amount he has"}), 400
        
        # the lender or borrower cannot be blank
        if(lender == "" or borrower == ""):
            return jsonify({"message": "The lender or borrower cannot be blank"}), 400
        
        if(amount <= 0):
            return jsonify({"message": "The amount must be greater than 0"}), 400
        
        lending_request = LendingRequestM(lender = lender, borrower = borrower, amount = amount)
        lending_request.requestHash = LendingRequest(lending_request).calculate_request_hash()
        
        for request in self.pendingRequests:
            if(request.requestHash == lending_request.requestHash):
                return jsonify({"message": "duplicate lending request not allowed"}), 400
        
        print("\n New lending request created \n")
        self.pendingRequests.append(lending_request)
        
        # return the new lending request
        return jsonify({"lendingRequest": [
            {
                "lender": lender,
                "borrower": borrower,
                "amount": amount,
                "requestHash": lending_request.requestHash,
                "requestDate": lending_request.requestDate
            }
        ]})
        
    def calculate_lender_balance(self, lender):
        # calculate the lender balance
        lender_balance = 0
        for account in self.AccountChain:
            lendingRequest = account.lendingRequest
                
            # money left the lender
            if lendingRequest.lender == lender:
                lender_balance -= lendingRequest.amount
                    
            # money lent to the borrower
            if lendingRequest.borrower.lower() == lender.lower():
                lender_balance += lendingRequest.amount
                  
        return lender_balance
            
        
    def process_pending_requests(self):
        # pro8cess the pending requests
        print(self.return_last_account().lastAccount)
        for request in self.pendingRequests:
            account = AccountM(lendingRequest = request, lastAccount = self.return_last_account().hashState)
            account.hashState = Account(account).calculate_hash_state()
            self.AccountChain.append(account)
            
        # clear the pending requests
        self.pendingRequests = []
            
        # mine new account transaction
        request1 = LendingRequestM(borrower = self.miningOutputOwner, amount = self.maxAmountMinable)
        request1.requestHash = LendingRequest(request1).calculate_request_hash()
        
        # adding the mined lending request to an account
        account1 = AccountM(lendingRequest = request1, lastAccount = self.return_last_account().hashState)
        account1.hashState = Account(account1).calculate_hash_state()
        
        # add the new account to the chain
        self.AccountChain.append(account1)
    
    def create_lender_group(self, name, amount, splitRate_inPercent = 0.25):
        # the lender group must be unique
        for group in self.groupLenders:
            if group.name == name:
                print("\n The lender group must be unique \n")
                return False
        
        lender_group = GroupLenderM(name = name, totalAmount = amount, splitRate_inPercent = splitRate_inPercent)
        lender_group.groupHash = GroupLender(lender_group).calculate_hash()
        self.groupLenders.append(lender_group)
        return True
        
    def add_lender_to_group(self, lender_name, lenderGroup_name):
        # the lender must be unique
        for group in self.groupLenders:
            
            # if the group name is not found
            if group.name.lower() == lenderGroup_name.lower():
                
                # if the lender has the right balance to fund the loan and the group is not full
                if self.calculate_lender_balance(lender_name) >= group.totalAmount * group.splitRate_inPercent:
                    
                    # if the lender is not already in the group
                    for lender in group.lenders:
                        if lender.lower() == lender_name.lower():
                            print("\n The lender must be unique \n")
                            return False
                        
                    lender = Lender(name=lender_name, amount=group.totalAmount*group.splitRate_inPercent)
                    group.lenders.append(lender)
                
                    # add to the pending request list
                    self.create_new_lending_request(lender.name, group.name, group.totalAmount * group.splitRate_inPercent)
                
                    # if payment complete, share the proof of participation with the lenders
                    if (GroupLender(group).calculate_total_lended() == group.totalAmount):
                        group.lenders = GroupLender(group).process_lender_stake(group.groupHash)
                
                    return True
        
        return False