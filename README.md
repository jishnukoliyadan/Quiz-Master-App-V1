# Quiz-Master-App-V1

## Overview

This is a Flask-based Quiz Application that allows users to take quizzes, track their performance, and provides an admin panel for managing quizzes and analyzing user performance.

![Quiz Master Screenshot](quizapp/static/images/admin_summary.png)

## Features

- **User Roles**
  - Admin : Create/manage subjects, chapters, quizzes, and questions
  - Users : Attempt quizzes, view scores/history
- **Quiz Management**
  - Time-limited quizzes with multiple questions
  - Automatic scoring system
  - Quiz attempt history tracking
- **Subject Hierarchy**
  - Subjects → Chapters → Quizzes → Questions
- **Search Functionality**
  - Unified search across users, subjects, chapters and quizzes
- **Analytics & Charts**
  - User performance analytics
  - Quiz statistics and participation metrics

## Installation & Setup

### 1.1 Clone the Repository

```bash
git clone https://github.com/21f1006877/Quiz-Master-App-V1.git
cd Quiz-Master-App-V1
```

### 1.2 Alternative : ZIP Extraction

```python
# extract.py
from zipfile import ZipFile

with ZipFile('Quiz-Master-App-V1-main.zip', 'r') as zip:
    zip.extractall('Quiz-Master-App-V1')
print("Extracted to 'Quiz-Master-App-V1' folder")
```

### 2. Create a Virtual Environment

#### Option 1 : Using Virtualenv / Python `venv`

```bash
# Prerequisites : Python 3.10.16

python -m venv env
source env/bin/activate  # On macOS/Linux
pip install -r requirements.txt  # install dependencies
```

#### Option 2 : Using `conda` and `YAML` file

```bash
conda env create -f environment.yml
conda activate quizapp
```

### 3. File Integrity Verification

Generate checksum to verify project integrity :

```bash
python check.py  # Generates SHA256 hash
```

### 4. Run the Flask App

```sh
python run.py
```
The application will be available at `http://localhost:5000/`

## Tech Stack

- **Backend** : Flask, Flask-SQLAlchemy
- **Frontend** : HTML, Bootstrap v5.3, CSS, Jinja2, JavaScript
- **Database** : SQLite
- **Visualization** : Plotly

## Database Schema & ER Diagram

The database follows the relational model with multiple tables linked via foreign keys. Below is the ER Diagram:

![ER Diagram](quizapp/static/images/ER_Diagram.png)

## Flask Application Structure

```bash
Quiz-Master-App-V1
├── .env
├── .gitignore
├── LICENSE
├── README.md
├── checksum.py
├── environment.yml
│
├── instance
│   └── quizapp.db
│
├── quizapp
│   ├── __init__.py
│   ├── db_seed.py
│   ├── models.py
│   ├── routes.py
│   ├── static
│   │   └── images
│   │       └── # directory stores images
│   │
│   ├── templates
│   │   ├── admin
│   │   │   └── # directory stores Jinja2 templates of Admin routes
│   │   │ 
│   │   ├── base_main.html
│   │   ├── login.html
│   │   ├── registration.html
│   │   │ 
│   │   └── users
│   │       └── # directory stores Jinja2 templates of User routes
│   │
│   └── utils.py
├── requirements.txt
└── run.py
```

## License

The license can be found in the [LICENSE](LICENSE) file.