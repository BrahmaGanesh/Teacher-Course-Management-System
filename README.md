# 🧑‍🏫 Teacher-Course Management System

A web-based admin dashboard built using **Python Flask** and **MySQL** to manage teachers and their assigned courses. Includes user authentication, CRUD operations, and relational data handling.

---

## 🚀 Features

- ✅ Admin Login, Register & Logout
- ✅ Secure session-based authentication
- ✅ Dashboard for managing data
- ✅ CRUD operations for:
  - Teachers (Add, Edit, Delete)
  - Courses (linked to teachers via `teacher_id`)
- ✅ Flash messages for feedback
- ✅ Decorator for protected routes (`@login_required`)
- ✅ Relational queries using **SQL Joins**

---

## 🛠 Tech Stack

- **Frontend**: HTML5, CSS3, Jinja2 (Flask templates)
- **Backend**: Python (Flask)
- **Database**: MySQL
- **Tools**: Flask, mysql-connector-python

---

## ⚙️ Setup Instructions

### 🔧 Prerequisites
- Python 3.x
- MySQL Server
- Flask: `pip install flask`
- MySQL Connector: `pip install mysql-connector-python`

### 🧱 Database Setup

```sql
CREATE DATABASE teacher_course_db;

USE teacher_course_db;

CREATE TABLE admin_users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(100) UNIQUE NOT NULL,
  password VARCHAR(100) NOT NULL
);

CREATE TABLE teachers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  experience INT
);

CREATE TABLE courses (
  id INT AUTO_INCREMENT PRIMARY KEY,
  course_name VARCHAR(100),
  teacher_id INT,
  FOREIGN KEY (teacher_id) REFERENCES teachers(id)
);
