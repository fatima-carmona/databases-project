# databases-project
# XYZ Company Database Project  

> Semester project for **CS 4347 — Database Systems (Spring 2025)**

## 📌 Project Overview  
This project models and implements a relational database for a fictional company (**XYZ Company**) that manufactures products using parts from multiple vendors, manages employees and customers, conducts hiring through interviews, and tracks sales at different sites.  

The project goes beyond schema design by including:  
- **Conceptual & Logical Design**: ER/EER diagrams, subclass/superclass modeling, normalization (3NF).  
- **Implementation**: MySQL database with full schema, constraints, and dependency diagrams.  
- **Queries & Views**: 15+ complex SQL queries and 4 predefined views for analytics.  
- **Frontend Application**: A **Streamlit web app** for interactive querying, editing, and visualizing data.  

---

## 🛠️ Tech Stack  
- **Database**: MySQL (MySQL Workbench used for modeling)  
- **Backend**: SQLAlchemy (Python → MySQL integration)  
- **Frontend**: Streamlit (interactive database exploration & editing)  
- **Scripting**: Python (Pandas, Faker for data generation)  
- **Modeling Tools**: draw.io / Lucidchart for ER/EER diagrams  

---

## 🚀 Features  

### 🔹 Database Design  
- Normalized relational schema (**3NF**) for:  
  - Employees, Departments, Customers, Vendors  
  - Products, Parts, and Part Costs  
  - Sites and Sales history  
  - Job postings, Applications, Interviews, Salaries  

### 🔹 SQL Views  
1. **View1**: Average monthly salary per employee  
2. **View2**: Number of interview rounds passed per job candidate  
3. **View3**: Number of items sold per product type  
4. **View4**: Part purchase cost per product  

### 🔹 Predefined Analytical Queries  
- Interviewers for specific job candidates  
- Departments with no job posts in a given period  
- Sites with no sales during a given timeframe  
- Employees without supervisees  
- Best-selling product types  
- Highest net profit product types  
- Vendors offering the lowest price for specific parts  
- Selected candidates with contact details  
*(and more — 15+ in total)*  

### 🔹 Streamlit Frontend  
- Write and run **custom SQL queries** interactively.  
- Explore predefined **views** and **queries** with results displayed in real-time.  
- Query results displayed in **Pandas dataframes** with filtering and sorting.  
- Error handling for invalid SQL commands.  

---

## ⚡ How to Run  

1. Clone the repository  
   git clone https://github.com/yourusername/xyz-company-db.git  
   cd xyz-company-db  

2. Set up MySQL Database  
   - Create a database named companyxyz  
   - Run the provided SQL scripts in /sql/ to create tables, constraints, and populate sample data:  

   mysql -u root -p companyxyz < sql/schema.sql  
   mysql -u root -p companyxyz < sql/data.sql  

3. Configure environment variables  
   Update the MySQL credentials in app.py (or create a .env file if extended):  

   DB_USER='root'  
   DB_PASSWORD='yourpassword'  
   DB_HOST='localhost'  
   DB_PORT='3306'  
   DB_NAME='companyxyz'  

4. Run Streamlit App  
   pip install -r requirements.txt  
   streamlit run app.py  

5. Open in Browser  
   Navigate to http://localhost:8501  
