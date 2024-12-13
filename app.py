from flask import Flask, jsonify, request, render_template, redirect, session
import mysql.connector
from config import db_config, home

app = Flask(__name__)

# 資料庫連線
def get_db_connection():
    return mysql.connector.connect(**db_config)

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
@app.route("/SellerHome")
def seller():
    uID = session.get('loginID')  # 取得目前登入使用者的 uID
    dat = home(uID)
    return render_template('SellerHome.html', data=dat)
