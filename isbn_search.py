import isbnlib
import sqlite3
import pandas as pd

# To get ANSI colors in Windows:
# import os
# os.system("color")


def print_yellow_background(string):
    """Prints string with a yellow background"""
    bg_yellow = "\033[1;30;43m"
    bg_reset = " \033[0;0m"
    print("\n" + bg_yellow + string + bg_reset)


def scanning():
    """returns inventory balance and sales history for given ISBN"""
    con = sqlite3.connect("book.db")
    cur = con.cursor()

    while True:
        input_isbn = str(input("\nLue ISBN:  "))
        if input_isbn == "":
            print("\n  Quitting\n")
            break

        # Validation
        isbn13 = isbnlib.to_isbn13(input_isbn)  # Convert to isbn13 if isbn10
        if not isbnlib.is_isbn13(isbn13):
            print("\n  Ei ole ISBN")
            continue

        # INVENTORY BALANCE:
        # SQL query returns inventory balance for the book
        cur.execute(
            "SELECT SUM(vapaasaldo) FROM data WHERE kuvaus=? GROUP BY kuvaus",
            (isbn13,),
        )
        result_inventory_balance = cur.fetchall()
        # fetchall() returns a list containing a tuple, for example [(3,)]

        # First copy of the book -> needs a product photo
        if len(result_inventory_balance) == 0:
            print_yellow_background(" -> KUVATTAVAKSI ")
            continue

        # Product photo exists:
        inventory_balance = result_inventory_balance[0][0]
        # Inventory balance 0-2 -> online store
        if inventory_balance < 3:
            print_yellow_background(
                " -> TUOTESYÖTTÖÖN, Saldo = " + str(inventory_balance)
            )

        # Inventory balance > 2 -> physical store
        else:
            print_yellow_background(" -> MYYMÄLÄÄN, Saldo = " + str(inventory_balance))

        # SALES HISTORY:
        # SQL query returns sales history for the book grouped by sales prices
        cur.execute(
            "SELECT hinta, SUM(myyty) FROM data WHERE kuvaus=? GROUP BY hinta ORDER BY hinta DESC",
            (isbn13,),
        )
        result_sales_history = cur.fetchall()
        # fetchall() returns a list containing tuples
        # For example [(10.0, 1), (8.0, 2), (6.0, 5)]
        # First value of a tuple is price and second value is number of sales

        # Format sales history for printing
        df = pd.DataFrame()
        for value in result_sales_history:
            dict = {"hinta": value[0], "myyty": value[1]}
            df = df.append(dict, ignore_index=True)
            df["myyty"] = df["myyty"].astype(int)
        if len(df) > 0:
            print(df.to_string(index=False))

    cur.close()
    con.close()
