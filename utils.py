import re, os, sys
filepath = "Students.csv"

def pre_process():
    '''
    Function to read and preprocess the dataset
    
    Returns:
    degrees -> type list -> Degrees table : Degree
    exams -> type list -> Exams table : Exam, Year
    students -> type list -> Students table : StudentID, First_Name, Last_Name, Degree
    studentExamScoresList -> type list -> StudentExamScores table : PK, StudentID, Exam, Score
    '''
    try:
        with open(filepath) as f:
            lines = [line.rstrip().split('\t') for line in f]
            headers = lines.pop(0)
            examYearDict = {}
            degrees = set()
            exams = set()
            students = []
            studentIDSet = set()
            studentExamScoresList = []
            id = 0
            for line in lines:
                #unique degree names table
                degrees.add(line[2])
                # print(degrees)

                #exam and year table
                examWithyear = [x.lstrip() for x in line[-2].split(',')]
                examNameList = []
                for x in examWithyear:
                    examName = x.split(' ')[0]
                    examYear = x.split(' ')[1]
                    a = re.search(r"\((\d+)\)", examYear)
                    examYear = a.group(1)
                    exams.add((examName, examYear))
                    examNameList.append(examName)
                # print(exams)

                #students table
                studentId = int(line[0])
                nameSplit = line[1].split(', ')
                firstName = nameSplit[1]
                lastName = nameSplit[0]
                if studentId not in studentIDSet:
                    students.append((studentId, firstName, lastName, line[2]))
                studentIDSet.add(studentId)
                # print(students)

                #StudentExamScores table
                examScores = [x.lstrip() for x in line[-1].split(',')]
                studentIdList = [studentId]*len(examNameList)
                for (a, b, c) in zip(studentIdList, examNameList, examScores):
                    studentExamScoresList.append((id,a,b,c))
                    id = id+1
                # print(studentExamScoresList)
            degrees = [(x,) for x in list(degrees)]
        return degrees, exams, students, studentExamScoresList

    except Exception as e:
        print(e)
        print("Error in data_preprocessing")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
        raise