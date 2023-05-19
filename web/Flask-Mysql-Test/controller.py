from flask import flash, render_template, Flask, request
import functions
import mysql.connector
#Assign the templates folder
app=Flask(__name__, template_folder='templates')
conn=None
#Further note, the issue of why the database was not working, because the database wasn't created, apparently the database has to created before launching the docker-compose command
#to create database: docker exec -it (container-id) bash
#mysql -u root -p (after which you enter the password that is on the python file)
#CREATE DATABASE (database name on python file, i.e. testingtesting123);
#exit; and then run the docker-compose up command

class Database:
	#This function is used to connect with the database if called by one of the other functions
	def __init__(self, user='root', password='Parole1', database='mydb', host='db'):
		self.connection=mysql.connector.connect(user=user, password=password, database=database, host=host)
		self.connection.autocommit=True
		self.cursor=self.connection.cursor()
	#this function drops, creates and fills out the tables
	def create_table(self, table_name,s1,s2,s3,s4):
		drop=f'DROP TABLE IF EXISTS {table_name}'
		self.cursor.execute(drop)
		print("hi")
		create_t=f"CREATE TABLE {table_name}({s1} INT AUTO_INCREMENT PRIMARY KEY NOT NULL, {s2} TEXT not null, {s3} TEXT, {s4} TEXT)"
		self.cursor.execute(create_t)

#The table that has foreign keys has to be dropped first, in this case tests, becuse nolikt and krasas are foreign keys, then nolikt because krasas is a foreign key, then krasas
		#Creates a test table with multiple foreign keys connecting it, this table tests multiple foreign keys and python variables
	def check_IP(self):
		sql_delete='DELETE t1 FROM IP_mysql t1 INNER JOIN IP_mysql t2 WHERE t1.id<t2.id AND t1.IP_key = t2.IP_key AND t1.ISP=t2.ISP AND t1.valsts=t2.valsts'
		self.cursor.execute(sql_delete)
	def drop_table(self):
		self.cursor.execute('DELETE FROM IP_mysql')
	def insert_IP(self, IPs, ISP, country, table_name):
		sql_insert='INSERT INTO IP_mysql(IP_key, ISP, valsts) VALUES(%s,%s,%s)'
		sql_values=[(IPs, ISP, country)]
		self.cursor.executemany(sql_insert, sql_values)
	def IP_select(self, table_name):
		self.cursor.execute('SELECT * FROM IP_mysql')
		select=self.cursor.fetchall()
		return select
@app.route('/')
def index():
	return render_template('index.html')
rezins='ip-lookup.html'
@app.route('/ip-lookup', methods=["GET", "POST"])
def ip_insert():
	#create an error variable for error messages
	error = None
	global conn
	data={}
	data_out={}
	list=[
		["IP_mysql", "id","IP_key","ISP","valsts"],
		["domain_db","id","domens","IP","VT_link"]
	]
	if not conn:
		conn=Database()
		for lst in list:
			table_name=lst[0]
			s1=lst[1]
			s2=lst[2]
			s3=lst[3]
			s4=lst[4]
			print(table_name, s1,s2,s3,s4)
			conn.create_table(table_name, s1,s2,s3,s4)
	if request.method == "POST":
		#AiPe is a variable that gathers information from the user input, if the input is empty, an error message will appear
		IP=request.form['AiPe']
		if not IP:
			error = "Tukšs lauks, lūdzu ievadiet derīgu IPv4 adresi"
		elif request.form.get('clear_btn') is not None:
			if conn:
				conn.drop_table()
			data_out.clear()
			data.clear()
			return render_template(rezins)
		else:
		#sends IP data to backend python file, depending on the result, it will be returned to ip-lookup.html
			info=functions.lookup(IP)
			print(info)
			for ip in info:
				data=info[ip]
				ISP=data['ISPI']
				country=data['country']
				conn.insert_IP(ip, ISP, country)
			conn.check_IP()
			data_out=conn.IP_select()
			print(data_out)
	return render_template(rezins, error=error, look=data_out)
#This starts the development server, checking whether the module is being run as the main program
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
