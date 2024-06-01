from flask import * 
from sqlite3 import * 
import pickle

app=Flask(__name__)
app.secret_key="kamalsir"

@app.route("/",methods=["GET", "POST"] )
def home():
	if request.method =="POST":
		session.pop("un")
		return redirect(url_for("login"))

	if "un" in session:
		return render_template("home.html", m=session["un"])
	else:
		return redirect(url_for("login"))

@app.route("/login",methods=["GET","POST"])
def login():
	if "un" in session:
		return redirect(url_for("home"))
	if request.method=="POST":
		un = request.form["un"]
		pw= request.form["pw"]
		con=None
		try:
			con=connect("kc.db")
			cursor=con.cursor()
			sql="select * from users where un='%s' and pw='%s'"	
			cursor.execute(sql%(un,pw))
			data=cursor.fetchall()	
			if len(data) == 0:
				return render_template("login.html",m="invalid username/password")
			else:
				session["un"] = un
				return redirect(url_for("home"))
		except Exception as e:
			return render_template("signup.html",m="issue" + str(e))
		finally:
			if con is not None:
				con.close()
	else:
		return render_template("login.html")
	

@app.route("/signup",methods=["GET" , "POST"])
def signup():
	if "un" in session:
		return redirect(url_for("home"))
	if request.method == "POST":
		un = request.form["un"]
		pw1= request.form["pw1"]
		pw2=request.form["pw2"]
		if pw1 == pw2:
			con = None
			try:
				con=connect("kc.db")
				cursor=con.cursor()
				sql="insert into users values('%s','%s')"
				cursor.execute(sql%(un,pw1))
				con.commit()
				return redirect(url_for("login"))
			except Exception as e:
				con.rollback()
				return render_template("signup.html" , m="user already exists")
			finally:
				if con is not None:
					con.close()
		else:
			return render_template("signup.html" , m="password didnt match")
	else:
		return render_template("signup.html")

@app.route("/checkup", methods=["GET" , "POST"])
def checkup():
	if "un" in session:
		if request.method=="POST":
			f=open("db.model","rb")
			model = pickle.load(f)
			f.close()
			rm=float(request.form["rm"])
			tm=float(request.form["tm"])
			pm=float(request.form["pm"])
			am=float(request.form["am"])
			sm=float(request.form["sm"])
			com=float(request.form["com"])
			conm=float(request.form["conm"])
			concm=float(request.form["concm"])
			sym=float(request.form["sym"])
			fdm=float(request.form["fdm"])
	
			d=[[rm,tm,pm,am,sm,com,conm,concm,sym,fdm]]
			result = model.predict(d)

			return render_template("checkup.html",m=result[0])
		else:
			return render_template("checkup.html")
	else:
		return redirect(url_for("login"))

@app.route("/changepass" , methods=["GET","POST"])
def changepass():	
	if "un" in session:
		if request.method=="POST":
			un = request.form["un"]	
			pw3= request.form["pw3"]
			pw4=request.form["pw4"]
			if session["un"] == un:
				con = None
				con=connect("kc.db")
				cursor=con.cursor()
				query = "DELETE from users where un= un"
				cursor.execute(query)			
				con.commit()
				if pw3 == pw4:
					sql="insert into users values('%s','%s')"
					cursor.execute(sql%(un,pw3))			
					con.commit()
					session.pop("un")
					return redirect(url_for("login"))
					if con is not None:
						con.close()
				else:
					return render_template("changepass.html" , msg="password didnt match")
			else:
				return render_template("changepass.html" , msg="User Does not Exists")
		else:
			return render_template("changepass.html")
	else:
		return redirect(url_for("login"))




if __name__ == "__main__":
	app.run(debug=True , use_reloader=True)
			
		
	