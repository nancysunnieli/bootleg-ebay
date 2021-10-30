"""Insert the initial mock data into database
"""

import csv

from users_functions import insert_many

def load_data_into_db(data_path):
    with open(data_path) as f:
        rows = list(csv.reader(f))

    insert_many(rows)



if __name__ == '__main__':
    load_data_into_db("users.csv")
