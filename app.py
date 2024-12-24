from flask import Flask, render_template, request, redirect, session, flash,url_for
import dbUtils  # 假設您使用 dbUtils 管理資料庫連線

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用於管理 session

@app.route("/")
def m():
	return redirect('/login')


# 註冊功能
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        try:
            add_user(role, name, email, password)  # 使用 db_utils 的方法
            flash("註冊成功！現在可以登入")
            return redirect(url_for('login'))
        except ValueError as e:
            flash(str(e))
        except Exception as e:
            flash("註冊失敗，請重試")

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        try:
            user = get_user_by_email(role, email)  # 使用 db_utils 的方法
            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['staffID'] if role == 'staff' else user['id']
                session['role'] = role
                flash("登入成功！")
                return redirect(url_for(f'{role}_dashboard'))
            else:
                flash("電子郵件或密碼錯誤")
        except ValueError as e:
            flash(str(e))
        except Exception as e:
            flash("登入失敗，請重試")

    return render_template('login.html')

@app.route('/customer_dashboard')
def customer_dashboard():
    return "顧客主畫面"

@app.route('/restaurant_dashboard')
def restaurant_dashboard():
    return "店家主畫面"



@app.route('/staff_dashboard')
def staff_dashboard():
    return "後台管理人員主畫面"



#外送員主畫面
@app.route('/bro_home')
def bro_home():
    if 'bID' not in session:
        return redirect(url_for('login'))  # 若未登入，導向登入頁

    bID = session['bID']  # 從 session 獲取外送員 ID
    orders = dbUtils.get_all_orders()  # 從資料庫獲取所有訂單資訊
    return render_template('bro_home.html', orders=orders,bID=bID)  


#接單功能
@app.route('/accept_order/<int:oID>', methods=['POST'])
def accept_order(oID):
    if 'bID' not in session:
        return redirect(url_for('login'))  # 若未登入，導向登入頁

    bID = session['bID']  # 獲取當前外送員的 ID
    success = dbUtils.accept_order(oID, bID)  # 更新訂單狀態

    if success:
        flash('恭喜你以單身的手速搶到訂單！')
    else:
        flash('看來你單身還是單身菜鳥未能搶到訂單。')

    return redirect(url_for('bro_home'))

