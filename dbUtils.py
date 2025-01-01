import mysql.connector

try:
    conn = mysql.connector.connect(
        user="root",
        password="",
        host="localhost",
        port=3306,
        database="foodpango"
    )
    cursor = conn.cursor(dictionary=True)
except mysql.connector.Error as e:
    print(e)
    print("Error connecting to DB")
    exit(1)


def validate_user(email, password, role):
    # 檢查角色是否有效，避免 SQL 注入攻擊
    valid_roles = ['customer', 'restaurant', 'bro']
    if role not in valid_roles:
        return None  # 如果角色無效，返回 None

    # 根據角色選擇資料表
    table = role  # 角色名與資料表名相同

    # 構造查詢語句
    sql = f"SELECT * FROM {table} WHERE email = %s AND password = PASSWORD(%s)"
    
    # 假設您有一個資料庫連接 cursor
    cursor.execute(sql, (email, password))
    user = cursor.fetchone()

    if user:
        return {
            'email': user['email'],
            'role': role  # 返回角色
        }   
    return None

def register_user(role, **kwargs):
    try:
        if role == 'customer':
            sql = """
                INSERT INTO customer (name, email, password, phone, address, card)
                VALUES (%s, %s, PASSWORD(%s), %s, %s, %s)
            """
            params = (kwargs['name'], kwargs['email'], kwargs['password'], kwargs['phone'], kwargs.get('address'), kwargs.get('card'))
        elif role == 'restaurant':
            sql = """
                INSERT INTO restaurant (name, email, password, phone, address, bank)
                VALUES (%s, %s, PASSWORD(%s), %s, %s, %s)
            """
            params = (kwargs['name'], kwargs['email'], kwargs['password'], kwargs['phone'], kwargs['address'], kwargs['bank'])
        elif role == 'bro':
            sql = """
                INSERT INTO bro (name, email, password, phone, bank)
                VALUES (%s, %s, PASSWORD(%s), %s, %s)
            """
            params = (kwargs['name'], kwargs['email'], kwargs['password'], kwargs['phone'], kwargs['bank'])
        else:
            raise ValueError("Invalid role specified")

        cursor.execute(sql, params)
        conn.commit()
        return True
    except mysql.connector.Error as e:
        print(f"Database Error: {e}")
        return False

