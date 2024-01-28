from pages import *
import sys
sys.path.append('../')
from Database import db
from Assets import plot

if __name__ == '__main__':
    app = App()
    # db.open()
    Dashboard(app)
    app.mainloop()
    # db.close()
