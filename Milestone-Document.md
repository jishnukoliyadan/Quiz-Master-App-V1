# Milestone Document

**[Project Statement : Quiz-Master-App-V1](https://github.com/jishnukoliyadan/Quiz-Master-App-V1/blob/main/Problem-Statement.md)**

The milestones are divided into **Core Requirements**, **Recommended Functionalities**, and **Optional Enhancements**. Students can complete any core milestone(1-7) in any order but recommended and optional (milestone 8-11) need to be done only after the core is completed. Each milestone includes a **brief explanation** and a **Git commit message** to track progress. When you finish a milestone, use the exact Git commit message given in every milestone to save your work. Then, push the changes to GitHub to update the online version of your project.

---

## Milestone 0 : GitHub Repository Setup (Mandatory)

✅ **Expected Time :** 1 day

📊 **Completion Progress :** 5%

- Create a **private GitHub repository** for the project.
- Add a **README.md** file with a basic project description.
- Set up a .gitignore file to exclude unnecessary files.
- Commit and push the initial setup to the repository.
- Refer to the [git tracker document](https://www.google.com/url?q=https://docs.google.com/document/d/e/2PACX-1vSQb6y00ELBQ4MC1FAhn1JO8LmVsxGe1ke_aJi8hEIEHYLO8RqHDzl0bxZtxj6J-AYumNrA7jdxRmyu/pub&sa=D&source=editors&ust=1744903895934436&usg=AOvVaw0uCznFANbDX-eVfxbPl3Vn) to add **MADI-cs2003** as your collaborator, so that we can track your project.
- Github Adding Collaborator Video: [Adding Github Collaborator using VSCode and WSL](https://www.google.com/url?q=https://youtu.be/fUY1MtqCoRU&sa=D&source=editors&ust=1744903895934894&usg=AOvVaw38vhpJOnnsMeB29Fa8nJg7)

**Git Commit Message :** `Initialized private GitHub repository with README and .gitignore`

---

## Core Requirements (Milestones 1-7)

### Milestone 1: Database Models and Schema Setup

✅ **Expected Time :** 5-7 days

📊 **Completion Progress :** 15%

- Define tables for User, Admin, Subject, Chapter, Quiz, Question, Score,etc. in SQLite.
- Set up relationships between tables (e.g., Subjects have multiple Chapters, Quizzes belong to Chapters).
- Ensure the database is programmatically created through a python script/file.

**Git Commit Message :** `Created database schema for users, subjects, quizzes, and scores`

---

### Milestone 2 : Authentication and Role Management

✅ **Expected Time :** 5 days

📊 **Completion Progress :** 10%

- Create an **Admin login** (Admin is predefined, no registration allowed).
- Implement **User registration and login** with required fields (username (email), password, full name, etc.).
- Users should be redirected to their respective dashboards after login.

**Git Commit Message :** `Implemented user registration and admin login functionality`

---

### Milestone 3 : Admin Dashboard and Management

✅ **Expected Time :** 7-9 days

📊 **Completion Progress :** 20%

- Admin should be able to :

- **Create/Edit/Delete Subjects**.
- **Create/Edit/Delete Chapters** under a subject.
- **Create/Edit/Delete Quizzes** under a chapter.
- **Create/Edit/Delete Questions** under a quiz.

- Admin should see a list of all users and their details.

**Git Commit Message :** `Built Admin dashboard with CRUD operations for subjects, chapters, quizzes, and questions`

---

### Milestone 4 : User Dashboard and Quiz Attempt System

✅ **Expected Time :** 7 days

📊 **Completion Progress :** 15%

- Users should see a list of **available subjects and quizzes**.
- Users should be able to **attempt a quiz** (MCQ format with one correct option).
- Implement a **timer** for each quiz.
- Users should get feedback on correct/incorrect answers after the quiz.
- Store **quiz scores in the database**.

**Git Commit Message :** `Developed User dashboard with quiz attempt functionality and timer`

---

### Milestone 5 : Score Management and Quiz Result Display

✅ **Expected Time :** 5 days

📊 **Completion Progress :** 15%

- Store quiz scores after submission.
- Users should see **past quiz attempts and scores**.
- Display a **quiz summary report** with total scores.

**Git Commit Message :** `Implemented score tracking and quiz result display`

---

### Milestone 6 : Search Functionality for Admin and Users

✅ **Expected Time :** 4 days

📊 **Completion Progress :** 10%

- **Admin Search :**

- Admin can search for **users, subjects, quizzes, and questions**.

- **User Search :**

- Users can search for **subjects and quizzes**.

**Git Commit Message :** `Added search functionality for Admin and Users`

---

### Milestone 7 : Quiz Time and Duration Management

✅ **Expected Time :** 4 days

📊 **Completion Progress :** 10%

- Admin should set **date and time duration** (HH:MM) when creating a quiz.
- Users should only be able to **attempt quizzes within the given timeframe**.

**Git Commit Message :** `Implemented quiz scheduling with time duration`

## Recommended Functionalities (Milestones 8-9)

---

### Milestone 8 : API Development for Data Access

✅ **Expected Time :** 7 days

- Develop API endpoints to fetch **subjects, chapters, quizzes, and scores**.
- Ensure APIs return **JSON responses**.

**Git Commit Message :** `Created API endpoints for subjects, quizzes, and scores`

---

### Milestone 9 : Summary Charts and Data Visualization

✅ **Expected Time :** 5 days

- Display **quiz performance charts** for users.
- Admin should see **summary statistics of quizzes and users**.

**Git Commit Message :** `Added summary charts for quiz statistics and user performance`

## Optional Enhancements (Milestones 10-11) → Extra Work

---

### Milestone 10 : Frontend Enhancements and UI Improvements

✅ **Expected Time :** 7-9 days

- Improve UI with **Bootstrap and CSS**.
- Implement **frontend validation** for forms.
- Ensure the app is **mobile-responsive**.

**Git Commit Message :** `Enhanced UI with Bootstrap styling and form validation`

---

### Milestone 11 : Security Enhancements and Final Testing

✅ **Expected Time :** 7 days

- Implement **backend validation** for form inputs.
- Perform **final testing** to fix any bugs or security loopholes.
- Ensure **all routes are protected** based on user roles.

**Git Commit Message :** `Enhanced security with backend validation and finalized testing`

---

## Final Project Submission

### Milestone 12 : Final Project Submission Details

✅ Expected Time : 2 days
📊 After, **Completion Progress is 100%.**
Ensure you submit the final project, including:

- Code ZIP file.
- 3-5 page report.
- 3-10 min video presentation.
- The video should be uploaded to your g-drive with access granted to anyone with the link.
- The link must be included in the report for review. Report pdf should be added to the zip file.

**Git Commit Message :** `Finalized project submission with report and presentation link`

---

## Tracking Progress

To track progress, you should:

1. **Use Git commits** for each milestone.
2. **Test functionality** after completing each milestone.
3. **Log issues** encountered and their resolutions in a README.md or GitHub Issues section.

## Timeline Overview

### Project Completion Overview

| Milestone                            | Average Time Estimate | Split (%) | Progress (%) |
| ------------------------------------ | :-------------------: | :-------: | :----------: |
| Milestone 00 : GitHub Setup          | 1 day                 | 5%        | 5%           |
| Milestone 01 : Database Setup        | 5-7 days              | 15%       | 20%          |
| Milestone 02 : Authentication        | 5 days                | 10%       | 30%          |
| Milestone 03 : Admin Dashboard       | 7-9 days              | 20%       | 50%          |
| Milestone 04 : User Dashboard & Quiz | 7 days                | 15%       | 65%          |
| Milestone 05 : Score Management      | 5 days                | 15%       | 80%          |
| Milestone 06 : Search Feature        | 4 days                | 10%       | 90%          |
| Milestone 07 : Quiz Time & Duration  | 4 days                | 10%       | 100%         |

### Extra Work Overview

| Milestone                               | Average Time Estimate |
| --------------------------------------- | :-------------------: |
| Milestone 08 : API Development          | 7 days                |
| Milestone 09 : Summary Charts           | 5 days                |
| Milestone 10 : UI Enhancements          | 7-9 days              |
| Milestone 11 : Security & Final Testing | 7 days                |

### Final Submission Overview

| Milestone                                       | Average Time Estimate |
| ----------------------------------------------- | :-------------------: |
| Milestone 12 : Final Project Submission Details | 2 days                |

**Note :** *The average time estimate is not a strict deadline. Each student has a different level of understanding, so you can take the time you need. The provided time estimates indicate the average duration students typically take to complete each milestone if they dedicate 2-3 hours (approx.) per day.*

---

**Reference :** [Milestones for Quiz Master Application Development-1](https://docs.google.com/document/d/e/2PACX-1vT1opu2dyxa2IJOKLS875jsI9hkkc7bFvEULZypXfogEBZM2iTVeX6h4OrNkZrnJSxN7T-c8iPIz36R/pub)
