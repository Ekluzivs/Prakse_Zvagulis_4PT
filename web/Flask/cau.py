from flask import flash, render_template, Flask, request
#HTML faili atrodas /templates failā
app=Flask(__name__, template_folder='templates')

# index lapa, nospiežot, url aizvedīs uz /ip-lookup
@app.route('/')
def index():
        return render_template('index.html')

@app.route('/ip-lookup', methods=["GET", "POST"])
def ipinsert():
        error=None
        if request.method == "POST":
                #AiPe ir no HTML ievades lauka, IP ir variable kas ņem no AiPe ievadītā
                #kurā tad IP tiek iemests ipchecker funkcijā kurā citā python failā
                #notiek vai IP adrese ir IPv4
                IP=request.form['AiPe']
                ch=ipchecker(IP)
                #ja nav, tad error kļūdu izmet
                if ch == False:
                        error = 'Invalid IP address'
                else:
                        #ja ir IPv4 tad notiek IPlookup funkcija, kurā tad izmetīs rezultātu tajā pašā lapā
                        look=iplookup(IP)
                        return render_template('ip-lookup.html', look=look)
        return render_template('ip-lookup.html', error=error)
