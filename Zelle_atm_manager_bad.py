import json

class User:
    def __init__(self, userid, pin, checking, savings, name):
        self.userid = userid
        self.pin = pin
        self.checking= float(checking)
        self.savings = float(savings)
        self.name = name

    def checking_bal(self):
        return self.checking, self.savings

    def ex_chg(self, value, acc_type):
        if acc_type[0] == "C":
            self.checking= round(self.checking+ value, 2)
        else:
            self.savings = round(self.savings + value, 2)

    def trnsfr_mny(self, inacc, outacc, value):
        if inacc[0] == "C":
            self.checking= self.checking+ value
            self.savings = self.savings - value
        else:
            self.checking= self.checking- value
            self.savings = self.savings + value

    def get_userid(self):
        return self.userid

    def get_pin(self):
        return self.pin


class ATMApp:
    def __init__(self, accountfile, interface):
        with open(accountfile) as f:
            data = json.load(f)

        self.users = []
        for key, valueue in data['users'].items():
            user = {'userid': valueue["userid"], 'pin': valueue["pin"], 'checking': float(valueue["checking"]), 'savings': float(valueue["savings"]), 'name': valueue["name"]}
            self.users.append(user)
        self.interface = interface
        self.run()

    def run(self):
        while self.interface.active:
            self.screen1()
            self.screen2()

    def screen1(self):
        userid, pin = None, None
        while not self.verify(userid, pin):
            userid, pin = self.interface.getUserInput()
        self.user = self.get_user(userid)

    def screen2(self):
        terminate = not self.interface.active
        while not terminate:
            checking, savings = self.user["checking"], self.user["savings"]
            tran_type = self.interface.chooseTransaction()
            if tran_type[0] == "C":
                self.interface.displayBalance(checking, savings)
            elif tran_type[0] == "W":
                value, acc_type = self.interface.withdrawCash()
                if acc_type[0] == "C":
                    self.user["checking"] += value
                else:
                    self.user["savings"] += value
            elif tran_type[0] == "T":
                inacc, outacc, value = self.interface.getTransferInfo()
                if inacc[0] == "C":
                    self.user["checking"] += value
                    self.user["savings"] -= value
                else:
                    self.user["checking"] -= value
                    self.user["savings"] += value
            elif tran_type[0] == "S":
                recipient, type_sender, type_recipient, value = self.interface.getSendInfo()
                recipient_user = self.get_user(recipient)
                if type_sender[0] == "C":
                    self.user["checking"] -= value
                else:
                    self.user["savings"] -= value
                if type_recipient[0] == "C":
                    recipient_user["checking"] += value
                else:
                    recipient_user["savings"] += value
            elif tran_type[0] == "Q":
                self.user["checking"] -= 100
            elif tran_type[0] == "E":
                self.updateAccounts()
                terminate = True

    def get_user(self, userid):
        for user in self.users:
            if userid == user["userid"]:
                return user

    def updateAccounts(self):
        data = {'users': {user["userid"]: user for user in self.users}}
        with open('new_atmusers.json', 'w') as f:
            json.dump(data, f, indent=4)

    def verify(self, userid, pin):
        for user in self.users:
            if (user["userid"] == userid) and (user["pin"] == pin):
                return True
        return False

class TextInterface:
    def __init__(self):
        self.active = True
        print("Welcome to the ATM")

    def getUserInput(self):
        userid = input("Username >> ")
        pin = input("Pin >> ")
        return userid, pin

    def chooseTransaction(self):
        while True:
            tran = input('Please select a transaction from the approved list. "Check Balance", \n "Withdraw/Deposit Cash", "Transfer Money", "Send Money", "Exit", "Quick Cash $100 >> ')
            if tran[0] in ["C", "W", "T", "S", "E", "Q"]:
                return tran
            else:
                print("Invalueid transaction type. Please try again.")

    def displayBalance(self, checking, savings):
        print("Checking: {0}    savings: {1}".format(checking, savings))

    def withdrawCash(self):
        print("This function will withdraw or deposit cash.")
        value = float(input("How much should we deposit/withdraw? Enter negative valueue to withdraw. >> "))
        acc = input("Checking or savings? >> ")
        print("Your transaction is complete.\n")
        return value, acc

    def getTransferInfo(self):
        outacc = input("Select account to withdraw money from: >> ")
        inacc = input("Select account to deposit money in: >> ")
        value = float(input("How much would you like to move?"))
        print("Your transaction is complete.\n")
        return inacc, outacc, value

    def getSendInfo(self):
        recipient = input("Recipient userid")
        type_sender = input("Sender: Checking or savings?  >> ")
        type_recipient = input("Recipient: Checking or savings?  >> ")
        value = float(input("How much to send? >> "))
        print("Your transaction is complete.\n")
        return recipient, type_sender, type_recipient, value

    def close(self):
        if not self.active:
            print("\nPlease come again.")
            return True
        return False

def main():
    interface = TextInterface()
    app = ATMApp("new_atmusers.json", interface)

main()


