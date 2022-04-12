from flask import Flask, request, render_template
import sqlite3 as sql

from werkzeug.utils import redirect

connection=sql.connect("MovieTicketBooking.db",check_same_thread=False)

listoftheatre=connection.execute("select name from sqlite_master where type='table' AND name='admin'").fetchall()

if listoftheatre!=[]:
    print("Table Exist already")
else:
    connection.execute('''create table admin(
                                ID integer primary key autoincrement,
                                theatre_name text,
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
                               ticket_price text
                               )''')
    print("Theatre-1 Table created successfully")

admin=Flask(__name__)

@admin.route("/",methods=["POST","GET"])
def admin_login():
    if request.method=="POST":
        getadminname=request.form["adminname"]
        getpassword=request.form["password"]
        print(getadminname)
        print(getpassword)
        if getadminname == "admin" and getpassword == "12345":
            return redirect("/addtheatre")
    return render_template("login.html")

@admin.route("/addtheatre",methods=["POST","GET"])
def add_theatre():
    if request.method=="POST":
        gettheatrename=request.form["theatrename"]
        getaddress=request.form["address"]
        getowner=request.form["owner"]
        getemail=request.form["email"]
        getpassword=request.form["password"]
        try:
            connection.execute("insert into admin(theatre_name,address,owner_name,email,password)\
                               values('"+gettheatrename+"','"+getaddress+"','"+getowner+"','"+getemail+"','"+getpassword+"')")
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
            Flask("Deleted Successfully")
        except Exception as e:
            print(e)

    return render_template("delete_theatre.html")

@admin.route("/viewtheatre")
def view_theatre():
    cursor=connection.cursor()
    count=cursor.execute("select * from admin")
    result=cursor.fetchall()
    return render_template("view_theatre.html",viewtheatre=result)

@admin.route("/updatetheatre",methods = ["GET","POST"])
def update_patient():
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


if __name__=="__main__":
    admin.run()

