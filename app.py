from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# My App
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)
Scss(app)


# Database: Data Class ~ Row of data
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Task {self.id}"


with app.app_context():
    db.create_all()


# Routes to Webpages
@app.route("/")  # Home Page
def index():
    return render_template("index.html")  # returns the chosen webpage to the link


@app.route("/about")  # About Page
def about():
    return render_template("about.html")


@app.route("/new")  # New Page
def new():
    return render_template("new.html")


@app.route("/project")  # Project Page
def project():
    return render_template("project.html")


@app.route("/contact")  # Contact Page
def contact():
    return render_template("contact.html")


@app.route("/notes", methods=["POST","GET"])  # Home Page
def notes():
    if request.method == "POST":  # Adding a User Input to the database
        # Name
        current_task = request.form['content']
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/notes")
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}"
    else:  # See all current tasks
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template("notes.html", tasks=tasks)  # returns the chosen webpage to the link


@app.route("/delete/<int:id>")  # Delete an Item
def delete(id:int):
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/notes")
    except Exception as e:
        print(f"ERROR:{e}")
        return f"ERROR:{e}"


@app.route("/edit/<int:id>", methods=["GET", "POST"])  # Edit an Item
def edit(id:int):
    task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/notes")
        except Exception as e:
            return f"ERROR:{e}"
    else:
        return render_template("edit.html", task=task)


if __name__ == "__main__":
    app.run(debug=True)
