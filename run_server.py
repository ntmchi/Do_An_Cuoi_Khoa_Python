from os import environ
from KiehlShop import app
app.secret_key = "2018"

if __name__=='__main__':
    HOST = environ.get('SERVER_HOST','127.0.0.1')  
    try:
        PORT = int(environ.get('SERVER_POST','5555'))
    except ValueError:
        PORT = 5555
    app.debug = True
    app.run(HOST,PORT) 