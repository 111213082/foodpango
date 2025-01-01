import mysql.connector
from datetime import datetime
from functools import wraps
from flask import session, redirect
from mysql.connector import Error


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

def get_restaurants():
    try:
        query = "SELECT rID, name FROM restaurant"
        cursor.execute(query)
        return cursor.fetchall()
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
    conn = None
    cursor = None
    try:
        # 確保 rateR 和 rateB 是有效的評分（1-5）
        try:
            rateR = int(rateR)
            rateB = int(rateB)
        except ValueError:
            print("評分必須是數字")
            return False

        # 確保評分範圍是 1 到 5
        if not (1 <= rateR <= 5) or not (1 <= rateB <= 5):
            print("無效的評分，請選擇 1 到 5 之間的數字")
            return False
        
        # 資料庫連接
        conn = mysql.connector.connect(
            host='localhost',
            database='foodpango',  # 確保你的資料庫名稱正確
            user='root',  # 填寫你的資料庫使用者名稱
            password='password'  # 填寫你的資料庫密碼
        )

        if conn.is_connected():
            cursor = conn.cursor()
            sql = "INSERT INTO star (oID, rateR, rateB, commentR, commentB) VALUES (%s, %s, %s, %s, %s)"
            val = (oID, rateR, rateB, commentR, commentB)
            cursor.execute(sql, val)
            conn.commit()  # 提交資料

            print(f"成功插入評價資料：{val}")  # 確認資料已成功插入
            return True
        else:
            print("無法連接到資料庫")
            return False

    except mysql.connector.Error as e:
        print(f"插入資料錯誤: {e}")
        return False
    finally:
        # 確保資料庫連線與游標被關閉
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()








# 插入訂單
def insert_order(cID, total_price, note, delivery_address, rID):
    try:
        query = """
        INSERT INTO `order` (cID, totalPrice, note, address, rID, createdAt)
        VALUES (%s, %s, %s, %s, %s, NOW())
        """
        cursor.execute(query, (cID, total_price, note, delivery_address, rID))
        conn.commit()
        return cursor.lastrowid  # 返回插入的訂單 ID
    except mysql.connector.Error as err:
        conn.rollback()
        print(f"資料庫錯誤: {err}")
        return None

# 插入訂單項目
def insert_order_item(oID, item_id, quantity, price):
    try:
        query = """
        INSERT INTO detail (oID, fID, quantity, price)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (oID, item_id, quantity, price))
        conn.commit()  # 確保提交事務
    except mysql.connector.Error as err:
        conn.rollback()  # 若發生錯誤，回滾事務
        print(f"資料庫錯誤: {err}")






# 根據食物ID獲取餐廳ID
def get_rid_by_item(item_id):
    try:
        query = """
        SELECT rID 
        FROM food 
        WHERE fID = %s
        """
        cursor.execute(query, (item_id,))
        result = cursor.fetchone()
        
        if result is None:
            print(f"未找到對應的 rID，請確認 fID: {item_id} 是否存在")
            return None
        
        if 'rID' in result:
            return result['rID']
        else:
            print(f"查詢結果沒有 'rID' 欄位，查詢結果: {result}")
            return None
    except mysql.connector.Error as err:
        print(f"資料庫錯誤: {err}")
        return None


def get_order():
    cursor = conn.cursor()
    query = "SELECT * FROM `order` LIMIT 1"  # 假設你的資料表叫 'orders'
    cursor.execute(query)
    result = cursor.fetchone()  # 取得第一筆資料
    return result

# 直接使用全局的 conn 物件
def get_order_details(order_id):
    cursor = conn.cursor(dictionary=True)
    
    # 查詢訂單基本資訊
    cursor.execute("SELECT * FROM `order` WHERE oID = %s", (order_id,))
    order = cursor.fetchone()

    if order:
        # 查詢該訂單的商品資訊
        cursor.execute("SELECT * FROM detail WHERE oID = %s", (order_id,))
        items = cursor.fetchall()
        
        # 把商品資料添加到訂單資料中
        order['items'] = items
    
    cursor.close()
    
    return order

# 用來處理訂單時，進行適當的處理邏輯
def create_order(data):
    try:
        # 驗證數據
        total_price = data.get('totalPrice')
        note = data.get('note', '')
        address = data.get('address')
        items = data.get('items', [])
        cID = data.get('cID')  # 客戶 ID
        
        if not address:
            return {'status': 'error', 'message': '請填寫送餐地址'}

        if not isinstance(items, list) or not items:
            return {'status': 'error', 'message': '訂單項目無效'}

        # 確認所有商品來自同一家餐廳
        first_rID = get_rid_by_item(items[0].get('item_id'))
        for item in items:
            rID = get_rid_by_item(item.get('item_id'))
            if rID != first_rID:
                return {'status': 'error', 'message': '訂單只能包含同一家店的商品'}

        # 插入訂單，取得新訂單的 ID
        order_id = insert_order(cID, total_price, note, address, first_rID)
        if not order_id:
            return {'status': 'error', 'message': '訂單創建失敗'}

        # 插入訂單項目
        for item in items:
            item_id = item.get('item_id')
            quantity = item.get('quantity', 0)
            price = item.get('price', 0.0)

            if not item_id or quantity <= 0 or price <= 0.0:
                return {'status': 'error', 'message': '訂單項目數據無效'}

            insert_order_item(order_id, item_id, quantity, price, first_rID)

        return {'status': 'success', 'order_id': order_id}
    except Exception as e:
        print(f"錯誤: {e}")
        return {'status': 'error', 'message': '系統錯誤'}
    
    
    
    
    
# 查詢訂單狀態
def get_order_status(oID):
    try:
        query = "SELECT status FROM `order` WHERE oID = %s"
        cursor.execute(query, (oID,))
        result = cursor.fetchone()
        if result:
            return result['status']
        else:
            return None  # 沒找到訂單
    except mysql.connector.Error as e:
        print(f"查詢錯誤: {e}")
        return None  # 返回 None 或您希望返回的錯誤處理值

