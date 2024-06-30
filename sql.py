import sqlite3


## connect to sqlite

connection=sqlite3.connect("student.db")

## create a curser obeject to insert,recors,create table,retrieve

cursor=connection.cursor()


## create the table
table_info="""
create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),SECTION VARCHAR(25),MARKS INT);
"""

cursor.execute(table_info)

## insert some more records

cursor.execute('''Insert Into STUDENT values('Vidushi','Data Science','A',99)''')
cursor.execute('''Insert Into STUDENT values('Sahil','Data Science','A',90)''')
cursor.execute('''Insert Into STUDENT values('Varad','Data Science','A',93)''')
cursor.execute('''Insert Into STUDENT values('Araman','Data Science','A',93)''')
cursor.execute('''Insert Into STUDENT values('Bubu','Data Science','A',95)''')
cursor.execute('''Insert Into STUDENT values('Dudu','Data Science','A',90)''')

## display all the records
print("The inserted records are")


data=cursor.execute('''Select * From  STUDENT''')

for row in data:
    print(row)   
    

 ## close the connection(for complete all the operation / imp)
   


connection.commit()
connection.close()
