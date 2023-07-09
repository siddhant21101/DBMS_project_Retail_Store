import mysql.connector
from datetime import date
newdeliveries=[]
timeLeft=[]
def insertquery(myquery,vals):
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="siddis",
        database="MyBasket"
    )
    mycursor = mydb.cursor()
    mycursor.execute(myquery, vals)
    mydb.commit()
    print(mycursor.rowcount , "table updated.")

def update_cart_query(custid,proid,nquantity,npayid):
    myquery="update Cart set payid = "+str(npayid)+" where pid="+str(proid)+" and cid="+str(custid)+" and status = 'not delivered' and quantity="+str(nquantity)+";"
    myquery2="update Cart set status='onway' where pid="+str(proid)+" and cid="+str(custid)+" and status = 'not delivered' and quantity="+str(nquantity)+";"
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="siddis",
        database="MyBasket"
    )
    mycursor = mydb.cursor()
    mycursor.execute(myquery)
    mycursor.execute(myquery2)
    mydb.commit()
    print(mycursor.rowcount, "record(s) affected")

def doquery(query):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="siddis",
        database="MyBasket"
    )
    mycursor = mydb.cursor()
    mycursor.execute(query)
    results = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    return results

def runquery(myquery):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="siddis",
        database="MyBasket"
    )
    mycursor = mydb.cursor()
    mycursor.execute(myquery)
    mydb.commit()
    print(mycursor.rowcount, "record(s) affected")

def checkPassword(id, passwor):
    query = "SELECT * FROM Customer where cid=" + str(id) + " and password=" + "\'" + passwor + "\'"
    r = doquery(query)
    if r:
        # r is not an empty list
        return True
    return False


def showPastOrder(id):
    deliverdquery = "SELECT * FROM Product WHERE pid in (SELECT pid FROM Cart WHERE cid = "+str(id)+"  AND (status ='delivered'));"
#     onwayquery="""SELECT p.name AS product_name
# FROM cart c
# INNER JOIN product p ON c.pid = p.pid
# WHERE c.cid = """+str(id)+" AND c.status = 'onway';"
    onwayquery="SELECT * FROM Product WHERE pid in (SELECT pid FROM Cart WHERE cid = "+str(id)+"  AND (status ='onway'));"
    delivered = (doquery(deliverdquery));
    onway=doquery(onwayquery);
    print("Delivered products are -")
    for result in delivered:
         print("name:", result[0], "rating :", result[1], "price:", result[2], "quantity:",
              result[3], "mfd:", result[4], "id:", result[5])
    print("On way products -")
    for result in onway:
         print("name:", result[0], "rating :", result[1], "price:", result[2], "quantity:",
              result[3], "mfd:", result[4], "id:", result[5])

def showCart(inp_id):
    myquery = "SELECT p.name as productName ,p.rating,p.price,c.quantity,p.manufacturingDate,p.pid FROM product p,cart c ,customer cu WHERE c.status='not delivered' AND c.cid=cu.cid AND cu.cid=" + \
              str(inp_id) + " AND p.pid=c.pid"
    myresults = (doquery(myquery))
    for result in myresults:
        print("name:", result[0], "rating :", result[1], "price:", result[2], "quantity:",
              result[3], "mfd:", result[4], "id:", result[5])

def showProducts(catid):
    myquery = "SELECT * FROM Product where catid =" + str(catid) + ";"
    myresults = (doquery(myquery))
    for result in myresults:
        # print(result)
        print("name:", result[0],"product id:",result[1], "MFD:", result[4], "rating:",
              result[5], "quantity:", result[6], "price:", result[7])

def showRetailerOrdersRevenue():
    myquery = "SELECT r.fname,r.mname, r.lname, COUNT(o.payid) AS total_orders, SUM(p.price) AS total_revenue FROM Retailer r JOIN product p ON r.rid = p.rid JOIN cart ON p.pid = cart.pid JOIN orderdetails o ON cart.payid = o.payid GROUP BY r.rid ORDER BY total_revenue DESC;"
    myresults = (doquery(myquery))
    for result in myresults:
        ans = ""
        if (result[0] != None):
            ans += result[0] + " "
        if (result[1] != None):
            ans += result[1] + " "
        if (result[2] != None):
            ans += result[2]
        print("name:", ans, "total orders:", result[3], "revenue:", result[4])


def showCustomerTotalOrders():
    myquery = "SELECT c.fname AS customer_fname, c.lname AS customer_lname, a.locality, COUNT(DISTINCT o.payid) AS num_orders, SUM(od.total_price) AS total_spent FROM customer c  JOIN address a ON c.cid = a.cid  LEFT JOIN payment p ON a.aid = p.aid  LEFT JOIN orderdetails o ON p.payid = o.payid  LEFT JOIN (SELECT payid, SUM(quantity * price) AS total_price FROM cart GROUP BY payid) od ON p.payid = od.payid  GROUP BY c.cid, a.aid ORDER BY total_spent DESC;"
    myresults = (doquery(myquery))
    for result in myresults:
        ans = ""
        if (result[0] != None):
            ans += result[0] + " "
        if (result[1] != None):
            ans += result[1]
        print("name:", ans, "locality: ",
              result[2], "total orders:", result[3], "revenue:", result[4])


def showTop5Customers():
    myquery = "SELECT c.fname,c.email, SUM(cart.price) AS total_spent FROM customer c JOIN cart ON c.cid = cart.cid WHERE cart.status = 'delivered' GROUP BY c.email ORDER BY total_spent DESC LIMIT 5;"
    myresults = (doquery(myquery))
    for result in myresults:
        print("name:", result[0], "email:",
              result[1], "money spend:", result[2])


def showDeliveredOrdersByDeliveryBoy(did):
    myquery = """SELECT p.name AS product_name, a.locality, a.pincode, a.state, a.city
FROM product p 
JOIN cart c ON p.pid = c.pid
JOIN payment pm ON c.payid = pm.payid
JOIN address a ON pm.aid = a.aid
JOIN delivery d ON pm.payid = d.payid
WHERE d.did ="""+str(did) +" AND c.status='delivered';"
    myresults = (doquery(myquery))
    for result in myresults:
        print("product name",result[0]," locality",result[1]," pincode ",result[2]," state ",result[3]," city ",result[4]);

def showOnwayOrdersByDeliveryBoy(did):
    myquery = """SELECT p.name AS product_name, a.locality, a.pincode, a.state, a.city
FROM product p 
JOIN cart c ON p.pid = c.pid
JOIN payment pm ON c.payid = pm.payid
JOIN address a ON pm.aid = a.aid
JOIN delivery d ON pm.payid = d.payid
WHERE d.did ="""+str(did) +" AND c.status='onway';"
    myresults = (doquery(myquery))
    cnt=0
    for result in myresults:
        cnt+=1
        print("product name",result[0]," locality",result[1]," pincode ",result[2]," state ",result[3]," city ",result[4]);
    if(cnt==0):
        print("No onway orders")
def acceptOrder(did):
    myquery = """SELECT p.name AS product_name, a.locality, a.pincode, a.state, a.city
FROM product p 
JOIN cart c ON p.pid = c.pid
JOIN payment pm ON c.payid = pm.payid
JOIN address a ON pm.aid = a.aid
JOIN delivery d ON pm.payid = d.payid
WHERE d.did ="""+str(did) +" AND c.status='onway';"
    myresults = (doquery(myquery))
    flag=0
    for result in myresults:
        flag=1
    if(flag==1):
        print("Cannot take new delivery currently")
    else:
        cnt=1
        for i in newdeliveries:
            print(cnt,"-order id-",i);
            cnt+=1
        neworder=int(input())
        myquery = "insert into delivery (payid, did) values (%s, %s);"
        print(newdeliveries[neworder-1])
        vals = (newdeliveries[neworder-1],did)
        insertquery(myquery,vals)
        newdeliveries.pop(neworder-1)

def updateOrderStatus(did):
    myquery="UPDATE Cart SET status ='delivered' WHERE payid in (SELECT payid FROM delivery WHERE did="+str(did)+")"
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="siddis",
        database="MyBasket"
    )
    mycursor = mydb.cursor()
    mycursor.execute(myquery)
    mydb.commit()
    print(mycursor.rowcount, "record(s) affected")

def adddeliveryBoy(n, a, r):
    myquery = "insert into deliveryboy (name, age, rating) values (%s, %s, %s);"
    vals = (n, a, r)
    insertquery(myquery,vals)

def addProduct(rid):
    pname = input("ENTER NAME")
    cid = int(input("ENTER CATEGORY ID"))
    mfd = input("ENTER MFD")
    prating = float(input("ENTER RATING"))
    pquantity = int(input("ENTER QUANTITY"))
    price = int(input("ENTER PRICE"))
    myquery = "insert into Product (catid, rid, price, name, quantity, rating, manufacturingdate) values (%s,%s,%s,%s,%s,%s,%s);"
    vals = (cid, rid, price, pname, pquantity, prating, mfd)
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="siddis",
        database="MyBasket"
    )
    mycursor = mydb.cursor()
    mycursor.execute("START TRANSACTION")
    mycursor.execute(myquery, vals)
    mydb.commit()
    print(mycursor.rowcount , "table updated.")


def showModeOfPayment():
    mop = input("ENTER MODE OF PAYMENT\n")
    myquery = "SELECT c.fname AS customer_fname, c.lname AS customer_lname, p.name AS product_name ,p.price,p.quantity FROM customer c  INNER JOIN cart ct ON c.cid = ct.cid INNER JOIN product p ON ct.pid = p.pid INNER JOIN payment pm ON ct.payid = pm.payid WHERE pm.modeofpayment =" + "\'" + mop + "\'" + ";"
    myresults = (doquery(myquery))
    for result in myresults:
        print(result)

def tax_trigger():
    mytrigger = """
                CREATE TRIGGER add_product_taxes
                BEFORE INSERT ON Product
                FOR EACH ROW
                BEGIN
                    DECLARE nprice int;
                    set nprice = NEW.price;
                    if(nprice<=5000) then set NEW.price = (nprice + (nprice*5)/100);
                    end if;
                    if(nprice>5000 and nprice <=25000)  then set NEW.price = (nprice + (nprice*10)/100);
                    end if;
                    if(nprice>25000 and nprice <100000)  then set NEW.price = (nprice + (nprice*18)/100);
                    end if;
                    if(nprice>100000)  then set NEW.price = (nprice + (nprice*28)/100);
                    end if;
                END;
                """
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="siddis",
        database="MyBasket"
    )
    mycursor = mydb.cursor()
    mycursor.execute(" drop trigger if exists add_product_taxes")
    mycursor.execute(mytrigger)
    mydb.commit()
    print(mycursor.rowcount, "trigger add_product_taxes created.")
    
def add_product_to_cart(proid,quant,custid):
    getprice="SELECT price from product where pid="+str(proid)
    pprice=doquery(getprice)
    myquery = "insert into Cart ( pid, cid, quantity, price) values (%s,%s,%s,%s);"
    vals = (proid,custid,quant,pprice[0][0])
    insertquery(myquery,vals)

def update_trigger():
    mytrigger="""CREATE TRIGGER update_product_quantity
    AFTER INSERT ON orderdetails
    FOR EACH ROW
    BEGIN
      DECLARE proId int; 
      DECLARE proQ int;
      set proId = (SELECT pid from cart where payid=NEW.payid);
      set proQ=(SELECT quantity from cart where payid=NEW.payid);
      UPDATE product SET quantity = quantity - proQ WHERE pid = proId;
      UPDATE cart SET status='onway' where payid=NEW.payid;
    END"""
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="siddis",
        database="MyBasket"
    )
    mycursor = mydb.cursor()
    mycursor.execute(" drop trigger if exists update_product_quantity")
    mycursor.execute(mytrigger)
    mydb.commit()
    print(mycursor.rowcount, "trigger update_product_quantity created.")
def get_aid(customer_id):
    myquery="SELECT aid FROM Address where cid="+str(customer_id)+";";
    results=doquery(myquery);
    return results[0][0]

def checkout_cart(customer_id):
    sizequery="SELECT * FROM Cart"
    sizequeryresult=doquery(sizequery)
    newpayid=0;
    for cart in sizequeryresult:
        if(cart[4]!=None):
            newpayid=cart[4]
    myquery = "SELECT p.pid,c.quantity,c.price FROM product p,cart c ,customer cu WHERE c.status='not delivered' AND c.cid=cu.cid AND cu.cid=" + str(customer_id ) + " AND p.pid=c.pid"
    myresults = (doquery(myquery))
    add_payment_query="insert into Payment (modeofpayment, aid) values (%s, %s);"
    add_orderdetails_query="insert into orderdetails (orderdate, payid) values (%s,%s);"
    mode = input("ENTER MODE OF PAYMENT COD/NETBANKING/NEFT")
    cartValue=0
    for result in myresults:
        cartValue+=(result[1]*result[2])
    if(cartValue<200):
        print("ADD MORE PRODUCT THE AMOUNT IS LESS THAN 200")
    else:
        for cart in myresults:
            newpayid+=1
            newdeliveries.append(newpayid)
            add_payment_vals=(mode,get_aid(customer_id))
            insertquery(add_payment_query,add_payment_vals)
            update_cart_query(customer_id,cart[0],cart[1],newpayid)
            today = date.today()
            add_orderdetails_vals=(today,newpayid)
            insertquery(add_orderdetails_query,add_orderdetails_vals)
        print("YOUR TOTAL ORDER AMOUNT IS ",cartValue)

def olap1():
    myquery="""SELECT modeofpayment,aid,count(*) 
FROM PAYMENT
GROUP BY MODEOFPAYMENT,AID WITH ROLLUP ;"""
    results=doquery(myquery)
    print("payment mode    aid   count")
    for result in results:
        print(result)


def olap2():
    myquery = """SELECT catid, manufacturingDate, count(pid)
FROM PRODUCT
where rating>3 and price<3000
GROUP BY catid, manufacturingDate WITH ROLLUP ;"""
    results = doquery(myquery)
    print("CATID   MFD   COUNT(PID)")
    for result in results:
        print(result)


def olap3():
    myquery = """SELECT State, City, count(aid) as COUNT_OF_CUSTOMERS
FROM ADDRESS where cid between 10 and 2000
GROUP BY State, City WITH ROLLUP;"""
    results = doquery(myquery)
    print("state   city    count of customers")
    for result in results:
        print(result)


def olap4():
    myquery = """SELECT COALESCE(retailer.rid, 'ALL products') as Retailer_ID, catid AS Category_ID, count(*) as COUNT_OF_PRODUCTS
FROM PRODUCT,RETAILER where product.rid = retailer.rid
GROUP BY retailer.rid, catid WITH ROLLUP ;"""
    results = doquery(myquery)
    print("retailer id    category id    count of products")
    for result in results:
        print(result)

def delete_category():
    catid=int(input("ENTER CATEGORY ID TO DELETE"))
    query="DELETE FROM Category WHERE catid="+str(catid)+";"
    runquery(query)

def enter_an_admin():
    admin_input = 1
    while (admin_input != 12):
        print(
            "1-List the total number of orders and the total revenue generated by retailer\n2-customer details with no of orders and total amount spent\n3-top 5 customers who have spent the most on orders\n4-customers and products that were ordered by COD/NEFT/NETBANKING as modeofpayment\n5-delete category \n6-activate tax trigger\n7-activate update cart trigger \n8-olap1 \n 9-olap2\n10-olap3\n11-olap4 \n12-exit")
        admin_input = int(input())
        if (admin_input == 1):
            showRetailerOrdersRevenue()
        elif (admin_input == 2):
            showCustomerTotalOrders()
        elif (admin_input == 3):
            showTop5Customers()
        elif (admin_input == 4):
            showModeOfPayment()
        elif (admin_input == 5):
            delete_category()
        elif (admin_input == 6):
            tax_trigger()
        elif(admin_input==7):
            update_trigger()
        elif(admin_input==8):
            olap1()
        elif (admin_input == 9):
            olap2()
        elif (admin_input == 10):
            olap3()
        elif (admin_input == 11):
            olap4()
        else:
            break

def enter_as_delivery_boy():
    print("1-SIGN UP \n 2-SIGN IN\n 3-EXIT")
    sign_flag = int(input())
    if (sign_flag == 1):
        print("ENTER YOUR DETAILS AS name age rating")
        dname = input()
        dage = int(input())
        drating = int(input())
        if (dage >= 18):
            adddeliveryBoy(dname, dage, drating)
            print("registered") 
    elif (sign_flag == 2):
        did = int(input("ENTER ID: "))
        flag = 1
        while (flag != 5):
            print("1-show delivered orders \n 2-show currently delivering orders \n 3-show order request\n4-update delivery status\n5-exit")
            flag = int(input())
            if (flag == 1):
                showDeliveredOrdersByDeliveryBoy(did)
            elif(flag==2):
                showOnwayOrdersByDeliveryBoy(did)
            elif(flag==3):
                acceptOrder(did)
            elif(flag==4):
                updateOrderStatus(did)
            else:
                break
    else:
        exit()


def enter_as_customer():
    signinp = int(input("1-sign up\n2-sign in\n3-exit\n"))
    if (signinp == 1):
        print("ENTER YOUR DETAILS AS fname mname lname email password number")
        fname = input()
        mname = input()
        lname = input()
        email = (input())
        password = (input())
        num = int(input())
        myquery = "insert into Customer (fname, mname, lname, email, number, password) values ( %s,%s,%s,%s,%s,%s);"
        vals = (fname, mname, lname, email, password, num)
        insertquery(myquery,vals)
    elif (signinp == 2):
        print("ENTER ID AND PASSWORD")
        uid = int(input())
        upassword = (input())
        # check if upassword is correct or not  
        while not checkPassword(uid, upassword):
            print("Invalid id or password. Please enter again:")
            uid = int(input())
            upassword = (input())
        inputflag2 = 1
        while (inputflag2 != 6):
            print("1-select category \n 2-show cart \n3-show past orders\n4-checkout cart \n5-add product to cart\n 6-exit")
            inputflag2 = int(input())
            if (inputflag2 == 1):
                category_input = 1
                while (category_input != 9):
                    print("1-T-shirts \n2-Jeans \n3-Shoes\n4-Shirts\n5-Pants\n6-Jackets\n7-Hoodies\n8-Air purifiers\n9-exit")
                    category_input = int(input())
                    if (category_input >= 9):
                        break
                    else:
                        showProducts(category_input)
            elif (inputflag2 == 2):
                showCart(uid)
            elif (inputflag2 == 3):
                showPastOrder(uid)
            elif(inputflag2==4):
                checkout_cart(uid)
            elif(inputflag2==5):
                proid=int(input("ENTER PRODUCT ID"))
                quant=int(input("ENTER PRODUCT QUANTITY"))
                add_product_to_cart(proid,quant,uid)
            else:
                break
    else:
        exit()

def delete_product():
    id=int(input())
    query="DELETE FROM Product WHERE pid="+str(id)+";"
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="siddis",
        database="MyBasket"
    )
    mycursor = mydb.cursor()
    mycursor.execute(query)
    mydb.commit()
    print(mycursor.rowcount, "record(s) affected")

def update_prod_quantity(did):
    pid=int(input("ENTER PRODUCT ID"))
    quan=int(input("ENTER NEW QUANTITY "))
    query="UPDATE Product SET quantity="+str(quan)+" WHERE pid="+str(pid)+";"
    runquery(query)

def update_retailer_name(did):
    fname=input("ENTER NEW FIRST NAME")
    mname=input("ENTER NEW MIDDLE NAME")
    lname=input("ENTER NEW LAST NAME")
    q1="UPDATE Retailer SET fname="+fname+" WHERE rid="+str(did)+";"
    q2="UPDATE Retailer SET mname="+mname+" WHERE rid="+str(did)+";"
    q3="UPDATE Retailer SET lname="+lname+" WHERE rid="+str(did)+";"
    runquery(q1)
    runquery(q2)
    runquery(q3)

def sign_up_retailer():
    print("ENTER ID AND PASSWORD")
    uid = int(input())
    upassword = (input())
    flag=1
    while(flag!=5):
        print("1-update retailer name \n 2-update product quantity \n3-add product \n4-delete product\n5-exit")
        flag=int(input())
        if(flag==1):
            update_retailer_name(uid)
        elif(flag==2):
            update_prod_quantity(uid)
        if(flag==3):
            addProduct(uid)
        elif(flag==4):
            delete_product()
        else:
            break

def enter_as_retailer():
    flag=1
    while(flag!=3):
        print("1-sign in \n2-sign up \n3-exit")
        flag=int(input())
        # if(flag==1):
            # sign_in_retailer()
        if(flag==2):
            sign_up_retailer()
        else:
            break


inputflag = 1
while (inputflag != 6):
    print("Enter as \n 1-Customer \n 2-Retailer \n 3-Admin \n 4-Delivery Boy \n 5-Employee \n 6-Exit")
    inputflag = int(input())
    if (inputflag == 1):
        enter_as_customer()
    elif(inputflag==2):
        enter_as_retailer()
    elif (inputflag == 3):
        enter_an_admin()
    elif (inputflag == 4):
        enter_as_delivery_boy()
    else:
        break
