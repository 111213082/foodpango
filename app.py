from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from functools import wraps
from dbUtils import validate_user,register_user #平台
from dbUtils import get_is_active,update_is_active,menu_food,add,get_categories_by_restaurant,edit_food,delete_food,get_food,get_orders_by_status,about_me,edit_me,star,acceptFood #餐廳
import json

app = Flask(__name__, static_folder='static', static_url_path='/')
app.config['SECRET_KEY'] = '123TyU%^&'

# 登入驗證裝飾器
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


@app.route('/login', methods=['POST'])
def login():
    form = request.form
    email = form['EMAIL']
    pwd = form['PWD']
    role = form['role']
    
    user_data = validate_user(email, pwd, role)
    if user_data:
        session['email'] = user_data['email']
        session['user_role'] = role  # 存入角色
        if role == 'customer':
            session['cID'] = user_data['id']  # 存入顧客 ID
        elif role == 'restaurant':
            session['rID'] = user_data['id']  # 存入餐廳 ID
        elif role == 'bro':
            session['bID'] = user_data['id']  # 存入外送員 ID
        return redirect("/")
    return redirect("/loginPage.html")

@app.route('/logout')
def logout():
    session.clear()  # 清除所有session
    return redirect('/loginPage.html')

# 路由：註冊頁面（角色選擇）
@app.route('/register/customer')
def register_customer_page():
    return render_template('registerCustomer.html')

@app.route('/register/restaurant')
def register_restaurant_page():
    return render_template('registerRestaurant.html')

@app.route('/register/bro')
def register_bro_page():
    return render_template('registerBro.html')
#"""
# 路由：註冊功能
@app.route('/register/<role>', methods=['POST'])
def register(role):
    valid_roles = ['customer', 'restaurant', 'bro']
    if role not in valid_roles:
        return "無效的角色", 400

    form = request.form
    data = {
        'name': form['name'],
        'email': form['email'],
        'password': form['password'],
        'phone': form['phone'],
    }

    # 根據角色增加特定欄位
    if role == 'customer':
        data.update({'address': form.get('address'), 'card': form.get('card')})
    elif role == 'restaurant':
        data.update({'address': form['address'], 'bank': form['bank']})
    elif role == 'bro':
        data.update({'bank': form['bank']})

    try:
        if register_user(role, **data):
            return redirect('/loginPage.html')  # 註冊成功後跳轉登入頁面
        else:
            return "註冊失敗，請稍後再試", 500
    except Exception as e:
        return str(e), 500
#"""
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
            rID = session.get('rID')  # 獲取商家 ID
            if rID:  # 如果 rID 存在，重定向到 /rHome/<int:rID>
                return redirect(f'/rHome/{rID}')
            else:  # rID 不存在，可能是數據不完整或會話問題
                return redirect('/loginPage.html')
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



# 路由：外送員專屬頁面
@app.route('/bro/dashboard')
@login_required(role='bro')
def bro_dashboard():
    return render_template('bro_dashboard.html')

#商家主畫面
#@app.route('/restaurant/dashboard')
@app.route("/rHome/<int:rID>")
@login_required(role='restaurant')
def rHome(rID=None):
    if rID is None:  # 如果 rID 未提供，從 Session 中獲取
        rID = session.get('rID')
    if not rID:  # 如果 rID 仍為 None，返回錯誤或重定向
        return redirect('/loginPage.html')  

    isActive = get_is_active(rID)
    categorized_food = menu_food(rID)
    return render_template('seller/SellerHome.html', categorized_food=categorized_food, rID=rID, isActive=isActive)

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
    # 查詢待接單的訂單
    pending_orders = get_orders_by_status(rID, status='待確認')
    # 查詢已接單的訂單
    accepted_orders = get_orders_by_status(rID, status='店家已接單')

    # 傳遞到模板
    return render_template(
        'seller/Order.html',
        pending_orders=pending_orders,
        accepted_orders=accepted_orders,
        rID=rID
    )

#確認接單
@app.route('/accept_food/<int:oID>', methods=['GET', 'POST'])
def accept_food(oID):
    if request.method == 'POST':
        prepareTime = request.form.get('prepareTime')
        if prepareTime:
            acceptFood(prepareTime,oID)  
        rID = session.get('rID')
        return redirect(url_for(f"/order/{rID}"))
    
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
