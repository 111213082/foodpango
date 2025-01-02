import dbUtils
from flask import Flask, render_template, request, session, redirect, jsonify, url_for
from functools import wraps
from dbUtils import get_restaurants, get_restaurant_by_id, get_foods, get_food_by_id, get_foods_by_shop_ids, insert_order_item, get_orders_by_cid
from dbUtils import get_customer_data, update_customer_data,create_order, get_order,get_order_details, insert_order, get_rid_by_item
from dbUtils import login_required, validate_user, get_rid_by_item,  get_order_status, insert_review, validate_order, validateOrder

# creates a Flask application, specify a static folder on /
app = Flask(__name__, static_folder='static', static_url_path='/')
# set a secret key to hash cookies
app.config['SECRET_KEY'] = '123TyU%^&'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['EMAIL']
        password = request.form['PWD']
        role = request.form.get('role')  # 確保從表單中獲取角色
        user = validate_user(email, password, role)  # 傳遞 role 參數
        if user:
            session['email'] = user['email']
            session['user_role'] = user['role']
            if role == 'customer':
                session['cID'] = user['cID']
                print(f"cID is stored in session: {session['cID']}")
            return redirect(url_for('main_page'))  # 登入成功後重定向到主頁
    return "登入失敗，請檢查帳號或密碼。"




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
        return render_template('loginpage.html')  # 確保路徑正確
  



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


@app.route('/api/get_rid', methods=['GET'])
def get_rid():
    shop_name = request.args.get('shop')
    if not shop_name:
        return jsonify({"success": False, "message": "店家名稱為必填參數"}), 400

    rID = get_restaurant_id(shop_name)
    if rID:
        return jsonify({"success": True, "rID": rID})
    else:
        return jsonify({"success": False, "message": "未找到對應的店家"}), 404



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



@app.route('/review/<order_id>')
def review(order_id):
    return render_template('GoodBad.html', oID=order_id)


# 提交評價的路由
# 提交評價的路由
@app.route('/submit_review', methods=['POST'])
def submit_review():
    oID = request.form.get('oID')  # 獲取表單中的 oID

    # 檢查 oID 是否有效
    if not oID or not validate_order(oID):  # 如果 oID 無效或訂單不存在
        return {'status': 'error', 'message': '無效的訂單ID'}

    # 繼續處理評論
    rateR = request.form.get('rateR')
    rateB = request.form.get('rateB')
    commentR = request.form.get('commentR')
    commentB = request.form.get('commentB')

    # 插入評論
    success = insert_review(oID, rateR, rateB, commentR, commentB)

    if success:
        return {'status': 'success', 'message': '評論已提交'}
    else:
        return {'status': 'error', 'message': '提交評論失敗'}




@app.route('/Thanks', methods=['GET', 'POST'])
def thanks():
    return render_template('thanks.html')


@app.route('/all', methods=['GET', 'POST'])
def all():
    return render_template('all.html')


@app.route("/ShopCart")
def ShopCart():
    return render_template("ShopCart.html")

@app.route('/Trace')
def track_order():
    order_id = request.args.get('order_id')  # 從查詢字符串中獲取 order_id
    if not order_id:
        return "缺少訂單 ID", 400  # 如果沒有傳遞 order_id，則返回錯誤

    # 查詢訂單詳細資料
    order = get_order_details(int(order_id))  # 記得將 order_id 轉換為整數
    
    if order:
        return render_template('Trace.html', order=order)
    else:
        return "訂單未找到", 404


@app.route('/api/createOrder', methods=['POST'])
def create_order_route():
    data = request.get_json()

    # 確認資料
    items = data.get('items', [])
    if not items:
        return jsonify({"success": False, "message": "未選擇任何商品"}), 400

    # 確認送餐地址
    delivery_address = data.get('deliveryAddress')
    if not delivery_address:
        return jsonify({"success": False, "message": "送餐地址必填"}), 400

    # 從 session 中獲取 cID
    cID = session.get('cID')
    if not cID:
        return jsonify({"success": False, "message": "未找到顧客資料"}), 400

    # 確認所有商品來自同一家餐廳
    first_rID = get_rid_by_item(items[0].get('itemId'))  # 根據第一個商品獲取餐廳ID
    if not first_rID:
        return jsonify({"success": False, "message": "無法找到餐廳ID"}), 500

    for item in items:
        item_rID = get_rid_by_item(item.get('itemId'))
        if item_rID != first_rID:
            return jsonify({"success": False, "message": "訂單只能包含來自同一家餐廳的商品"}), 400

    # 插入訂單資料，並傳遞 rID
    total_price = data.get('totalPrice', 0)
    note = data.get('note', '')
    order_id = insert_order(cID, total_price, note, delivery_address, first_rID)  # 傳遞 rID

    if not order_id:
        return jsonify({"success": False, "message": "無法創建訂單"}), 500

    # 插入訂單項目
    for item in items:
        item_id = item.get('itemId')
        quantity = item.get('quantity')
        price = item.get('price')
        total_price_for_item = price * quantity  # 每個商品的總價
        insert_order_item(order_id, item_id, quantity, total_price_for_item)  # 插入訂單項目，使用每個商品的總價

    return jsonify({"success": True, "orderId": order_id}), 200



@app.route('/orders/<int:cID>', methods=['GET'])
def get_orders(cID):
    # 使用 dbUtils.py 中的函數查詢顧客的訂單資料
    orders = get_orders_by_cid(cID)

    if not orders:
        return jsonify({"message": "沒有找到訂單資料"}), 404

    # 返回訂單資料
    return jsonify(orders)



@app.route('/get-order-status/<int:oID>', methods=['GET'])
def get_order_status_api(oID):
    """
    API 端點: 根據 oID 返回訂單狀態
    """
    # 驗證訂單是否存在
    if not validate_order(oID):
        print(f"訂單 {oID} 不存在")
        return jsonify({'error': '訂單未找到'}), 404

    # 查詢訂單狀態
    status = get_order_status(oID)
    if status is None:
        return jsonify({'error': '無法獲取訂單狀態，請稍後再試'}), 500
    print(f"訂單 {oID} 狀態: {status}")  # 確認後端回應的狀態
    return jsonify({'status': status})  # 返回訂單的狀態

@app.route('/update-order-status/<int:order_id>', methods=['POST'])
def update_status(order_id):
    data = request.get_json()
    status = data.get('status')
    if status:
        update_order_status(order_id, status)
        return jsonify({'message': '訂單狀態更新成功'})
    return jsonify({'message': '缺少狀態字段'}), 400

