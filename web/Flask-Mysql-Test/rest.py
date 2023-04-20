#import pymysql
#from cau import app
#from db import mysql
import mysql.connector
from flask import jsonify, render_template
def krasas():
	conn=mysql.connect(user='root', password='Parole1', host='db' ,database='testingtesting123')
	if conn.is_connected():
		print("connection")
	else:
		print("NOP")
	print(conn.get_server_info())
	cursor = conn.cursor()
	cursor.execute("DROP TABLE IF EXISTS krasas")
	sql='''CREATE TABLE krasas(
	krasa VARCHAR(20) NOT NULL,
	prieksmets VARCHAR(30) NOT NULL
	)'''
	cursor.execute(sql)
	sqlin="""INSERT INTO krasas(
	krasas, prieksmets)
	VALUES('zils','trauks')
	('bruns','galds')
	('melna','riepa')"""
	try:
		cursor.execute(sqlin)
		conn.commit()
	except:
		conn.rollback()
	sqlsel='''SELECT * FROM krasas'''
	cursor.execute(sqlsel)
	data=cursor.fetchall();
	conn.close()
	return render_template("index.html", data=data)
#if __name__ == "__main__":
#	app.run(host="0.0.0.0")
