import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import csv
import random
import os

# Function to generate the CSV with random data
def generate_csv():
    # Sample student names and subjects
    names = ["Amir", "Arun", "Ram", "Ravi", "Yusuf", "Esha", "Afra", "Savi", "Riya", "Tanvi", "Sana"]
    subjects = ["Maths", "Science", "English", "History", "Geography", "Physics", "Chemistry", "Biology"]

    # Create and write to the CSV file
    with open("scores.csv", mode="w", newline="") as file:
        writer = csv.writer(file)

        # Write the header row
        writer.writerow(["Name", "Subject", "Marks"])

        # Generate 50 random student records
        for i in names:
            for j in subjects:
                name = i
                subject = j
                marks = random.randint(60, 100)
                writer.writerow([name, subject, marks])

    st.success("Random student data has been generated and saved in 'scores.csv'.")

# Function to assign grades based on marks
def assign_grade(marks):
    if 100 >= marks >= 90:
        return "A"
    elif 89 >= marks >= 80:
        return "B"
    elif 79 >= marks >= 70:
        return "C"
    elif 69 >= marks >= 60:
        return "D"
    else:
        return "F"
def validate_file(df):
    required_columns = {"Name", "Subject", "Marks"}
    if not required_columns.issubset(df.columns):
        return False
    return True
# Streamlit App Interface
st.title('Student Grade and Insights Generator')

# Button to generate random student data
if st.button('Generate Random Student Data'):
    generate_csv()
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Check if columns match
    if not validate_file(df):
        st.error("Invalid file format! Please upload a file with columns: Name, Subject, Marks.")
    else:
        st.success("File uploaded successfully!")
        st.dataframe(df)
# Upload student CSV file

file_path = r"C:\Users\maniv\PycharmProjects\pythonProject\scores.csv"
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    st.subheader('Student Marks Table')
    st.dataframe(df)

    # Assign grades based on marks
    df["Grade"] = df["Marks"].apply(assign_grade)

    # Total Marks per Student
    total = df.groupby("Name")["Marks"].sum().sort_values(ascending=False).reset_index()

    # Display total marks per student
    st.subheader("Total Marks per Student")
    st.write(total)

    # Bar plot for total marks per student
    st.subheader("Bar Plot: Total Marks per Student")
    plt.figure(figsize=(10, 6))
    sns.barplot(x=total["Name"], y=total["Marks"], hue=total["Name"])
    plt.title("Total Marks per Student")
    plt.xticks(rotation=90)
    plt.xlabel("Name")
    plt.ylabel("Total Marks")
    st.pyplot()

    # Average Marks per Student
    avg_marks = df.groupby("Name")["Marks"].mean().sort_values(ascending=False).reset_index()

    # Display average marks per student
    st.subheader("Average Marks per Student")
    st.write(avg_marks)

    # Bar plot for average marks per student
    st.subheader("Bar Plot: Average Marks per Student")
    plt.figure(figsize=(10, 6))
    sns.barplot(x=avg_marks["Name"], y=avg_marks["Marks"], hue=avg_marks["Name"])
    plt.title("Average Marks per Student")
    plt.xticks(rotation=90)
    plt.xlabel("Name")
    plt.ylabel("Average Marks")
    st.pyplot()

    # Grade Distribution Pie Chart
    st.subheader("Grade Distribution")
    grade_dist = df['Grade'].value_counts()
    grade_dist.plot(kind="pie", autopct='%1.1f%%', startangle=90, title="Grade Distribution")
    plt.ylabel("")  # Hide the y-label
    st.pyplot()

    # Rank based on total marks
    total_marks = df.groupby("Name")["Marks"].sum().reset_index()
    total_marks['Rank'] = total_marks['Marks'].rank(ascending=False, method="min")
    total_marks_sorted = total_marks.sort_values("Marks", ascending=False)

    # Display total marks and rank information
    st.subheader("Rank Based on Total Marks")
    st.write(total_marks_sorted)

    # Bar plot for total marks and ranks
    st.subheader("Bar Plot: Total Marks per Student (Ranked)")
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Marks", y="Name", data=total_marks_sorted, palette="viridis")
    plt.title("Total Marks per Student (Ranked)")
    plt.xlabel("Total Marks")
    plt.ylabel("Student Name")
    st.pyplot()

