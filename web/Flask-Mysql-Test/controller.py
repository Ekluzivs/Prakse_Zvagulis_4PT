from flask import flash, render_template, Flask, request
import functions
import mysql.connector
#Assign the templates folder
app=Flask(__name__, template_folder='templates')
conn=None
# Assnigning INT to variables for inserting into table value
t1=200
t2=21525
t3=0
t4=2
#Further note, the issue of why the database was not working, because the database wasn't created, apparently the database has to created before launching the docker-compose command
#to create database: docker exec -it (container-id) bash
#mysql -u root -p (after which you enter the password that is on the python file)
#CREATE DATABASE (database name on python file, i.e. testingtesting123);
#exit; and then run the docker-compose up command

class Database:
	#This function is used to connect with the database if called by one of the other functions
	def __init__(self, user='root', password='Parole1', database='mydb', host='db'):
		self.connection=mysql.connector.connect(user=user, password=password, database=database, host=host)
		self.cursor=self.connection.cursor()
	#this function drops, creates and fills out the tables
	def create_table(self):
#The table that has foreign keys has to be dropped first, in this case tests, becuse nolikt and krasas are foreign keys, then nolikt because krasas is a foreign key, then krasas
		self.cursor.execute('DROP TABLE IF EXISTS IP_mysql')

		self.cursor.execute('CREATE TABLE IP_mysql(id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, IP_key VARCHAR(16) not null, ISP VARCHAR(100), valsts VARCHAR(3))')
		#Creates a test table with multiple foreign keys connecting it, this table tests multiple foreign keys and python variables
		self.connection.commit()

	def check_IP(self):
		sql_check='SELECT IP_key, COUNT(*) AS count FROM IP_mysql GROUP BY IP_key HAVING count > 1'
		if sql_check:
			sql_delete='DELETE t1 FROM IP_mysql t1 INNER JOIN IP_mysql t2 WHERE t1.id<t2.id AND t1.IP_key = t2.IP_key AND t1.ISP=t2.ISP AND t1.valsts=t2.valsts'
			self.cursor.execute(sql_delete)
			self.connection.commit()
	def insert_IP(self, IPs, ISP, country):
		sql_insert='INSERT INTO IP_mysql(IP_key, ISP, valsts) VALUES(%s,%s,%s)'
		print(sql_insert)
		sql_values=[(IPs, ISP, country)]
		self.cursor.executemany(sql_insert, sql_values)
		self.connection.commit()
	def IP_select(self):
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
	if request.method == "POST":
		#AiPe is a variable that gathers information from the user input, if the input is empty, an error message will appear
		IP=request.form['AiPe']
		if not IP:
			error = "Tukšs lauks, lūdzu ievadiet derīgu IPv4 adresi"
		else:
		#sends IP data to backend python file, depending on the result, it will be returned to ip-lookup.html
			info=functions.lookup(IP)
			if not conn:
				conn=Database()
				conn.create_table()

			data=info[IP]
			print(data)
			ISP=data['ISPI']
			country=data['country']
			conn.insert_IP(IP, ISP, country)
			conn.check_IP()
			data_out=conn.IP_select()
	return render_template(rezins, error=error, look=data_out)
#This starts the development server, checking whether the module is being run as the main program
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
