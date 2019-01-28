import json
import sqlite3

connectionFile = sqlite3.connect("manyStudentsInManyCourses.sqlite")
cursorHandle = connectionFile.cursor()

cursorHandle.executescript('''
	DROP TABLE IF EXISTS User;
	DROP TABLE IF EXISTS Course;
	DROP TABLE IF EXISTS Member;

	CREATE TABLE User (
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		name TEXT UNIQUE
	);

	CREATE TABLE Course (
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		title TEXT UNIQUE
	);

	CREATE TABLE Member (
		user_id INTEGER,
		course_id INTEGER,
		role INTEGER,
		PRIMARY KEY(user_id,course_id)
	)
''')

fileName = input("Please enter the file name: ")
if len(fileName) < 1: fileName = "roster_data.json"

fileHandle = open(fileName).read()
jsonData = json.loads(fileHandle)

for entry in jsonData:
	name = entry[0]
	title = entry[1]
	role = entry[2]

	## Print out as a tuple
	print((name,title,role))

	cursorHandle.execute("INSERT OR IGNORE INTO User (name) VALUES (?)",(name,))
	## To know the primary key for the particular user
	cursorHandle.execute("SELECT id FROM User WHERE name = ?",(name,))
	## The sub 0 just means if there were more than one thing that I was selecting
	user_id = cursorHandle.fetchone()[0]

	cursorHandle.execute("INSERT OR IGNORE INTO Course (title) VALUES (?)",(title,))
	## To know the primary key for the particular course
	cursorHandle.execute("SELECT id FROM Course WHERE title = ?",(title,))
	## The sub 0 just means if there were more than one thing that I was selecting
	course_id = cursorHandle.fetchone()[0]

	cursorHandle.execute('''INSERT OR REPLACE INTO Member (user_id,course_id,role) VALUES (?,?,?)''',
		(user_id,course_id,role))

	connectionFile.commit()

'''
SELECT hex(User.name||Course.title||Member.role) AS X FROM 
User JOIN Course JOIN Member 
ON Member.user_id = User.id AND Member.course_id = Course.id 
ORDER BY X
'''