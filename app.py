from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import mysql.connector
from config import db_config
from functools import wraps
from dbUtils import get_is_active,update_is_active,menu_food,add,get_categories_by_restaurant,edit_food,delete_food,get_food,orderList,about_me,edit_me,star,orderList,acceptFood
from dbUtils import validate_user#, register_customer,register_restaurant,register_bro
import json

app = Flask(__name__)

# 資料庫連線
def get_db_connection():
    return mysql.connector.connect(**db_config)

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
def pending_orders():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT id, restaurant_id, delivery_address, total_price FROM orders WHERE status = 'pending'"
        cursor.execute(query)
        orders = cursor.fetchall()

        cursor.close()
        conn.close()
        return render_template('pending_orders.html', orders=orders)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 外送員接單 API
@app.route('/orders/accept', methods=['POST'])
def accept_order():
    try:
        data = request.get_json()
        order_id = data['order_id']
        delivery_person_id = data['delivery_person_id']

        conn = get_db_connection()
        cursor = conn.cursor()

        # 更新訂單狀態為 '配送中'
        update_query = """
            UPDATE orders 
            SET status = 'in_delivery', delivery_person_id = %s 
            WHERE id = %s AND status = 'pending'
        """
        cursor.execute(update_query, (delivery_person_id, order_id))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({'message': '訂單已被接取或不存在。'}), 400

        cursor.close()
        conn.close()
        return jsonify({'message': '接單成功！'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


# 顯示外送員的收入記錄與總收入
@app.route('/delivery/<int:delivery_person_id>/income', methods=['GET'])
def get_income(delivery_person_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # 查詢外送員的所有收入記錄
        query = """
            SELECT order_id, base_income, bonus_income, tips, total_income
            FROM delivery_earnings 
            WHERE delivery_person_id = %s
        """
        cursor.execute(query, (delivery_person_id,))
        earnings = cursor.fetchall()

        # 計算總收入
        total_income = sum(earning['total_income'] for earning in earnings)

        cursor.close()
        conn.close()

        return jsonify({
            'total_income': total_income,
            'earnings': earnings
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# 顯示外送員可提現的金額
@app.route('/delivery/<int:delivery_person_id>/withdrawable', methods=['GET'])
def get_withdrawable_amount(delivery_person_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # 查詢外送員的總收入
        query = """
            SELECT SUM(total_income) AS total_income
            FROM delivery_earnings
            WHERE delivery_person_id = %s
        """
        cursor.execute(query, (delivery_person_id,))
        result = cursor.fetchone()
        total_income = result['total_income'] if result['total_income'] else 0

        # 查詢已提現的金額
        query = """
            SELECT SUM(amount) AS total_withdrawn
            FROM withdrawals
            WHERE delivery_person_id = %s AND status = 'completed'
        """
        cursor.execute(query, (delivery_person_id,))
        result = cursor.fetchone()
        total_withdrawn = result['total_withdrawn'] if result['total_withdrawn'] else 0

        withdrawable_amount = total_income - total_withdrawn

        cursor.close()
        conn.close()

        return jsonify({
            'withdrawable_amount': withdrawable_amount
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 提現請求
@app.route('/delivery/<int:delivery_person_id>/withdraw', methods=['POST'])
def request_withdrawal(delivery_person_id):
    try:
        data = request.get_json()
        amount = data['amount']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # 查詢可提現的金額
        query = """
            SELECT SUM(total_income) AS total_income
            FROM delivery_earnings
            WHERE delivery_person_id = %s
        """
        cursor.execute(query, (delivery_person_id,))
        result = cursor.fetchone()
        total_income = result['total_income'] if result['total_income'] else 0

        # 查詢已提現的金額
        query = """
            SELECT SUM(amount) AS total_withdrawn
            FROM withdrawals
            WHERE delivery_person_id = %s AND status = 'completed'
        """
        cursor.execute(query, (delivery_person_id,))
        result = cursor.fetchone()
        total_withdrawn = result['total_withdrawn'] if result['total_withdrawn'] else 0

        withdrawable_amount = total_income - total_withdrawn

        # 檢查提款金額是否超過可提現金額
        if amount > withdrawable_amount:
            return jsonify({'error': '提款金額超過可用金額'}), 400

        # 假設手續費為 5%
        fee = 0.05 * amount
        final_amount = amount - fee

        # 插入提現記錄
        query = """
            INSERT INTO withdrawals (delivery_person_id, amount, fee, final_amount, status)
            VALUES (%s, %s, %s, %s, 'processing')
        """
        cursor.execute(query, (delivery_person_id, amount, fee, final_amount))
        conn.commit()

        cursor.close()
        conn.close()

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

