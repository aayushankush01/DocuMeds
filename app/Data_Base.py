from datetime import datetime
from flask import Flask, render_template, request
import mysql.connector as m
mydatabase=m.connect(host="localhost",user="root",password="Aayush",database="projectdb1")
cursor=mydatabase.cursor()
app=Flask(__name__)
def table_format(rows):
    column = ('Date & Time', 'Name', 'Sex', 'Age', 'prescribed Medicine','InHouse Medicine','Investigations Asked','History')
    data = [dict(zip(column, row)) for row in rows]
    return column, data
@app.route("/")
def home():
    now = datetime.now().strftime("%Y-%m-%d")  # Format needed for datetime-local input
    return render_template("Home.html",now=now)

@app.route("/submit",methods=['POST'])
def submit():
    name=request.form['Name']
    sex=request.form['Sex']
    age=request.form['Age']
    age=int(age)
    his=request.form['His']
    presmed=request.form['PresMed']
    inhousemed=request.form['InMed']
    investigations=request.form['Investigations']
    if age<0 or age>121: #Age Data type Validation
        error="Invalid Input"
        return render_template("Home.html",name=name,sex=sex,age=age,his=his,presmed=presmed,inhousemed=inhousemed,investigations=investigations,error=error)
    else:
        qs="INSERT INTO P1 (patientname,sex,age,Prescribed_Medicine,Inhouse_Medicine,Investigations,His) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        val=(name,sex,age,presmed,inhousemed,investigations,his)
        cursor.execute(qs,val)
        mydatabase.commit()
        # return f"Data for {name} added successfully!"
        return render_template("AfterPost.html",name=name)

@app.route("/get",methods=['GET'])
def get():
    start_date=request.args.get('start_date')
    start_date=start_date+" 00:00:00"
    end_date=request.args.get('end_date')
    end_date=end_date+" 23:59:59"
    #date_format_str = '%%d/%%m/%%y--%%h:%%i:%%s %%p'
    #qg=f'''SELECT DATE_FORMAT(Date_Time,'{date_format_str}') as Formatted_Date_Time,patientname,sex,age,Prescribed_Medicine,Inhouse_Medicine,Investigations,His FROM P1 WHERE Date_Time BETWEEN %s AND %s'''
    qg = "SELECT Date_Time,patientname,sex,age,Prescribed_Medicine,Inhouse_Medicine,Investigations,His FROM P1 WHERE Date_Time BETWEEN %s AND %s"
    cursor.execute(qg,(start_date,end_date))
    print(end_date)
    rows=cursor.fetchall()
 #   column=cursor.column_names
    column,data=table_format(rows)
    #print(repr(rows[0]['His']))
    return render_template("AllData_Table.html",data=data,columns=column)

@app.route("/search",methods=['GET'])
def search():
    Search_name=request.args.get('Search_name')
    Search_name_Og=Search_name
    Search_name=Search_name.lower()
    search_query="Select Date_Time,patientname,sex,age,Prescribed_Medicine,Inhouse_Medicine,Investigations,His From p1 where LOWER(patientname) = %s "
    cursor.execute(search_query,(Search_name,))
    rows=cursor.fetchall()
    column,data=table_format(rows)
    age_query="SELECT age FROM p1 ORDER BY Sr_No DESC LIMIT 1"
    cursor.execute(age_query)
    age=cursor.fetchone()
    age=age[0]
    sex_query="SELECT sex FROM p1 ORDER BY Sr_No DESC LIMIT 1"
    cursor.execute(sex_query)
    sex=cursor.fetchone()
    sex=sex[0]
    return render_template("SearchData_Table.html",data=data,columns=column,Search_name_Og=Search_name_Og,age=age,sex=sex)


if __name__=="__main__":
    app.run(debug=True)