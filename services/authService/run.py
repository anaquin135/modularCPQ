from app import app
from config import *

if __name__ == '__main__':
    if DEBUG:
        app.run(debug=True)
    else:
        app.run(host='0.0.0.0')
