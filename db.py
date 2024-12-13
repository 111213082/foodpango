#!/usr/local/bin/python
# Connect to MariaDB Platform
import mysql.connector #mariadb

try:
    #連線DB
    conn = mysql.connector.connect(
        user="root",
        password="",
        host="localhost",
        port=3306,
        database="bidonline"
    )
    #建立執行SQL指令用之cursor, 設定傳回dictionary型態的查詢結果 [{'欄位名':值, ...}, ...]
    cursor=conn.cursor(dictionary=True)
except mysql.connector.Error as e: # mariadb.Error as e:
    print(e)
    print("Error connecting to DB")
    exit(1)

#使用者
def verify_user(uname, pwd):
    sql = "SELECT * FROM user WHERE uname = %s AND password = %s"
    cursor.execute(sql, (uname, pwd))
    return cursor.fetchone()  # 如果找到用戶，返回用戶資料；否則返回 None

#個人拍賣品清單
def getListSB(uID):
    sql="select pID,pname,description,baseprice from product where uID=%s;"
    param=(uID,)
    cursor.execute(sql,param)
    return cursor.fetchall()

#所有拍賣品清單
def getListBL():
    sql="select pID,pname,highest from product ;"
    #param=('值',...)
    cursor.execute(sql,)
    return cursor.fetchall()

#商品詳細內容
def getListP(pID):
    sql="""
    SELECT product.pID, product.pname, product.description, product.baseprice, product.highest, user.uname
    FROM product 
    JOIN user  ON product.uID = user.uID
    WHERE product.pID = %s;
    """
    cursor.execute(sql,(pID,))
    return cursor.fetchone() #只返回一個商品的詳細資料
    
#新增拍賣品
def add(uID,pname, description, baseprice):
    sql = "INSERT INTO product (uID, pname, description, baseprice, highest) VALUES (%s, %s, %s, %s, %s)"
    param = (uID, pname, description, baseprice, baseprice)
    cursor.execute(sql, param)
    conn.commit() #將變更保存到資料庫
    return

#修改拍賣品
def update(uID,pID, pname, description, baseprice):
    sql = "UPDATE product SET pname = %s, description = %s, baseprice = %s WHERE pID = %s AND uID = %s;"
    param = (pname, description, baseprice, pID,uID)
    cursor.execute(sql, param)
    conn.commit()
    return

    
#刪除拍賣品
def delete(pID):
    sql="delete from product where pID = %s;"
    cursor.execute(sql,(pID,))
    conn.commit()
    return

#出價紀錄
def Bidlog(pID):
    sql="select uname,price,time from bids WHERE pID = %s ORDER BY time DESC;"
    #param=('值',...)
    cursor.execute(sql,(pID,))
    return cursor.fetchall()

#競標
def addBid(pID, price,uname,uID, pname): 
    sql = "INSERT INTO bids (pID, price, uname, time,uID, pname) VALUES (%s, %s, %s, NOW(), %s, %s)"
    cursor.execute(sql, (pID, price, uname,uID, pname))  # 確保這裡替換為當前用戶的名稱
    conn.commit()

    # 更新對應的 product 表中的最高價
    sql_update_highest = "UPDATE product SET highest = %s WHERE pID = %s"
    cursor.execute(sql_update_highest, (price, pID))
    conn.commit()

