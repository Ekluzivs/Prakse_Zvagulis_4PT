from flask import flash, render_template, Flask, request
import function
#it creates a templates folder and at the same time we set a global variable for the result html
app=Flask(__name__, template_folder='templates')
result='ip-lookup.html'
# home page, we can choose if want to go there
@app.route('/')
def index():
        return render_template('index.html')

@app.route('/ip-lookup', methods=["GET", "POST"])
def ipinsert():
        #we create an error variable, for now it's empty, we also create a dictionary so it would output the result
        error=None
        info={}
        if request.method == "POST":
                #AiPe is getting the input from the ip-lookup.html as a request, anything we input get's passed to IP variable
                #if we press submit wihout entering anything, the if statement will check if there is any input in the IP variable
                #if it is empty, it'll output an error message on the website
                IP=request.form['AiPe']
                if not IP:
                        error = "Empty field, Input IPv4 Address"
                else:
                        #if IP is not empty, the next check begins at function.py
                        #if the check get's a False result from the function.py, then it'll output an error message on the website
                        check=function.check(IP)
                        if check == False:
                                error = 'Invalid IP address'
                        else:
                                #if so far the check statements are good, then info will request the result from the lookup function in funtion.py
                                info=function.lookup(IP)
        return render_template(result, error=error, look=info)
