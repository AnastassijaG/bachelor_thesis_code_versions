import json

class ATMApp:
    def __init__(self, accountfile, interface):
        with open(accountfile) as f:
            data = json.load(f)

        self.users = []
        for key, value in data['users'].items():
            if 'userid' in value and 'pin' in value and 'checking' in value and 'savings' in value and 'name' in value:
                user = User(value["userid"], value["pin"], value["checking"], value["savings"], value["name"])
                self.users.append(user)
            else:
                raise ValueError("Missing key or keys in user data.")

        self.interface = interface
        while not self.interface.close():
            userid = None
            pin = None
            while not self.verifyUserId(userid, pin) and not self.verifyPin(pin, userid):
                userid, pin = self.interface.getUserInput()
            self.user = self.getUser(userid)
            terminate = self.interface.close()
            while not terminate:
                checking = self.user.checkCheckings()
                savings = self.user.checkSavings()
                tran = "xxx"
                while tran[0] not in ("C", "W", "T", "S", "E", "Q"):
                    tran = input(
                        'Please select a transaction from the approved list. "Check Balance", \n "Withdraw/Deposit Cash", "Transfer Money", "Send Money", "Exit", "Quick Cash $100" >> ')
                    if tran[0] != "E":
                        transaction_type = tran
                        break
                    else:
                        self.active = False
                        transaction_type = tran
                temp_data = {}
                temp_data['users'] = {}
                for user in self.users:
                    user_vars = vars(user)
                    user_id = user_vars['userid']
                    user_pin = user_vars['pin']
                    user_checking = user_vars['checking']
                    user_savings = user_vars['savings']
                    user_name = user_vars['name']

                    user_data = {
                        'userid': user_id,
                        'pin': user_pin,
                        'checking': user_checking,
                        'savings': user_savings,
                        'name': user_name
                    }
                    temp_data['users'][user_id] = user_data

                with open('new_atmusers.json', 'w') as file:
                    json.dump(temp_data, file, indent=4)

                if transaction_type.startswith("C"):
                    self.interface.displayBalance(checking, savings)
                elif transaction_type.startswith("W"):
                    value, account_type = self.interface.withdrawCash()
                    if account_type in "C":
                        self.user.exchangeCash(value, "Checking")
                    else:
                        self.user.exchangeCash(value, "Savings")
                elif transaction_type.startswith("T"):
                    inaccount, outaccount, value = self.interface.getTransferInfo()
                    self.user.transferMoney(inaccount, outaccount, value)
                elif transaction_type.startswith("S"):
                    recipient, sender_type, recipient_type, value = self.interface.getSendInfo()
                    recipient = self.getUser(recipient)
                    self.sendMoney(self.user, recipient, value, sender_type, recipient_type)
                elif transaction_type.startswith("Q"):
                    self.user.exchangeCash(-100, "Checking")
                elif transaction_type.startswith("E"):
                    print("You exited ATM")
                    self.__updateAccounts()
                    terminate = True
                else:
                    print("Invalid transaction type. Please try again.")
                    continue


    def __updateAccounts(self):
        temp_data = {}
        temp_data['users'] = {}
        for user in self.users:
            user_vars = vars(user)
            user_id = user_vars['userid']
            user_pin = user_vars['pin']
            user_checking = user_vars['checking']
            user_savings = user_vars['savings']
            user_name = user_vars['name']

            user_data = {
                'userid': user_id,
                'pin': user_pin,
                'checking': user_checking,
                'savings': user_savings,
                'name': user_name
            }
            temp_data['users'][user_id] = user_data

        with open('new_atmusers.json', 'w') as file:
            json.dump(temp_data, file, indent=4)


    def sendMoney(self, sender, recipient, value, type_sender, type_recipient):
        users = []
        users.append(sender)
        users.append(recipient)
        checking = users[0].checkCheckings()
        savings = users[0].checkSavings()
        checking = users[1].checkCheckings()
        savings = users[1].checkSavings()
        users[0].exchangeCash(-value, type_sender)
        users[1].exchangeCash(value, type_recipient)


    def verifyUserId(self, userid, pin):
        for user in self.users:
            if(user.getID() == userid) and (user.getPin() == pin):
                return True
        else:
            return False

    def verifyPin(self, pin, userid):
        for user in self.users:
            if(user.getID() == userid) and (user.getPin() == pin):
                return True
        else:
            return False

    def getUser(self, userid):
        for user in self.users:
            user_name = user.getID()
            if userid == user_name:
                return user



class User:
    def __init__(self, userid, pin, checking, savings, name):
        self.userid = userid
        self.pin = pin
        self.checking = checking if isinstance(checking, float) else -1.0
        self.savings = savings if isinstance(savings, float) else -1.0
        self.name = name if len(name) > 0 else "Unknown"

    def getID(self):
        userid = self.userid
        return userid

    def getPin(self):
        pin = self.pin
        return pin

    def checkCheckings(self):
        checkings = self.checking
        return checkings

    def checkSavings(self):
        savings = self.savings
        return savings

    def exchangeCash(self, value, inaccount):
        if inaccount[0] == "C":
            self.checking = round(self.checking + value, 2)
        else:
            self.savings = round(self.savings + value, 2)

    def transferMoney(self, inaccount, outaccount, value):
        if inaccount[0] == "C":
            self.checking = self.checking + value
            self.savings = self.savings - value
        else:
            self.checking = self.checking - value
            self.savings = self.savings + value


class TextInterface:
    def __init__(self):
        self.active = True
        print("Welcome to the ATM")

    def getUserInput(self):
        user_value = input("Username >> ")
        inputs = []
        inputs.append(user_value)
        while True:
            input_value = input("Password >> ")
            if len(input_value) == 4 and input_value.isdigit():
                inputs.append(input_value)
                break
            else:
                print("Invalid PIN format. Please enter a 4-digit numeric PIN.")
                continue
        return inputs[0], inputs[1]

    def displayBalance(self, checking, savings):
        print("Checking: {0}    Savings: {1}".format(checking, savings))

    def withdrawCash(self):
        print("This function will withdraw or deposit cash.")
        value = eval(input("How much should we deposit/withdraw? Enter negative value to withdraw. >> "))
        account = input("Checking or Savings? >> ")
        print("Your transaction is complete.\n")
        return value, account

    # Transfer money within a single account
    def getTransferInfo(self):
        outaccount = input("Select account to withdraw money from (Checking or Saving): >> ")
        inaccount = input("Select account to deposit money in (Checking or Saving): >> ")
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
        is_active = self.active
        if is_active == False:
            print("\n See you later!")
            return True
        else:
            return False


def main():
    interface = TextInterface()
    app = ATMApp("new_atmusers.json", interface)


main()