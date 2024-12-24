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


def add_user(role, name, email, password):
    """新增使用者至對應資料表"""
    table_map = {
        'customer': 'customer',
        'restaurant': 'restaurant',
        'bro': 'bro',
        'staff': 'staff'
    }
    table_name = table_map.get(role)
    if not table_name:
        raise ValueError("無效的角色")

    hashed_password = generate_password_hash(password)  # 加密密碼
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = f"INSERT INTO {table_name} (name, email, password) VALUES (%s, %s, %s)"
    cursor.execute(sql, (name, email, hashed_password))
    conn.commit()
    conn.close()

def get_user_by_email(role, email):
    """根據電子郵件取得使用者資訊"""
    table_map = {
        'customer': 'customer',
        'restaurant': 'restaurant',
        'bro': 'bro',
        'staff': 'staff'
    }
    table_name = table_map.get(role)
    if not table_name:
        raise ValueError("無效的角色")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql = f"SELECT * FROM {table_name} WHERE email = %s"
    cursor.execute(sql, (email,))
    user = cursor.fetchone()
    conn.close()
    return user


#抓所有訂單
def get_all_orders():
    sql = """
    SELECT o.oID, c.name AS customer_name, r.name AS restaurant_name, o.address, o.note, o.status, o.bID
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

