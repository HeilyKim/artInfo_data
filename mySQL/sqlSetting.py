import mysql.connector

mydb = mysql.connector.connect(
    host="192.168.0.10",
    user="art",
    password="1234",
    database="art"
)

cursor = mydb.cursor()
exhibitions = ("""
CREATE TABLE exhibitions (exhibition_idx INT AUTO_INCREMENT PRIMARY KEY
,exhibition_title VARCHAR(50) NOT NULL
,exhibition_registDate DATETIME NOT NULL
,exhibition_start DATE NOT NULL,exhibition_end DATE NOT NULL
,exhibition_status VARCHAR(7) NOT NULL
,exhibition_region VARCHAR(7) NOT NULL
,exhibition_location VARCHAR(10) NOT NULL
,exhibition_file VARCHAR(50)
,exhibition_contents VARCHAR(500) NOT NULL,exhibition_url VARCHAR(200)
,exhibition_category VARCHAR(3) NOT NULL
,CONSTRAINT CHECK (exhibition_category IN ('개인전', '단체전')))
""")
cursor.execute(exhibitions)
exhibitions_trigger = ("""
DELIMITER //
CREATE TRIGGER set_exhibition_status
BEFORE INSERT ON exhibitions
FOR EACH ROW
BEGIN
    DECLARE current_datetime DATETIME;
    SET current_datetime = NOW();

    IF current_datetime < NEW.exhibition_start THEN
        SET NEW.exhibition_status = '예정';
    ELSEIF current_datetime > NEW.exhibition_end THEN
        SET NEW.exhibition_status = '종료';
    ELSE
        SET NEW.exhibition_status = '진행';
    END IF;
END //
DELIMITER ;
""")
cursor.execute(exhibitions_trigger)
mydb.commit()
cursor.close()
mydb.close()
