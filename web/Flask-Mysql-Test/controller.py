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
	#this function drops and creates the tables over an iteration from another function, with the help of f-string, s1 is the id, s2,s3,s4 are the data values
	def create_table(self, table_name,s1,s2,s3,s4):
		drop=f'DROP TABLE IF EXISTS {table_name}'
		self.cursor.execute(drop)
		create_t=f"CREATE TABLE {table_name}({s1} INT AUTO_INCREMENT PRIMARY KEY NOT NULL, {s2} TEXT not null, {s3} TEXT, {s4} TEXT)"
		self.cursor.execute(create_t)

# Function group that is used for deleting any duplicates in the tables
	def check_hash(self):
		sql_delete='DELETE t1 FROM hash_db t1 INNER JOIN hash_db t2 WHERE t1.id<t2.id AND t1.hash = t2.hash AND t1.drosiba=t2.drosiba AND t1.VT_hash_link=t2.VT_hash_link'
		self.cursor.execute(sql_delete)
	def check_dom(self):
		dom_delete='DELETE t1 FROM domain_db t1 INNER JOIN domain_db t2 WHERE t1.id<t2.id AND t1.domens = t2.domens AND t1.VT_link=t2.VT_link'
		self.cursor.execute(dom_delete)
	def check_IP(self):
		sql_delete='DELETE t1 FROM IP_mysql t1 INNER JOIN IP_mysql t2 WHERE t1.id<t2.id AND t1.IP_key = t2.IP_key AND t1.ISP=t2.ISP AND t1.valsts=t2.valsts'
		self.cursor.execute(sql_delete)
#Function group that is used for deleting any and all data in tables
# NOTE!!! CURRENTLY THIS ISN'T WORKING FOR REASONS UNKNOWN
	def drop_domain(self):
		self.cursor.execute('DELETE FROM domain_db')
	def drop_table(self):
		self.cursor.execute('DELETE FROM IP_mysql')

#Function group used for inserting data into tables
	def insert_hash(self, hash_loop, hash_dros, VT_hash):
		SQL_i_hash='INSERT INTO hash_db(hash, drosiba, VT_hash_link) VALUES(%s, %s, %s)'
		sql_v_hash=[(hash_loop, hash_dros, VT_hash)]
		self.cursor.executemany(SQL_i_hash, sql_v_hash)
	def insert_dom(self, dom_loop, dom_IP, VT_link):
		SQL_i='INSERT INTO domain_db(domens, IP, VT_link) VALUES(%s, %s, %s)'
		sql_v=[(dom_loop, dom_IP, VT_link)]
		self.cursor.executemany(SQL_i, sql_v)
	def insert_IP(self, IPs, ISP, country):
		sql_insert='INSERT INTO IP_mysql(IP_key, ISP, valsts) VALUES(%s,%s,%s)'
		sql_values=[(IPs, ISP, country)]
		self.cursor.executemany(sql_insert, sql_values)

#Function group used for selecting the tables and it's values for output
	def IP_select(self):
		self.cursor.execute('SELECT * FROM IP_mysql')
		select=self.cursor.fetchall()
		return select
	def hash_select(self):
		self.cursor.execute('SELECT * FROM hash_db')
		select=self.cursor.fetchall()
		return select
	def dom_select(self):
		self.cursor.execute('SELECT * FROM domain_db')
		select1=self.cursor.fetchall()
		return select1
@app.route('/')
def index():
	return render_template('index.html')
rezins='ip-lookup.html'
@app.route('/ip-lookup', methods=["GET", "POST"])
def ip_insert():
	#create an error variable for error messages
	error = None
	warning=None
	global conn
	#create necessary dictionaries, 1 dictionary for inputting data to mysql, 1 dictionary for outputting data to front-end
	data={}
	data_out={}
	data_dom={}
	dom_data_out={}
	data_hash={}
	hash_data_out={}
	#create list for creating tables in Database class
	list=[
		["IP_mysql", "id","IP_key","ISP","valsts"],
		["domain_db","id","domens","IP","VT_link"],
		["hash_db", "id","hash","drosiba","VT_hash_link"]
	]
	#if no connection, it'll create a Database class and then over each iteration it'll create a table
	if not conn:
		conn=Database()
		for lst in list:
			table_name=lst[0]
			s1=lst[1]
			s2=lst[2]
			s3=lst[3]
			s4=lst[4]
			conn.create_table(table_name, s1,s2,s3,s4)
	if request.method == "POST":
		#AiPe is a variable that gathers information from the user input, if the input is empty, an error message will appear
		radio_option=request.form.get('Radioinput')
		IP=request.form['AiPe']
		dom=request.form['domain']
		hash=request.form['hesh']
		if radio_option == "hash-lookup-v":
			if not hash:
				error = "tukšs lauks, lūdzu ievadiet derīgu jaucējvērtību"
			else:
				info_hash, flagged_Hash=functions.hash_lookup(hash)
				if flagged_Hash:
                                        warning="Kļūda ievadītajā indikatorā"
				for hash_loop in info_hash:
					data_hash=info_hash[hash_loop]
					hash_dros=data_hash['drosiba']
					VT_hash=data_hash['VT_hash']
					conn.insert_hash(hash_loop, hash_dros, VT_hash)
				conn.check_hash()
				hash_data_out=conn.hash_select()
				return render_template(rezins, hash_data=hash_data_out, error=error ,zinojums=warning)
		if radio_option == "domain-lookup-v":
			if not dom:
				error = "Tukšs lauks, lūdzu ievadiet derīgu domēnu"
			elif request.form.get('clear_btn') is not None:
				if conn:
					conn.drop_domain()
				data_dom.clear()
				dom_data_out.clear()
			else:
				info_dom, flagged_Dom=functions.dom_lookup(dom)
				print(flagged_Dom)
				if flagged_Dom:
					warning="Kļūda ievadītajā indikatorā"
				for dom_loop in info_dom:
					data_dom=info_dom[dom_loop]
					dom_IP=data_dom['IP']
					VT_link=data_dom['VT-LINK']
					conn.insert_dom(dom_loop, dom_IP, VT_link)
				conn.check_dom()
				dom_data_out=conn.dom_select()
				print(warning)
				return render_template(rezins, dom_data=dom_data_out, error=error, zinojums=warning)
		elif radio_option=="ip-lookup-v":
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
				info, flagged_IP=functions.lookup(IP)
				if flagged_IP:
					warning="Kļūda ievadītajā indikatorā"
				for ip in info:
					data=info[ip]
					ISP=data['ISPI']
					country=data['country']
					conn.insert_IP(ip, ISP, country)
				conn.check_IP()
				data_out=conn.IP_select()
				print(data_out)
				return render_template(rezins, look=data_out, error=error, zinojums=warning)
	return render_template(rezins, error=error)
#@app.route('/ip-lookup', methods=["GET", "POST"])
#def user_input():
#	if request.method






#This starts the development server, checking whether the module is being run as the main program
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
