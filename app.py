from flask import Flask, render_template, request, session, redirect, jsonify, url_for
from functools import wraps
from dbUtils import get_restaurants, get_restaurant_by_id, get_foods, get_food_by_id, get_foods_by_shop_ids
from dbUtils import get_customer_data, update_customer_data, add_order_detail,
from dbUtils import login_required, validate_user

# creates a Flask application, specify a static folder on /
app = Flask(__name__, static_folder='static', static_url_path='/')
# set a secret key to hash cookies
app.config['SECRET_KEY'] = '123TyU%^&'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['EMAIL']
        password = request.form['PWD']
        #role = request.form['role']
        role = request.form.get('role')  # 確保從表單中獲取角色
        user = validate_user(email, password, role)  # 傳遞 role 參數
    if user:
        session['email'] = user['email']
        session['user_role'] = user['role']
        
    if role == 'customer':
        session['cID'] = user['cID']
        print(f"cID is stored in session: {session['cID']}")
    
    return "登入失敗，請檢查帳號或密碼。"
    return render_template('loginpage.html')



@app.route('/customer/dashboard')
def main_page():
    if 'email' not in session:
        return redirect('loginpage.html')
    return render_template('main.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/loginpage.html')


@app.route('/')
def home():
    email = session.get('email')
    if email:
        user_role = session.get('user_role')
        if user_role == 'customer':
            return redirect('/customer/dashboard')
        elif user_role == 'restaurant':
            return redirect('/restaurant/dashboard')
        elif user_role == 'bro':
            return redirect('/bro/dashboard')
    else:
        return render_template('/loginpage.html')   



@app.route('/information')
def customer_information():
    if 'email' not in session:
        return redirect(url_for('login'))

    email = session['email']
    customer_data = get_customer_data(email)
    session['cID'] = customer_data['cID']

    if customer_data:
        return render_template('information.html', customer_data=customer_data)
    else:
        return "顧客資料未找到", 404


@app.route('/edit', methods=['GET'])
def edit_profile():
    email = session.get('email')
    customer_data = get_customer_data(email)

    if customer_data:
        return render_template('edit.html', customer_data=customer_data)
    return "顧客資料未找到", 404


@app.route('/update', methods=['POST'])
def update_profile():
    email = session.get('email')

    name = request.form.get('name')
    phone = request.form.get('phone')
    address = request.form.get('address')
    card_number = request.form.get('card')

    if update_customer_data(email, name, phone, address, card_number):
        return redirect(url_for('customer_information'))
    return "資料更新失敗，請稍後再試。", 500


@app.route('/api/cart/checkout', methods=['POST'])
def checkout_cart_api():
    """結帳購物車"""
    if 'cID' not in session:
        return jsonify({"success": False, "message": "未登入"}), 401
    cID = session['cID']
    data = request.get_json()
    rID = data['rID']
    note = data.get('note', '')
    address = data.get('address', '')
    # 取得購物車內容
    cart_items = get_cart(cID)
    if not cart_items:
        return jsonify({"success": False, "message": "購物車為空"}), 400
    # 計算總金額
    total_price = sum(item['quantity'] * item['price'] for item in cart_items)
    # 建立訂單
    oID = create_order(cID, rID, total_price, note, address)
    if not oID:
        return jsonify({"success": False, "message": "建立訂單失敗"}), 500
    # 新增訂單明細
    for item in cart_items:
        if not add_order_detail(oID, item['fID'], item['quantity'], item['price']):
            return jsonify({"success": False, "message": f"新增商品 {item['fID']} 明細失敗"}), 500
    # 清空購物車
    if not clear_cart(cID):
        return jsonify({"success": False, "message": "清空購物車失敗"}), 500

    return jsonify({"success": True, "message": "結帳成功", "oID": oID}), 200



@app.route('/Trace')
def track_order():
    order_id = request.args.get('order_id')  # 使用 order_id 而非 oID
    print(f"接收到的訂單 ID: {order_id}")
    if not order_id:
        return "缺少訂單 ID", 400

    order = get_order_details(int(order_id))

    if order:
        return render_template('Trace.html', order=order)
    else:
        return "訂單未找到", 404



@app.route('/ShopList')
def ShopList():
    restaurants = get_restaurants()
    return render_template('ShopList.html', restaurants=restaurants)


@app.route('/shop/<int:shop_id>')
def shop_detail(shop_id):
    shop = get_restaurant_by_id(shop_id)

    if shop:
        return render_template('ShopDetail.html', Shop=shop)
    else:
        return "店家資料未找到", 404


@app.route('/FoodList')
def food_list():
    shop_ids = request.args.get('shopIds')
    if shop_ids:
        shop_ids = list(map(int, shop_ids.split(',')))
    else:
        shop_ids = []
    foods = get_foods_by_shop_ids(shop_ids)
    return render_template('FoodList.html', foods=foods)


@app.route('/food/<int:food_id>')
def food_detail(food_id):
    food = get_food_by_id(food_id)
    if food:
        shop_name = get_restaurant_by_id(food['rID'])
        return render_template('FoodDetail.html', food=food, shop_name=shop_name)
    else:
        return "菜品資料未找到", 404


@app.route('/ShopCart')
def ShopCart():
    # 確保已登入並能取得 cID
    if 'cID' not in session:
        return redirect(url_for('login'))  # 若未登入，跳轉到登入頁面

    cID = session['cID']  # 從 session 提取 cID
    # 現在可以使用 cID 查詢購物車資料
    # 例如: 查詢該 cID 的購物車內容    
    return render_template('ShopCart.html')


@app.route("/GoodBad")
def GoodBad():
    return render_template("GoodBad.html")

@app.route('/submit', methods=['POST'])
def submit_review():
    # 從表單獲取資料
    oID = request.form['oID']
    rateR = request.form['store_rating']
    rateB = request.form['delivery_rating']
    commentR = request.form['store_comment']
    commentB = request.form['delivery_comment']

    # 使用 dbUtils 儲存評價資料
    save_review(oID, rateR, rateB, commentR, commentB)

    return "評價提交成功！"


@app.route('/Thanks', methods=['POST'])
def thanks():
    return render_template('thanks.html')