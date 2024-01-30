from nerodia.browser import Browser
import pandas as pd
import glob
import os

def main():
    """
    Set these accordingly for both yourself and the assignment.
    The csv should be acquired from the main eClass page -> Grades -> Export
    """
    file_location = os.path.dirname(os.path.realpath(__file__))
    mark_csv_path = glob.glob(os.path.join(file_location, "csv", "*.csv"))[0]
    primary_key = "Student ID"

    df = pd.read_csv(mark_csv_path)
    df.sort_values(primary_key, inplace=True)
    br = Browser(browser='firefox')
    br.goto("https://docsdb.cs.ualberta.ca/")

    # Login
    br.text_field(name="oracle.login").value = os.environ["DOCSDB_USERNAME"]
    br.text_field(name="oracle.password").value = os.environ["DOCSDB_PASSWORD"]
    br.button(value="Get Menu").click()

    # Go to section marks
    br.radio(value="entersec").click()
    br.button(value="Run Form").click()

    # Get specific assignment
    assignmentType = "Assignment"  # Change this to the correct assignment type
    assignmentNo = "5"  # Change this to the correct assignment number
    courseNum = "204"  # Change this to the correct course number
    br.text_field(name="coursenum").value = courseNum
    br.text_field(name="type").value = assignmentType
    br.text_field(name="num").value = assignmentNo
    br.button(value="Get List").click()

    # Input marks
    assignmentName = "Assignment: Assignment 5 (due Mar 7) (Real)"
    for i in range(len(df)):
        mark = df.loc[i][assignmentName]
        if df.loc[i][assignmentName] != "-":
            student_id = str(df.loc[i][primary_key])
            br.text_field(css=f"[value='{student_id}'] + input").value = mark

    # Display warning
    print("Please double check the marks before submission!")
    print("This includes fixing excused absences, etc.")
    
if __name__ == "__main__":
    main()