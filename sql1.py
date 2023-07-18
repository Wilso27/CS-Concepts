# sql1.py


import sqlite3 as sql
import csv
import matplotlib.pyplot as plt
import numpy as np


def student_db(db_file="students.db", student_info="student_info.csv",
                                      student_grades="student_grades.csv"):
    """Connect to the database db_file (or create it if it doesn’t exist).
    Drop the tables MajorInfo, CourseInfo, StudentInfo, and StudentGrades from
    the database (if they exist). Recreate the following (empty) tables in the
    database with the specified columns.

        - MajorInfo: MajorID (integers) and MajorName (strings).
        - CourseInfo: CourseID (integers) and CourseName (strings).
        - StudentInfo: StudentID (integers), StudentName (strings), and
            MajorID (integers).
        - StudentGrades: StudentID (integers), CourseID (integers), and
            Grade (strings).

    Next, populate the new tables with the following data and the data in
    the specified 'student_info' 'student_grades' files.

                MajorInfo                         CourseInfo
            MajorID | MajorName               CourseID | CourseName
            -------------------               ---------------------
                1   | Math                        1    | Calculus
                2   | Science                     2    | English
                3   | Writing                     3    | Pottery
                4   | Art                         4    | History

    Finally, in the StudentInfo table, replace values of −1 in the MajorID
    column with NULL values.

    Parameters:
        db_file (str): The name of the database file.
        student_info (str): The name of a csv file containing data for the
            StudentInfo table.
        student_grades (str): The name of a csv file containing data for the
            StudentGrades table.
    """

    try:  
        # Drop all tables
        with sql.connect(db_file) as conn:
            cur = conn.cursor()  # Get the cursor.
            cur.execute("DROP TABLE IF EXISTS MajorInfo;")  # Execute a SQL command.
            cur.execute("DROP TABLE IF EXISTS CourseInfo;")
            cur.execute("DROP TABLE IF EXISTS StudentInfo;")
            cur.execute("DROP TABLE IF EXISTS StudentGrades;")

            # Add all tables and columns
            cur.execute("CREATE TABLE MajorInfo (MajorID INTEGER, MajorName TEXT);")
            cur.execute("CREATE TABLE CourseInfo (CourseID INTEGER, CourseName TEXT);")
            cur.execute("CREATE TABLE StudentInfo (StudentID INTEGER, StudentName TEXT, MajorID INTEGER);")
            cur.execute("CREATE TABLE StudentGrades (StudentID INTEGER, CourseID INTEGER, Grade TEXT);")

            # Create the MajorInfo and CourseInfo tables
            rows_major = [(1, "Math"), (2, "Science"), (3, "Writing"), (4, "Art")]
            rows_course = [(1, "Calculus"), (2, "English"), (3, "Pottery"), (4, "History")]
            # Read in the CSV files
            with open(student_info, 'r') as infile:
                rows_info = list(csv.reader(infile))
            with open(student_grades, 'r') as infile:
                rows_grades = list(csv.reader(infile))

            # Add all info to the tables
            cur.executemany("INSERT INTO MajorInfo VALUES(?,?);", rows_major)
            cur.executemany("INSERT INTO CourseInfo VALUES(?,?);", rows_course)
            cur.executemany("INSERT INTO StudentInfo VALUES(?,?,?);", rows_info)
            cur.executemany("INSERT INTO StudentGrades VALUES(?,?,?);", rows_grades)

            # replace -1 with NULL values
            cur.execute("UPDATE StudentInfo SET MajorID=NULL WHERE MajorID==-1")

    except sql.Error:  # If there is an error,
        conn.rollback()  # revert the changes
        raise  # and raise the error.
    else:  # If there are no errors,
        conn.commit()
    finally:  # Commit or revert, then
        conn.close()


def earthquakes_db(db_file="earthquakes.db", data_file="us_earthquakes.csv"):
    """Connect to the database db_file (or create it if it doesn’t exist).
    Drop the USEarthquakes table if it already exists, then create a new
    USEarthquakes table with schema
    (Year, Month, Day, Hour, Minute, Second, Latitude, Longitude, Magnitude).
    Populate the table with the data from 'data_file'.

    For the Minute, Hour, Second, and Day columns in the USEarthquakes table,
    change all zero values to NULL. These are values where the data originally
    was not provided.

    Parameters:
        db_file (str): The name of the database file.
        data_file (str): The name of a csv file containing data for the
            USEarthquakes table.
    """
    try:  
        # Drop all tables
        with sql.connect(db_file) as conn:
            cur = conn.cursor()  # Get the cursor.
            cur.execute("DROP TABLE IF EXISTS USEarthquakes;")  # Execute a SQL command.
            cur.execute("CREATE TABLE USEarthquakes (Year INTEGER, Month INTEGER, Day INTEGER, Hour INTEGER, Minute INTEGER, Second INTEGER, Latitude REAL, Longitude REAL, Magnitude REAL);")

            # Read in the CSV files
            with open(data_file, 'r') as infile:
                rows = list(csv.reader(infile))

            # Add all info to the table
            cur.executemany("INSERT INTO USEarthquakes VALUES(?,?,?,?,?,?,?,?,?);", rows)

            # Remove rows with magnitude 0
            cur.execute("DELETE FROM USEarthquakes WHERE Magnitude==0")

            # Replace 0 vals in day, hour, minute, second with NULL
            cur.execute("UPDATE USEarthquakes SET Day=NULL WHERE Day==0")
            cur.execute("UPDATE USEarthquakes SET Hour=NULL WHERE Hour==0")
            cur.execute("UPDATE USEarthquakes SET Minute=NULL WHERE Minute==0")
            cur.execute("UPDATE USEarthquakes SET Second=NULL WHERE Second==0")

    except sql.Error:  # If there is an error,
        conn.rollback()  # revert the changes
        raise  # and raise the error.
    else:  # If there are no errors,
        conn.commit()
    finally:  # Commit or revert, then
        conn.close()


def prob5(db_file="students.db"):
    """Query the database for all tuples of the form (StudentName, CourseName)
    where that student has an 'A' or 'A+'' grade in that course. Return the
    list of tuples.

    Parameters:
        db_file (str): the name of the database to connect to.

    Returns:
        (list): the complete result set for the query.
    """
    try:
        # Drop all tables
        with sql.connect(db_file) as conn:
            cur = conn.cursor()  # Get the cursor

            # Return the Student and Course Names for students that received A or A+
            temp = cur.execute("SELECT SI.StudentName, CI.CourseName "
                               "FROM StudentInfo AS SI, CourseInfo AS CI, StudentGrades AS SG "
                               "WHERE (SG.Grade=='A' OR SG.Grade=='A+') AND SI.StudentID==SG.StudentID AND CI.CourseID==SG.CourseID").fetchall()

    except sql.Error:  # If there is an error,
        conn.rollback()  # revert the changes
        raise  # and raise the error.
    else:  # If there are no errors,
        conn.commit()
    finally:  # Commit or revert, then
        conn.close()

    return temp  # Return the tuple


def prob6(db_file="earthquakes.db"):
    """Create a single figure with two subplots: a histogram of the magnitudes
    of the earthquakes from 1800-1900, and a histogram of the magnitudes of the
    earthquakes from 1900-2000. Also calculate and return the average magnitude
    of all of the earthquakes in the database.

    Parameters:
        db_file (str): the name of the database to connect to.

    Returns:
        (float): The average magnitude of all earthquakes in the database.
    """
    try:
        with sql.connect(db_file) as conn:
            cur = conn.cursor()  # Get the cursor

            # query to get the magnitudes by century and avg mag
            mag_1800 = cur.execute("SELECT Magnitude FROM USEarthquakes WHERE Year<1900 AND Year>= 1800").fetchall()
            mag_1900 = cur.execute("SELECT Magnitude FROM USEarthquakes WHERE Year<2000 AND Year>= 1900").fetchall()
            avg_mag = cur.execute("SELECT AVG(Magnitude) FROM USEarthquakes").fetchall()
    except sql.Error:  # If there is an error,
        conn.rollback()  # revert the changes
        raise  # and raise the error.
    else:  # If there are no errors,
        conn.commit()
    finally:  # Commit or revert, then
        conn.close()

    # Convert from list of tuples to array of floats
    data_1800 = np.ravel(mag_1800)
    data_1900 = np.ravel(mag_1900)

    # plot the two histograms
    plt.subplot(121)
    plt.ylim(0, 850)
    plt.ylabel("# of Earthquakes")
    plt.xlabel("Magnitude")
    plt.title("19th Century")
    plt.hist(data_1800)
    plt.subplot(122)
    plt.ylim(0, 850)
    plt.xlabel("Magnitude")
    frame1 = plt.gca()
    frame1.axes.get_yaxis().set_visible(False)
    plt.title("20th Century")
    plt.hist(data_1900)

    plt.tight_layout()
    plt.show()

    return avg_mag[0][0]  # return the avg magnitude
