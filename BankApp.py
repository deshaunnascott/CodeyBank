# Author: ShaunCodes
# Date:   September 4, 2020

import tkinter as tk
from BankDatabase import Database

class BankApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        # create GUI window
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("CodeyBank Portal")

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
        """
        for F in (StartScene, MemberScene, CreateScene):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartScene)
        """
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def create_frame(self, scene, container):
        frame = scene(container, self)

        self.frames[scene] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(scene)

# create start scene frame
class StartScene(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label_heading = tk.Label(self, text="Codey Bank Portal", font=("Verdana", 16, "bold"))
        self.label_heading.pack(padx=5, pady=5)

        self.info_frame = tk.Frame(self)
        self.label_entry = tk.Label(master=self.info_frame, text="Enter Account Pin:")
        self.entry_wgt = tk.Entry(master=self.info_frame, width=10)
        self.info_frame.pack(fill=tk.BOTH, padx=10, pady=10)

        # place label name and entry widget into frame
        self.label_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.entry_wgt.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

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
        self. button_create.pack(side=tk.LEFT, padx=10, ipadx=10)

    def clear_entry(self):
        self.entry_wgt.delete(0, 'end')

    def verify_acct(self, parent, controller):
        pin = self.entry_wgt.get().strip()

        # check for pin in account database
        exists = controller.database.in_database(controller.database.table, int(pin))

        # if in database proceed, but if not clear entry
        if exists:
            controller.acct_info = controller.database.get_acct_info(controller.database.table, int(pin))
            controller.create_frame(MemberScene, parent)
            # controller.show_frame(MemberScene)
        else:
            self.clear_entry()

# create member scene frame
class MemberScene(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label_heading = tk.Label(self, text="Account Options", font=("Verdana", 16, "bold"))
        self.label_heading.pack(padx=5, pady=5)

        self.button_withdrawal = tk.Button(self, text="Withdrawal",
                                           command=lambda: controller.create_frame(WithdrawalScene, parent))
        self.button_withdrawal.pack(padx=5, pady=5)

        self.button_deposit = tk.Button(self, text="Deposit",
                                        command=lambda: controller.create_frame(DepositScene, parent))
        self.button_deposit.pack(padx=5, pady=5)

        self.button_acct_balance = tk.Button(self, text="Account Balance",
                                             command=lambda: controller.create_frame(AccountScene, parent))
        self.button_acct_balance.pack(padx=5, pady=5)

        self.label_id = tk.Label(self, text="Acct ID: {id}".format(id=controller.acct_info[1]))
        self.label_id.pack(side=tk.LEFT, padx=5, pady=5)

        self.label_member = tk.Label(self, text="Member: {fname} {lname}".format(fname=controller.acct_info[2],
                                                                                 lname=controller.acct_info[3]))
        self.label_member.pack(side=tk.RIGHT, padx=5, pady=5)

# TODO: Update
# create account creation scene frame
class CreateScene(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Create Page!!!", font=("Verdana", 16, "bold"))
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartScene, parent))
        button1.pack()

        button2 = tk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()

# TODO: Update
# create withdrawal scene frame
class WithdrawalScene(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="WithDrawl Page!!!", font=("Verdana", 16, "bold"))
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartScene))
        button1.pack()

        button2 = tk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()

# TODO: Update
# create deposit scene frame
class DepositScene(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Deposit Page!!!", font=("Verdana", 16, "bold"))
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartScene))
        button1.pack()

        button2 = tk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()

# TODO: Update
# create account scene frame
class AccountScene(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Account Details Page!!!", font=("Verdana", 16, "bold"))
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartScene))
        button1.pack()

        button2 = tk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()

# TODO: Update
# create exit scene frame
class ExitScene(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Exit Page!!!", font=("Verdana", 16, "bold"))
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartScene))
        button1.pack()

        button2 = tk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()
app = BankApp()
app.mainloop()
