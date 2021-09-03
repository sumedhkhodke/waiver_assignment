import sqlite3
from utils import pre_process
import os, sys
try:
    import tabulate
except Exception as e:
    print(str(e))
    print("PLEASE CHECK THE README.md FOR STEPS and req.txt FOR DEPENDENCIES AND INSTALL THEM")
    sys.exit()

def create_connection(db_file, delete_db=False):
    '''
    This function creates connection with SQL database using sqlite3
    '''
    if delete_db and os.path.exists(db_file):
        os.remove(db_file)
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.execute("PRAGMA foreign_keys = 1")
    except Exception as e:
        print(e)
        print("Error in db connection")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
    return conn

def create_table(conn, create_table_sql):
    '''
    Common function to create all tables using sqlite3 : Degrees, Exams, Students, StudentExamScores
    '''
    try:
        c = conn.cursor()
        # print(create_table_sql)
        c.execute(create_table_sql)
        return "Table created successfully."
    except Exception as e:
        print(e)
        print("Error in table creation")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
        raise

def insert_into_table(conn, values, sql_query):
    '''
    Common function to insert values into all tables using sqlite3 : Degrees, Exams, Students, StudentExamScores
    '''
    try:
        cur = conn.cursor()
        cursor_1 = cur.executemany(sql_query,values)
        return "Inserted successfully."
    except Exception as e:
        print(e)
        print("Error in inserting values in table")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
        raise

def run_query(conn, sql_query):
    '''
    Common function to run select queries on all tables using sqlite3 : Degrees, Exams, Students, StudentExamScores
    '''
    try:
        curr = conn.cursor()
        c = curr.execute(sql_query)
        column_names = [x[0] for x in c.description]
        rows = c.fetchall()
        print(tabulate.tabulate(rows, headers=column_names, tablefmt='psql'))
        return column_names, rows
    except Exception as e:
        print(e)
        print("Error on running query in table")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
        raise

def commit():
    '''
    Function to commit inserted values into the tables of the database
    '''
    conn.commit()

db_file = 'normalized.db'
conn = create_connection(db_file, True)

with conn:
    sql_create_degrees_table = """ CREATE TABLE IF NOT EXISTS Degrees (
        Degree TEXT PRIMARY KEY
    ); """
    sql_create_exams_table = """ CREATE TABLE IF NOT EXISTS Exams (
        Exam TEXT PRIMARY KEY,
        Year INTEGER 
    );"""
    sql_create_students_table = """ CREATE TABLE IF NOT EXISTS Students (
        StudentID INT PRIMARY KEY,
        First_Name TEXT,
        Last_Name TEXT,
        Degree TEXT,
        FOREIGN KEY(Degree) REFERENCES Degrees(Degree)
    );"""
    sql_create_studentexamscores_table = """ CREATE TABLE IF NOT EXISTS StudentExamScores (
        PK INT PRIMARY KEY,
        StudentID INT,
        Exam TEXT,
        Score INT,
        FOREIGN KEY(StudentID) REFERENCES Students(StudentID),
        FOREIGN KEY(Exam) REFERENCES Exams(Exam)
    );"""
    #Note: PK can also be autoincremented but here it has been explicitly declared during preprocessing steps

    create_table(conn, sql_create_degrees_table)
    create_table(conn, sql_create_exams_table)
    create_table(conn, sql_create_students_table)
    create_table(conn, sql_create_studentexamscores_table)

    commit()

    sql_insert_degrees = " INSERT INTO Degrees(Degree) VALUES(?) "
    sql_insert_exams = " INSERT INTO Exams(Exam,Year) VALUES(?,?)"
    sql_insert_students = " INSERT INTO Students(StudentID,First_Name,Last_Name,Degree) VALUES(?,?,?,?)"
    sql_insert_studentexamscores = " INSERT INTO StudentExamScores(PK,StudentID,Exam,Score) VALUES(?,?,?,?)"
    
    #preprocessing results coming from the pre_process function of the utils file
    #degrees -> Degrees table : Columns [(Degree,)]
    #exams -> Exams table : Columns [(Exam, Year)]
    #students -> Students table : Columns [(StudentID, First_Name, Last_Name, Degree)]
    #studentExamScoresList -> StudentExamScores table : Columns [(PK, StudentID, Exam, Score)]
    degrees, exams, students, studentExamScoresList = pre_process()
    
    insert_into_table(conn, degrees, sql_insert_degrees)
    insert_into_table(conn, exams, sql_insert_exams)
    insert_into_table(conn, students, sql_insert_students)
    insert_into_table(conn, studentExamScoresList, sql_insert_studentexamscores)

    commit()

    # Question 1
    # Write an SQL statement that selects all rows from the `Exams` table and sorts the exams by year and then exam name
    # Output columns: exam, year
    query_1 = " SELECT * from Exams ORDER BY Year, Exam;"
    print("Answer #1")
    query_1_results = run_query(conn, query_1)

    # Question 2:
    # Write an SQL statement that selects all rows from the `Degrees` table and sorts the degrees by name
    # Output column: degree
    query_2 = " SELECT * from Degrees ORDER BY Degree ;"
    print("\n")
    print("Answer #2")
    query_2_results = run_query(conn, query_2)

    # Question 3:
    # Write an SQL statement that counts the numbers of graduate and undergraduate students
    # # Output columns: degree, count_degree
    query_3 = " SELECT Degree, COUNT(Degree) as Count from Students GROUP BY Degree;"
    print("\n")
    print("Answer #3")
    query_3_results = run_query(conn, query_3)

    # Question 4:
    # Write an SQL statement that calculates the exam averages for exams and sort by the averages in descending order.
    # Output columns: exam, year, average
    # round to two decimal places
    query_4 = """ SELECT Exams.Exam, Year, ROUND(AVG(Score),2) as average 
                from Exams 
                INNER JOIN StudentExamScores 
                where Exams.Exam = StudentExamScores.Exam 
                GROUP BY Exams.Exam 
                ORDER BY average DESC """
    print("\n")
    print("Answer #4")
    query_4_results = run_query(conn, query_4)

    # Question 5:
    # Write an SQL statement that calculates the exam averages for degrees and sorts by average in descending order.
    # Output columns: degree, average 
    # round to two decimal places
    query_5 = """ SELECT Degree, ROUND(AVG(Score),2) as average 
                from Students 
                INNER JOIN StudentExamScores as b 
                where Students.StudentId = b.StudentId 
                GROUP BY Degree 
                ORDER BY average DESC;"""
    print("\n")
    print("Answer #5")
    query_5_results = run_query(conn, query_5)

    # Question 6:
    # Write an SQL statement that calculates the exam averages for students and sorts by average in descending order. Show only the top 10 students.
    # Output columns: first_name, last_name, degree, average
    # round to two decimal places
    query_6 = """SELECT First_Name, Last_Name, Degree, ExamAverage as average 
                from Students 
                INNER JOIN (SELECT StudentId, AVG(Score) as ExamAverage 
                            from StudentExamScores 
                            GROUP BY StudentId 
                            ORDER BY ExamAverage 
                            DESC LIMIT 10) 
                            as b 
                where Students.StudentId = b.StudentId;"""
    print("\n")
    print("Answer #6")
    query_6_results = run_query(conn, query_6)
    print("\n")

conn.close()