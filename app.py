import sys
from PyQt5.QtWidgets import QApplication
from ui_main import MainUI

def main():
    app = QApplication(sys.argv)
    window = MainUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
