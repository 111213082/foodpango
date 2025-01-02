from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import mysql.connector
from functools import wraps
from dbUtils import get_is_active,update_is_active,menu_food,add,get_categories_by_restaurant,edit_food,delete_food,get_food,get_orders_by_status,about_me,edit_me,star,acceptFood
#from dbUtils import validate_user#, register_customer,register_restaurant,register_bro
import json

app = Flask(__name__)

#商家主畫面
@app.route("/rHome/<int:rID>")
def rHome(rID):
    rID = session.get('loginID')  
    isActive = get_is_active(rID)
    categorized_food = menu_food(rID)
    return render_template('seller/SellerHome.html', categorized_food=categorized_food, rID=rID,isActive=isActive)

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
