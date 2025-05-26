"""_summary_
    This is a blockchain implementation for a money lender.
    It allows users to lend out money as a group using an agreed smart contract or sharing the payment.
    The group determines how much each person lends out, when they money is complete, they get a proof of participation key.
"""

from flask import jsonify
from flask_openapi3 import Info, OpenAPI

from money_lender_blockchain import MoneyLenderBlockChain
from lending_requests import create_request, balance, create_group, add_lender

# instantiate the blockchain server
info = Info(title="Money Lender Blockchain", version='1.0.0', description="""This is a blockchain implementation for a money lender. </br>
    It allows users to lend out money as a group using an agreed smart contract or sharing the payment. </br>
    The group determines how much each person lends out, when they money is complete, they get a proof of participation key. </br>
            </br> Process: </br>
            1 - Create a lending request or fund wallet for upto 5 lenders, Femi receives all funds mined into the blockchain, get some from him</br>
            2 - check the pending request list</br>
            3 - process the pending requests and wallets have now been funded</br>
            4 - check the wallet balance of any of the added lender</br>
            5 - Create a new group with the total amount to be lended out and the split rate </br>
            6 - Add the lenders to the lending group you just created</br>
            7 - process the pending requests and lenders have now been funded</br>
            7 - if the total amount is equal to the total amount lended out, the proof of participation would be </br> automatically shared with the lenders in the group</br>
            8 - Check the balance of the lender group as a lender</br>
            9 - list all groups to confirm transaction and proof of participation key was shared with all the lenders</br>""")

money_lender_app = OpenAPI("Money Lender Blockchain", info=info)

money_lender_blockchain = MoneyLenderBlockChain()

# sample lending requests
#money_lender_blockchain.create_new_lending_request("Femi", "John", 100)

# show the accounts as json
@money_lender_app.get('/accounts', summary="List all account blocks in the blockchain")
def show_accounts():
    accounts = []
    for acc in money_lender_blockchain.AccountChain:
        request = acc.lendingRequest
        accounts.append({
                "lendingRequest": [
                        {
                            "lender": request.lender,
                            "borrower": request.borrower,
                            "amount": request.amount,
                            "requestDate": request.requestDate,
                            "requestHash": request.requestHash
                        }
                    ],
                "lastAccount": acc.lastAccount,
                "creationDate": acc.creationDate,
                "hashState": acc.hashState 
            })
    
    return jsonify(accounts)

# get list of pending requests
@money_lender_app.get('/pending_requests', summary="List all pending requests")
def show_pending_requests():
    requests = []
    for request in money_lender_blockchain.pendingRequests:
        requests.append({
                "lender": request.lender,
                "borrower": request.borrower,
                "amount": request.amount,
                "requestDate": request.requestDate
            })
    
    return jsonify(requests)

# process all prending requests
@money_lender_app.post('/process_requests', summary="Process all pending requests")
def process_requests():
    money_lender_blockchain.process_pending_requests()
    
    return jsonify({"message": "All pending requests have been processed"})



@money_lender_app.post('/create_lending_requests/', summary="Create a new lending request or fund wallet")
def create_new_lending_request(query: create_request):
    lender = query.lender
    borrower = query.borrower
    amount = query.amount
    
    # create a new lending request
    res = money_lender_blockchain.create_new_lending_request(lender, borrower, amount)
    
    return res
    
# get the balance of a lender
@money_lender_app.get('/lender/balance', summary="Get the balance of a lender")
def get_lender_balance(query: balance):
    return jsonify({"balance": money_lender_blockchain.calculate_lender_balance(query.lender)})

# create lending group
@money_lender_app.post('/create_lending_group/', summary="Create a new lending group")
def create_new_lending_group(query: create_group):
    group = {
                "name": query.name,
                "totalAmount": query.totalAmount,
                "splitRate": query.splitRate_inPercent,
                "lenders": []
            }
    
    if(money_lender_blockchain.create_lender_group(query.name, query.totalAmount, query.splitRate_inPercent) == True):
        return jsonify(group)
    else:
        return jsonify({"message": "Lending group already exists or could not be created"})

# add lender to lending group
@money_lender_app.post('/lending_group/add_lender', summary="Add a lender to a lending group")
def add_lender_to_lending_group(query: add_lender):
    
    if(money_lender_blockchain.add_lender_to_group(query.lender, query.group) == True):
        return jsonify({"message": "Lender added to group"})
    else:
        return jsonify({"message": "Lender already exists in group or could not be added"})

# show all lending groups and their lenders
@money_lender_app.get('/lending_groups', summary="Show all lending groups and their lenders")
def show_lending_groups():
    groups = []
    for group in money_lender_blockchain.groupLenders:
        lenders = []
        for lender in group.lenders:
            lenders.append({
                "name": lender.name,
                "amount": lender.amount,
                "proof_of_participation_key": lender.proof_of_participation_key
            })
            
                      
        groups.append({
                "name": group.name,
                "totalAmount": group.totalAmount,
                "splitRate_inPercent": group.splitRate_inPercent,
                "groupCreationDate": group.groupCreationDate,
                "groupHash": group.groupHash,                
                "lenders": lenders,                
            })
    
    return jsonify(groups)

# list all lenders in the account blocks in the blockchain
@money_lender_app.get('/lender_requests', summary="List all lender requests (transactions) in the blockchain")
def show_lenders():
    lenders = []
    for acc in money_lender_blockchain.AccountChain:
        request = acc.lendingRequest
        lenders.append({
                "lender": request.lender,
                "borrower": request.borrower,
                "amount": request.amount,
                "requestDate": request.requestDate
            })
    
    return jsonify(lenders)

@money_lender_app.route('/', methods=['GET'])
def get_root():
    # html page
    html = """
        <h1>Welcome to the Money Lender Blockchain</h1>
        <p> This is a blockchain implementation for money lending service.
        <p> This service allows users to borrow money from one another using an agreed smart contract.
        <p> The blockchain currently has {0} accounts.
        <p> and it is currently valid: {1}
        <p> The default lending duration is 12 months.
        <p> The default interest rate is 25%.
        <p> The maximum amount of money that can be lent is 1000.
        <p> The main lender is "Femi".
        <p> The current number of pending loan requests are: {2}
        <p> smart contract before the loan request is made: simple interest formula applied, and current balance of lender when the request is made.
        """.format(len(money_lender_blockchain.AccountChain), 
                   money_lender_blockchain.is_the_blockchain_valid(),
                   len(money_lender_blockchain.pendingRequests))
    
    return html

# Instantiate the Blockchain Network and create the first block
if __name__ == '__main__':
    # Start the Blockchain Server
    money_lender_app.run(host='0.0.0.0', port=5000)