# Author: ShaunCodes
# Date:   September 4, 2020

# database library for account database
import sqlite3

class Database:
    DB_LOCATION = './Database/acct_db.sqlite'

    def __init__(self):
        """Initialize db class variables"""
        self.connection = sqlite3.connect(Database.DB_LOCATION)
        self.cur = self.connection.cursor()
        self.table = 'Accounts'
        self.create_table(self.table)

    def close(self):
        """Close database connection"""
        self.connection.close()

    # create account table
    def create_table(self, tablename):
        create_acct_table = """
        CREATE TABLE IF NOT EXISTS {name} (
          pin INTEGER,
          id INTEGER  PRIMARY KEY,
          first_name TEXT NOT NULL,
          last_name TEXT NOT NULL,
          balance FLOAT
        );""".format(name=tablename)

        # execute query
        self.cur.execute(create_acct_table)
        # commit changes
        self.connection.commit()

    def add_new_acct(self, table_name, acctObj):
        insert_query = """
        INSERT INTO
          {name} (pin, id, first_name, last_name, balance)
        VALUES
          ({pin}, {id}, '{firstName}', '{lastName}', {balance});
        """.format(name=table_name, pin=acctObj.acct_pin, id=acctObj.member_id, firstName=acctObj.mem_first_name,
                   lastName=acctObj.mem_last_name, balance=acctObj.mem_balance)

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
          id = {acct_id};
        """.format(name=table_name, acct_balance=mem_balance, acct_id=mem_id)

        # execute query
        self.cur.execute(update_query)

        # commit changes
        self.connection.commit()

    def member_exists(self, table_name, pin_info, id_info):
        select_query = """SELECT * FROM {table} 
        WHERE pin = {pin}
        AND id = {id};""".format(table=table_name, pin=pin_info, id=id_info)

        # execute query
        self.cur.execute(select_query)

        # get data from database
        data = self.cur.fetchone()

        if not data:
            return False  # data for member not found
        else:
            return True  # data found

    def in_database(self, table_name, table_column, get_info):
        data = self.get_acct_info(table_name, table_column, get_info)

        if not data:
            return False  # data for pin not found
        else:
            return True  # data found

    def get_acct_info(self, table_name, table_column, get_info):
        select_query = """SELECT * FROM {table} WHERE {column} = {info};""".format(table=table_name,
                                                                                   column=table_column, info=get_info)
        # execute query
        self.cur.execute(select_query)

        # get data from database
        data = self.cur.fetchone()

        return data
