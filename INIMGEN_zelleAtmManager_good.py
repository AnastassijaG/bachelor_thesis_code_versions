"""GOOD CODE INIMGEN"""
import json

# valid account types written to avoid duplication
valid_account_types = {"Checking", "Savings"}


# get UserID and Pin
def getUserInput():
    username = input("Username >> ")
    pin = input("Pin >> ")
    return username, pin


# display savings and checking
def displayBalance(checking, savings):
    print(f"Checking: {checking}    Savings: {savings}")


def withdrawCash():
    """Withdraw or deposit cash."""
    value = get_valid_float("How much should we deposit/withdraw? Enter negative value to withdraw: ")
    account = get_account_type("Checking or Savings? ")
    print("Your transaction is complete.\n")
    return value, account


def readJsonData(account_file):
    try:
        with open(account_file) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{account_file}' not found.")
        return None


def get_valid_float(prompt):
    """Prompt user for input and validate it's a float."""
    while True:
        user_input = input(prompt)
        try:
            value = float(user_input)
            return value
        except ValueError:
            print("Invalid input! Please enter a valid number.")


def get_account_type(prompt):
    """Prompt user for account type (Checking or Savings)."""
    while True:
        account_type = input(prompt).strip().capitalize()
        if account_type in valid_account_types:
            return account_type
        else:
            print("Invalid account type. Please provide 'Checking' or 'Savings'.")


def getTransferInfo():
    """Get transfer information."""
    in_account = get_account_type("Select account to deposit money to (Checking or Savings): ")
    value = get_valid_float("How much would you like to move? ")
    print("Your transaction is complete.\n")
    return in_account, value


def getSendInfo():
    """Get send information."""
    recipient = input("Recipient user ID: ")
    type_sender = get_account_type("Sender account type (Checking or Savings): ")
    type_recipient = get_account_type("Recipient account type (Checking or Savings): ")
    value = get_valid_float("How much to send: ")
    print("Your transaction is complete.\n")
    return recipient, type_sender, type_recipient, value


def sendMoney(sender, recipient, value, type_sender, type_recipient):
    """Used to move money from one user to another."""
    # Validating account types
    if type_sender not in valid_account_types or type_recipient not in valid_account_types:
        print("Invalid account type. Please provide 'Checking' or 'Savings'.")
        return
    # Performing money transfer
    sender.exchangeCash(-value, type_sender)
    recipient.exchangeCash(value, type_recipient)


class ATMApp:
    # Class ATM calls account information from a JSON file and manipulates it per commands given through an interface
    # class. The JSON file is then updated to reflect transactional commands
    def __init__(self, account_file, interface):
        data = readJsonData(account_file)

        self.users = [User(user_data["userid"], user_data["pin"], user_data["checking"], user_data["savings"],
                           user_data["name"]) for user_data in data.get("users", {}).values()]
        self.interface = interface
        self.run()

    def run(self):
        while not self.interface.close():
            self.getATMUser()
            self.chooseTransaction()

    def getATMUser(self):
        while True:
            userid, pin = getUserInput()
            if self.verifyUser(userid, pin):
                self.user = self.getUser(userid)
                break
            print("Credentials are invalid. Please try again.")

    def chooseTransaction(self):
        terminate = self.interface.close()
        while not terminate:
            checking, savings = self.user.checkBalances()
            transaction_type = self.interface.chooseTransaction()
            self.__updateAccounts()
            if transaction_type[0] == "C":
               displayBalance(checking, savings)
            elif transaction_type[0] == "W":
                value, account_type = withdrawCash()
                self.user.exchangeCash(value, account_type)
            elif transaction_type[0] == "T":
                in_account, value = getTransferInfo()
                self.user.transferMoney(in_account, value)
            elif transaction_type[0] == "S":
                recipient, type_sender, type_recipient, value = getSendInfo()
                recipient = self.getUser(recipient)
                sendMoney(self.user, recipient, value, type_sender, type_recipient)
            elif transaction_type[0] == "Q":
                self.user.exchangeCash(-100, "Checking")
            elif transaction_type[0] == "E":
                self.__updateAccounts()
                terminate = True

    def verifyUser(self, userid, pin):
        return any(user.userid == userid and user.pin == pin for user in self.users)

    def getUser(self, userid):
        return next((user for user in self.users if user.userid == userid), None)

    def __updateAccounts(self):
        data = {"users": {}}
        for user in self.users:
            user_data = {
                "userid": user.userid,
                "pin": user.pin,
                "checking": user.checking,
                "savings": user.savings,
                "name": user.name
            }
            data["users"][user.userid] = user_data

        with open('new_atmusers.json', 'w') as f:
            json.dump(data, f, indent=4)


class User:
    def __init__(self, userid, pin, checking, savings, name):
        self.userid = userid
        self.pin = pin
        self.checking = float(checking)
        self.savings = float(savings)
        self.name = name

    # Returns two values, one for checking account balance, and one for savings account balance
    def checkBalances(self):
        return self.checking, self.savings

    # Used to deposit or withdraw money from checking or savings accounts.
    # Param account_type is the account type ("C" for checking, "S" for savings
    def exchangeCash(self, value, account_type):
        if account_type[0] == "C":
            self.checking = round(self.checking + value, 2)
        else:
            self.savings = round(self.savings + value, 2)

    # Used to move money between checking and savings accounts within a single user.
    def transferMoney(self, account, value):
        if account[0] == "C":
            self.checking = self.checking + value
            self.savings = self.savings - value
        else:
            self.checking = self.checking - value
            self.savings = self.savings + value


class TextInterface:
    def __init__(self):
        self.active = True

    # give user choice of "Check Balance", "Withdraw Cash", "Transfer Money", "Exit", "Quick Cash $100", "Send Money"
    def chooseTransaction(self):
        while True:
            tran = input('Please select a transaction from the approved list: \n'
                         '"Check Balance", "Withdraw/Deposit Cash", "Transfer Money", "Send Money", "Exit", "Quick Cash $100" >> ')
            if tran.startswith(("C", "W", "T", "S", "Q")):
                return tran
            elif tran.startswith("E"):
                self.active = False
                return tran
            else:
                print("Invalid transaction. Please try again.")

    def close(self):
        return not self.active


def main():
    print("Welcome to the ATM")
    interface = TextInterface()
    ATMApp("new_atmusers.json", interface)


main()
