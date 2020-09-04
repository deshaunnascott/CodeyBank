# Author: ShaunCodes
# Date:   September 4, 2020

import sqlite3

class Database:
    DB_LOCATION = './Database/acct_db.sqlite'

    def __init__(self):
        """Initialize db class variables"""
        self.connection = sqlite3.connect(Database.DB_LOCATION)
        self.cur = self.connection.cursor()

    def close(self):
        """Close database connection"""
        self.connection.close()

    # create account table
    def create_table(self, tablename):
        create_acct_table = """
        CREATE TABLE IF NOT EXISTS {name} (
          pin INTEGER PRIMARY KEY AUTOINCREMENT,
          id INTEGER,
          first_name TEXT NOT NULL,
          last_name TEXT NOT NULL,
          balance FLOAT
        );""".format(name=tablename)

        # execute query
        self.cur.execute(create_acct_table)
        # commit changes
        self.connection.commit()

    def add_new_acct(self, table_name, acct_pin, member_id, mem_first_name, mem_last_name, mem_balance):
        insert_query = """
        INSERT INTO
          {name} (pin, id, first_name, last_name, balance)
        VALUES
          ({pin}, {id}, {firstName}, {lastName}, {balance})
        """.format(name=table_name, pin=acct_pin, id=member_id, firstName=mem_first_name, lastName=mem_last_name,
                   balance=mem_balance)

        # execute query
        self.cur.execute(insert_query)
        # commit changes
        self.connection.commit()

    def update_balance(self, table_name, mem_id, mem_balance):
        update_query = """
        UPDATE
          {name}
        SET
          balance = {acct_balance}
        WHERE
          id = {acct_id}
        """.format(name=table_name, acct_balance=mem_balance, acct_id=mem_id)

        # execute query
        self.cur.execute(update_query)

        # commit changes
        self.connection.commit()
