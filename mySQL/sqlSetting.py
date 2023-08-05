import mysql.connector

mydb = mysql.connector.connect(
    host="13.209.64.243"
    , user="root"
    , password="1234"
    , database="aws"
)
cursor = mydb.cursor()
cursor.execute()
result = cursor.fetchall()
for row in result:
    print(row)
cursor.close()
mydb.close()
