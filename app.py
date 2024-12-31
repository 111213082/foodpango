<<<<<<< HEAD

from flask import Flask, render_template, request, redirect, url_for, session
from dbUtils import get_db_connection



=======
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import mysql.connector
from config import db_config
from functools import wraps
from dbUtils import get_is_active,update_is_active,menu_food,add,get_categories_by_restaurant,edit_food,delete_food,get_food,orderList,about_me,edit_me,star,orderList,acceptFood
from dbUtils import validate_user#, register_customer,register_restaurant,register_bro
import json
>>>>>>> d3f1586 (商家)

app.secret_key = 'your_secret_key'  # 用於管理 session

@app.route("/")
def m():
	return redirect('/login')

<<<<<<< HEAD


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT bID FROM bro WHERE email = %s AND password = %s", (email, password))
        courier = cursor.fetchone()
        conn.close()

        if courier:
            session['bID'] = courier['bID']
            return redirect(url_for('pending_orders'))
        else:
            error = "登入失敗，請檢查您的帳號與密碼。"
            return render_template('login.html', error=error)

    return render_template('login.html')

   
@app.route('/pending_orders')
=======
#登入驗證裝飾器
def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            email = session.get('email')
            user_role = session.get('user_role')  # 使用 'user_role'
            if not email:
                return redirect('/loginPage.html')
            if role and user_role != role:
                return redirect('/loginPage.html')
            return f(*args, **kwargs)
        return wrapper
    return decorator

#登入
@app.route('/login', methods=['POST'])
def login():
    form = request.form
    email = form['EMAIL']
    pwd = form['PWD']
    role = form['role']
    
    user_data = validate_user(email, pwd, role)
    if user_data:
        session['email'] = user_data['email']
        session['user_role'] = user_data['role']  # 確保這裡存儲的是 'user_role'
        return redirect("/")
    return redirect("/loginPage.html")

#登出
@app.route('/logout')
def logout():
    session.clear()  # 清除所有session
    return redirect('/loginPage.html')

# 路由：首頁
@app.route('/')
def home():
    email = session.get('email')
    if email:
        # 已登入，檢查用戶角色
        user_role = session.get('user_role')  # 提取用戶角色
        if user_role == 'customer':
            return redirect('/customer/dashboard')
        elif user_role == 'restaurant':
            return redirect('/restaurant/dashboard')
        elif user_role == 'bro':
            return redirect('/bro/dashboard')
    else:
        # 未登入，展示公共首頁
        return render_template('index.html')

# 路由：顧客專屬頁面
@app.route('/customer/dashboard')
@login_required(role='customer')
def customer_dashboard():
    return render_template('customer_dashboard.html')

# 路由：餐廳專屬頁面
@app.route('/restaurant/dashboard')
@login_required(role='restaurant')
def restaurant_dashboard():
    return render_template('SellerHome.html')

# 路由：外送員專屬頁面
@app.route('/bro/dashboard')
@login_required(role='bro')
def bro_dashboard():
    return render_template('bro_dashboard.html')

# 渲染待接單頁面
@app.route('/orders/pending', methods=['GET'])
>>>>>>> d3f1586 (商家)
def pending_orders():
    if 'bID' not in session:  # 確認外送員登入
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT oID, cID, rID, totalPrice, note, address, createdAt FROM `order` WHERE status = '待接單' AND bID IS NULL")
    orders = cursor.fetchall()
    conn.close()

    return render_template('bro_home.html', orders=orders)


@app.route('/accept_order/<int:oID>', methods=['POST'])
def accept_order(oID):
    if 'bID' not in session:  # 確認外送員登入
        return redirect(url_for('login'))

    bID = session['bID']  # 從 session 取得外送員 ID

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE `order`
        SET status = '已接單', bID = %s
        WHERE oID = %s AND status = '待接單' AND bID IS NULL
    """, (bID, oID))
    conn.commit()
    conn.close()

    return redirect(url_for('pending_orders'))







@app.route('/orders_status')
def orders_status():
    if 'bID' not in session:  # 確認外送員登入
        return redirect(url_for('login'))

    bID = session['bID']

    # 查詢所有已接但未取餐的訂單
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT oID, address, totalPrice, note FROM `order`
        WHERE status = '已接單' AND bID = %s
    """, (bID,))
    orders_pending_pickup = cursor.fetchall()

    # 查詢所有已取餐但未送達的訂單
    cursor.execute("""
        SELECT oID, address, totalPrice, note FROM `order`
        WHERE status = '已取餐' AND bID = %s
    """, (bID,))
    orders_pending_delivery = cursor.fetchall()

    # 查詢所有已完成的訂單
    cursor.execute("""
        SELECT oID, address, totalPrice, note FROM `order`
        WHERE status = '已送達' AND bID = %s
    """, (bID,))
    orders_pending_delivery = cursor.fetchall()

    conn.close()

    return render_template('orders_status.html', orders_pending_pickup=orders_pending_pickup, orders_pending_delivery=orders_pending_delivery)


@app.route('/update_order_status/<int:oID>/<status>', methods=['POST'])
def update_order_status(oID, status):
    if 'bID' not in session:  # 確認外送員登入
        return redirect(url_for('login'))

    bID = session['bID']  # 從 session 取得外送員 ID

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 更新訂單狀態
    cursor.execute("""
        UPDATE `order`
        SET status = %s
        WHERE oID = %s AND bID = %s
    """, (status, oID, bID))
    conn.commit()
    conn.close()

    return redirect(url_for('orders_status'))  # 更新後重新載入訂單頁面






#查看評價列表
@app.route('/ratings', methods=['GET', 'POST'])
def ratings():
    if 'bID' not in session:  # 確認外送員登入
        return redirect(url_for('login'))

    bID = session['bID']
    selected_star = request.form.get('star_filter', None)  # 從表單獲取篩選的星級

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 基本查詢，列出外送員的所有評價
    query = """
        SELECT s.sID, s.oID, s.rateB, s.commentB
        FROM star AS s
        JOIN `order` AS o ON s.oID = o.oID
        WHERE o.bID = %s
    """
    params = [bID]

    # 如果篩選特定星級
    if selected_star:
        query += " AND s.rateB = %s"
        params.append(selected_star)

<<<<<<< HEAD

    cursor.execute(query, tuple(params))
    ratings = cursor.fetchall()

    # 計算 rateB 的平均分
    cursor.execute("""
        SELECT AVG(rateB) AS avg_rating
        FROM star AS s
        JOIN `order` AS o ON s.oID = o.oID
        WHERE o.bID = %s
    """, (bID,))
    avg_rating = cursor.fetchone()['avg_rating']
    conn.close()

    return render_template('star.html', ratings=ratings, avg_rating=avg_rating, selected_star=selected_star)



# 查看訂單詳情
@app.route('/order_details/<int:oID>')
def order_details(oID):
    if 'bID' not in session:  # 確認外送員登入
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 查詢訂單詳情
    cursor.execute("""
        SELECT o.oID, o.totalPrice, o.address, o.note, o.createdAt
        FROM `order` AS o
        WHERE o.oID = %s
    """, (oID,))
    order = cursor.fetchone()
    conn.close()

    return render_template('order_details.html', order=order)
=======
        return jsonify({'message': '提現請求已提交，處理中！'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
#商家主畫面
@app.route("/rHome/<int:rID>")
def rHome(rID):
    #rID = session.get('loginID')  # 取得目前登入使用者的 uID
    isActive = get_is_active(rID)
    categorized_food = menu_food(rID)
    return render_template('seller/SellerHome.html', categorized_food=categorized_food, rID=rID,isActive=isActive)

# 更新是否營業
@app.route('/update_active/<int:rID>', methods=['POST'])
def update_active(rID):
    is_active = request.form.get('active') == '1' 
    update_is_active(is_active, rID)
    return redirect(url_for('rHome', rID=rID))

#菜單
@app.route('/menu/<int:rID>')
def menu(rID):
    categorized_food = menu_food(rID)
    return render_template('seller/Menu.html', categorized_food=categorized_food, rID=rID)

#新增餐點    
@app.route('/addFood/<int:rID>', methods=['GET', 'POST'])
def addFood(rID):
    categories = get_categories_by_restaurant(rID)
    if request.method == 'POST':
        form = request.form
        name = form.get('name')
        description = form.get('description')
        price = form.get('price')
        category_id = form.get('ID')
        is_vegetarian = form.get('vegetarian') == '素'
        add(rID, name, description, price, category_id, is_vegetarian)
        return redirect(f"/menu/{rID}")
    return render_template('seller/AddMenu.html', categories=categories,rID=rID)

# 修改菜單
@app.route('/edit/<int:rID>/<int:fID>', methods=['GET', 'POST'])
def edit(rID, fID):
    if request.method == 'POST':
        form = request.form
        name = form.get('name')
        description = form.get('description')
        price = form.get('price')
        category_id = form.get('category_id')
        is_vegetarian = form.get('is_vegetarian') == 'on'
        # 更新餐點資料
        edit_food(fID, name, description, price, category_id,is_vegetarian)
        return redirect(f"/menu/{rID}")

    # 獲取當前餐點資料
    food = get_food(fID)
    categories = get_categories_by_restaurant(rID)
    return render_template('seller/MenuEdit.html', food=food, categories=categories,rID=rID)

# 刪除餐點
@app.route('/delete/<int:rID>', methods=['POST'])
def delete(rID):
    form = request.form
    fID = form.get('fID')  # 假設表單中有隱藏欄位傳遞 fID
    if fID:
        delete_food(fID)  # 執行刪除操作
        return redirect(f"/menu/{rID}")
    else:
        return "未提供 fID", 400  # 如果未提供 fID，返回錯誤

#訂單列表
@app.route('/order/<int:rID>')
def order(rID):
    order_list = orderList(rID)
    return render_template('seller/Order.html',order_list=order_list,rID=rID)

#確認接單
@app.route('/accept_food/<int:oID>', methods=['GET','POST'])
def accept_food(oID):
    if request.method == 'POST':
        form = request.form
        prepareTime = form.get('prepareTime')
        acceptFood(prepareTime,oID)
        return redirect(f"/contact_bro/{oID}")
    
    return render_template('ContactBro.html', oID=oID)

#我的資料
@app.route('/aboutME/<int:rID>')
def aboutME(rID):
    about = about_me(rID)
    return render_template('seller/About.html',about=about,rID=rID)

# 修改我的資料
@app.route('/editME/<int:rID>', methods=['GET', 'POST'])
def editME(rID):
    if request.method == 'POST':
        form = request.form
        name = form.get('name')
        email = form.get('email')
        phone = form.get('phone')
        address = form.get('address')
        bank = form.get('bank')
        time = form.get('time')

        edit_me(name,email,phone,address,bank,time,rID)
        return redirect(f"/aboutME/{rID}")

    restaurant_info = about_me(rID)
    return render_template('seller/AboutEdit.html',restaurant_info=restaurant_info, rID=rID)

#我的評價
@app.route('/review/<int:rID>')
def review(rID):
    stars = star(rID)
    return render_template('seller/Review.html',stars=stars,rID=rID)

>>>>>>> d3f1586 (商家)
