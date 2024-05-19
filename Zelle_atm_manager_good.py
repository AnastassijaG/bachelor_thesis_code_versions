import json


class User:
    def __init__(self, userid, pin, checking, savings, name):
        self.userid = userid
        self.pin = pin
        self.checking = float(checking)
        self.savings = float(savings)
        self.name = name

    def get_id(self):
        return self.userid

    def get_pin(self):
        return self.pin

    def get_balances(self):
        return self.checking, self.savings

    def exchange_cash(self, value, account_type):
        if account_type.lower() == "checking":
            self.checking += value
        else:
            self.savings += value


class ATMApp:
    def __init__(self, account_file, interface):
        self.users = self.load_users(account_file)
        self.interface = interface
        self.run()

    def load_users(self, account_file):
        with open(account_file) as f:
            data = json.load(f)

        users = []
        for user_data in data['users'].values():
            user = User(user_data["userid"], user_data["pin"], user_data["checking"], user_data["savings"],
                        user_data["name"])
            users.append(user)
        return users

    def run(self):
        while not self.interface.should_close():
            self.process_login()
            self.process_transactions()

    def process_login(self):
        userid, pin = None, None
        while not self.verify_user(userid, pin):
            userid, pin = self.interface.get_user_input()
        self.current_user = self.get_user(userid)

    def process_transactions(self):
        while not self.interface.should_close():
            checking, savings = self.current_user.get_balances()
            transaction_type = self.interface.choose_transaction()
            if transaction_type == "Check Balance":
                self.interface.display_balance(checking, savings)
            elif transaction_type == "Withdraw/Deposit Cash":
                value, account_type = self.interface.withdraw_cash()
                self.current_user.exchange_cash(value, account_type)
            elif transaction_type == "Transfer Money":
                in_account, out_account, value = self.interface.get_transfer_info()
                self.transfer_money(out_account, value, in_account)
            elif transaction_type == "Send Money":
                recipient, sender_account_type, recipient_account_type, value = self.interface.get_send_info()
                recipient_user = self.get_user(recipient)
                self.send_money(self.current_user, recipient_user, value, sender_account_type, recipient_account_type)
            elif transaction_type == "Quick Cash $100":
                self.current_user.exchange_cash(-100, "Checking")
            elif transaction_type == "Exit":
                self.update_accounts()
                self.interface.set_active(False)
                break

    def verify_user(self, userid, pin):
        for user in self.users:
            if user.get_id() == userid and user.get_pin() == pin:
                return True
        return False

    def get_user(self, userid):
        for user in self.users:
            if userid == user.get_id():
                return user

    def transfer_money(self, out_account, value, in_account):
        user = self.current_user
        if out_account.lower() == "checking":
            user.exchange_cash(-value, "Checking")
            user.exchange_cash(value, "Savings")
        else:
            user.exchange_cash(-value, "Savings")
            user.exchange_cash(value, "Checking")


    def send_money(self, sender, recipient, value, sender_account_type, recipient_account_type):
        sender.exchange_cash(-value, sender_account_type)
        recipient.exchange_cash(value, recipient_account_type)

    def update_accounts(self):
        data = {'users': {}}
        for user in self.users:
            data['users'][user.get_id()] = vars(user)
        with open('new_atmusers.json', 'w') as f:
            json.dump(data, f, indent=4)


class TextInterface:
    def __init__(self):
        self.active = True
        print("Welcome to the ATM")

    def get_user_input(self):
        username = input("Username >> ")
        pin = input("Pin >> ")
        return username, pin

    def choose_transaction(self):
        while True:
            transaction = input(
                'Please select a transaction: "Check Balance", "Withdraw/Deposit Cash", "Transfer Money", "Send Money", "Quick Cash $100", "Exit" >> ')
            if transaction in ["Check Balance", "Withdraw/Deposit Cash", "Transfer Money", "Send Money",
                               "Quick Cash $100", "Exit"]:
                return transaction

    def display_balance(self, checking, savings):
        print(f"Checking: {checking}    Savings: {savings}")

    def withdraw_cash(self):
        print("This function will withdraw or deposit cash.")
        value = float(input("How much should we deposit/withdraw? Enter negative value to withdraw. >> "))
        account = input("Checking or Savings? >> ")
        print("Your transaction is complete.\n")
        return value, account

    def get_transfer_info(self):
        out_account = input("Select account to deposit money to: >> ")
        in_account = input("Select account to withdraw money from: >> ")
        value = float(input("How much would you like to move? "))
        print("Your transaction is complete.\n")
        return out_account, in_account, value

    def get_send_info(self):
        recipient = input("Recipient userid: ")
        sender_account_type = input("Sender: Checking or Savings?  >> ")
        recipient_account_type = input("Recipient: Checking or Savings?  >> ")
        value = float(input("How much to send? >> "))
        print("Your transaction is complete.\n")
        return recipient, sender_account_type, recipient_account_type, value

    def should_close(self):
        if not self.active:
            print("\nPlease come again.")
            return True
        else:
            return False

    def set_active(self, active):
        self.active = active


def main():
    interface = TextInterface()
    app = ATMApp("new_atmusers.json", interface)


main()
