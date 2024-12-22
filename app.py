from flask import Flask, render_template, request, redirect, session, flash,url_for
import dbUtils  # 假設您使用 dbUtils 管理資料庫連線

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用於管理 session


#外送員主畫面
@app.route('/bro_home')
def bro_home():
#    if 'bID' not in session:
#        return redirect(url_for('login'))  # 若未登入，導向登入頁

    orders = dbUtils.get_all_orders()  # 從資料庫獲取所有訂單資訊
    return render_template('bro_home.html', orders=orders)


#接單功能
@app.route('/accept_order/<int:oID>', methods=['POST'])
def accept_order(oID):
#    if 'bID' not in session:
#        return redirect(url_for('login'))  # 若未登入，導向登入頁

    bID = session['bID']  # 獲取當前外送員的 ID
    success = dbUtils.accept_order(oID, bID)  # 更新訂單狀態

    if success:
        flash('恭喜你以單身的手速搶到訂單！')
    else:
        flash('看來你單身還是單身菜鳥未能搶到訂單。')

    return redirect(url_for('bro_home'))

