# Author: ShaunCodes
# Date:   September 4, 2020

# class definition
class Account:

    # Object constructor
    def __init__(self, acct_pin=0, member_id=0, mem_first_name='John', mem_last_name='Doe', mem_balance=0):
        self.acct_pin = acct_pin
        self.member_id = member_id
        self.mem_first_name = mem_first_name
        self.mem_last_name = mem_last_name
        self.mem_balance = mem_balance

    # Get functions for each property
    def getAcctPin(self):
        return self.acct_pin

    def getId(self):
        return self.member_id

    def getMemName(self):
        return self.mem_first_name + ' ' + self.mem_last_name

    def getBalance(self):
        return self.mem_balance

    # Class action functions
    def withdraw(self, amount):
        self.mem_balance -= amount

    def deposit(self, amount):
        self.mem_balance += amount
