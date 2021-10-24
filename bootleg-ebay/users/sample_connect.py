# from mysql.connector import connect, Error

# try:
#     with connect(
#         host="localhost:3306",
#         user="%s" % ("root"),
#         password="%s" % ("bootleg"),
#         # user=input("Enter username: "),
#         # password=getpass("Enter password: "),
#     ) as connection:
#         print(connection)
# except Error as e:
#     print(e)

from getpass import getpass
from mysql.connector import connect, Error

try:
    with connect(
        # host="mysql:8://db",
        # host="mysql",
        host="users-db",
        port="3306",
        user="%s" % ("root"),
        password="%s" % ("bootleg"),
        # user=input("Enter username: "),
        # password=getpass("Enter password: "),
    ) as connection:
        print(connection)
except Error as e:
    print(e)