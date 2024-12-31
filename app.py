
from flask import Flask, render_template, request, redirect, url_for, session
from dbUtils import get_db_connection




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
