import mysql.connector  # 使用 MySQL 進行資料庫操作

# 連接資料庫
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost', # 資料庫主機地址
        user='root',
        password='',  # XAMPP 的默認密碼
        database='foodpangolin'  # 資料庫名稱
    )
    return connection


#抓所有訂單
def get_all_orders():
    sql = """
    SELECT o.oID, c.name AS customer_name, r.name AS restaurant_name, o.address, o.note, o.status
    FROM `order` o
    JOIN customer c ON o.cID = c.cID
    JOIN restaurant r ON o.rID = r.rID
    ORDER BY FIELD(o.status, '待接單', '已接單'), o.createdAt
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        return cursor.fetchall()  # 返回所有訂單資料
    finally:
        conn.close()


#接單(待--->已)
def accept_order(oID, bID):
    sql = """
    UPDATE `order`
    SET status = '已接單', bID = %s
    WHERE oID = %s AND status = '待接單'
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        affected_rows = cursor.execute(sql, (bID, oID))
        conn.commit()
        return affected_rows > 0  # 是否成功更新
    finally:
        conn.close()

