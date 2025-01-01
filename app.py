from flask import Flask, render_template, request, redirect, url_for, session
from dbUtils import get_pending_orders, accept_order, validate_courier, get_orders_by_status, update_order_status_in_db, get_ratings_for_courier, get_average_rating, get_order_details,update_order_status_and_time_in_db

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用於管理 session

@app.route("/")
def m():
    return redirect('/login')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        courier = validate_courier(email, password)

        if courier:
            session['bID'] = courier['bID']
            return redirect(url_for('pending_orders'))
        else:
            error = "登入失敗，請檢查您的帳號與密碼。"
            return render_template('login.html', error=error)

    return render_template('login.html')



@app.route('/pending_orders')
def pending_orders():
    if 'bID' not in session:  # 確認外送員登入
        return redirect(url_for('login'))

    orders = get_pending_orders()
    return render_template('bro_home.html', orders=orders)



@app.route('/accept_order/<int:oID>', methods=['POST'])
def accept_order_route(oID):
    if 'bID' not in session:  # 確認外送員登入
        return redirect(url_for('login'))

    bID = session['bID']  # 從 session 取得外送員 ID
    accept_order(oID, bID)
    return redirect(url_for('pending_orders'))



@app.route('/orders_status')
def orders_status():
    if 'bID' not in session:  # 確認外送員登入
        return redirect(url_for('login'))

    bID = session['bID']

    # 取得不同狀態的訂單
    orders_pending_pickup = get_orders_by_status(bID, '已接單')
    orders_pending_delivery = get_orders_by_status(bID, '已取餐')
    completed_orders = get_orders_by_status(bID, '已送達')

    # 計算已完成訂單數量
    completed_count = len(completed_orders)

    return render_template(
        'orders_status.html',
        orders_pending_pickup=orders_pending_pickup,
        orders_pending_delivery=orders_pending_delivery,
        completed_orders=completed_orders,
        completed_count=completed_count
    )



@app.route('/update_order_status/<int:oID>/<status>', methods=['POST'])
def update_order_status(oID, status):
    if 'bID' not in session:  # 確認外送員登入
        return redirect(url_for('login'))

    bID = session['bID']  # 從 session 取得外送員 ID

    # 更新訂單狀態
    update_order_status_in_db(oID, bID, status)

    return redirect(url_for('orders_status'))  # 更新後重新載入訂單頁面



#處理帶有送達時間的表單提交
@app.route('/update_order_status_with_time/<int:oID>', methods=['POST'])
def update_order_status_with_time(oID):
    if 'bID' not in session:  # 確認外送員登入
        return redirect(url_for('login'))

    bID = session['bID']  # 從 session 取得外送員 ID
    delivery_time = request.form.get('delivery_time')  # 獲取送達時間

    if not delivery_time:
        return "送達時間未提供", 400  # 如果沒有提供送達時間，返回錯誤

    # 更新訂單狀態並添加送達時間
    update_order_status_and_time_in_db(oID, bID, '已送達', delivery_time)

    return redirect(url_for('orders_status'))



# 查看評價列表
@app.route('/ratings', methods=['GET', 'POST'])
def ratings():
    if 'bID' not in session:  # 確認外送員登入
        return redirect(url_for('login'))

    bID = session['bID']
    selected_star = request.form.get('star_filter', None)  # 從表單獲取篩選的星級

    # 取得評價列表與平均分
    ratings = get_ratings_for_courier(bID, selected_star)
    avg_rating = get_average_rating(bID)

    return render_template(
        'star.html',
        ratings=ratings,
        avg_rating=avg_rating,
        selected_star=selected_star
    )

# 查看訂單詳情
@app.route('/order_details/<int:oID>')
def order_details(oID):
    if 'bID' not in session:  # 確認外送員登入
        return redirect(url_for('login'))

    # 取得訂單詳情
    order = get_order_details(oID)

    return render_template('order_details.html', order=order)


if __name__ == '__main__':
    app.run(debug=True)



