#!/usr/bin/env python3
"""
GradeBook Analyzer CLI
Author:Ritika yadav
Date: 2025-11-15
Description:
A Python CLI tool that:
- Reads student marks (manual input or CSV)
- Performs statistical analysis (average, median, min, max)
- Assigns grades
- Displays pass/fail lists
- Prints formatted results table
- Allows repeated runs using a CLI loop
"""

import csv
import statistics
import os

# ---------------------------------------------------------
# Welcome Screen
# ---------------------------------------------------------
def welcome():
    
    print("=" * 60)
    print("           📘 GradeBook Analyzer - Python CLI")
    print("Options:")
    print("  1) Manual Input of Students")
    print("  2) Load from CSV")
    print("  3) Export Results to CSV")
    print("  4) Sample Test Data")
    print("  5) Exit")
    print("=" * 60)

# ---------------------------------------------------------
# Menu Prompt
# ---------------------------------------------------------
def prompt_menu():
    return input("Choose an option (1–5): ").strip()

# ---------------------------------------------------------
# Task 2 – Manual Entry
# ---------------------------------------------------------
def manual_input():
    print("\nManual Data Entry Mode")
    print("Enter student name and marks.")
    print("Leave name empty to finish.\n")

    marks = {}
    while True:
        name = input("Student Name: ").strip()
        if name == "":
            break
        
        try:
            score = float(input(f"Enter marks for {name}: "))
            if score < 0 or score > 100:
                print("Marks must be between 0 and 100.")
                continue
        except ValueError:
            print("Invalid number. Try again.")
            continue

        marks[name] = score

    return marks

# ---------------------------------------------------------
# Task 2 – Load from CSV
# ---------------------------------------------------------
def load_csv(path):
    marks = {}

    if not os.path.exists(path):
        print("❌ File does not exist!")
        return {}

    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header if present

        for row in reader:
            if len(row) != 2:
                print("Skipping invalid row:", row)
                continue

            name = row[0].strip()
            try:
                score = float(row[1].strip())
            except ValueError:
                print("Invalid score, skipping:", row)
                continue

            marks[name] = score

    return marks

# ---------------------------------------------------------
# Task 3 – Statistical Analysis
# ---------------------------------------------------------
def calculate_average(marks):
    return sum(marks.values()) / len(marks)

def calculate_median(marks):
    return statistics.median(list(marks.values()))

def find_max_score(marks):
    name = max(marks, key=marks.get)
    return (name, marks[name])

def find_min_score(marks):
    name = min(marks, key=marks.get)
    return (name, marks[name])

# ---------------------------------------------------------
# Task 4 – Grade Assignment
# ---------------------------------------------------------
def assign_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

# ---------------------------------------------------------
# Grade Distribution
# ---------------------------------------------------------
def grade_distribution(grades):
    dist = { "A":0, "B":0, "C":0, "D":0, "F":0 }
    for grade in grades.values():
        dist[grade] += 1
    return dist

# ---------------------------------------------------------
# Task 5 – Pass / Fail (List Comprehension)
# ---------------------------------------------------------
def pass_fail_lists(marks):
    passed = [name for name, m in marks.items() if m >= 40]
    failed = [name for name, m in marks.items() if m < 40]
    return passed, failed

# ---------------------------------------------------------
# Task 6 – Results Table
# ---------------------------------------------------------
def print_table(marks, grades):
    print("\n" + "-"*40)
    print(f"{'Name':<15} {'Marks':<10} {'Grade':<5}")
    print("-"*40)
    
    for name, score in marks.items():
        print(f"{name:<15} {score:<10.2f} {grades[name]:<5}")

    print("-"*40)

# ---------------------------------------------------------
# Export Results to CSV
# ---------------------------------------------------------
def export_to_csv(marks, grades, filename):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Marks", "Grade"])
        for name, score in marks.items():
            writer.writerow([name, score, grades[name]])

    print(f"\n✔ Results exported successfully to {filename}\n")

# ---------------------------------------------------------
# Analysis Function
# ---------------------------------------------------------
def analyze_and_report(marks):
    if not marks:
        print("❌ No student data found.")
        return {}

    print("\n📊 ANALYSIS SUMMARY")
    print("-" * 60)

    avg = calculate_average(marks)
    med = calculate_median(marks)
    max_name, max_val = find_max_score(marks)
    min_name, min_val = find_min_score(marks)

    grades = {name: assign_grade(score) for name, score in marks.items()}

    print(f"Total Students : {len(marks)}")
    print(f"Average Score  : {avg:.2f}")
    print(f"Median Score   : {med:.2f}")
    print(f"Highest Score  : {max_val} ({max_name})")
    print(f"Lowest Score   : {min_val} ({min_name})")

    dist = grade_distribution(grades)
    print("\nGrade Distribution:")
    for g, count in dist.items():
        print(f"  {g}: {count}")

    passed, failed = pass_fail_lists(marks)
    print("\nPass/Fail Summary:")
    print("Passed:", passed)
    print("Failed:", failed)

    print_table(marks, grades)

    return grades

# ---------------------------------------------------------
# Sample Data (for testing)
# ---------------------------------------------------------
def sample_data():
    return {
        "Alice": 78,
        "Bob": 92,
        "Charlie": 65,
        "Diana": 55,
        "Ethan": 35
    }

# ---------------------------------------------------------
# Main Program Loop
# ---------------------------------------------------------
def main():
    marks = {}
    grades = {}

    while True:
        welcome()
        choice = prompt_menu()

        if choice == "1":
            marks = manual_input()
            grades = analyze_and_report(marks)

        elif choice == "2":
            path = input("Enter CSV file path: ")
            marks = load_csv(path)
            grades = analyze_and_report(marks)

        elif choice == "3":
            if not marks:
                print("❌ No data available. Run analysis first.")
            else:
                filename = input("Enter export filename: ")
                export_to_csv(marks, grades, filename)

        elif choice == "4":
            marks = sample_data()
            grades = analyze_and_report(marks)

        elif choice == "5":
            print("\nExiting program... Goodbye! 👋")
            break

        else:
            print("Invalid choice. Try again.")

# ---------------------------------------------------------
# Run Program
# ---------------------------------------------------------
if __name__ == "__main__":
    main()