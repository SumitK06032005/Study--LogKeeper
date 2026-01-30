# Imports
from flask import Flask, render_template, request, redirect
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime

# App
app = Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

class Subjects(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    sub_name = db.Column(db.String(25),nullable=False)
    created_on = db.Column(db.DateTime, nullable = False,default=datetime.now)

    def __repr__(self):
        return f"Subject {self.id}"


class Timeline(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(200))
    Day_of_task = db.Column(db.DateTime,nullable=False,default=datetime.now)

    def __repr__(self):
        return f"Task {self.id}"

@app.route("/",methods=["POST","GET"]) # Creates a route to the main page with the url being /
# The first webpage of our app - index
def index():
    # Add new subject to the list of subjects
    if request.method=="POST":
        current_subj = request.form['subject']
        new_subject = Subjects(sub_name=current_subj)

        try:
            db.session.add(new_subject)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR: {e}")
            return f"ERROR: {e}"
    
    # See all the subjects
    else :
        subjects = Subjects.query.order_by(Subjects.created_on).all()
        return render_template("index.html", subjects = subjects)

@app.route("/Subjects/<int:id>",methods=["POST","GET"])
def timeline(id:int):
    e = id
    if request.method == "POST":
        curr_task = request.form['task']
        new_task = Timeline(content=curr_task)

        try :
            db.session.add(new_task)
            db.session.commit()
            return redirect(f"/Subjects/{e}")
        except Exception as e:
            print(f"ERROR:{e}")
    
    else:
        subject = Subjects.query.get_or_404(id)
        timeline = Timeline.query.order_by(desc(Timeline.Day_of_task)).all()
        return render_template("timeline.html",subject = subject,timeline = timeline)


@app.route("/delete/<int:id>")
def delete(id:int):
    delete_subj = Subjects.query.get_or_404(id)
    try:
        db.session.delete(delete_subj)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        print(f"ERROR:{e}")

@app.route("/deleteTask/<int:id1>/<int:id2>")
def deleteTask(id1:int,id2:int):
    e = id1
    delete_task = Timeline.query.get_or_404(id2)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect(f"/Subjects/{e}")
    except Exception as e:
        print(f"ERROR:{e}")

if __name__ in "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)