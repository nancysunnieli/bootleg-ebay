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
        database="users",
        # user=input("Enter username: "),
        # password=getpass("Enter password: "),
    ) as connection:
        select_movies_query = "SELECT * FROM users LIMIT 5"
        with connection.cursor() as cursor:
            cursor.execute(select_movies_query)
            result = cursor.fetchall()

        import pdb; pdb.set_trace()
            # for row in result:
            #     print(row)
        print(connection)
except Error as e:
    print(e)