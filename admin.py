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

if __name__=="__main__":
    admin.run()
