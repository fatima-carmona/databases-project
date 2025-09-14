import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

# MySQL credentials 
DB_USER = 'root'
DB_PASSWORD = '9956'
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'companyxyz'  


engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

st.title("Databases CompanyXYZ Project")


query = st.text_area("Write your SQL command here", height=200)


if st.button("Run SQL"):
    with engine.connect() as conn:
        try:
            result = conn.execute(text(query))

            if result.returns_rows:
                df = pd.DataFrame(result.fetchall(), columns=result.keys())
                st.success(" Query executed successfully!")
                st.dataframe(df)
            else:
                st.success(" Command executed successfully! (No rows returned)")

        except Exception as e:
            st.error(f" Error executing query:\n\n{e}")


st.header("Predefined Views")

def run_view(view_name):
    with engine.connect() as conn:
        try:
            result = conn.execute(text(f"SELECT * FROM {view_name}"))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            st.dataframe(df)
        except Exception as e:
            st.error(f"Error loading {view_name}: {e}")

with st.expander("View1: Average Monthly Salary per Employee"):
    run_view("View1")

with st.expander("View2: Interviewee Passed Rounds per Job"):
    run_view("View2")

with st.expander("View3: Number of Items Sold per Product Type"):
    run_view("View3")

with st.expander("View4: Part Purchase Cost per Product"):
    run_view("View4")


st.header("Predefined Queries")

predefined_queries = {
    "Interviewers who interviewed Hellen Cole for JobID 273": """
        SELECT DISTINCT e.PersonID, p.FirstName, p.LastName
        FROM Interview i
        JOIN InterviewResult ir ON i.InterviewID = ir.InterviewID
        JOIN Employee e ON ir.InterviewerID = e.PersonID
        JOIN Person p ON e.PersonID = p.PersonID
        WHERE i.JobID = 273
          AND i.IntervieweeID IN (
            SELECT PersonID FROM Person
            WHERE FirstName = 'Hellen' AND LastName = 'Cole'
          );
    """,
    "Marketing jobs posted in Jan 2011": """
        SELECT JobID
        FROM Job j
        JOIN Department d ON j.DepartmentID = d.DepartmentID
        WHERE d.DepartmentName = 'Marketing'
          AND j.PostedDate BETWEEN '2011-01-01' AND '2011-01-31';
    """,
    "Employees who are not supervisors": """
        SELECT e.PersonID, p.FirstName, p.LastName
        FROM Employee e
        JOIN Person p ON e.PersonID = p.PersonID
        WHERE e.PersonID NOT IN (
            SELECT DISTINCT SupervisorID
            FROM Employee
            WHERE SupervisorID IS NOT NULL
        );
    """,
    "Marketing sites with no sales in March 2011": """
        SELECT ms.SiteID, ms.SiteLocation
        FROM MarketingSite ms
        WHERE ms.SiteID NOT IN (
            SELECT SiteID
            FROM Sale
            WHERE SaleTime BETWEEN '2011-03-01' AND '2011-03-31'
        );
    """,
    "Jobs without passing interviews within one month of posting": """
        SELECT j.JobID, j.JobDescription
        FROM Job j
        WHERE NOT EXISTS (
            SELECT 1
            FROM Application a
            JOIN Interview i ON a.ApplicantID = i.IntervieweeID AND a.JobID = i.JobID
            JOIN InterviewResult ir ON i.InterviewID = ir.InterviewID
            WHERE a.JobID = j.JobID
              AND i.InterviewTime <= DATE_ADD(j.PostedDate, INTERVAL 1 MONTH)
              AND ir.Grade >= 60
        );
    """,
    "Departments without jobs posted in Jan-Feb 2011": """
        SELECT d.DepartmentID, d.DepartmentName
        FROM Department d
        WHERE d.DepartmentID NOT IN (
            SELECT DepartmentID
            FROM Job
            WHERE PostedDate BETWEEN '2011-01-01' AND '2011-02-01'
        );
    """,
    "Applicants and their department history for JobID 995": """
        SELECT p.PersonID, p.FirstName, p.LastName, edh.DepartmentID
        FROM Application a
        JOIN Employee e ON a.ApplicantID = e.PersonID
        JOIN Person p ON e.PersonID = p.PersonID
        JOIN EmployeeDepartmentHistory edh ON e.PersonID = edh.PersonID
        WHERE a.JobID = 995;
    """,
    "Product type with highest total sales count": """
        SELECT pr.ProductType, SUM(1) AS TotalSales
        FROM Sale s
        JOIN Product pr ON s.ProductID = pr.ProductID
        GROUP BY pr.ProductType
        ORDER BY TotalSales DESC
        LIMIT 1;
    """,
    "Product type with highest net profit": """
        SELECT 
    s.ProductID,
    pr.ProductType,
    COUNT(*) AS TotalSalesCount,
    pr.ListPrice,
    (COUNT(*) * pr.ListPrice) AS TotalSalesAmount
FROM Sale s
JOIN Product pr ON s.ProductID = pr.ProductID
GROUP BY s.ProductID, pr.ProductType, pr.ListPrice
ORDER BY TotalSalesAmount DESC
LIMIT 1;

    """,
    "Interviewees who scored 60 or more": """
        SELECT DISTINCT p.FirstName, p.LastName
        FROM InterviewResult ir
        JOIN Interview i ON ir.InterviewID = i.InterviewID
        JOIN Person p ON i.IntervieweeID = p.PersonID
        WHERE ir.Grade >= 60;
    """,
    "Employee with highest average monthly salary": """
        SELECT e.PersonID, p.FirstName, p.LastName,
               AVG(s.Amount) AS AvgMonthlySalary
        FROM Salary s
        JOIN Employee e ON s.PersonID = e.PersonID
        JOIN Person p ON e.PersonID = p.PersonID
        GROUP BY e.PersonID
        ORDER BY AvgMonthlySalary DESC
        LIMIT 1;
    """,
    "Vendor with lowest price for part 'watch'": """
        SELECT v.VendorID, v.Vname
        FROM Vendor v
        JOIN VendorPartPrice vpp ON v.VendorID = vpp.VendorID
        JOIN PartType pt ON vpp.PartTypeID = pt.PartTypeID
        WHERE pt.PartName = 'blood'
          AND vpp.Price = (
            SELECT MIN(vpp2.Price)
            FROM VendorPartPrice vpp2
            JOIN PartType pt2 ON vpp2.PartTypeID = pt2.PartTypeID
            WHERE pt2.PartName = 'blood'
          );
    """,
    "Applicants with passing grades and their phone numbers": """
        SELECT DISTINCT p.FirstName, p.LastName, ph.PhoneNumber
        FROM Application a
        JOIN Interview i ON a.ApplicantID = i.IntervieweeID AND a.JobID = i.JobID
        JOIN InterviewResult ir ON i.InterviewID = ir.InterviewID
        JOIN Person p ON a.ApplicantID = p.PersonID
        LEFT JOIN Phone ph ON ph.PersonID = p.PersonID
        WHERE ir.Grade >= 60;
    """
}

for name, sql in predefined_queries.items():
    with st.expander(name):
        with engine.connect() as conn:
            try:
                result = conn.execute(text(sql))
                df = pd.DataFrame(result.fetchall(), columns=result.keys())
                st.dataframe(df)
            except Exception as e:
                st.error(f"Error executing query '{name}': {e}")
