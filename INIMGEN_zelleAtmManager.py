import json


class ATMApp:
    """Class ATM calls account information from a JSON file and manipulates it
    per commands given through an interface class. The JSON file is then updated
    to reflect transactional commands"""

    def __init__(self, accountfile, interface):
        """Creates a list of Users labeled self.users with which to manage account
        information. Users can be sorted by userid when given the proper key."""
        with open(accountfile) as f:
            data = json.load(f)

        self.users = []
        for key, value in data['users'].items():
            user = User(value["userid"], value["pin"], value["checking"], value["savings"], value["name"])
            self.users.append(user)
        self.interface = interface
        self.run()

    def run(self):
        while not self.interface.close():
            self.screen1()
            self.screen2()

    def screen1(self):
        userid = None
        pin = None
        while not self.verify(userid, pin):
            userid, pin = self.interface.getUserInput()
        self.user = self.getUser(userid)

    def screen2(self):
        terminate = self.interface.close()
        while not terminate:
            checking, savings = self.user.checkBalances()
            tran_type = self.interface.chooseTransaction()
            self.__updateAccounts()
            if tran_type[0] == "C":
                self.interface.displayBalance(checking, savings)
            elif tran_type[0] == "W":
                value, account_type = self.interface.withdrawCash()
                self.user.exchangeCash(value, account_type)
            elif tran_type[0] == "T":
                inaccount, outaccount, value = self.interface.getTransferInfo()
                self.user.transferMoney(inaccount, outaccount, value)
            elif tran_type[0] == "S":
                recipient, type_sender, type_recipient, value = self.interface.getSendInfo()
                recipient = self.getUser(recipient)
                self.sendMoney(self.user, recipient, value, type_sender, type_recipient)
            elif tran_type[0] == "Q":
                self.user.exchangeCash(-100, "Checking")
            elif tran_type[0] == "E":
                self.__updateAccounts()
                terminate = True

    def getUser(self, userid):
        """Returns user object with given userid"""
        for user in self.users:
            if userid == user.getID():
                return user

    def sendMoney(self, sender, recipient, value, type_sender, type_recipient):
        # validate types as str "Checking" or "Savings"
        """Used to move money from one user to another. "sender" refers to the user
        itiating the transaction. "recipient" refers to the user recieving the transaction.
        "Value" should be negative to move money from sender to recipient. "type_" refers
        to the type of account being used eg. "Checking" or "Savings". """
        checking, savings = sender.checkBalances()
        checking, savings = recipient.checkBalances()
        sender.exchangeCash(-value, type_sender)
        recipient.exchangeCash(value, type_recipient)

    def __updateAccounts(self):
        data = {}
        data['users'] = {}
        for user in self.users:
            json_str = (vars(user))
            userid = user.getID()
            data['users'][userid] = json_str
        with open('new_atmusers.json', 'w') as f:
            json.dump(data, f, indent=4)

    def verify(self, userid, pin):
        for user in self.users:
            if (user.getID() == userid) and (user.getPIN() == pin):
                return True
        else:
            return False


class User:
    def __init__(self, userid, pin, checking, savings, name):
        self.userid = userid
        self.pin = pin
        self.checking = float(checking)
        self.savings = float(savings)
        self.name = name

    def checkBalances(self):
        """Returns two values, one for checking account balance, and
        one for savings account balance"""
        return self.checking, self.savings

    def exchangeCash(self, value, inaccount):
        """Used to deposit or withdraw money from checking or savings accounts."""

        if inaccount[0] == "C":
            self.checking = round(self.checking + value, 2)
        else:
            self.savings = round(self.savings + value, 2)

    def transferMoney(self, inaccount, outaccount, value):
        ####Verify that inaccount and outaccount can only be savings or checking
        """Used to move money between checking and savings accounts within a single user."""
        if inaccount[0] == "C":
            self.checking = self.checking + value
            self.savings = self.savings - value
        else:
            self.checking = self.checking - value
            self.savings = self.savings + value

    def getID(self):
        """Returns userid"""
        return self.userid

    def getPIN(self):
        return self.pin


class TextInterface:
    def __init__(self):
        self.active = True
        print("Welcome to the ATM")

    def getUserInput(self):
        # get UserID and Pin
        a = input("Username >> ")
        b = input("Pin >> ")
        return a, b

    def displayBalance(self, checking, savings):
        # display savings and checking
        print("Checking: {0}    Savings: {1}".format(checking, savings))

    def withdrawCash(self):
        print("This function will withdraw or deposit cash.")
        value = eval(input("How much should we deposit/withdraw? Enter negative value to withdraw. >> "))
        account = input("Checking or Savings? >> ")
        print("Your transaction is complete.\n")
        return value, account

    def chooseTransaction(self):
        # give user choice of "Check Balance",
        # "Withdraw Cash", "Transfer Money", "Exit", "Quick Cash $100"
        # Display user balance

        tran = "xxx"
        while tran[0] != ("C" or "W" or "T" or "S" or "E" or "Q"):
            tran = input(
                'Please select a transaction from the approved list. "Check Balance", \n "Withdraw/Deposit Cash", "Transfer Money", "Send Money", "Exit", "Quick Cash $100" >> ')
            if tran[0] != "E":
                return tran
            else:
                self.active = False
                return tran

    def getTransferInfo(self):
        outaccount = input("Select account to withdraw money from: >> ")
        inaccount = input("Select account to deposit money in: >> ")
        value = eval(input("How much would you like to move?"))
        print("Your transaction is complete.\n")
        return inaccount, outaccount, value

    def getSendInfo(self):
        recipient = input("Recipient userid")
        type_sender = input("Sender: Checking or Savings?  >> ")
        type_recipient = input("Recipient: Checking or Savings?  >> ")
        value = eval(input("How much to send? >> "))
        print("Your transaction is complete.\n")
        return recipient, type_sender, type_recipient, value

    def close(self):
        if self.active == False:
            print("\nPlease come again.")
            return True
        else:
            return False

def main():
    interface = TextInterface()
    app = ATMApp("new_atmusers.json", interface)


main()


