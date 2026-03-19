from flask import Flask, request, render_template
import server4_students 


app = Flask(__name__)


def api_call(controler, *args):
    try:
        result = controler(*args)
        if result is None:
            return {"success": False, "error": "Student not found"}, 404
        return {"success": True, "result": result}, 200
    except TypeError as e:
        return {"success": False, "error": str(e)}, 400
    except NotImplementedError as e:
        return {"success": False, "error": str(e)}, 501
    
def html_call(template, controller, *args):
    try:
        result = controller(*args)
        if result is None:
            return render_template('error.html', code=404, message='Student not found'), 404
        return render_template(template, data=result), 200
    except TypeError as e:
        return render_template('error.html', code=400, error=str(e)), 400
    except NotImplementedError as e:
        return render_template('error.html', code=501, error=str(e)), 501
    
@app.route('/students')
def get_students():
    return api_call(server4_students.get_all)

@app.route('/students/<id>')
def get_student(id):
    return api_call(server4_students.get_student, id)

@app.route('/student_list', methods=['GET', 'POST'])
def get_students_list():
    if request.method == 'POST':
        if request.form.get('delete_id'):
            id = request.form.get('delete_id')
            try:
                server4_students.delete_student(int(id))
            except Exception as e:
                return render_template('error.html', code=500, message='Deleting error: '+str(e))
        elif request.form.get('edit_id'):
            id = request.form.get('edit_id')
            student_name = request.form.get('student_name')
            student_age = request.form.get('student_age')
            student = {'name': student_name, 'age': int(student_age)}
            try:
                server4_students.edit_student(id, student)
            except Exception as e:
                return render_template('error.html', code=500, message='Saving error: '+str(e))
        else:
            student_name = request.form.get('student_name')
            student_age = request.form.get('student_age')
            student = {'name': student_name, 'age': int(student_age)}
            try:
                server4_students.add_student(student)
            except:
                return render_template('error.html', code=500, message='Saving error')
    return html_call('student_list.html', server4_students.get_all)

@app.route('/student_profile/<id>')
def get_student_profile(id):
    return html_call('student_profile.html', server4_students.get_student, id)

@app.route('/add_student')
def add_student_page():
    return render_template('student_edit.html')

@app.route('/edit_student')
def edit_student_page():
    id = request.args.get('edit_id')
    student = server4_students.get_student(id)
    if student is None:
        return render_template('error.html', code=404, message='Student not found'), 404
    return render_template('student_edit.html', id=id, name=student['name'], age=student['age'])

@app.route('/students', methods=['POST'])
def add_student():
    student = request.get_json() or {}
    return api_call(server4_students.add_student, student)

@app.route('/students/<id>', methods=['PUT'])
def edit_student(id):
    student = request.get_json() or {}
    return api_call(server4_students.edit_student, id, student)

@app.route('/students/<id>', methods=['DELETE'])
def delete_student(id):
    return api_call(server4_students.delete_student, id)    


if __name__ == '__main__':
    app.run(port=5000, debug=True)   