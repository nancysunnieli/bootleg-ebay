"""Insert the initial mock data into database
"""

import csv

from payments_functions import PaymentCardsDBManager

def load_data_into_db(data_path):
    with open(data_path) as f:
        rows = list(csv.reader(f))

    for row in rows:
        PaymentCardsDBManager.insert(row)



if __name__ == '__main__':
    load_data_into_db("cards.csv")
