from typing import List
from college import Student, Course
import utils

def calculate_gpa(student: Student, courses: List[Course]) -> float:
    '''
    This function takes a student and a list of course
    It should compute the GPA for the student
    The GPA is the sum(hours of course * grade in course) / sum(hours of course)
    The grades come in the form: 'A+', 'A' and so on.
    But you can convert the grades to points using a static method in the course class
    To know how to use the Student and Course classes, see the file "college.py"  
    '''

    count_of_courses=len(courses)
    id = student.id
    hours_total=0
    gpa : float = 0
    for i in range(count_of_courses) :
        hours = courses[i].hours 
        if id in courses[i].grades:
            points = Course.convert_grade_to_points((courses[i].grades)[id])
            hours_total+=hours
        else:
         points = 0
        gpa += hours * points 
    
    if gpa > 0: #3shan testcase (division of zero)
        return (gpa / hours_total)
    
    return 0




# Student1 = Student('1105', 'Ahmed')
# course1 = [Course('CMPN402', 'MI', 3, {'1105':'A', '1203':'B'}), Course('CMPN205', 'CG', 2, {'1105':'B', '1203':'A'}), Course('CMPN666', 'AHS', 2, {'1203':'D'})]
# print(calculate_gpa(Student1,course1))


