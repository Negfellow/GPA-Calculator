# Yared Nega
# August 2026
# Final Project - Cumulative GPA Calculator
# Built with tkinter (included in every standard Python install)
# No third-party libraries required - runs in IDLE or any Python 3 environment

import tkinter as tk
from tkinter import messagebox

FILE_NAME = "grades.txt"

GRADE_POINTS = {
    "A+": 4.0, "A": 4.0, "A-": 3.7,
    "B+": 3.3, "B": 3.0, "B-": 2.7,
    "C+": 2.3, "C": 2.0, "C-": 1.7,
    "D+": 1.3, "D": 1.0, "D-": 0.7,
    "F":  0.0
}

# ── Course Class ─────────────────────────────────────────────────────────────
class Course:
    """Represents a single college course with a name, grade, and credit hours."""

    def __init__(self, name, grade, credits):
        self.name    = name
        self.grade   = grade.upper()
        self.credits = int(credits)

    def gradePoints(self):
        """Returns the total quality points earned (grade value x credits)."""
        return GRADE_POINTS.get(self.grade, 0.0) * self.credits

    def __str__(self):
        """Returns a comma-separated string for file storage."""
        return f"{self.name},{self.grade},{self.credits}"


# ── GPA Calculator GUI Class ─────────────────────────────────────────────────
class GPACalculator:
    """A tkinter GUI application that tracks multiple courses and
    computes cumulative GPA. Saves and loads data from a text file."""

    def __init__(self, root):
        self.root    = root
        self.courses = []
        self.root.title("Cumulative GPA Calculator")
        self.root.resizable(False, False)
        self._buildWidgets()

    # ── Build all widgets ────────────────────────────────────────────────────
    def _buildWidgets(self):

        # ── Title banner ─────────────────────────────────────────────────────
        tk.Label(self.root, text="Cumulative GPA Calculator",
                 font=("Helvetica", 16, "bold"),
                 bg="#1a237e", fg="white",
                 padx=10, pady=8).grid(row=0, column=0, columnspan=4,
                                       sticky="we")

        # ── Input frame ──────────────────────────────────────────────────────
        inputFrame = tk.LabelFrame(self.root, text="Add a Course",
                                   font=("Helvetica", 10, "bold"),
                                   padx=10, pady=8)
        inputFrame.grid(row=1, column=0, columnspan=4,
                        padx=12, pady=8, sticky="we")

        tk.Label(inputFrame, text="Course Name:").grid(row=0, column=0, sticky="e")
        self.nameVar = tk.StringVar()
        tk.Entry(inputFrame, textvariable=self.nameVar,
                 width=22).grid(row=0, column=1, padx=6, pady=4)

        tk.Label(inputFrame, text="Grade:").grid(row=0, column=2, sticky="e")
        self.gradeVar = tk.StringVar()
        gradeOptions = ["A+","A","A-","B+","B","B-",
                        "C+","C","C-","D+","D","D-","F"]
        self.gradeMenu = tk.OptionMenu(inputFrame, self.gradeVar, *gradeOptions)
        self.gradeVar.set("A")
        self.gradeMenu.config(width=4)
        self.gradeMenu.grid(row=0, column=3, padx=6)

        tk.Label(inputFrame, text="Credit Hours:").grid(row=1, column=0, sticky="e")
        self.creditsVar = tk.StringVar()
        tk.Entry(inputFrame, textvariable=self.creditsVar,
                 width=6).grid(row=1, column=1, padx=6, pady=4, sticky="w")

        tk.Button(inputFrame, text="Add Course",
                  bg="#1a237e", fg="white", width=12,
                  command=self.addCourse).grid(row=1, column=2,
                                               columnspan=2, padx=6)

        # ── Course list display ───────────────────────────────────────────────
        listFrame = tk.LabelFrame(self.root, text="Courses",
                                  font=("Helvetica", 10, "bold"),
                                  padx=10, pady=6)
        listFrame.grid(row=2, column=0, columnspan=4,
                       padx=12, pady=4, sticky="we")

        self.listbox = tk.Listbox(listFrame, width=58, height=10,
                                  font=("Courier", 10))
        self.listbox.pack(side="left", fill="both")

        scrollbar = tk.Scrollbar(listFrame, orient="vertical",
                                 command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        # ── Buttons row ───────────────────────────────────────────────────────
        btnFrame = tk.Frame(self.root)
        btnFrame.grid(row=3, column=0, columnspan=4, pady=6)

        buttons = [
            ("Calculate GPA",  "#2e7d32", self.calculateGPA),
            ("Remove Selected","#b71c1c", self.removeSelected),
            ("Save to File",   "#e65100", self.saveToFile),
            ("Load from File", "#4527a0", self.loadFromFile),
            ("Clear All",      "#37474f", self.clearAll),
        ]
        for label, color, cmd in buttons:
            tk.Button(btnFrame, text=label, bg=color, fg="white",
                      width=14, command=cmd).pack(side="left", padx=4)

        # ── GPA result display ────────────────────────────────────────────────
        resultFrame = tk.Frame(self.root, pady=6)
        resultFrame.grid(row=4, column=0, columnspan=4)

        tk.Label(resultFrame, text="Cumulative GPA:",
                 font=("Helvetica", 13, "bold")).pack(side="left", padx=8)

        self.gpaVar = tk.StringVar(value="---")
        tk.Label(resultFrame, textvariable=self.gpaVar,
                 font=("Helvetica", 22, "bold"),
                 fg="#1a237e", width=6).pack(side="left")

        self.letterVar = tk.StringVar(value="")
        tk.Label(resultFrame, textvariable=self.letterVar,
                 font=("Helvetica", 13),
                 fg="#555").pack(side="left", padx=4)

        # ── Status bar ────────────────────────────────────────────────────────
        self.statusVar = tk.StringVar(value="Ready. Add courses to get started.")
        tk.Label(self.root, textvariable=self.statusVar,
                 anchor="w", relief="sunken",
                 font=("Helvetica", 9), fg="#333",
                 padx=6).grid(row=5, column=0, columnspan=4,
                               sticky="we", padx=0, pady=(4,0))

    # ── Command methods ───────────────────────────────────────────────────────
    def addCourse(self):
        """Validates inputs and adds a Course object to the list."""
        name    = self.nameVar.get().strip()
        grade   = self.gradeVar.get().strip().upper()
        credits = self.creditsVar.get().strip()

        if name == "":
            messagebox.showerror("Input Error", "Please enter a course name.")
            return
        if not credits.isdigit() or int(credits) <= 0:
            messagebox.showerror("Input Error",
                                 "Credit hours must be a positive whole number (e.g. 3).")
            return

        course = Course(name, grade, credits)
        self.courses.append(course)
        self._refreshListbox()
        self.nameVar.set("")
        self.creditsVar.set("")
        self.statusVar.set(f"Added: {name}  |  Grade: {grade}  |  Credits: {credits}")

    def calculateGPA(self):
        """Computes cumulative GPA weighted by credit hours."""
        if len(self.courses) == 0:
            messagebox.showwarning("No Courses",
                                   "Add at least one course before calculating.")
            return

        totalPoints  = sum(c.gradePoints() for c in self.courses)
        totalCredits = sum(c.credits       for c in self.courses)
        gpa = totalPoints / totalCredits if totalCredits > 0 else 0.0

        self.gpaVar.set(f"{gpa:.2f}")
        self.letterVar.set(f"({self._letterGrade(gpa)})")
        self.statusVar.set(
            f"GPA calculated across {len(self.courses)} course(s) "
            f"and {totalCredits} total credit hour(s)."
        )

    def removeSelected(self):
        """Removes the course selected in the listbox."""
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showinfo("Nothing Selected",
                                "Click a course in the list to select it, then Remove.")
            return
        idx = selection[0]
        removed = self.courses.pop(idx)
        self._refreshListbox()
        self.statusVar.set(f"Removed: {removed.name}")

    def saveToFile(self):
        """Writes all courses to grades.txt (one course per line)."""
        if len(self.courses) == 0:
            messagebox.showwarning("Nothing to Save", "Add courses before saving.")
            return
        f = open(FILE_NAME, "w")
        for course in self.courses:
            f.write(str(course) + "\n")
        f.close()
        self.statusVar.set(
            f"Saved {len(self.courses)} course(s) to '{FILE_NAME}'."
        )

    def loadFromFile(self):
        """Reads courses from grades.txt and adds them to the current list."""
        try:
            f = open(FILE_NAME, "r")
            lines = f.readlines()
            f.close()
        except FileNotFoundError:
            messagebox.showerror("File Not Found",
                                 f"'{FILE_NAME}' was not found.\n"
                                 "Save your courses first to create the file.")
            return

        count = 0
        for line in lines:
            parts = line.strip().split(",")
            if len(parts) == 3:
                name, grade, credits = parts
                if grade.upper() in GRADE_POINTS and credits.isdigit():
                    self.courses.append(Course(name, grade, credits))
                    count += 1

        self._refreshListbox()
        self.statusVar.set(f"Loaded {count} course(s) from '{FILE_NAME}'.")

    def clearAll(self):
        """Clears every course and resets the GPA display."""
        if len(self.courses) == 0:
            return
        confirm = messagebox.askyesno("Clear All",
                                      "Are you sure you want to remove all courses?")
        if confirm:
            self.courses = []
            self._refreshListbox()
            self.gpaVar.set("---")
            self.letterVar.set("")
            self.statusVar.set("All courses cleared.")

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _refreshListbox(self):
        """Rebuilds the course listbox from the current courses list."""
        self.listbox.delete(0, tk.END)
        if len(self.courses) == 0:
            self.listbox.insert(tk.END, "  (no courses added yet)")
            return
        header = f"  {'#':<4}{'Course':<24}{'Grade':<8}{'Credits':<10}{'Pts'}"
        self.listbox.insert(tk.END, header)
        self.listbox.insert(tk.END, "  " + "-" * 50)
        for i, c in enumerate(self.courses, 1):
            row = (f"  {i:<4}{c.name:<24}{c.grade:<8}"
                   f"{c.credits:<10}{c.gradePoints():.1f}")
            self.listbox.insert(tk.END, row)

    def _letterGrade(self, gpa):
        """Returns a letter grade label for a given GPA value."""
        if gpa >= 3.7: return "A / A+"
        if gpa >= 3.3: return "A-"
        if gpa >= 3.0: return "B+"
        if gpa >= 2.7: return "B"
        if gpa >= 2.3: return "B-"
        if gpa >= 2.0: return "C+"
        if gpa >= 1.7: return "C"
        if gpa >= 1.3: return "C-"
        if gpa >= 1.0: return "D"
        return "F"


# ── Entry point ───────────────────────────────────────────────────────────────
def main():
    root = tk.Tk()
    app  = GPACalculator(root)
    root.mainloop()

main()
