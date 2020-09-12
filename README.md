# CodeyBank
Personal project to practice database and GUI development with Python. This project is developed with the 
Tkinter framework and Sqlite3 Database.
 
This project is intended to mock the basic operations of a bank account owner.

## Table of Contents
* [Current Features](#Current_Features)
* [Resources](#Resources)
* [Setup](#LocalStep)
* [Extra Information](#Extra_Information)
* [Possible Future Developments](#Possible_Future_Dev)

## Current_Features
    * Withdrawal
    * Deposit
    * View Account Details
    * Account Creation

These are the basic features I started with. I want to add more account features in the future
such as Amount Transfer between account existing in the database

## Resources

    random
    tkinter
    sqlite

## LocalStep
1) Navigate to your local CodeyBank project folder

2) Create a folder named `Database` at the top level of your CodeyBank project folder

3) Run Main Driver File

		python CBPortal.py

## Extra_Information
Something to note about these accounts is that they currently allow for the user to overdraw their account.
So it is possible for an account to have a negative balance.

## Possible_Future_Dev
* Add new account features (i.e. Amount Transfer)
* Add a sample database
* Create a CodeyBank Manager Portal for access to total bank database