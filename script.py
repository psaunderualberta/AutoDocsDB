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
    primary_key = "Student ID"  # 7 digit student ID

    df = pd.read_csv(mark_csv_path)
    df.sort_values(primary_key, inplace=True)
    br = Browser(browser='firefox')
    br.goto("https://docsdb.cs.ualberta.ca/")

    # Login to docsdb
    # Set these environment variables, or hardcode them here.
    # IF YOU HARDCODE THEM, DO NOT COMMIT THIS FILE TO GITHUB
    br.text_field(name="oracle.login").value = os.environ["DOCSDB_USERNAME"]
    br.text_field(name="oracle.password").value = os.environ["DOCSDB_PASSWORD"]
    br.button(value="Get Menu").click()

    # Go to section marks
    br.radio(value="entersec").click()
    br.button(value="Run Form").click()

    # Get specific assignment
    assignment_type = "Assignment"  # Change this to the correct assignment type
    assignment_no = "5"  # Change this to the correct assignment number
    course_num = "204"  # Change this to the correct course number
    br.text_field(name="coursenum").value = course_num
    br.text_field(name="type").value = assignment_type
    br.text_field(name="num").value = assignment_no
    br.button(value="Get List").click()

    # Change to column in the CSV file containing the marks
    assignment_name = "Assignment: Assignment 5 (due Mar 7) (Real)"

    # Input marks
    missing_mark_str = "-"
    valid_df = df[df[assignment_name] != missing_mark_str]
    for _, (student_id, mark) in valid_df[[primary_key, assignment_name]].iterrows():
        br.text_field(css=f"[value='{student_id}'] + input").value = mark

    # Warn about missing marks
    missing_df = df[df[assignment_name] == missing_mark_str]
    ccid = "CCID"
    if len(missing_df) > 0:
        print("The following students are missing marks:")
        print(missing_df[ccid].values)
        print("These might be excused absences, or they might be missing marks.")
        print()

    # Display warning
    print("Please double check the marks before submission!")
    print("Press enter to continue.")
    input()
    
if __name__ == "__main__":
    main()