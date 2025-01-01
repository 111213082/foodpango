from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from functools import wraps
from dbUtils import validate_user,register_user
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
        session['user_role'] = user_data['role']  # 確保這裡存儲的是 'user_role'
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
    return render_template('restaurant_dashboard.html')

# 路由：外送員專屬頁面
@app.route('/bro/dashboard')
@login_required(role='bro')
def bro_dashboard():
    return render_template('bro_dashboard.html')

