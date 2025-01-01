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
        database="foodpangolin"
    )
    #建立執行SQL指令用之cursor, 設定傳回dictionary型態的查詢結果 [{'欄位名':值, ...}, ...]
    cursor=conn.cursor(dictionary=True)
except mysql.connector.Error as e: # mariadb.Error as e:

    print(e)
    print("Error connecting to DB")
    exit(1)

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
    cursor.execute(sql, (rID, status))
    return cursor.fetchall()

#確認接單
def acceptFood(oID, prepareTime):
    sql = "UPDATE `order` SET status = '已接單', prepareTime = %s WHERE oID = %s"
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
