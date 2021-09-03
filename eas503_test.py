"""
------------
INSTRUCTIONS
------------

The file 'Students.csv' contains a dump of a non-normalized database. Your assignment is to first normalize the database
and then write some SQL queries.

To normalize the database, create the following four tables in sqlite3 and populate them with data from 'Students.csv'.

1) Degrees table has one column:
    [Degree] column is the primary key

2) Exams table has two columns:
    [Exam] column is the primary key column
    [Year] column stores the exam year

3) Students table has four columns:
    [StudentID] primary key column 
    [First_Name] stores first name
    [Last_Name] stores last name
    [Degree] foreign key to Degrees table
    
4) StudentExamScores table has four columns:
    [PK] primary key column,
    [StudentID] foreign key to Students table,
    [Exam] foreign key to Exams table ,
    [Score] exam score


Call the normalized database: 'normalized.db'.

Q1:
Write an SQL statement that selects all rows from the `Exams` table and sorts the exams by year and then exam name
Output columns: exam, year

Q2:
Write an SQL statement that selects all rows from the `Degrees` table and sorts the degrees by name
Output column: degree

Q3:
Write an SQL statement that counts the numbers of gradate and undergraduate students
Output columns: degree, count_degree

Q4:
Write an SQL statement that calculates the exam averages for exams and sort by the averages in descending order.
Output columns: exam, year, average
round to two decimal places

Q5:
Write an SQL statement that calculates the exam averages for degrees and sorts by average in descending order.
Output columns: degree, average 
round to two decimal places

Q6:
Write an SQL statement that calculates the exam averages for students and sorts by average in descending order. Show only the top 10 students.
Output columns: first_name, last_name, degree, average
round to two decimal places


More instructions:
1) All work must be done in Python.
2) You CANNOT use 'pandas'.
3) You CANNOT use the 'csv' module to read the file
3) All SQL queries must be executed through Python.
4) Neatly print the output of the SQL queries using Python.

Hint:
Ensure to strip all strings so there is no space in them
"""


