#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

# start session
from session import start_session
session = start_session()

from PyQt5.QtWidgets import QApplication
from gui import MainWindow


def main():
    app = QApplication([])
    window = MainWindow()
    app.exec_()
    sys.exit(0)


if __name__ == '__main__':
    main()
