import os

from flask import Flask, request, render_template, session
import sqlite3 as sql
from flask_session import Session
from werkzeug.utils import redirect


connection=sql.connect("MovieTicketBooking.db",check_same_thread=False)

listoftheatre=connection.execute("select name from sqlite_master where type='table' AND name='admin'").fetchall()

if listoftheatre!=[]:
    print("Table Exist already")
else:
    connection.execute('''create table admin(
                                ID integer primary key autoincrement,
                                theatre_name text,
                                theatre_pic BLOB,
                                address text,
                                owner_name text,
                                email text,
                                password text
                                )''')
    print("Table created successfully")

theatre1=connection.execute("select name from sqlite_master where type='table' AND name='theatre1'").fetchall()

if theatre1!=[]:
    print("Table Exist already")
else:
    connection.execute('''create table theatre1(
                               ID integer primary key autoincrement,
                               movie_name text,
                               language text,
                               release_date text,
                               seating_arrangement integer,
                               show_time1 text,
                               show_time2 text,
                               show_time3 text,
                               show_time4 text,
                               ticket_price integer,
                               theatre_name text
                               )''')
    print("Theatre-1 Table created successfully")


listofuser = connection.execute("select name from sqlite_master where type='table' AND name='user'").fetchall()

if listofuser!=[]:
    print("Table exist already")
else:
    connection.execute('''create table user(
                             ID integer primary key autoincrement,
                             name text,
                             address text,
                             email text,
                             phone integer,
                             password text                                                      
                             )''')
    print("Table Created Successfully")

ticketbooking = connection.execute("select name from sqlite_master where type='table' AND name='ticketbooking'").fetchall()

if ticketbooking!=[]:
    print("Table exist already")
else:
    connection.execute('''create table ticketbooking(
                             ID integer primary key autoincrement,
                             theatre_name text,
                             movie_name text,
                             show_time text,
                             ticket_count integer,
                             show_date text,                             
                             ticket_price integer,
                             total_price integer,
                             email text                                             
                             )''')
    print("Table Created Successfully")

admin=Flask(__name__)
admin.config["SESSION_PERMANENT"] = False
admin.config["SESSION_TYPE"] = "filesystem"
Session(admin)
admin.config['UPLOAD_FOLDER'] = "static\images"

@admin.route("/",methods=["POST","GET"])
def admin_login():
    if request.method=="POST":
        getadminname=request.form["adminname"]
        getpassword=request.form["password"]
        print(getadminname)
        print(getpassword)
        if getadminname == "admin" and getpassword == "12345":
            return redirect("/addtheatre")
        return render_template("login.html",status=True)
    return render_template("login.html",status=False)

@admin.route("/addtheatre",methods=["POST","GET"])
def add_theatre():
    if request.method=="POST":
        theatreimage=request.files["image"]
        if theatreimage != '':
            filepath=os.path.join(admin.config['UPLOAD_FOLDER'],theatreimage.filename)
            theatreimage.save(filepath)
            gettheatrename=request.form["theatrename"]
            getaddress=request.form["address"]
            getowner=request.form["owner"]
            getemail=request.form["email"]
            getpassword=request.form["password"]
            try:
                cursor=connection.cursor()
                cursor.execute("insert into admin(theatre_name,theatre_pic,address,owner_name,email,password)\
                                   values('"+gettheatrename+"','"+theatreimage.filename+"','"+getaddress+"','"+getowner+"','"+getemail+"','"+getpassword+"')")
                connection.commit()
                print("Theatre added Successfully")
            except Exception as e:
                print(e)

    return render_template("add_theatre.html")

@admin.route("/deletetheatre",methods = ["GET","POST"])
def delete_theatre():
    if request.method == "POST":
        gettheatrename = request.form["theatrename"]
        print(gettheatrename)


        try:
            connection.execute("delete from admin where theatre_name='"+gettheatrename+"'")
            connection.commit()
            print("Theatre Deleted Successfully.")
        except Exception as e:
            print(e)

    return render_template("delete_theatre.html")

@admin.route("/viewtheatre")
def view_theatre():
    cursor=connection.cursor()
    count=cursor.execute("select * from admin")
    result=cursor.fetchall()
    return render_template("view_theatre.html",viewtheatre=result)

@admin.route("/searchtheatre",methods=["POST","GET"])
def search_theatre():
    if request.method == "POST":
        gettheatrename = request.form["theatrename"]
        cursor=connection.cursor()
        count=cursor.execute("select * from admin where theatre_name like '%"+gettheatrename+"%'")
        result=cursor.fetchall()
        return render_template("search_theatre.html",searchtheatre=result)
    return render_template("search_theatre.html")

@admin.route("/updatetheatre",methods = ["GET","POST"])
def update_Theatre():
    if request.method == "POST":
        theatrename = request.form["theatrename"]
        address = request.form["address"]
        owner = request.form["owner"]
        email = request.form["email"]
        password = request.form["password"]
        try:
            query="update admin set theatre_name='"+theatrename+"',address='"+address+"',owner_name='"+owner+"',password='"+password+"' where email='"+email+"'"
            print(query)
            connection.execute(query)
            connection.commit()
            print("Updated Successfully")
            return redirect("/viewtheatre")
        except Exception as e:
            print(e)

    return render_template("update_theatre.html")

@admin.route("/updatesearch",methods = ["GET","POST"])
def update_search_theatre():
    if request.method == "POST":
        getemail=request.form["email"]
        print(getemail)
        cursor = connection.cursor()
        count = cursor.execute("select * from admin where email='"+getemail+"'")
        result = cursor.fetchall()
        print(len(result))
        return render_template("update_theatre.html", updatesearch=result)

    return render_template("update_theatre.html")

@admin.route("/revenue",methods=["POST","GET"])
def view_revenue():
    if request.method == "POST":
        gettheatrename=request.form["theatrename"]
        cursor=connection.cursor()
        count=cursor.execute("select theatre_name,sum(total_price) as total_price from ticketbooking where theatre_name='"+gettheatrename+"'")
        result1=cursor.fetchall()
        return render_template("revenue.html",revenue=result1)
    return render_template("revenue.html")


@admin.route("/ownerlogin",methods=["POST","GET"])
def owner_login():
    if request.method == "POST":
        getemail = request.form["email"]
        getpassword = request.form["password"]
        cursor = connection.cursor()
        query = "select * from admin where email='"+getemail+"' and password='"+getpassword+"'"
        print(query)
        result = cursor.execute(query).fetchall()
        if len(result) > 0:
            for i in result:
                getname=i[1]
                getid=i[0]
                session["name"]=getname
                session["id"]=getid
            return redirect("/ownerpage")
        return render_template("owner_login.html",status=True)
    return render_template("owner_login.html",status=False)

@admin.route("/ownerpage")
def owner_session():
    if not session.get("name"):
        return redirect("/")
    else:
        return render_template("owner_addmovie.html")

@admin.route("/addmovie",methods=["POST","GET"])
def owner_add_movie():
    if request.method == "POST":
        gettheatrename = request.form["theatrename"]
        getmoviename=request.form["moviename"]
        getlanguage=request.form["language"]
        getreleasedate=request.form["releasedate"]
        getseating=request.form["seatingcapacity"]
        getshow1=request.form["show1"]
        getshow2=request.form["show2"]
        getshow3=request.form["show3"]
        getshow4=request.form["show4"]
        getprice=request.form["price"]
        try:
            connection.execute("insert into theatre1(movie_name,language,release_date,seating_arrangement,show_time1,show_time2,show_time3,show_time4,ticket_price,theatre_name)\
                               values('"+getmoviename+"','"+getlanguage+"','"+getreleasedate+"',"+getseating+",'"+getshow1+"','"+getshow2+"','"+getshow3+"','"+getshow4+"',"+getprice+",'"+gettheatrename+"')")
            connection.commit()
            print("Movie Inserted")
        except Exception as e:
            print(e)

    return render_template("owner_addmovie.html")

@admin.route("/viewmovie",methods=["POST","GET"])
def view_all_movies():
    if request.method == "POST":
        gettheatrename = request.form["theatrename"]
        cursor=connection.cursor()
        count=cursor.execute("select t.movie_name,t.language,t.release_date,t.seating_arrangement,t.show_time1,t.show_time2,t.show_time3,t.show_time4,t.ticket_price from theatre1 t JOIN admin a ON t.theatre_name=a.theatre_name where t.theatre_name='"+gettheatrename+"'")
        result=cursor.fetchall()
        return render_template("owner_viewmovie.html",viewallmovie=result)
    return render_template("owner_viewmovie.html")

@admin.route("/deletemovie",methods=["POST","GET"])
def delete_movie():
    if request.method == "POST":
        getmoviename=request.form["moviename"]
        try:
            connection.execute("delete from theatre1 where movie_name='"+getmoviename+"'")
            connection.commit()
            print("Deleted Movie")
        except Exception as e:
            print(e)
    return render_template("owner_deletemovie.html")

@admin.route("/updatemovie",methods=["POST","GET"])
def update_movie():
    if request.method == "POST":
        gettheatrename = request.form["theatrename"]
        getmoviename = request.form["moviename"]
        getlanguage = request.form["language"]
        getreleasedate = request.form["releasedate"]
        getseating = request.form["seatingcapacity"]
        getshow1 = request.form["show1"]
        getshow2 = request.form["show2"]
        getshow3 = request.form["show3"]
        getshow4 = request.form["show4"]
        getprice = request.form["price"]
        try:
            query="update theatre1 set movie_name='"+getmoviename+"',language='"+getlanguage+"',release_date='"+getreleasedate+"',seating_arrangement="+getseating+",show_time1='"+getshow1+"',show_time2='"+getshow2+"',show_time3='"+getshow3+"',show_time4='"+getshow4+"',ticket_price="+getprice+" where theatre_name='"+gettheatrename+"'"
            print(query)
            connection.execute(query)
            connection.commit()
            print("Updated Successfully")
            return redirect("/viewmovie")
        except Exception as e:
            print(e)

    return render_template("owner_updatemovie.html")

@admin.route("/updatemoviesearch",methods = ["GET","POST"])
def update_search_Movie():
    if request.method == "POST":
        gettheatrename = request.form["theatrename"]
        getpassword = request.form["password"]
        print(gettheatrename)
        print(getpassword)
        cursor = connection.cursor()
        count = cursor.execute("select t.theatre_name,t.movie_name,t.language,t.release_date,t.seating_arrangement,t.show_time1,t.show_time2,t.show_time3,t.show_time4,t.ticket_price from theatre1 t JOIN admin a ON t.theatre_name=a.theatre_name where t.theatre_name='"+gettheatrename+"' and password='"+getpassword+"'")
        result = cursor.fetchall()
        print(len(result))
        return render_template("owner_updatemovie.html", updatemovies=result)

    return render_template("owner_updatemovie.html")

@admin.route("/userregistration",methods=["POST","GET"])
def user_registration_details():
    if request.method == "POST":
        getname=request.form["name"]
        getaddress=request.form["address"]
        getemail=request.form["email"]
        getphone=request.form["phone"]
        getpassword=request.form["password"]
        print(getemail)
        print(getpassword)
        try:
            connection.execute("insert into user(name,address,email,phone,password)\
                                   values('" + getname + "','" + getaddress + "','" + getemail + "'," + getphone + ",'" + getpassword + "')")
            connection.commit()
            print("User Data Added Successfully.")
        except Exception as e:
            print(e)

        return redirect("/userlogin")

    return render_template("user_registration.html")

@admin.route("/userlogin",methods=["POST","GET"])
def user_login():
    global result
    if request.method == "POST":
        getemail = request.form["email"]
        getpassword = request.form["password"]
        cursor = connection.cursor()
        query = "select * from user where email='"+getemail+"' and password='"+getpassword+"'"
        print(query)
        result = cursor.execute(query).fetchall()
        if len(result) > 0:
            for i in result:
                getname=i[1]
                getid=i[0]
                session["name"]=getname
                session["id"]=getid

            return redirect("/userhome")
        return render_template("user_login.html",status=True)
    return render_template("user_login.html",status=False)

@admin.route("/session")
def user_session():
    if not session.get("name"):
        return redirect("/userlogin")
    else:
        return render_template("user_home.html")

@admin.route("/userhome")
def user_home():
    cursor = connection.cursor()
    count = cursor.execute("select theatre_pic,theatre_name from admin")
    result = cursor.fetchall()
    return render_template("user_home.html", theatre=result)

@admin.route("/searchmovie",methods=["POST","GET"])
def user_search_movies():
    if request.method == "POST":
        getmoviename = request.form["moviename"]
        cursor=connection.cursor()
        count=cursor.execute("select ID,theatre_name,seating_arrangement,ticket_price from theatre1 where movie_name like '%"+getmoviename+"%'")
        result=cursor.fetchall()
        return render_template("user_searchmovie.html",searchmovie=result)
    return render_template("user_searchmovie.html")

@admin.route("/userupdate",methods=["GET","POST"])
def edit_profile():
    if request.method == "POST":
        getemail = request.form["email"]
        getname = request.form["name"]
        getaddress = request.form["address"]
        getphone = request.form["phone"]
        getpassword = request.form["password"]
        try:
            query="update user set name='"+getname+"',address='"+getaddress+"',phone="+getphone+",password='"+getpassword+"'  where email='"+getemail+"'"
            print(query)
            connection.execute(query)
            connection.commit()
            print("Updated Successfully")
        except Exception as e:
            print(e)

    return render_template("user_update.html")

@admin.route("/userupdatesearch",methods = ["GET","POST"])
def update_search_patient():
    if request.method == "POST":
        getemail=request.form["email"]
        print(getemail)
        cursor = connection.cursor()
        count = cursor.execute("select * from user where email='"+getemail+"'")
        result = cursor.fetchall()
        print(len(result))
        return render_template("user_update.html", userupdate=result)

    return render_template("user_update.html")

@admin.route("/bookmyshow")
def BookMyShow():
        getid = request.args.get('id')
        cursor=connection.cursor()
        count=cursor.execute("select theatre_name,movie_name,seating_arrangement,show_time1,show_time2,show_time3,show_time4,ticket_price from theatre1 where ID="+getid)
        result=cursor.fetchall()
        return render_template("user_bookmyshow.html",searchmovie=result)

@admin.route("/popupbookmyshow",methods=["POST","GET"])
def popup_bookmyshow():
    if request.method == "POST":
        gettheatrename=request.form["theatrename"]
        getmoviename=request.form["moviename"]
        getshowtime=request.form["showtime"]
        getticketcount=request.form["ticketcount"]
        getintcount=int(getticketcount)
        getshowdate=request.form["showdate"]
        getticketprice=request.form["ticketprice"]
        getprice=int(getticketprice)
        getemail=request.form["email"]
        gettotalprice=((getprice)*(getintcount))
        totalprice=str(gettotalprice)
        print(totalprice)
        print(getshowtime)
        print(getticketcount)
        print(getshowdate)
        try:
            connection.execute("insert into ticketbooking(theatre_name,movie_name,show_time,ticket_count,show_date,ticket_price,email,total_price)\
                                       values('" + gettheatrename + "','"+getmoviename+"','"+getshowtime+"',"+getticketcount+",'"+getshowdate+"',"+getticketprice+",'"+getemail+"',"+totalprice+")")
            connection.commit()
            print("Ticket Booked Successfully.")
            return redirect("/userpayment")
        except Exception as e:
            print(e)

    return render_template("user_bookmyshow.html")

@admin.route("/viewtickethistory",methods=["POST","GET"])
def view_ticket_booking_history():
    if request.method == "POST":
        getemail=request.form["email"]
        cursor=connection.cursor()
        count=cursor.execute("select * from ticketbooking where email='"+getemail+"'")
        result1=cursor.fetchall()
        return render_template("view_tickethistory.html",viewhistory=result1)
    return render_template("view_tickethistory.html")

@admin.route("/userpayment")
def payment():
    return render_template("user_payment.html")


@admin.route("/cancelticket")
def cancel_ticket():
    getid = request.args.get('id')
    cursor = connection.cursor()
    count = cursor.execute("delete from ticketbooking where ID='"+getid+"'")
    connection.commit()
    print("Ticket Cancelled")
    return render_template("view_tickethistory.html")


if __name__=="__main__":
    admin.run()

