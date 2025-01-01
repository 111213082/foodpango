import mysql.connector

# 連接資料庫
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost', # 資料庫主機地址
        user='root',
        password='',  # XAMPP 的默認密碼
        database='foodpangolin'  # 資料庫名稱
    )
    return connection


def get_pending_orders():
    """取得所有待接單的訂單"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT oID, cID, rID, totalPrice, note, address, createdAt FROM `order` WHERE status = '待接單' AND bID IS NULL")
    orders = cursor.fetchall()
    conn.close()
    return orders


def accept_order(oID, bID):
    """更新訂單狀態為已接單，並指定外送員"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE `order`
        SET status = '已接單', bID = %s
        WHERE oID = %s AND status = '待接單' AND bID IS NULL
    """, (bID, oID))
    conn.commit()
    conn.close()


def validate_courier(email, password):
    """驗證外送員的帳號與密碼"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT bID FROM bro WHERE email = %s AND password = %s", (email, password))
    courier = cursor.fetchone()
    conn.close()
    return courier


def get_orders_by_status(bID, status):
    """根據外送員 ID 和訂單狀態取得訂單"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT oID, address, totalPrice, note, deliveryTime FROM `order`
        WHERE status = %s AND bID = %s
    """, (status, bID))
    orders = cursor.fetchall()
    conn.close()
    return orders


def update_order_status_and_time_in_db(oID, bID, status, delivery_time):
    """更新訂單狀態並設置送達時間"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE `order`
        SET status = %s, deliveryTime = %s
        WHERE oID = %s AND bID = %s
    """, (status, delivery_time, oID, bID))
    conn.commit()
    conn.close()



def update_order_status_in_db(oID, bID, status):
    """更新訂單狀態"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE `order`
        SET status = %s
        WHERE oID = %s AND bID = %s
    """, (status, oID, bID))
    conn.commit()
    conn.close()


def get_ratings_for_courier(bID, star_filter=None):
    """取得外送員的評價列表，根據星級篩選"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT s.sID, s.oID, s.rateB, s.commentB
        FROM star AS s
        JOIN `order` AS o ON s.oID = o.oID
        WHERE o.bID = %s
    """
    params = [bID]
    if star_filter:
        query += " AND s.rateB = %s"
        params.append(star_filter)

    cursor.execute(query, tuple(params))
    ratings = cursor.fetchall()
    conn.close()
    return ratings


def get_average_rating(bID):
    """計算外送員評價的平均分數"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT AVG(rateB) AS avg_rating
        FROM star AS s
        JOIN `order` AS o ON s.oID = o.oID
        WHERE o.bID = %s
    """, (bID,))
    avg_rating = cursor.fetchone()['avg_rating']
    conn.close()
    return avg_rating


def get_order_details(oID):
    """取得指定訂單的詳細資訊"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT o.oID, o.totalPrice, o.address, o.note, o.createdAt
        FROM `order` AS o
        WHERE o.oID = %s
    """, (oID,))
    order = cursor.fetchone()
    conn.close()
    return order

