from flask import Flask, render_template, request, redirect, session, flash
import dbUtils  # 假設您使用 dbUtils 管理資料庫連線

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用於管理 session


#外送員主畫面
@app.route("/bro_home")
def bro_home():
    if 'bID' not in session:
        return redirect('/login')  # 若未登入則導向登入頁面
    
    # 查詢訂單資料
    orders = dbUtils.get_orders()
    
    return render_template('bro_home.html', orders=orders)


#接單邏輯
@app.route("/accept_order/<int:oID>", methods=["POST"])
def accept_order(oID):
    if 'bID' not in session:
        return redirect('/login')
    
    bID = session['bID']
    
    # 更新訂單狀態
    affected_rows = dbUtils.accept_order(oID, bID)
    
    if affected_rows > 0:
        flash('恭喜你以單身的手速搶到訂單！')
    else:
        flash('看來你單身還是單身菜鳥未能搶到訂單。')
    
    return redirect('/bro_home')
