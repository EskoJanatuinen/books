import isbnlib
import sqlite3
import pandas as pd

# To get ANSI colors in Windows:
# import os
# os.system("color")


def scanning():
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
        # Query
        cur.execute(
            "SELECT SUM(vapaasaldo) FROM data WHERE kuvaus=? GROUP BY kuvaus",
            (isbn13,),
        )
        result = cur.fetchall()
        # First copy of the book -> needs a product photo
        if len(result) == 0:
            print("\n" + "\033[1;30;43m" + " -> KUVATTAVAKSI " + " \033[0;0m")
        # Product photo exists
        else:
            # Inventory balance 0-2 -> online store
            if result[0][0] < 3:
                print(
                    "\n"
                    + "\033[1;30;43m"
                    + " -> TUOTESYÖTTÖÖN, Saldo = "
                    + str(result[0][0])
                    + " \033[0;0m"
                )
            # Inventory balance > 2 -> physical store
            else:
                print(
                    "\n"
                    + "\033[1;30;43m"
                    + " -> MYYMÄLÄÄN, Saldo = "
                    + str(result[0][0])
                    + " \033[0;0m"
                )

        cur.execute(
            "SELECT hinta, SUM(myyty) FROM data WHERE kuvaus=? GROUP BY hinta ORDER BY hinta DESC",
            (isbn13,),
        )
        res = cur.fetchall()

        df = pd.DataFrame()
        for row in res:
            dict = {"hinta": row[0], "myyty": row[1]}
            df = df.append(dict, ignore_index=True)
            df["myyty"] = df["myyty"].astype(int)
        if len(df) > 0:
            print(df.to_string(index=False))

    cur.close()
    con.close()
