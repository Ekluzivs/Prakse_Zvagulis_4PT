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

class Datubaze:
	#This function is used to connect with the database if called by one of the other functions
	def __init__(self, user='root', password='Parole1', database='mydb', host='db'):
		self.connection=mysql.connector.connect(user=user, password=password, database=database, host=host)
		self.cursor=self.connection.cursor()
	#this function drops, creates and fills out the tables
	def tabuluievade(self):
#The table that has foreign keys has to be dropped first, in this case tests, becuse nolikt and krasas are foreign keys, then nolikt because krasas is a foreign key, then krasas
		self.cursor.execute('DROP TABLE IF EXISTS tests')
		self.cursor.execute('DROP TABLE IF EXISTS nolikt')
		self.cursor.execute('DROP TABLE IF EXISTS krasas')

		self.cursor.execute('CREATE TABLE krasas (id_test INT PRIMARY KEY AUTO_INCREMENT, krasa VARCHAR(20) NOT NULL, prieksmets VARCHAR(30) NOT NULL)')
		self.cursor.execute('INSERT INTO krasas(krasa, prieksmets) VALUES("galds","bruns"), ("melns","telefons"), ("melns", "meness"), ("balts","muspapirs"), ("zals","zimulis")')
		self.cursor.execute('CREATE TABLE nolikt(id_test INT NOT NULL, id_nolikt INT PRIMARY KEY AUTO_INCREMENT, cena Double(5,2) NOT NULL, noliktava VARCHAR(25) NOT NULL, FOREIGN KEY (id_test) REFERENCES krasas(id_test))')
		sqlin="""INSERT INTO nolikt(id_test, cena, noliktava) VALUES (%s,%s,%s)"""
		sqlval=[
			(1, 40.22, "Ir noliktava"),
			(2, 400.99, "nav nolitava"),
			(3, 0.00, "nav nolitava"),
			(4, 3.00, "Ir noliktava"),
			(5, 2.99, "Ir noliktava")]
		self.cursor.executemany(sqlin, sqlval)
		#Creates a test table with multiple foreign keys connecting it, this table tests multiple foreign keys and python variables
		self.cursor.execute('CREATE TABLE tests(id_test INT, id_nolikt INT, testvalue INT, FOREIGN KEY (id_test) REFERENCES krasas(id_test), FOREIGN KEY (id_nolikt) REFERENCES nolikt(id_nolikt))')
		SQLinsert="""INSERT INTO tests(id_test,id_nolikt,testvalue) VALUES (%s,%s,%s)"""
		SQLvalues=[(1,1,t1),(2,2,t3),(3,3,t2),(4,4,t4),(5,5,t2)]
		self.cursor.executemany(SQLinsert, SQLvalues)
		self.connection.commit()
	def table_insert(self, val1):
		sqlval
	def krassel(self):
		self.cursor.execute('SELECT * FROM krasas')
		rez=[]
		for i in self.cursor:
			rez.append(i)
		return rez
	def lietsel(self):
		self.cursor.execute('SELECT id_test, cena, noliktava FROM nolikt')
		rez1=[]
		for o in self.cursor:
			rez1.append(o)
		return rez1
	def testsel(self):
		self.cursor.execute('SELECT * FROM tests')
		rez2=[]
		for o in self.cursor:
			rez2.append(o)
		return rez2
#	def IPsel(self):
#		self.cursor.execute("SELECT * FROM IPsdb")
#		rezIP=[]
#		for o in self.cursor:
#			rezIP.append(o)
#		return rezIP
@app.route('/')
def index():
	#conn is used to be used a variable to connect with the database if not connected
	global conn
	if not conn:
		conn=Datubaze()
		conn.tabuluievade()
	#data gathers information from the class Datubaze and then returns that data to index.html
	data=conn.krassel()
	data1=conn.lietsel()
	data2=conn.testsel()
	return render_template('index.html', data=data, data1=data1, data2=data2)
rezins='ip-lookup.html'
@app.route('/ip-lookup', methods=["GET", "POST"])
def ipinsert():
	#create an error variable for error messages
	error = None
#	global conn
	info={}
	if request.method == "POST":
		#AiPe is a variable that gathers information from the user input, if the input is empty, an error message will appear
		IP=request.form['AiPe']
		if not IP:
			error = "Empty Field, please input a valid IPv4 address"
		else:
		#sends IP data to backend python file, depending on the result, it will be returned to ip-lookup.html
			info=functions.lookup(IP)
#			if not conn:
#				conn=Datubaze()
#			dataIP=conn.IPsel()
	return render_template(rezins, error=error, look=info)
#This starts the development server, checking whether the module is being run as the main program
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
