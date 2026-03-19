
from server4_sql import connect, students_table

students = {}
id_count = 1


def raw_to_dict(raw):
     id,name,age = raw
     return {"id": id, "name": name, "age": age}

def get_all():
    with connect() as conn:
        students_table(conn)
        students_raw = conn.execute('''SELECT ID, name, age FROM students;''').fetchall()
        students = [raw_to_dict(student) for student in students_raw]
        return students

def get_student(id):

    with connect() as conn:
        students_table(conn)
        student_raw = conn.execute('''SELECT ID, name, age FROM students WHERE id=?;''', (id,)).fetchone()
        if student_raw is None:
            return None
        return raw_to_dict(student_raw)
   

def add_student(student):
    if "name" not in student or "age" not in student:
           raise TypeError("Missing proprieretis") 
    elif type(student["name"]) != str or type(student["age"]) != int:
           raise TypeError("Invalid proprieretis")  
    elif len(student) > 2:  
           raise TypeError("redundent proprieretis")
    
    with connect() as conn:
        students_table(conn)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO students (name, age) VALUES (?, ?);''', (student["name"], student["age"]))
        student_id = cursor.lastrowid
        conn.commit()
        return get_student(student_id)


def delete_student(id):
     
     with connect() as conn:
         students_table(conn)
         to_delete = get_student(id)
         if to_delete is None:
             return None
         cursor = conn.cursor()
         cursor.execute('''DELETE FROM students WHERE ID=?;''', (id,))
         conn.commit()
         return to_delete

def edit_student(id, edit_student):
     if type(edit_student.get("name", "")) != str or type(edit_student.get("age", 0)) != int:
         raise TypeError("Invalid proprieretis")
     if "name" not in edit_student and "age" not in edit_student:
         raise TypeError("Missing proprieretis")
     if len(edit_student) == 2 and ("name" not in edit_student or "age" not in edit_student) or len(edit_student) > 2:
         raise TypeError("too many proprieretis")
     with connect() as conn:    
        students_table(conn)
        cursor = conn.cursor()
        query = "UPDATE students SET "
        parameters = []
        sets = []
        for key in edit_student:
             sets.append(f'{key} = ?')
             parameters.append(edit_student[key])
        query += ', '.join(sets) + " WHERE id = ?;"
        parameters.append(id)
        cursor.execute(query, tuple(parameters))
        conn.commit()
        return get_student(id)




