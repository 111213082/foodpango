import mysql.connector
from datetime import datetime
from functools import wraps
from flask import session, redirect


# 建立全局資料庫連接和游標
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
    print(f"資料庫錯誤: {e}")
    exit(1)

# 裝飾器函數，用於檢查登入狀態和角色權限
def login_required(role=None):  # 默認為 None，若需要特定角色則傳遞
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            email = session.get('email')
            user_role = session.get('user_role')
            if not email:
                return redirect('/loginpage')  # 若未登入，跳轉至登入頁面
            if role and user_role != role:  # 檢查角色
                return "您沒有權限訪問該頁面", 403  # 若角色不符，返回權限錯誤
            return f(*args, **kwargs)  # 符合條件則執行原始函數
        return decorator
    return decorator




def validate_user(email, password, role):
    # 檢查角色是否有效，避免 SQL 注入攻擊
    valid_roles = ['customer', 'restaurant', 'bro']
    if role not in valid_roles:
        return None  # 如果角色無效，返回 None

    # 根據角色選擇資料表
    table = role  # 角色名與資料表名相同

    # 明確指定查詢欄位，不查詢不存在的 role 欄位
    sql = f"SELECT cID, email, password FROM {table} WHERE email = %s AND password = PASSWORD(%s)"
    
    cursor.execute(sql, (email, password))
    user = cursor.fetchone()

    if user:
        return {
            'email': user['email'],
            'cID': user['cID'],  # 確保返回 cID
            'role': role  # 返回傳入的角色
        }
    return None


def get_customer_data(email):
    cursor.execute("SELECT * FROM customer WHERE email = %s", (email,))
    return cursor.fetchone()

def update_customer_data(email, name, phone, address, card):
    try:
        # 使用 MySQL 進行資料庫操作
        query = '''
            UPDATE customer
            SET name = %s, phone = %s, address = %s, card = %s
            WHERE email = %s
        '''
        cursor.execute(query, (name, phone, address, card, email))  # 執行更新操作
        conn.commit()  # 提交更改
        return True
    except mysql.connector.Error as e:
        print(f"資料更新失敗: {e}")
        conn.rollback()  # 發生錯誤時回滾變更
        return False




# 獲取單筆訂單的函數
def get_order():
    # 查詢最新的訂單，根據 createdAt 排序
    query = "SELECT * FROM order ORDER BY createdAt DESC LIMIT 1"
    cursor.execute(query)
    result = cursor.fetchone()  # 取得最新的訂單資料
    return result


def create_order(cID, rID, totalPrice, note, address):
    """新增訂單"""
    try:
        query = """
        INSERT INTO `order` (cID, rID, totalPrice, note, address, createdAt)
        VALUES (%s, %s, %s, %s, %s, NOW())
        """
        cursor.execute(query, (cID, rID, totalPrice, note, address))
        conn.commit()
        return cursor.lastrowid  # 回傳新增的 oID
    except Exception as e:
        print(f"新增訂單失敗: {e}")
        conn.rollback()
        return None


def add_order_detail(oID, fID, quantity, price):
    """新增訂單明細"""
    try:
        query = """
        INSERT INTO detail (oID, fID, quantity, price)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (oID, fID, quantity, price))
        conn.commit()
        return True
    except Exception as e:
        print(f"新增訂單明細失敗: {e}")
        conn.rollback()
        return False




# 獲取所有餐廳資料的函數
def get_restaurants():
    try:
        query = "SELECT rID, name FROM restaurant"  # 查詢餐廳的 ID 與名稱
        cursor.execute(query)
        return cursor.fetchall()  # 返回所有結果
    except mysql.connector.Error as err:
        print(f"資料庫錯誤: {err}")
        return []

# 根據餐廳 ID 獲取餐廳資料的函數
def get_restaurant_by_id(shop_id):
    try:
        query = "SELECT * FROM restaurant WHERE rID = %s"  # 查詢特定餐廳資料
        cursor.execute(query, (shop_id,))
        return cursor.fetchone()  # 返回單筆結果
    except mysql.connector.Error as err:
        print(f"資料庫錯誤: {err}")
        return None

# 獲取所有可用食物資料的函數
def get_foods():
    try:
        query = """
        SELECT food.fID, food.name, food.price, restaurant.name AS shopName
        FROM food
        JOIN restaurant ON food.rID = restaurant.rID
        WHERE food.is_available = 1
        """
        cursor.execute(query)
        return cursor.fetchall()  # 返回所有結果
    except mysql.connector.Error as err:
        print(f"資料庫錯誤: {err}")
        return []

# 根據食物 ID 獲取特定食物資料的函數
def get_food_by_id(food_id):
    try:
        query = "SELECT * FROM food WHERE fID = %s"  # 查詢特定食物資料
        cursor.execute(query, (food_id,))
        return cursor.fetchone()  # 返回單筆結果
    except mysql.connector.Error as err:
        print(f"資料庫錯誤: {err}")
        return None

# 根據餐廳 ID 列表獲取食物資料的函數
def get_foods_by_shop_ids(shop_ids):
    if not shop_ids:
        query = """
        SELECT food.fID, food.name, food.price, restaurant.name AS shopName
        FROM food
        JOIN restaurant ON food.rID = restaurant.rID
        """
        params = ()
    else:
        placeholders = ','.join(['%s'] * len(shop_ids))  # 動態生成查詢條件
        query = f"""
        SELECT food.fID, food.name, food.price, restaurant.name AS shopName
        FROM food
        JOIN restaurant ON food.rID = restaurant.rID
        WHERE food.rID IN ({placeholders})
        """
        params = tuple(shop_ids)
    try:
        cursor.execute(query, params)
        foods = cursor.fetchall()
        return foods if foods else []
    except mysql.connector.Error as err:
        print(f"資料庫錯誤: {err}")
        return []



# 儲存評價資料
def save_review(oID, rateR, rateB, commentR, commentB):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        sql = "INSERT INTO star (oID, rateR, rateB, commentR, commentB) VALUES (%s, %s, %s, %s, %s)"
        val = (oID, rateR, rateB, commentR, commentB)
        try:
            cursor.execute(sql, val)
            conn.commit()
            print("評價資料已成功儲存")
        except Error as e:
            print(f"插入資料錯誤: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("無法連接資料庫，無法儲存資料")

