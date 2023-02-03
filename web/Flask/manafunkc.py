from flask import Flask
from cau.iplookup import iplookup
funkc=Flask(__name__)
funkc=register_blueprint(iplookup)

@funkc.route('/ip-lookup')
def lookup('IP'):
        l=IP.split=('.')
        if len(l)!=4:
                print ("Not Valid IP Address")
                return False
        for x in l:
                if not x.isdigit():
                        print ("Not Valid IP Address")
                        return False
                i=int(x)
                if i < 0 or i > 255:
                        print ("Not Valid IP Address")
                        return False
        return True
