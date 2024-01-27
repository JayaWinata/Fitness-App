from pages import *
import sys
sys.path.append('../')
from Database import db

if __name__ == '__main__':
    app = App()
    Dashboard(app)
    app.mainloop()
    db.close()
    
