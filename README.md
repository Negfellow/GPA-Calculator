##Cumulative GPA Calculator

A desktop GPA calculator built with Python and tkinter as a final project for **ITSE-1370 (Intro to Python)** at Dallas College. No third-party libraries required — runs on any machine with Python 3 installed, including IDLE.

---

## Features

- Add multiple courses with name, letter grade (A+ through F), and credit hours
- Calculates **cumulative GPA** weighted by credit hours using the standard 4.0 scale
- Displays a **letter grade label** alongside the GPA (e.g. 3.50 → B+)
- **Save** your course list to a `grades.txt` file
- **Load** a previously saved course list back into the app
- **Remove** any selected course from the list
- **Clear all** courses with a confirmation prompt
- Input validation with pop-up error messages
- Scrollable course table showing course name, grade, credits, and quality points
- Status bar showing feedback after every action

---

## How to Run

1. Make sure Python 3 is installed on your computer — [download here](https://www.python.org/downloads/)
2. Clone or download this repository
3. Run the program:

```bash
python gpacalculator.py
```

Or open `gpacalculator.py` in IDLE and press **F5**.

No pip installs needed — tkinter comes built into Python 3.

---

## GPA Formula

GPA is calculated using the standard weighted formula:

```
GPA = Total Quality Points / Total Credit Hours

Quality Points per course = Grade Value × Credit Hours
```

### Grade Scale

| Grade | Points | Grade | Points |
|-------|--------|-------|--------|
| A+    | 4.0    | C+    | 2.3    |
| A     | 4.0    | C     | 2.0    |
| A-    | 3.7    | C-    | 1.7    |
| B+    | 3.3    | D+    | 1.3    |
| B     | 3.0    | D     | 1.0    |
| B-    | 2.7    | D-    | 0.7    |
|       |        | F     | 0.0    |

---

## File Storage

Courses are saved to a plain text file named `grades.txt` in the same folder as the program. Each line stores one course in the format:

```
Course Name, Grade, Credits
Math 1314, A,3
English 1301, B+,3
History 1301, A-,4
```

This file can be opened, edited, or shared like any other text file.

---

## Project Structure

```
gpa-calculator/
├── gpacalculator.py   # main program
├── grades.txt         # auto-generated when you save courses
└── README.md          # this file
```

---

## Concepts Used

- Object-oriented programming — `Course` class and `GPACalculator` class
- tkinter GUI — labels, entries, buttons, listbox, scrollbar, option menu
- File I/O — reading and writing course data to a text file
- Input validation and error handling
- Weighted average calculation

---
##Downoad ZIP
Visit https://negfellow.github.io/GPA-Calculator/ to copy the entire repository. 

## Author

Negfellow
Python course final project
August 2026
