# solutions.py


import sqlite3 as sql
import numpy as np


def prob1(db_file="students.db"):
    """Query the database for the list of the names of students who have a
    'B' grade in any course. Return the list.

    Parameters:
        db_file (str): the name of the database to connect to.

    Returns:
        (list): a list of strings, each of which is a student name.
    """
    try:
        # Drop all tables
        with sql.connect(db_file) as conn:
            cur = conn.cursor()  # Get the cursor

            # Return the Student and Course Names for students that received A or A+
            temp = cur.execute("SELECT SI.StudentName FROM StudentInfo AS SI INNER JOIN StudentGrades AS SG ON SI.StudentID = SG.StudentID WHERE SG.Grade == 'B'").fetchall()

    except sql.Error:  # If there is an error,
        conn.rollback()  # revert the changes
        raise  # and raise the error.
    else:  # If there are no errors,
        conn.commit()
    finally:  # Commit or revert, then
        conn.close()

    return np.ravel(temp)  # Return the list of strings


def prob2(db_file="students.db"):
    """Query the database for all tuples of the form (Name, MajorName, Grade)
    where 'Name' is a student's name and 'Grade' is their grade in Calculus.
    Only include results for students that are actually taking Calculus, but
    be careful not to exclude students who haven't declared a major.

    Parameters:
        db_file (str): the name of the database to connect to.

    Returns:
        (list): the complete result set for the query.
    """
    try:
        # Drop all tables
        with sql.connect(db_file) as conn:
            cur = conn.cursor()  # Get the cursor

            # Select the tuples with left outer join for major info
            temp = cur.execute("SELECT SI.StudentName, MI.MajorName, SG.Grade "
                               "FROM StudentInfo AS SI LEFT OUTER JOIN MajorInfo AS MI ON MI.MajorID == SI.MajorID "
                               "INNER JOIN StudentGrades AS SG ON SI.StudentID == SG.StudentID "
                               "WHERE SG.CourseID == 1;").fetchall()

    except sql.Error:  # If there is an error,
        conn.rollback()  # revert the changes
        raise  # and raise the error.
    else:  # If there are no errors,
        conn.commit()
    finally:  # Commit or revert, then
        conn.close()

    return temp  # Return the list of tuples


def prob3(db_file="students.db"):
    """Query the given database for tuples of the form (MajorName, N) where N
    is the number of students in the specified major. Sort the results in
    descending order by the counts N, then in alphabetic order by MajorName.

    Parameters:
        db_file (str): the name of the database to connect to.

    Returns:
        (list): the complete result set for the query.
    """
    try:
        # Drop all tables
        with sql.connect(db_file) as conn:
            cur = conn.cursor()  # Get the cursor

            # Select the tuples with left outer join for major info
            temp = cur.execute("SELECT MI.MajorName, COUNT(*) as N "
                               "FROM StudentInfo AS SI "
                               "LEFT OUTER JOIN MajorInfo AS MI "
                               "ON MI.MajorID == SI.MajorID "
                               "GROUP BY MI.MajorID "
                               "ORDER BY N DESC, MI.MajorName ASC;").fetchall()

    except sql.Error:  # If there is an error,
        conn.rollback()  # revert the changes
        raise  # and raise the error.
    else:  # If there are no errors,
        conn.commit()
    finally:  # Commit or revert, then
        conn.close()
    return temp  # Return the list of tuples


def prob4(db_file="students.db"):
    """Query the database for tuples of the form (StudentName, N, GPA) where N
    is the number of courses that the specified student is in and 'GPA' is the
    grade point average of the specified student according to the following
    point system.

        A+, A  = 4.0    B  = 3.0    C  = 2.0    D  = 1.0
            A- = 3.7    B- = 2.7    C- = 1.7    D- = 0.7
            B+ = 3.4    C+ = 2.4    D+ = 1.4

    Order the results from greatest GPA to least.

    Parameters:
        db_file (str): the name of the database to connect to.

    Returns:
        (list): the complete result set for the query.
    """
    try:
        # Drop all tables
        with sql.connect(db_file) as conn:
            cur = conn.cursor()  # Get the cursor

            # Select the tuples with left outer join for major info
            temp = cur.execute("SELECT SI.StudentName, COUNT(*), AVG(SG.GPA) "
                               "FROM ("
                                    "SELECT StudentID, CASE Grade "
                                       "WHEN 'A+' THEN 4.0 "
                                       "WHEN 'A' THEN 4.0 "
                                       "WHEN 'A-' THEN 3.7 "
                                       "WHEN 'B+' THEN 3.4 "
                                       "WHEN 'B' THEN 3.0 "
                                       "WHEN 'B-' THEN 2.7 "
                                       "WHEN 'C+' THEN 2.4 "
                                       "WHEN 'C' THEN 2.0 "
                                       "WHEN 'C-' THEN 1.7 "
                                       "WHEN 'D+' THEN 1.4 "
                                       "WHEN 'D' THEN 1.0 "
                                       "WHEN 'D-' THEN 0.7 "
                                       "ELSE 0 END AS GPA "
                                    "FROM StudentGrades) AS SG "
                               "INNER JOIN StudentInfo AS SI "
                               "ON SG.StudentID == SI.Studentid "
                               "GROUP BY SG.StudentID "
                               "ORDER BY AVG(SG.GPA) DESC;").fetchall()

    except sql.Error:  # If there is an error,
        conn.rollback()  # revert the changes
        raise  # and raise the error.
    else:  # If there are no errors,
        conn.commit()
    finally:  # Commit or revert, then
        conn.close()

    return temp  # Return the list of tuples


def prob5(db_file="mystery_database.db"):
    """Use what you've learned about SQL to identify the outlier in the mystery
    database.

    Parameters:
        db_file (str): the name of the database to connect to.

    Returns:
        (list): outlier's name, outlier's ID number, outlier's eye color, outlier's height
    """
    try:
        # Drop all tables
        with sql.connect(db_file) as conn:
            cur = conn.cursor()  # Get the cursor

            # Narrow it down to find the outlier
            ID_number = cur.execute("SELECT t2.ID_Number FROM table_2 AS t2 "
                         "WHERE t2.description LIKE '%William Thomas%';").fetchall()[0][0]

            # find appropriate data
            name, eye_color = cur.execute("SELECT t1.name, t1.eye_color "
                               "FROM table_1 AS t1 "
                               "WHERE t1.name LIKE '%William T. Riker%';").fetchall()[0]

            height = cur.execute("SELECT t3.eye_color, t3.height "
                               "FROM table_3 AS t3 "
                               "WHERE t3.eye_color == 'Hazel-blue' "
                                 "AND t3.gender == 'Male';").fetchall()[0][1]

    except sql.Error:  # If there is an error,
        conn.rollback()  # revert the changes
        raise  # and raise the error.
    else:  # If there are no errors,
        conn.commit()
    finally:  # Commit or revert, then
        conn.close()

    return [name, ID_number, eye_color, height]  # Return the list of info
