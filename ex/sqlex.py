import mysql.connector

# MySQL 데이터베이스에 연결합니다.
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='yks2693',
            database='mypython'
        )
        print("MySQL 데이터베이스에 연결되었습니다.")
        return connection

    except mysql.connector.Error as error:
        print("Error while connecting to MySQL:", error)
        return None

# 데이터를 삽입하는 함수
def insert_data(content):
    # MySQL 데이터베이스 연결
    connection = connect_to_database()
    try:
        # 데이터베이스 커서를 생성합니다.
        cursor = connection.cursor()

        # INSERT 쿼리문을 작성합니다.
        sql = "INSERT INTO test (idx,content) VALUES (%s,%s)"

        # 쿼리를 실행합니다.
        cursor.execute(sql,( 0,content))

        # 데이터베이스에 변경사항을 반영합니다.
        connection.commit()

        print("데이터가 성공적으로 삽입되었습니다.")

    except mysql.connector.Error as error:
        print("Error while inserting data into MySQL:", error)
    finally:
        # 연결을 닫습니다.
        connection.close()