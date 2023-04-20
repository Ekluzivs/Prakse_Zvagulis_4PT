from flask import flash, render_template, Flask, request
import manafunkc
import mysql.connector
app=Flask(__name__, template_folder='templates')
conn=None
class Datubaze:
        def __init__(self, user='root', password='Parole1', database='testingtesting123', host='db'):
                self.connection=mysql.connector.connect(user=user, password=password, host=host,database=database)
                self.cursor=self.connection.cursor()
        def tabuluievade(self):
                self.cursor.execute('DROP TABLE IF EXISTS krasas')
                self.cursor.execute('CREATE TABLE krasas (krasa VARCHAR(20) NOT NULL, prieksmets VARCHAR(30) NOT NULL)')
                self.cursor.execute('INSERT INTO krasas(krasa, prieksmets) VALUES("galds","bruns"), ("melns","telefons"), ("melns", "meness"), ("balts","muspapirs"), ("zals","zimulis")')
                self.connection.commit()
        def tabsel(self):
                self.cursor.execute('SELECT * FROM krasas')
                rez=[]
                for i in self.cursor:
                        rez.append(i)
                return rez
@app.route('/')
def index():
        global conn
        if not conn:
                conn=Datubaze()
                conn.tabuluievade()
        data=conn.tabsel()
        print("tu te")
        return render_template('index.html',data=data)
rezins='ip-lookup.html'
@app.route('/ip-lookup', methods=["GET", "POST"])
def ipinsert():
        error = None
        info={}
        if request.method == "POST":
                IP=request.form['AiPe']
                if not IP:
                        error = "Empty Field, please input a valid IPv4 address"
                else:
                        info=manafunkc.lookup(IP)
        return render_template(rezins, error=error, look=info)
if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)
