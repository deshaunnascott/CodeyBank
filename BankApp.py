# Author: ShaunCodes
# Date:   September 4, 2020

# GUI library
import tkinter as tk
from tkinter import messagebox

# random number generator needed for new member IDs
import random

# import created classes
from BankDatabase import Database
from AccountClass import Account

class BankApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        # create GUI window
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("CodeyBank Portal")
        self.resizable(False, False)
        self.iconphoto(False, tk.PhotoImage(file='./Icon/CBP_Icon(50x50).png'))

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        # set window size
        container.rowconfigure(index=0, weight=1, minsize=150)
        container.columnconfigure(index=0, weight=1, minsize=300)

        self.frames = {}

        # create and connect to database
        self.database = Database()

        self.acct_info = ()

        self.create_frame(StartScene, container)

    def show_frame(self, scene):
        frame = self.frames[scene]
        frame.tkraise()

    def create_frame(self, scene, container):
        frame = scene(container, self)

        self.frames[scene] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(scene)

    @staticmethod
    def popupmsg(text="Try again. If you're not a member, please create an account."):
        messagebox.showinfo("CBP", text)
        return

# create start scene frame
class StartScene(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label_heading = tk.Label(self, text="Codey Bank Portal", font=("Verdana", 16, "bold"))
        self.label_heading.pack(padx=5, pady=5)

        self.info_frame = tk.Frame(self)
        self.info_frame.pack(fill=tk.BOTH, padx=5, pady=5)

        self.label_acct_id = tk.Label(master=self.info_frame, text="Enter Member ID:")
        self.entry_acct_id = tk.Entry(master=self.info_frame, width=50)

        # place label name and entry widget into frame
        self.label_acct_id.grid(row=0, column=0, sticky="nsew", pady=5)
        self.entry_acct_id.grid(row=0, column=1, sticky="nsew", pady=5)

        self.label_pin = tk.Label(master=self.info_frame, text="Enter Account Pin:")
        self.entry_pin = tk.Entry(master=self.info_frame, show="*", width=50)

        # place label name and entry widget into frame
        self.label_pin.grid(row=1, column=0, sticky="nsew")
        self.entry_pin.grid(row=1, column=1, sticky="nsew")

        # create and place entry buttons
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(fill=tk.BOTH, ipadx=5, ipady=5)

        self.button_enter = tk.Button(master=self.button_frame, text="Enter",
                                      command=lambda: self.verify_acct(parent, controller))
        self.button_enter.pack(side=tk.RIGHT, padx=10, ipadx=10)

        self.button_clear = tk.Button(master=self.button_frame, text="Clear", command=lambda: self.clear_entry())
        self.button_clear.pack(side=tk.RIGHT, padx=10, ipadx=10)

        # create account creation button
        self.create_account_frame = tk.Frame(self)
        self.create_account_frame.pack(fill=tk.BOTH, ipadx=5, ipady=5)

        self.button_create = tk.Button(master=self.create_account_frame, text="Create Account",
                                       command=lambda: controller.create_frame(CreateScene, parent))
        self.button_create.pack(side=tk.LEFT, padx=10, ipadx=10)

    def clear_entry(self):
        self.entry_pin.delete(0, 'end')
        self.entry_acct_id.delete(0, 'end')

    def verify_acct(self, parent, controller):
        acct_id = self.entry_acct_id.get().strip()
        pin = self.entry_pin.get().strip()

        # check for pin in account database
        exists = controller.database.member_exists(controller.database.table, int(pin), int(acct_id))

        # check for member pin in database
        if exists:
            controller.acct_info = controller.database.get_acct_info(controller.database.table, 'id', int(acct_id))
            controller.create_frame(MemberScene, parent)
        else:
            self.clear_entry()
            controller.popupmsg()

# create member scene frame
class MemberScene(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label_heading = tk.Label(self, text="Account Options", font=("Verdana", 16, "bold"))
        self.label_heading.pack(padx=5, pady=5)

        # create and pack the account option buttons
        self.button_withdrawal = tk.Button(self, text="Withdrawal",
                                           command=lambda: controller.create_frame(WithdrawalScene, parent))
        self.button_withdrawal.pack(padx=5, pady=5)

        self.button_deposit = tk.Button(self, text="Deposit",
                                        command=lambda: controller.create_frame(DepositScene, parent))
        self.button_deposit.pack(padx=5, pady=5)

        self.button_acct_balance = tk.Button(self, text="Account Balance",
                                             command=lambda: controller.create_frame(AccountScene, parent))
        self.button_acct_balance.pack(padx=5, pady=5)

        # list account ID number of current account owner
        self.label_id = tk.Label(self, text="Acct ID: {id}".format(id=controller.acct_info[1]))
        self.label_id.pack(side=tk.LEFT, padx=5, pady=5)

        self.button_exit = tk.Button(master=self, text="exit",
                                     command=lambda: controller.create_frame(ExitScene, parent))
        self.button_exit.pack(side=tk.RIGHT, padx=5, pady=5)

        # list name of current account owner
        self.label_member = tk.Label(self, text="Member: {fname} {lname}".format(fname=controller.acct_info[2],
                                                                                 lname=controller.acct_info[3]))
        self.label_member.pack(side=tk.RIGHT, padx=5, pady=5)

# create account creation scene frame
class CreateScene(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label_heading = tk.Label(self, text="Create Member Account", font=("Verdana", 16, "bold"))
        self.label_heading.pack(pady=10, padx=10)

        # Form title list
        self.entry_names = ['First Name:', 'Last Name:', 'Account Pin:']

        # create form frame and pack into window
        self.form_frame = tk.Frame(self)
        self.form_frame.pack(fill=tk.BOTH, ipadx=5, ipady=5, expand=True)

        # get new mem id
        self.mem_id = self.get_new_mem_id(controller)

        self.label_mem_id = tk.Label(master=self.form_frame,
                                     text="Member ID: ")
        self.label_mem_id_num = tk.Label(master=self.form_frame,
                                         text="{id}".format(id=self.mem_id))

        # create new account form
        self.label_mem_id.grid(row=0, column=0, sticky="ew")
        self.label_mem_id_num.grid(row=0, column=1, sticky="ew")

        self.label_first_name = tk.Label(master=self.form_frame, text=self.entry_names[0])
        self.ent_first_name = tk.Entry(master=self.form_frame, width=50)
        self.label_first_name.grid(row=1, column=0, sticky="ew")
        self.ent_first_name.grid(row=1, column=1, sticky="ew")

        self.label_last_name = tk.Label(master=self.form_frame, text=self.entry_names[1])
        self.ent_last_name = tk.Entry(master=self.form_frame, width=50)
        self.label_last_name.grid(row=2, column=0, sticky="ew")
        self.ent_last_name.grid(row=2, column=1, sticky="ew")

        self.label_pin = tk.Label(master=self.form_frame, text=self.entry_names[2])
        self.ent_pin = tk.Entry(master=self.form_frame, width=50)
        self.label_pin.grid(row=3, column=0, sticky="ew")
        self.ent_pin.grid(row=3, column=1, sticky="ew")

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(fill=tk.BOTH, ipadx=5, ipady=5, expand=True)

        self.button_submit = tk.Button(master=self.button_frame, text="Submit",
                                       command=lambda: self.create_new_account(controller))
        self.button_submit.pack(side=tk.RIGHT, padx=10, ipadx=10)

        self.button_cancel = tk.Button(master=self.button_frame, text="Cancel",
                                       command=lambda: controller.show_frame(StartScene))

        self.button_cancel.pack(side=tk.RIGHT, padx=10, ipadx=10)

    @staticmethod
    def get_new_mem_id(controller):
        # assign a member id
        mem_id = random.randint(1000, 9999)

        # check for id in account database
        exists = controller.database.in_database(controller.database.table, 'id', mem_id)

        while exists:
            mem_id = random.randint(1000, 9999)

            # check for id in account database
            exists = controller.database.in_database(controller.database.table, 'id', mem_id)

        return mem_id

    def create_new_account(self, controller):
        # get input information
        first_name = self.ent_first_name.get().strip()
        last_name = self.ent_last_name.get().strip()
        pin = self.ent_pin.get().strip()

        # create new account object
        new_account = Account(int(pin), self.mem_id, first_name, last_name)
        controller.database.add_new_acct(controller.database.table, new_account)

        controller.popupmsg(text="New Account Created")

        # Go back to login page
        controller.show_frame(StartScene)

# create withdrawal scene frame
class WithdrawalScene(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label_heading = tk.Label(self, text="Codey Bank Withdrawal", font=("Verdana", 16, "bold"))
        self.label_heading.pack(padx=5, pady=5)

        # create GUI elements for amount withdrawal
        self.info_frame = tk.Frame(self)
        self.info_frame.pack(fill=tk.BOTH, padx=5, pady=5)

        self.label_withdrawal = tk.Label(master=self.info_frame, text="Withdrawal Amount:")
        self.entry_withdrawal = tk.Entry(master=self.info_frame, width=20)

        self.label_withdrawal.pack(fill=tk.BOTH, pady=10)
        self.entry_withdrawal.pack()

        # create and place entry buttons
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(fill=tk.BOTH, ipadx=5, ipady=5)

        self.button_enter = tk.Button(master=self.button_frame, text="Submit",
                                      command=lambda: self.update_member_account(controller, parent))
        self.button_enter.pack(side=tk.RIGHT, padx=10, ipadx=10)

        self.button_clear = tk.Button(master=self.button_frame, text="Clear", command=lambda: self.clear_entry())
        self.button_clear.pack(side=tk.RIGHT, padx=10, ipadx=10)

        # create account creation button
        self.create_account_frame = tk.Frame(self)
        self.create_account_frame.pack(fill=tk.BOTH, ipadx=5, ipady=5)

        self.button_create = tk.Button(master=self.create_account_frame, text="Cancel",
                                       command=lambda: controller.create_frame(MemberScene, parent))
        self.button_create.pack(side=tk.LEFT, padx=10, ipadx=10)

    def clear_entry(self):
        self.entry_withdrawal.delete(0, 'end')

    def update_member_account(self, controller, parent):
        # withdrawal requested amount
        withdrawal_amt = self.entry_withdrawal.get().strip()
        new_amt = controller.acct_info[4] - float(withdrawal_amt)

        controller.database.update_balance(controller.database.table, controller.acct_info[1], new_amt)

        # get updated information
        controller.acct_info = controller.database.get_acct_info(controller.database.table, 'id',
                                                                 int(controller.acct_info[1]))
        if new_amt < float(0):
            controller.popupmsg(text="Account Balance Updated. But Account is Overdrawn")
        else:
            controller.popupmsg(text="Account Balance Updated")

        # update and go back to account options
        controller.create_frame(MemberScene, parent)

# create deposit scene frame
class DepositScene(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label_heading = tk.Label(self, text="Codey Bank Deposit", font=("Verdana", 16, "bold"))
        self.label_heading.pack(padx=5, pady=5)

        # create GUI elements for amount deposit
        self.info_frame = tk.Frame(self)
        self.info_frame.pack(fill=tk.BOTH, padx=5, pady=5)

        self.label_withdrawal = tk.Label(master=self.info_frame, text="Deposit Amount:")
        self.entry_withdrawal = tk.Entry(master=self.info_frame, width=20)

        self.label_withdrawal.pack(fill=tk.BOTH, pady=10)
        self.entry_withdrawal.pack()

        # create and place entry buttons
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(fill=tk.BOTH, ipadx=5, ipady=5)

        self.button_enter = tk.Button(master=self.button_frame, text="Submit",
                                      command=lambda: self.update_member_account(controller, parent))
        self.button_enter.pack(side=tk.RIGHT, padx=10, ipadx=10)

        self.button_clear = tk.Button(master=self.button_frame, text="Clear", command=lambda: self.clear_entry())
        self.button_clear.pack(side=tk.RIGHT, padx=10, ipadx=10)

        # create account creation button
        self.create_account_frame = tk.Frame(self)
        self.create_account_frame.pack(fill=tk.BOTH, ipadx=5, ipady=5)

        self.button_create = tk.Button(master=self.create_account_frame, text="Cancel",
                                       command=lambda: controller.create_frame(MemberScene, parent))
        self.button_create.pack(side=tk.LEFT, padx=10, ipadx=10)

    def clear_entry(self):
        self.entry_withdrawal.delete(0, 'end')

    def update_member_account(self, controller, parent):
        # deposit requested amount
        deposit_amt = self.entry_withdrawal.get().strip()
        new_amt = controller.acct_info[4] + float(deposit_amt)

        controller.database.update_balance(controller.database.table, controller.acct_info[1], new_amt)

        # get updated information
        controller.acct_info = controller.database.get_acct_info(controller.database.table, 'id',
                                                                 int(controller.acct_info[1]))

        controller.popupmsg(text="Account Balance Updated")

        # update and go back to account options
        controller.create_frame(MemberScene, parent)

# create account details scene frame
class AccountScene(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label_heading = tk.Label(self, text="Account Details", font=("Verdana", 16, "bold"))
        self.label_heading.pack(padx=5, pady=5)

        # create frame for current account owner information
        self.info_frame = tk.Frame(self)
        self.info_frame.pack(fill=tk.BOTH, padx=5, pady=5)

        self.label_balance = tk.Label(master=self.info_frame,
                                      text="Balance: {balance}".format(balance=controller.acct_info[4]))
        self.label_balance.pack(fill=tk.BOTH, pady=5)

        self.label_id = tk.Label(master=self.info_frame,
                                 text="Account ID: {id}".format(id=controller.acct_info[1]))
        self.label_id.pack(fill=tk.BOTH, pady=5)

        self.label_name = tk.Label(master=self.info_frame,
                                   text="Member: {fname} {lname}".format(fname=controller.acct_info[2],
                                                                         lname=controller.acct_info[3]))
        self.label_name.pack(fill=tk.BOTH, pady=5)

        # create back button to return to account options page
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(fill=tk.BOTH, padx=5, pady=5)

        self.button_back = tk.Button(master=self.button_frame, text="Back",
                                     command=lambda: controller.create_frame(MemberScene, parent))
        self.button_back.pack(side=tk.RIGHT, padx=10, ipadx=10)

# create exit scene frame
class ExitScene(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label_heading = tk.Label(self, text="Thank You For Using", font=("Verdana", 16, "bold"))
        self.label_heading.pack(padx=5, pady=5)

        self.label_heading = tk.Label(self, text="Codey Bank Portal", font=("Verdana", 16, "bold"))
        self.label_heading.pack(padx=5, pady=5)

        # create exit button to destroy GUI application
        self.button_EXIT = tk.Button(master=self, text="EXIT",
                                     command=controller.destroy)
        self.button_EXIT.pack()
