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

    if not user:  # 如果未找到任何資料
        return None

    # 根據角色確定 ID 欄位名稱
    id_field = {
        'customer': 'cID',
        'restaurant': 'rID',
        'bro': 'bID',
    }.get(role, 'id')  # 預設為 'id'

    return {
        'id': user.get(id_field),  # 使用 `get` 避免 KeyError
        'email': user.get('email'),
        'role': role
    }

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

#查詢是否營業
def get_is_active(rID):
    sql = "SELECT is_active FROM restaurant WHERE rID = %s"
    cursor.execute(sql, (rID,))
    result = cursor.fetchone()
    return result['is_active'] if result else None

#更新是否營業
def update_is_active(is_active, rID):
    sql = "UPDATE restaurant SET is_active = %s WHERE rID = %s"
    cursor.execute(sql, (is_active, rID))
    conn.commit()

# 菜單
def menu_food(rID):
    sql = """
    SELECT food.fID, food.name, food.description, food.price, food.is_vegetarian, categories.name AS category_name
    FROM food
    INNER JOIN categories ON food.ID = categories.ID
    WHERE food.rID = %s
    ORDER BY categories.name
    """
    param = (rID,)
    cursor.execute(sql, param)
    foods = cursor.fetchall()

    categorized_food = {}
    for food in foods:
        food['is_vegetarian'] = '素' if food['is_vegetarian'] == 1 else '葷'
        category = food['category_name']
        if category not in categorized_food:
            categorized_food[category] = []
        categorized_food[category].append(food)

    return categorized_food


#類別
def get_categories_by_restaurant(rID):
    sql = "SELECT ID, name FROM categories WHERE rID = %s"
    param = (rID,)
    cursor.execute(sql, param)
    categories = cursor.fetchall()  # 獲取所有符合條件的資料
    return categories

#新增餐點
def add(rID, name, description, price, category_id, is_vegetarian):
    sql = """
        INSERT INTO food (rID, name, description, price, ID, is_vegetarian)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    param = (rID, name, description, price, category_id, is_vegetarian)
    cursor.execute(sql, param)
    conn.commit()


#修改餐點
def edit_food(fID, name, description, price, category_id, is_vegetarian):
    sql = """
    UPDATE food 
    SET name = %s, description = %s, price = %s, ID = %s, is_vegetarian = %s
    WHERE fID = %s
    """
    param = (name, description, price, category_id, is_vegetarian, fID)
    cursor.execute(sql, param)
    conn.commit()

#刪除餐點
def delete_food(fID):
    sql = "DELETE FROM food WHERE fID = %s"
    param = (fID,)
    cursor.execute(sql, param)
    conn.commit()

#獲得餐點資料
def get_food(fID):
    sql = "SELECT fID, name, description, price, ID,is_vegetarian  FROM food WHERE fID = %s"
    param = (fID,)
    cursor.execute(sql, param)
    return cursor.fetchone() 

#訂單列表
def get_orders_by_status(rID, status):
    sql = """
    SELECT 
        `order`.oID,
        `order`.cID,
        `order`.totalPrice,
        `order`.note AS description,
        GROUP_CONCAT(CONCAT(food.name, ' * ', detail.quantity) SEPARATOR ', ') AS food_list
    FROM `order`
    INNER JOIN detail ON `order`.oID = detail.oID
    INNER JOIN food ON detail.fID = food.fID
    WHERE `order`.rID = %s AND `order`.status = %s
    GROUP BY `order`.oID, `order`.cID, `order`.totalPrice, `order`.note
    """
    param = ((rID, status))
    cursor.execute(sql, param)
    return cursor.fetchall()

#確認接單
def acceptFood(oID, prepareTime):
    sql = "UPDATE `order` SET status = '店家已接單', prepareTime = %s WHERE oID = %s"
    param = (prepareTime, oID)
    cursor.execute(sql, param)
    conn.commit()

#我的資料
def about_me(rID):
    sql = "SELECT name,email,phone,address,bank,time FROM restaurant WHERE rID = %s"
    param = (rID,)
    cursor.execute(sql, param)
    return cursor.fetchone() 

#修改我的資料
def edit_me(name,email,phone,address,bank,time,rID):
    sql = """
    UPDATE restaurant 
    SET name = %s, email = %s, phone = %s, address = %s, bank = %s, time = %s
    WHERE rID = %s
    """
    param = (name,email,phone,address,bank,time,rID)
    cursor.execute(sql, param)
    conn.commit()

#我的評價
def star(rID):
    sql = """
    SELECT sID, rateR, commentR
    FROM star 
    INNER JOIN `order` ON `order`.oID = star.oID
    WHERE `order`.rID = %s
    """
    param = (rID,)
    cursor.execute(sql, param)
    return cursor.fetchall()
