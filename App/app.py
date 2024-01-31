import sys
from pages import *
from Database import db
sys.path.append('../')
from Assets import plot


def main():
    db.open()
    app = App()
    plot.plot_all()
    Dashboard(app)
    app.mainloop()
    db.close()

if __name__ == '__main__':
    main()
