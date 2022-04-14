from flask import Flask, request, render_template, session, flash
import sqlite3 as sql
from flask_session import Session
from werkzeug.utils import redirect

connection=sql.connect("MovieTicketBooking.db",check_same_thread=False)

owner=Flask(__name__)
owner.config["SESSION_PERMANENT"] = False
owner.config["SESSION_TYPE"] = "filesystem"
Session(owner)

@owner.route("/",methods=["POST","GET"])
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
    return render_template("owner_login.html")

@owner.route("/ownerpage")
def owner_session():
    if not session.get("name"):
        return redirect("/")
    else:
        return render_template("owner_addmovie.html")

@owner.route("/addmovie",methods=["POST","GET"])
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

@owner.route("/viewmovie",methods=["POST","GET"])
def view_all_movies():
    if request.method == "POST":
        gettheatrename = request.form["theatrename"]
        cursor=connection.cursor()
        count=cursor.execute("select t.movie_name,t.language,t.release_date,t.seating_arrangement,t.show_time1,t.show_time2,t.show_time3,t.show_time4,t.ticket_price from theatre1 t JOIN admin a ON t.theatre_name=a.theatre_name where t.theatre_name='"+gettheatrename+"'")
        result=cursor.fetchall()
        return render_template("owner_viewmovie.html",viewallmovie=result)
    return render_template("owner_viewmovie.html")

@owner.route("/deletemovie",methods=["POST","GET"])
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

@owner.route("/updatemovie",methods=["POST","GET"])
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

@owner.route("/updatemoviesearch",methods = ["GET","POST"])
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

if __name__=="__main__":
    owner.run()