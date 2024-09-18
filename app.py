from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    class_ = db.Column(db.String(50), nullable=False)
    section = db.Column(db.String(50), nullable=False)
    roll_no = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Student {self.name}>"

@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form['name']
    class_ = request.form['class']
    section = request.form['section']
    roll_no = request.form['roll_no']

    new_student = Student(name=name, class_=class_, section=section, roll_no=roll_no)
    db.session.add(new_student)
    db.session.commit()

    return redirect('/')

@app.route('/search_student', methods=['POST'])
def search_student():
    name = request.form['name']
    student = Student.query.filter_by(name=name).first()

    if student:
        return render_template('student_details.html', student=student)
    else:
        students = Student.query.all()
        return render_template('index.html', students=students, message="Student not found.")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)