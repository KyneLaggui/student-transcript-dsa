# This work was done by Group 4
# Kyle Kryzel R. Carandang, 2021-04994-MN-0, (25%)
# Justin Carl C. De Guia. 2021-05775-MN-0, (25%)
# William James R. Elumba, 2021-05779-MN-0, (25%)
# Kyne Domerei N. Laggui, 2021-05787-MN-0, (25%)

import csv
import sys
import os
import time
import os.path
import datetime

"""
Read StudentTranscript.csv file and parses the necessary information 
and passes it into other functions that need it.
"""
with open("StudentTranscript.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    studentIDs = []
    studentDetails = []
    next(csv_reader)
    for line in csv_reader:
        studentIDs.append(line[1])
        studentDetails.append(line)

"""
startFeature is the starting function when the program opens
This function allows the user to choose which student level and degree
they want to find. It also asks them for the student ID number.
If the student level chosen is "U", then degree is an empty string.
This function returns userStudent information, the student ID number,
the degree and student level chosen.
"""
def startFeature(numOfProcess):
    try:
        studentLevel = input("\n[U] UNDERGRADUATE \n[G] GRADUATE \n[B] BOTH \nWhat is the Student Level? ").upper()
        if studentLevel == "G" or studentLevel == "B":
            askDegree = input("\n[M] MASTER \n[D] DOCTORATE \n[B0] BOTH \nWhat is the Degree? ").upper()
        else:
            askDegree = ""
    except ValueError:
        menu(numOfProcess)
    if studentLevel in ["U", "G", "B"] and askDegree in ["M", "D", "B0", ""]:
        pass
    else:
        menu(numOfProcess)

    while True:
        stdID = input("What is your Student ID: ")
        authenticate = authenticatingUser(studentIDs, stdID)
        if authenticate:
            break
    userStudent = gettingUserInfo(authenticate, studentDetails)   
    return userStudent, stdID, askDegree, studentLevel

"""
menuFeature function displays a user interface in which the user
can choose from 8 features in the program. If the entered value is invalid,
then it will keep asking the user for a valid input.
"""
def menuFeature(informationOfUser, stdID, numOfProcess, degree, studentLevel):
    try:
        while True:
            studentTranscriptMenu = input("""
Student Transcript Generation System
========================================
1. Student Details
2. Statistics
3. Transcript based on major courses
4. Transcript based on minor courses
5. Full Transcript
6. Previous Transcript requests
7. Select another student
8. Terminate the System
========================================
Enter your Feature: """)
            if studentTranscriptMenu == "1":
                detailsFeature(informationOfUser, stdID)
            elif studentTranscriptMenu == "2":
                statisticsFeature(stdID, degree, studentLevel)
            elif studentTranscriptMenu == "3":
                majorTranscriptFeature(stdID, degree, studentLevel)
            elif studentTranscriptMenu == "4":
                minorTranscriptFeature(stdID, degree, studentLevel)
            elif studentTranscriptMenu == "5":
                fullTranscriptFeature(stdID, degree, studentLevel)
            elif studentTranscriptMenu == "6":
                previousRequestsFeature(stdID)
            elif studentTranscriptMenu == "7":
                newStudentFeature(numOfProcess)
            elif studentTranscriptMenu == "8":
                terminateFeature(numOfProcess)
            countdown(informationOfUser, stdID, numOfProcess, degree, studentLevel)
    except ValueError:
        print("Input a valid number")
        menu(numOfProcess)

"""
detailsFeature allows the user to view the details of the chosen student
It will then generate a .txt file that contains the same details.
"""
def detailsFeature(userStudent, stdID):
    level = levels(userStudent)
    college = colleges(userStudent)
    department = departments(userStudent)
    term = terms(userStudent)

    print(f"\nName: {userStudent[0][2]}")
    print(f"stdID: {userStudent[0][1]}")
    print("Level(s): ", end="")
    print(", ".join(level))
    print("Number of terms: ", end="")
    print(", ".join(term))
    print("College(s): ", end="")
    print(", ".join(college))
    print("Department(s): ", end="")
    print(", ".join(department))

    studentFile = open(f"std{stdID}details.txt", "w")
    studentFile.write(f"Name: {userStudent[0][2]}\n")
    studentFile.write(f"stdID: {userStudent[0][1]}\n")
    studentFile.write("Level(s): ")
    studentFile.write(", ".join(level))
    studentFile.write("\nNumber of terms: ")
    studentFile.write(", ".join(term))
    studentFile.write("\nCollege(s): ")
    studentFile.write(", ".join(college))
    studentFile.write("\nDepartment(s): ")
    studentFile.write(", ".join(department))

"""
statisticsFeature displays the statistics of the chosen student's records.
It only displays whichever student level was chosen by the user.
It will then generate a .txt file that contains the same statistics.
"""
def statisticsFeature(stdID, degree, studentLevel):  
    statisticsFile = open(f"std{stdID}statistics.txt", "w")
    
    term1Uavg, term2Uavg, term3Uavg, term4Uavg, uGrades, uTerms, uCourses = [], [], [], [], [], [], []
    uCourseDup = "No"
    
    term1Mavg, term2Mavg, term3Mavg, term4Mavg, mGrades, mTerms, mCourses = [], [], [], [], [], [], []
    mCourseDup = "No"
    
    term1Davg, term2Davg, term3Davg, term4Davg, dGrades, dTerms, dCourses = [], [], [], [], [], [], []
    dCourseDup = "No"
    
    with open(f"{stdID}.csv", "rt") as stdStatistics:
        stdStatisticsReader = csv.DictReader(stdStatistics, delimiter=",")
        for row in stdStatisticsReader:
            if row["Level"] == "U":
                if row["Term"] == "1":
                    term1Uavg.append(row["Grade"])
                elif row["Term"] == "2":
                    term2Uavg.append(row["Grade"])
                elif row["Term"] == "3":
                    term3Uavg.append(row["Grade"])
                elif row["Term"] == "4":
                    term4Uavg.append(row["Grade"])        
                uGrades.append(row["Grade"])
                uTerms.append(row["Term"])
                uCourses.append(row["courseName"])
                uniqueCourses = set(uCourses)
                if len(uniqueCourses) == len(uCourses):
                    uCourseDup = "No"
                else:
                    uCourseDup = "Yes"
                
            elif row["Level"] == "M":
                if row["Term"] == "1":
                    term1Mavg.append(row["Grade"])
                elif row["Term"] == "2":
                    term2Mavg.append(row["Grade"])
                elif row["Term"] == "3":
                    term3Mavg.append(row["Grade"])
                elif row["Term"] == "4":
                    term4Mavg.append(row["Grade"])    
                mGrades.append(row["Grade"])
                mTerms.append(row["Term"])
                mCourses.append(row["courseName"])
                uniqueCourses = set(mCourses)
                if len(uniqueCourses) == len(mCourses):
                    mCourseDup = "No"
                else:
                    mCourseDup = "Yes"
                
            elif row["Level"] == "D":
                if row["Term"] == "1":
                    term1Davg.append(row["Grade"])
                elif row["Term"] == "2":
                    term2Davg.append(row["Grade"])
                elif row["Term"] == "3":
                    term3Davg.append(row["Grade"])
                elif row["Term"] == "4":
                    term4Davg.append(row["Grade"]) 
                dGrades.append(row["Grade"])
                dTerms.append(row["Term"])
                dCourses.append(row["courseName"])
                uniqueCourses = set(dCourses)
                if len(uniqueCourses) == len(dCourses):
                    dCourseDup = "No"
                else:
                    dCourseDup = "Yes"
        
    def graduateStatistics():
        if degree == "M":
            masteralStatistics(term1Mavg, term2Mavg, term3Mavg, term4Mavg, mGrades, mTerms, mCourseDup, statisticsFile)
    
        elif degree == "D":
            doctorateStatistics(term1Davg, term2Davg, term3Davg, term4Davg, dGrades, dTerms, dCourseDup, statisticsFile)
            
        elif degree == "B0":
            masteralStatistics(term1Mavg, term2Mavg, term3Mavg, term4Mavg, mGrades, mTerms, mCourseDup, statisticsFile)
            doctorateStatistics(term1Davg, term2Davg, term3Davg, term4Davg, dGrades, dTerms, dCourseDup, statisticsFile)
                                
    if studentLevel == "U":
        undergradStatistics(term1Uavg, term2Uavg, term3Uavg, term4Uavg, uGrades, uTerms, uCourseDup, statisticsFile)
        
    elif studentLevel == "G":
        graduateStatistics()            
    
    elif studentLevel == "B":
        undergradStatistics(term1Uavg, term2Uavg, term3Uavg, term4Uavg, uGrades, uTerms, uCourseDup, statisticsFile)
        graduateStatistics() 
        
    statisticsFile.close()

""""
undergradStatistics is a part of statisticsFeature.
This function only handles the statistics 
under student level "Undergraduate"
It also writes into the .txt file what it displays.
"""
def undergradStatistics(term1Uavg, term2Uavg, term3Uavg, term4Uavg, uGrades, uTerms, uCourseDup, statisticsFile):
    maxGrade = max(uGrades)
    minGrade = min(uGrades)
    print(f"""
    =====================================================
    **************** Undergraduate Level ****************
    =====================================================
    Overall average (major and minor) for all terms: 
    Average (major and minor) of each term: 
    \tTerm 1: {average(term1Uavg)}
    \tTerm 2: {average(term2Uavg)}
    \tTerm 3: {average(term3Uavg)}
    \tTerm 4: {average(term4Uavg)}
    
    Maximum grade(s) and in which term(s): {maxGrade}, {uTerms[uGrades.index(maxGrade)]}
    Minimum grade(s) and in which term(s): {minGrade}, {uTerms[uGrades.index(minGrade)]}
    Do you have any repeated course(s)? {uCourseDup}
    """)
    
    statisticsFile.write(f"""
    =====================================================
    **************** Undergraduate Level ****************
    =====================================================
    Overall average (major and minor) for all terms: 
    Average (major and minor) of each term: 
    \tTerm 1: {average(term1Uavg)}
    \tTerm 2: {average(term2Uavg)}
    \tTerm 3: {average(term3Uavg)}
    \tTerm 4: {average(term4Uavg)}
    
    Maximum grade(s) and in which term(s): {maxGrade}, {uTerms[uGrades.index(maxGrade)]}
    Minimum grade(s) and in which term(s): {minGrade}, {uTerms[uGrades.index(minGrade)]}
    Do you have any repeated course(s)? {uCourseDup}
    """)

""""
masteralStatistics is a part of statisticsFeature.
This function only handles the statistics 
under student level "Masteral"
It also writes into the .txt file what it displays.
"""
def masteralStatistics(term1Mavg, term2Mavg, term3Mavg, term4Mavg, mGrades, mTerms, mCourseDup, statisticsFile):
    maxGrade = max(mGrades)
    minGrade = min(mGrades)
    print(f"""
    =====================================================
    ***************** Graduate(M) Level *****************
    =====================================================
    Overall average (major and minor) for all terms: 
    Average (major and minor) of each term: 
    \tTerm 1: {average(term1Mavg)}
    \tTerm 2: {average(term2Mavg)}
    \tTerm 3: {average(term3Mavg)}
    \tTerm 4: {average(term4Mavg)}
    Maximum grade(s) and in which term(s): {maxGrade}, {mTerms[mGrades.index(maxGrade)]}
    Minimum grade(s) and in which term(s): {minGrade}, {mTerms[mGrades.index(minGrade)]}
    Do you have any repeated course(s)? {mCourseDup}
    """)
    
    statisticsFile.write(f"""
    =====================================================
    ***************** Graduate(M) Level *****************
    =====================================================
    Overall average (major and minor) for all terms: 
    Average (major and minor) of each term: 
    \tTerm 1: {average(term1Mavg)}
    \tTerm 2: {average(term2Mavg)}
    \tTerm 3: {average(term3Mavg)}
    \tTerm 4: {average(term4Mavg)}
    Maximum grade(s) and in which term(s): {maxGrade}, {mTerms[mGrades.index(maxGrade)]}
    Minimum grade(s) and in which term(s): {minGrade}, {mTerms[mGrades.index(minGrade)]}
    Do you have any repeated course(s)? {mCourseDup}
    """)

""""
doctorateStatistics is a part of statisticsFeature.
This function only handles the statistics 
under student level "Doctorate"
It also writes into the .txt file what it displays.
"""
def doctorateStatistics(term1Davg, term2Davg, term3Davg, term4Davg, dGrades, dTerms, dCourseDup, statisticsFile):
    maxGrade = max(dGrades)
    minGrade = min(dGrades)
    print(f"""
    =====================================================
    ***************** Graduate(D) Level *****************
    =====================================================
    Overall average (major and minor) for all terms: 
    Average (major and minor) of each term: 
    \tTerm 1: {average(term1Davg)}
    \tTerm 2: {average(term2Davg)}
    \tTerm 3: {average(term3Davg)}
    \tTerm 4: {average(term4Davg)}
    Maximum grade(s) and in which term(s): {maxGrade}, {dTerms[dGrades.index(maxGrade)]}
    Minimum grade(s) and in which term(s): {minGrade}, {dTerms[dGrades.index(minGrade)]}
    Do you have any repeated course(s)? {dCourseDup}
    """)
    
    statisticsFile.write(f"""
    =====================================================
    ***************** Graduate(D) Level *****************
    =====================================================
    Overall average (major and minor) for all terms: 
    Average (major and minor) of each term: 
    \tTerm 1: {average(term1Davg)}
    \tTerm 2: {average(term2Davg)}
    \tTerm 3: {average(term3Davg)}
    \tTerm 4: {average(term4Davg)}
    Maximum grade(s) and in which term(s): {maxGrade}, {dTerms[dGrades.index(maxGrade)]}
    Minimum grade(s) and in which term(s): {minGrade}, {dTerms[dGrades.index(minGrade)]}
    Do you have any repeated course(s)? {dCourseDup}
    """)

"""
majorTranscriptFeature displays the transcript of major courses of the chosen student's records.
It only displays whichever student level was chosen by the user.
It will then generate a .txt file that contains the same statistics.
"""
def majorTranscriptFeature(stdID, degree, studentLevel):
    courseType = "Major"
    majorTranscriptFile = open(f"std{stdID}{courseType}Transcript.txt", "w")
    with open("StudentTranscript.csv", "rt") as stdTranscript:
        stdTranscriptReader = csv.DictReader(stdTranscript, delimiter=",")
        for row in stdTranscriptReader:
            
            if row["Level"] == "U" and row["Student ID"] == stdID:
                name = row["Name"]
                college = row["College"]
                department = row["Department"]
                major = row["Major"]
                minor = row["Minor"]
                level = row["Level"]
                numOfTerms = row["Terms"]
                
            elif row["Level"] == "G" and row["Student ID"] == stdID and row["Degree"] in ["M1", "M2"]:
                name = row["Name"]
                college = row["College"]
                department = row["Department"]
                major = row["Major"]
                minor = row["Minor"]
                level = row["Level"]
                numOfTerms = row["Terms"]
                
            elif row["Level"] == "G" and row["Student ID"] == stdID and row["Degree"] in ["D1"]:
                name = row["Name"]
                college = row["College"]
                department = row["Department"]
                major = row["Major"]
                minor = row["Minor"]
                level = row["Level"]
                numOfTerms = row["Terms"]
            
        displayTranscriptDetails(name, stdID, college, department, major, minor, level, numOfTerms, majorTranscriptFile)

    uterms, uallTerms, ucourseID, ucourseName, ucreditHours, ugrade, uallGrade = [], [], [], [], [], [], []
    mterms, mallTerms, mcourseID, mcourseName, mcreditHours, mgrade, mallGrade = [], [], [], [], [], [], []
    dterms, dallTerms, dcourseID, dcourseName, dcreditHours, dgrade, dallGrade = [], [], [], [], [], [], []

    with open(f"{stdID}.csv", "rt") as stdMajorTranscript:
        stdMajorTranscriptReader = csv.DictReader(stdMajorTranscript, delimiter=",")
        for row in stdMajorTranscriptReader:
            if row["courseType"] == "Major":
                if row["Level"] == "U" and degree in ["M", "D", "B0", ""]:
                    uterms.append(row["Term"])
                    ucourseID.append(row["courseID"])
                    ucourseName.append(row["courseName"])
                    ucreditHours.append(row["creditHours"])
                    ugrade.append(row["Grade"])

                elif row["Level"] == "M" and degree in ["M", "B0"] :
                    mterms.append(row["Term"])
                    mcourseID.append(row["courseID"])
                    mcourseName.append(row["courseName"])
                    mcreditHours.append(row["creditHours"])
                    mgrade.append(row["Grade"])

                elif row["Level"] == "D" and degree in ["D", "B0"]:
                    dterms.append(row["Term"])
                    dcourseID.append(row["courseID"])
                    dcourseName.append(row["courseName"])
                    dcreditHours.append(row["creditHours"])
                    dgrade.append(row["Grade"])
                

            uallTerms.append(row["Term"])
            uallGrade.append(row["Grade"])
            mallTerms.append(row["Term"])
            mallGrade.append(row["Grade"])
            dallTerms.append(row["Term"])
            dallGrade.append(row["Grade"])

    def graduateMajorTranscript():
        if degree == "M":
            masteralTranscript(mterms, mcourseID, mcourseName, mcreditHours, mgrade, mallTerms, mallGrade, courseType, majorTranscriptFile)
        elif degree == "D":
            doctorateTranscript(dterms, dcourseID, dcourseName, dcreditHours, dgrade,  dallTerms, dallGrade, courseType, majorTranscriptFile)
        elif degree == "B0":
            masteralTranscript(mterms, mcourseID, mcourseName, mcreditHours, mgrade, mallTerms, mallGrade, courseType, majorTranscriptFile)
            doctorateTranscript(dterms, dcourseID, dcourseName, dcreditHours, dgrade, dallTerms, dallGrade, courseType, majorTranscriptFile)

    if studentLevel == "U":
        undergraduateTranscript(uterms, ucourseID, ucourseName, ucreditHours, ugrade, uallTerms, uallGrade, courseType, majorTranscriptFile)

    elif studentLevel == "G":
        graduateMajorTranscript()
        
    elif studentLevel == "B":
        undergraduateTranscript(uterms, ucourseID, ucourseName, ucreditHours, ugrade, uallTerms, uallGrade, courseType, majorTranscriptFile)
        graduateMajorTranscript()

    majorTranscriptFile.close()

"""
minorTranscriptFeature displays the transcript of minor courses of the chosen student's records.
It only displays whichever student level was chosen by the user.
It will then generate a .txt file that contains the same statistics.
"""
def minorTranscriptFeature(stdID, degree, studentLevel):
    courseType = "Minor"
    minorTranscriptFile = open(f"std{stdID}{courseType}Transcript.txt", "w")
    with open("StudentTranscript.csv", "rt") as stdTranscript:
        stdTranscriptReader = csv.DictReader(stdTranscript, delimiter=",")
        for row in stdTranscriptReader:

            if row["Level"] == "U" and row["Student ID"] == stdID:
                name = row["Name"]
                college = row["College"]
                department = row["Department"]
                major = row["Major"]
                minor = row["Minor"]
                level = row["Level"]
                numOfTerms = row["Terms"]
                
            elif row["Level"] == "G" and row["Student ID"] == stdID and row["Degree"] in ["M1", "M2"]:
                name = row["Name"]
                college = row["College"]
                department = row["Department"]
                major = row["Major"]
                minor = row["Minor"]
                level = row["Level"]
                numOfTerms = row["Terms"]
                
            elif row["Level"] == "G" and row["Student ID"] == stdID and row["Degree"] in ["D1"]:
                name = row["Name"]
                college = row["College"]
                department = row["Department"]
                major = row["Major"]
                minor = row["Minor"]
                level = row["Level"]
                numOfTerms = row["Terms"]
            
        displayTranscriptDetails(name, stdID, college, department, major, minor, level, numOfTerms, minorTranscriptFile)

    uterms, uallTerms, ucourseID, ucourseName, ucreditHours, ugrade, uallGrade = [], [], [], [], [], [], []
    mterms, mallTerms, mcourseID, mcourseName, mcreditHours, mgrade, mallGrade = [], [], [], [], [], [], []
    dterms, dallTerms, dcourseID, dcourseName, dcreditHours, dgrade, dallGrade = [], [], [], [], [], [], []

    with open(f"{stdID}.csv", "rt") as stdMajorTranscript:
        stdMajorTranscriptReader = csv.DictReader(stdMajorTranscript, delimiter=",")
        for row in stdMajorTranscriptReader:
            if row["courseType"] == "Minor":
                if row["Level"] == "U" and degree in ["M", "D", "B0", ""]:
                    uterms.append(row["Term"])
                    ucourseID.append(row["courseID"])
                    ucourseName.append(row["courseName"])
                    ucreditHours.append(row["creditHours"])
                    ugrade.append(row["Grade"])

                elif row["Level"] == "M" and degree in ["M", "B0"] :
                    mterms.append(row["Term"])
                    mcourseID.append(row["courseID"])
                    mcourseName.append(row["courseName"])
                    mcreditHours.append(row["creditHours"])
                    mgrade.append(row["Grade"])

                elif row["Level"] == "D" and degree in ["D", "B0"]:
                    dterms.append(row["Term"])
                    dcourseID.append(row["courseID"])
                    dcourseName.append(row["courseName"])
                    dcreditHours.append(row["creditHours"])
                    dgrade.append(row["Grade"])
                

            uallTerms.append(row["Term"])
            uallGrade.append(row["Grade"])
            mallTerms.append(row["Term"])
            mallGrade.append(row["Grade"])
            dallTerms.append(row["Term"])
            dallGrade.append(row["Grade"])

    def graduateMajorTranscript():
        if degree == "M":
            masteralTranscript(mterms, mcourseID, mcourseName, mcreditHours, mgrade, mallTerms, mallGrade, courseType, minorTranscriptFile)
        elif degree == "D":
            doctorateTranscript(dterms, dcourseID, dcourseName, dcreditHours, dgrade,  dallTerms, dallGrade, courseType, minorTranscriptFile)
        elif degree == "B0":
            masteralTranscript(mterms, mcourseID, mcourseName, mcreditHours, mgrade, mallTerms, mallGrade, courseType, minorTranscriptFile)
            doctorateTranscript(dterms, dcourseID, dcourseName, dcreditHours, dgrade, dallTerms, dallGrade, courseType, minorTranscriptFile)

    if studentLevel == "U":
        undergraduateTranscript(uterms, ucourseID, ucourseName, ucreditHours, ugrade, uallTerms, uallGrade, courseType, minorTranscriptFile)

    elif studentLevel == "G":
        graduateMajorTranscript()
        
    elif studentLevel == "B":
        undergraduateTranscript(uterms, ucourseID, ucourseName, ucreditHours, ugrade, uallTerms, uallGrade, courseType, minorTranscriptFile)
        graduateMajorTranscript()

    minorTranscriptFile.close()

"""
fullTranscriptFeature displays the transcript of all courses of the chosen student's records.
It only displays whichever student level was chosen by the user.
It will then generate a .txt file that contains the same statistics.
"""
def fullTranscriptFeature(stdID, degree, studentLevel):
    courseType = "Full"
    fullTranscriptFile = open(f"std{stdID}{courseType}Transcript.txt", "w")
    with open("StudentTranscript.csv", "rt") as stdTranscript:
        stdTranscriptReader = csv.DictReader(stdTranscript, delimiter=",")
        for row in stdTranscriptReader:
            
            if row["Level"] == "U" and row["Student ID"] == stdID:
                name = row["Name"]
                college = row["College"]
                department = row["Department"]
                major = row["Major"]
                minor = row["Minor"]
                level = row["Level"]
                numOfTerms = row["Terms"]
                
            elif row["Level"] == "G" and row["Student ID"] == stdID and row["Degree"] in ["M1", "M2"]:
                name = row["Name"]
                college = row["College"]
                department = row["Department"]
                major = row["Major"]
                minor = row["Minor"]
                level = row["Level"]
                numOfTerms = row["Terms"]
                
            elif row["Level"] == "G" and row["Student ID"] == stdID and row["Degree"] in ["D1"]:
                name = row["Name"]
                college = row["College"]
                department = row["Department"]
                major = row["Major"]
                minor = row["Minor"]
                level = row["Level"]
                numOfTerms = row["Terms"]
            
        displayTranscriptDetails(name, stdID, college, department, major, minor, level, numOfTerms, fullTranscriptFile)

    majoruterms, majoruallTerms, majorucourseID, majorucourseName, majorucreditHours, majorugrade, majoruallGrade = [], [], [], [], [], [], []
    majormterms, majormallTerms, majormcourseID, majormcourseName, majormcreditHours, majormgrade, majormallGrade = [], [], [], [], [], [], []
    majordterms, majordallTerms, majordcourseID, majordcourseName, majordcreditHours, majordgrade, majordallGrade = [], [], [], [], [], [], []

    minoruterms, minoruallTerms, minorucourseID, minorucourseName, minorucreditHours, minorugrade, minoruallGrade = [], [], [], [], [], [], []
    minormterms, minormallTerms, minormcourseID, minormcourseName, minormcreditHours, minormgrade, minormallGrade = [], [], [], [], [], [], []
    minordterms, minordallTerms, minordcourseID, minordcourseName, minordcreditHours, minordgrade, minordallGrade = [], [], [], [], [], [], []

    with open(f"{stdID}.csv", "rt") as stdMajorTranscript:
        stdMajorTranscriptReader = csv.DictReader(stdMajorTranscript, delimiter=",")
        for row in stdMajorTranscriptReader:
            if row["courseType"] == "Major":
                if row["Level"] == "U" and degree in ["M", "D", "B0", ""]:
                    majoruterms.append(row["Term"])
                    majorucourseID.append(row["courseID"])
                    majorucourseName.append(row["courseName"])
                    majorucreditHours.append(row["creditHours"])
                    majorugrade.append(row["Grade"])

                elif row["Level"] == "M" and degree in ["M", "B0"] :
                    majormterms.append(row["Term"])
                    majormcourseID.append(row["courseID"])
                    majormcourseName.append(row["courseName"])
                    majormcreditHours.append(row["creditHours"])
                    majormgrade.append(row["Grade"])

                elif row["Level"] == "D" and degree in ["D", "B0"]:
                    majordterms.append(row["Term"])
                    majordcourseID.append(row["courseID"])
                    majordcourseName.append(row["courseName"])
                    majordcreditHours.append(row["creditHours"])
                    majordgrade.append(row["Grade"])
            
            if row["courseType"] == "Minor":
                if row["Level"] == "U" and degree in ["M", "D", "B0", ""]:
                    minoruterms.append(row["Term"])
                    minorucourseID.append(row["courseID"])
                    minorucourseName.append(row["courseName"])
                    minorucreditHours.append(row["creditHours"])
                    minorugrade.append(row["Grade"])

                elif row["Level"] == "M" and degree in ["M", "B0"] :
                    minormterms.append(row["Term"])
                    minormcourseID.append(row["courseID"])
                    minormcourseName.append(row["courseName"])
                    minormcreditHours.append(row["creditHours"])
                    minormgrade.append(row["Grade"])

                elif row["Level"] == "D" and degree in ["D", "B0"]:
                    minordterms.append(row["Term"])
                    minordcourseID.append(row["courseID"])
                    minordcourseName.append(row["courseName"])
                    minordcreditHours.append(row["creditHours"])
                    minordgrade.append(row["Grade"])
                

            majoruallTerms.append(row["Term"])
            majoruallGrade.append(row["Grade"])
            majormallTerms.append(row["Term"])
            majormallGrade.append(row["Grade"])
            majordallTerms.append(row["Term"])
            majordallGrade.append(row["Grade"])

            minoruallTerms.append(row["Term"])
            minoruallGrade.append(row["Grade"])
            minormallTerms.append(row["Term"])
            minormallGrade.append(row["Grade"])
            minordallTerms.append(row["Term"])
            minordallGrade.append(row["Grade"])

    def graduateFullTranscript():
        if degree == "M":
            fullmasteralTranscript(majormterms, majormcourseID, majormcourseName, majormcreditHours, majormgrade, majormallTerms, majormallGrade, minormterms, minormcourseID, minormcourseName, minormcreditHours, minormgrade, minormallTerms, minormallGrade, fullTranscriptFile)
        elif degree == "D":
            fulldoctorateTranscript(majordterms, majordcourseID, majordcourseName, majordcreditHours, majordgrade, majordallTerms, majordallGrade, minordterms, minordcourseID, minordcourseName, minordcreditHours, minordgrade, minordallTerms, minordallGrade, fullTranscriptFile)
        elif degree == "B0":
            fullmasteralTranscript(majormterms, majormcourseID, majormcourseName, majormcreditHours, majormgrade, majormallTerms, majormallGrade, minormterms, minormcourseID, minormcourseName, minormcreditHours, minormgrade, minormallTerms, minormallGrade, fullTranscriptFile)
            fulldoctorateTranscript(majordterms, majordcourseID, majordcourseName, majordcreditHours, majordgrade, majordallTerms, majordallGrade, minordterms, minordcourseID, minordcourseName, minordcreditHours, minordgrade, minordallTerms, minordallGrade, fullTranscriptFile)

    if studentLevel == "U":
        fullundergraduateTranscript(majoruterms, majorucourseID, majorucourseName, majorucreditHours, majorugrade, majoruallTerms, majoruallGrade, minoruterms, minorucourseID, minorucourseName, minorucreditHours, minorugrade, minoruallTerms, minoruallGrade, fullTranscriptFile)

    elif studentLevel == "G":
        graduateFullTranscript()
        
    elif studentLevel == "B":
        fullundergraduateTranscript(majoruterms, majorucourseID, majorucourseName, majorucreditHours, majorugrade, majoruallTerms, majoruallGrade, minoruterms, minorucourseID, minorucourseName, minorucreditHours, minorugrade, minoruallTerms, minoruallGrade, fullTranscriptFile)
        graduateFullTranscript()

    fullTranscriptFile.close()

""""
undergraduateTranscript is a part of major/minorTranscriptFeature.
This function only handles the statistics 
under student level "Undergraduate"
It also writes into the .txt file what it displays.
"""
def undergraduateTranscript(uterms, ucourseID, ucourseName, ucreditHours, ugrade, uallTerms, uallGrade, courseType, transcriptFile):
    termList = []
    [termList.append(term) for term in uterms if term not in termList]
    termList.sort()
    for term in termList:
        termidx = termsIndexing(uterms, term)
        ualltermidx = termsIndexing(uallTerms, term)
        uallGradeAvg = []
        courseTypeAvg = []

        print(f"""=====================================================
***************     Term {term}      *****************
=====================================================
Course ID   Course Name     Credit Hours    Grade""")

        transcriptFile.write(f"""=====================================================
***************     Term {term}      *****************
=====================================================
Course ID   Course Name     Credit Hours    Grade\n""")

        for idx in termidx:
            courseTypeAvg.append(ugrade[idx])
            print(f"""{ucourseID[idx]}         {ucourseName[idx]}        {ucreditHours[idx]}\t\t     {ugrade[idx]}""")

            transcriptFile.write(f"""{ucourseID[idx]}         {ucourseName[idx]}        {ucreditHours[idx]}\t\t\t\t{ugrade[idx]}\n""")

        for idx in ualltermidx:
            uallGradeAvg.append(uallGrade[idx])
        print(f"""{courseType} Average = {round(average(courseTypeAvg))}           Overall Average = {round(average(ugrade))}""")
        transcriptFile.write(f"""{courseType} Average = {round(average(courseTypeAvg))}          Overall Average = {round(average(ugrade))}\n""")
    print(f"""=====================================================
******** End of Transcript for Level (U) ********
=====================================================""")
    transcriptFile.write(f"""=====================================================
******** End of Transcript for Level (U) ********
=====================================================\n""")

""""
masteralTranscript is a part of major/minorTranscriptFeature.
This function only handles the statistics 
under student level "Masteral"
It also writes into the .txt file what it displays.
"""
def masteralTranscript(mterms, mcourseID, mcourseName, mcreditHours, mgrade, mallTerms, mallGrade, courseType, transcriptFile):
    termList = []
    [termList.append(term) for term in mterms if term not in termList]
    termList.sort()
    for term in termList:
        termidx = termsIndexing(mterms, term)
        malltermidx = termsIndexing(mallTerms, term)
        mallGradeAvg = []
        courseTypeAvg = []

        print(f"""=====================================================
***************     Term {term}      *****************
=====================================================
Course ID   Course Name     Credit Hours    Grade""")

        transcriptFile.write(f"""=====================================================
***************     Term {term}      *****************
=====================================================
Course ID   Course Name     Credit Hours    Grade\n""")

        for idx in termidx:
            courseTypeAvg.append(mgrade[idx])
            print(f"""{mcourseID[idx]}         {mcourseName[idx]}        {mcreditHours[idx]}\t\t     {mgrade[idx]}""")

            transcriptFile.write(f"""{mcourseID[idx]}         {mcourseName[idx]}        {mcreditHours[idx]}\t\t\t\t{mgrade[idx]}\n""")

        for idx in malltermidx:
            mallGradeAvg.append(mallGrade[idx])
        print(f"""{courseType} Average = {round(average(courseTypeAvg))}           Overall Average = {round(average(mgrade))}""")
        transcriptFile.write(f"""{courseType} Average = {round(average(courseTypeAvg))}          Overall Average = {round(average(mgrade))}\n""")
    print(f"""=====================================================
******** End of Transcript for Level (M) ********
=====================================================""")
    transcriptFile.write(f"""=====================================================
******** End of Transcript for Level (M) ********
=====================================================\n""")

""""
doctorateTranscript is a part of major/minorTranscriptFeature.
This function only handles the statistics 
under student level "Doctorate"
It also writes into the .txt file what it displays.
"""
def doctorateTranscript(dterms, dcourseID, dcourseName, dcreditHours, dgrade, dallTerms, dallGrade, courseType, transcriptFile):
    termList = []
    [termList.append(term) for term in dterms if term not in termList]
    termList.sort()
    for term in termList:
        termidx = termsIndexing(dterms, term)
        dalltermidx = termsIndexing(dallTerms, term)
        dallGradeAvg = []
        courseTypeAvg = []

        print(f"""=====================================================
***************     Term {term}      *****************
=====================================================
Course ID   Course Name     Credit Hours    Grade""")

        transcriptFile.write(f"""=====================================================
***************     Term {term}      *****************
=====================================================
Course ID   Course Name     Credit Hours    Grade\n""")

        for idx in termidx:
            courseTypeAvg.append(dgrade[idx])
            print(f"""{dcourseID[idx]}         {dcourseName[idx]}        {dcreditHours[idx]}\t\t     {dgrade[idx]}""")

            transcriptFile.write(f"""{dcourseID[idx]}         {dcourseName[idx]}        {dcreditHours[idx]}\t\t\t\t{dgrade[idx]}\n""")

        for idx in dalltermidx:
            dallGradeAvg.append(dallGrade[idx])
        print(f"""{courseType} Average = {round(average(courseTypeAvg))}           Overall Average = {round(average(dgrade))}""")
        transcriptFile.write(f"""{courseType} Average = {round(average(courseTypeAvg))}          Overall Average = {round(average(dgrade))}\n""")
    print(f"""=====================================================
******** End of Transcript for Level (D) ********
=====================================================""")
    transcriptFile.write(f"""=====================================================
******** End of Transcript for Level (D) ********
=====================================================\n""")

""""
fullundergraduateTranscript is a part of fullTranscriptFeature.
This function only handles the statistics 
under student level "Undergraduate"
It also writes into the .txt file what it displays.
"""
def fullundergraduateTranscript(majoruterms, majorucourseID, majorucourseName, majorucreditHours, majorugrade, majoruallTerms, majoruallGrade, minoruterms, minorucourseID, minorucourseName, minorucreditHours, minorugrade, minoruallTerms, minoruallGrade, transcriptFile):
    combinedTerms = majoruterms + minoruterms
    combinedallTerms = majoruallTerms + minoruallTerms
    combinedGrade = majorugrade + minorugrade
    combinedCreditHours = majorucreditHours + minorucreditHours
    combinedCourseName = majorucourseName + minorucourseName
    combinedCourseID = majorucourseID + minorucourseID
    combinedAllGrade = majoruallGrade + minoruallGrade
    termList = []
    [termList.append(term) for term in combinedTerms if term not in termList]
    termList.sort()
    for term in termList:
        termidx = termsIndexing(combinedTerms, term)
        umajortermidx = termsIndexing(majoruterms, term)
        uminortermidx = termsIndexing(minoruterms, term)
        ualltermidx = termsIndexing(combinedallTerms, term)
        uallGradeAvg, courseTypeAvg, umajorAvg, uminorAvg = [], [], [], []

        print(f"""=====================================================
***************     Term {term}      *****************
=====================================================
Course ID   Course Name     Credit Hours    Grade""")

        transcriptFile.write(f"""=====================================================
***************     Term {term}      *****************
=====================================================
Course ID   Course Name     Credit Hours    Grade\n""")

        for idx in termidx:
            courseTypeAvg.append(combinedGrade[idx])
            print(f"""{combinedCourseID[idx]}         {combinedCourseName[idx]}        {combinedCreditHours[idx]}\t\t     {combinedGrade[idx]}""")

            transcriptFile.write(f"""{combinedCourseID[idx]}         {combinedCourseName[idx]}        {combinedCreditHours[idx]}\t\t\t\t{combinedGrade[idx]}\n""")

        for idx in umajortermidx:
            umajorAvg.append(majorugrade[idx])
            
        for idx in uminortermidx:
            uminorAvg.append(minorugrade[idx])

        for idx in ualltermidx:
            uallGradeAvg.append(combinedAllGrade[idx])
            
        print(f"""Major Average = {round(average(umajorAvg))}           Minor Average = {round(average(uminorAvg))}
Term Average = {round(average(courseTypeAvg))}           Overall Average = {round(average(combinedGrade))}""")
        transcriptFile.write(f"""Major Average = {round(average(umajorAvg))}          Minor Average = {round(average(uminorAvg))}
Term Average = {round(average(courseTypeAvg))}            Overall Average = {round(average(combinedGrade))}\n""")
    print(f"""=====================================================
******** End of Transcript for Level (U) ********
=====================================================""")
    transcriptFile.write(f"""=====================================================
******** End of Transcript for Level (U) ********
=====================================================\n""")

""""
fullmasteralTranscript is a part of fullTranscriptFeature.
This function only handles the statistics 
under student level "Masteral"
It also writes into the .txt file what it displays.
"""
def fullmasteralTranscript(majormterms, majormcourseID, majormcourseName, majormcreditHours, majormgrade, majormallTerms, majormallGrade, minormterms, minormcourseID, minormcourseName, minormcreditHours, minormgrade, minormallTerms, minormallGrade, transcriptFile):   
    combinedTerms = majormterms + minormterms
    combinedallTerms = majormallTerms + minormallTerms
    combinedGrade = majormgrade + minormgrade
    combinedCreditHours = majormcreditHours + minormcreditHours
    combinedCourseName = majormcourseName + minormcourseName
    combinedCourseID = majormcourseID + minormcourseID
    combinedAllGrade = majormallGrade + minormallGrade
    termList = []
    [termList.append(term) for term in combinedTerms if term not in termList]
    termList.sort()
    for term in termList:
        termidx = termsIndexing(combinedTerms, term)
        malltermidx = termsIndexing(combinedallTerms, term)
        mmajortermidx = termsIndexing(majormterms, term)
        mminortermidx = termsIndexing(minormterms, term)
        mallGradeAvg, courseTypeAvg, mmajorAvg, mminorAvg = [], [], [], []

        print(f"""=====================================================
***************     Term {term}      *****************
=====================================================
Course ID   Course Name     Credit Hours    Grade""")

        transcriptFile.write(f"""=====================================================
***************     Term {term}      *****************
=====================================================
Course ID   Course Name     Credit Hours    Grade\n""")

        for idx in termidx:
            courseTypeAvg.append(combinedGrade[idx])
            print(f"""{combinedCourseID[idx]}         {combinedCourseName[idx]}        {combinedCreditHours[idx]}\t\t     {combinedGrade[idx]}""")

            transcriptFile.write(f"""{combinedCourseID[idx]}         {combinedCourseName[idx]}        {combinedCreditHours[idx]}\t\t\t\t{combinedGrade[idx]}\n""")

        for idx in mmajortermidx:
            mmajorAvg.append(majormgrade[idx])
            
        for idx in mminortermidx:
            mminorAvg.append(minormgrade[idx])
        
        for idx in malltermidx:
            mallGradeAvg.append(combinedAllGrade[idx])
            
        print(f"""Major Average = {round(average(mmajorAvg))}           Minor Average = {round(average(mminorAvg))}
Term Average = {round(average(courseTypeAvg))}           Overall Average = {round(average(combinedGrade))}""")
        transcriptFile.write(f"""Major Average = {average(mmajorAvg)}          Minor Average = {average(mminorAvg)}
Term Average = {round(average(courseTypeAvg))}            Overall Average = {round(average(combinedGrade))}\n""")
    print(f"""=====================================================
******** End of Transcript for Level (M) ********
=====================================================""")
    transcriptFile.write(f"""=====================================================
******** End of Transcript for Level (M) ********
=====================================================\n""")

""""
fulldoctorateTranscript is a part of fullTranscriptFeature.
This function only handles the statistics 
under student level "Doctorate"
It also writes into the .txt file what it displays.
"""
def fulldoctorateTranscript(majordterms, majordcourseID, majordcourseName, majordcreditHours, majordgrade, majordallTerms, majordallGrade, minordterms, minordcourseID, minordcourseName, minordcreditHours, minordgrade, minordallTerms, minordallGrade, transcriptFile):
    combinedTerms = majordterms + minordterms
    combinedallTerms = majordallTerms + minordallTerms
    combinedGrade = majordgrade + minordgrade
    combinedCreditHours = majordcreditHours + minordcreditHours
    combinedCourseName = majordcourseName + minordcourseName
    combinedCourseID = majordcourseID + minordcourseID
    combinedAllGrade = majordallGrade + minordallGrade
    termList = []
    [termList.append(term) for term in combinedTerms if term not in termList]
    termList.sort()
    for term in termList:
        termidx = termsIndexing(combinedTerms, term)
        dalltermidx = termsIndexing(combinedallTerms, term)
        dmajortermidx = termsIndexing(majordterms, term)
        dminortermidx = termsIndexing(minordterms, term)
        dallGradeAvg, courseTypeAvg, dmajorAvg, dminorAvg = [], [], [], []

        print(f"""=====================================================
***************     Term {term}      *****************
=====================================================
Course ID   Course Name     Credit Hours    Grade""")

        transcriptFile.write(f"""=====================================================
***************     Term {term}      *****************
=====================================================
Course ID   Course Name     Credit Hours    Grade\n""")

        for idx in termidx:
            courseTypeAvg.append(combinedGrade[idx])
            print(f"""{combinedCourseID[idx]}         {combinedCourseName[idx]}        {combinedCreditHours[idx]}\t\t     {combinedGrade[idx]}""")

            transcriptFile.write(f"""{combinedCourseID[idx]}         {combinedCourseName[idx]}        {combinedCreditHours[idx]}\t\t\t\t{combinedGrade[idx]}\n""")

        for idx in dmajortermidx:
            dmajorAvg.append(majordgrade[idx])
            
        for idx in dminortermidx:
            dminorAvg.append(minordgrade[idx])
        
        for idx in dalltermidx:
            dallGradeAvg.append(combinedAllGrade[idx])
            
        print(f"""Major Average = {round(average(dmajorAvg))}           Minor Average = {round(average(dminorAvg))}
Term Average = {round(average(courseTypeAvg))}           Overall Average = {round(average(combinedGrade))}""")
        transcriptFile.write(f"""Major Average = {round(average(dmajorAvg))}          Minor Average = {round(average(dminorAvg))}
Term Average = {round(average(courseTypeAvg))}            Overall Average = {round(average(combinedGrade))}\n""")
    print(f"""=====================================================
******** End of Transcript for Level (D) ********
=====================================================""")
    transcriptFile.write(f"""=====================================================
******** End of Transcript for Level (D) ********
=====================================================\n""")

"""
termsIndexing function allows the traversal of termsList
and stores their individual indices.
"""
def termsIndexing(terms, termNumber):
    indices = []
    for index, value in enumerate(terms):
        if value == termNumber:
            indices.append(index)
    return indices

"""
displayTranscriptDetails function is a part of major/minor/fullTranscriptFeature.
This function displays the student details into a header for the transcripts.
It also writes into the .txt file what it displays.
"""
def displayTranscriptDetails(name, stdID, college, department, major, minor, level, numOfTerms, transcriptFile):
    print(f"""\nName: {name}\tstdID: {stdID}
College: {college}\t\tDepartment: {department}
Major: {major}\t\tMinor: {minor}
Level: {level}\t\t\tNumber of terms: {numOfTerms}""")

    transcriptFile.write(f"""Name: {name}\tstdID: {stdID}
College: {college}\t\tDepartment: {department}
Major: {major}\t\tMinor: {minor}
Level: {level}\t\t\t\tNumber of terms: {numOfTerms}\n""")

"""
previousRequestsFeature function displays when the request to see records was first made.
This function displays what record it was, the date and time.
It also writes into the .txt file what it displays.
"""
def previousRequestsFeature(stdID):
    requestFile = open(f"std{stdID}PreviousRequests.txt", "w")
    detailsFile = f"std{stdID}details.txt"
    statisticsFile = f"std{stdID}statistics.txt"
    majorTranscriptFile = f"std{stdID}MajorTranscript.txt"
    minorTranscriptFile = f"std{stdID}MinorTranscript.txt"
    fullTranscriptFile = f"std{stdID}FullTranscript.txt"
    fileList = [detailsFile, statisticsFile, majorTranscriptFile, minorTranscriptFile, fullTranscriptFile]
    filename = {detailsFile: "Details   ", statisticsFile: "Statistics", majorTranscriptFile: "Major     ",
                minorTranscriptFile: "Minor     ", fullTranscriptFile: "Full      "}

    print("""\nRequest\t\t\tDate\t\t\tTime
============================================""")

    requestFile.write("""Request\t\tDate\t\t\tTime
============================================""")

    for file in fileList:
        try:
            fileDateTime = time.ctime(os.path.getctime(file))
            fileNameDateTime = datetime.datetime.strptime(fileDateTime, "%a %b %d %H:%M:%S %Y")
            fileDate = fileNameDateTime.strftime("%d/%m/%Y")
            fileTime = fileNameDateTime.strftime("%H:%M %p")
            print(f"{filename[file]}\t\t{fileDate}\t\t{fileTime}")
            requestFile.write(f"\n{filename[file]}\t\t{fileDate}\t\t{fileTime}")
        except Exception:
            pass
    requestFile.close()

"""
newStudentFeature function allows the user to access another student record.
Once this function is called, all displayed details will be cleared
and startFeature will be called again.
"""
def newStudentFeature(numOfProcess):
    numOfProcess += 1
    menu(numOfProcess)

"""
terminateFeature function allows the user to exit the program freely.
It will also show how many requests have been made during the session.
After that, it will clear all displayed details.
"""
def terminateFeature(numOFProcess):
    sys.exit(f"Thank you for using our Program!\nYou have requested {numOFProcess} time(s).")

"""
authenticatingUser function compares the entered studentID from startFeature
to the available records from the StudentTranscript.csv.
After comparing, it will store its indices.
"""
def authenticatingUser(listToCheck, idNumber):
    indices = []
    for index, value in enumerate(listToCheck):
        if value == idNumber:
            indices.append(index)
    return indices

"""
This is a part of authenticatingUser under startFeature.
gettingUserInfo function gets the index list and stores the student list.
It returns the student list.
"""
def gettingUserInfo(indexList, studentList):
    student = []
    for x in indexList:
        student.append(studentList[x])
    return student

"""
This function is under detailsFeature.
It chooses which studentID will match the user's chosen studentID.
This function aims to return only one studentID.
"""
def studentID(userStudent):
    idStr = []
    for id in userStudent:
        if id[1] not in idStr:
            idStr.append(id[1])
    return idStr

"""
This function is under detailsFeature.
It chooses which level will match the user's chosen level.
This function aims to return only one level.
"""
def levels(userStudent):
    levelStr = []
    for level in userStudent:
        if level[5] not in levelStr:
            levelStr.append(level[5])
    return levelStr

"""
This function is under detailsFeature.
It chooses which college will match the user's chosen college.
This function aims to return only one college.
"""
def colleges(userStudent):
    collegeStr = []
    for college in userStudent:
        if college[3] not in collegeStr:
            collegeStr.append(college[3])
    return collegeStr

"""
This function is under detailsFeature.
It chooses which department will match the user's chosen department.
This function aims to return only one department.
"""
def departments(userStudent):
    departmentStr = []
    for department in userStudent:
        if department[4] not in departmentStr:
            departmentStr.append(department[4])
    return departmentStr

"""
This function is under detailsFeature.
It chooses which term will match the user's chosen term.
This function aims to return only one term.
"""
def terms(userStudent):
    termsStr = []
    for term in userStudent:
        termsStr.append(term[9])
    return termsStr

"""
This average function is used whenever the average of
a list of grades is needed. It computes the average.
"""
def average(grades):
    if len(grades) == 0:
        return ("")
    sum = 0
    for grade in grades:
        sum += int(grade)
    return sum/len(grades)

"""
countdown function is used whenever a feature is finished.
It adds 1 into the numOfProcess variable every time it is called.
It will wait 3 seconds to clear the console.
It will then redirect the user to the menuFeature
"""
def countdown(userStudent, stdID, numOfProcess, degree, studentLevel):
    numOfProcess += 1
    print("\nWaiting...\n")
    time.sleep(3)
    # os.system("cls")
    menuFeature(userStudent, stdID, numOfProcess, degree, studentLevel)

"""
menu function is the primary start of the program.
It has informationOfUser, stdID, degree, studentLevel which
depends upon the startFeature.

numOfProcess variable is used to know how many requests the user
has made during the session.
"""
def menu(numOfProcess):
    os.system("cls")
    informationOfUser, stdID, degree, studentLevel = startFeature(numOfProcess)
    menuFeature(informationOfUser, stdID, numOfProcess, degree, studentLevel)


menu(numOfProcess=0)
