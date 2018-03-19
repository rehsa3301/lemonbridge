# -*- coding: utf-8 -*-

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import util

# scraping
from scrape import get_movies

# all modules
from modules import leetx


IMG_LOAD = QImage('./img/load.gif')
IMG_NO_POSTER = QImage('./img/noposter.jpg')

# make conf later
DOWNLOAD_DIR = '/home/user/Downloads'


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.w = QWidget()

        # search box
        self.search = QLineEdit(self.w)
        self.search.move(10, 10)
        self.search.setFixedWidth(500)
        self.search.setFixedHeight(40)
        f = self.search.font()
        f.setPointSize(18)
        self.search.setFont(f)
        self.search.returnPressed.connect(self.button_pressed)

        # search button
        self.button = QPushButton(self.w)
        self.button.setFixedSize(QSize(40, 40))
        self.button.move(520, 10)
        self.button.setIconSize(QSize(32, 32))
        self.button.setIcon(QIcon("./img/search.png"))
        self.button.pressed.connect(self.button_pressed)

        self.setGeometry(0, 0, 800, 400)
        self.setCentralWidget(self.w)
        self.show()
    
    def button_pressed(self):
        # loading animation here

        self.clean_up_screen()

        search_query = self.search.displayText()

        if search_query:
            self.movies = get_movies(search_query)

            self.current_screen = []
            for i, movie in enumerate(self.movies):
                t = QTextEdit(self.w)
                t.setReadOnly(True)
                t.textCursor().insertHtml('%s (%s)' % (self.movies[i]['title'],
                    self.movies[i]['year']))
                t.setFixedWidth(182)
                t.setFixedHeight(55)
                t.move(10+200*i, 330)
                t.show()

                p = QLabel(self.w)

                if movie['poster']:
                    # response = requests.get(movie['poster'])
                    response = util.http_get_request_raw(movie['poster'])
                    pixmap = QPixmap()
                    pixmap.loadFromData(response.content)
                    p.setPixmap(pixmap)
                else:
                    p.setPixmap(QPixmap.fromImage(IMG_NO_POSTER))
                
                # note; maybe something like- self.mouse_pressed(i=i)
                # p.mousePressEvent = self.mouse_pressed

                # this is probably a horrible idea, fuck it
                exec("p.mousePressEvent = self.mouse_pressed_%s" % str(i))
                p.move(10+200*i, 60)
                p.show()

                self.current_screen.append(t)
                self.current_screen.append(p)
    
    def clean_up_screen(self):
        try:
            for i in self.current_screen:
                i.deleteLater()
            self.current_screen = []
        except:
            pass

    def mouse_pressed_0(self, event):
        self.download(0)
    
    def mouse_pressed_1(self, event):
        self.download(1)
    
    def mouse_pressed_2(self, event):
        self.download(2)
    
    def mouse_pressed_3(self, event):
        self.download(3)
    
    def download(self, i):
        self.clean_up_screen()

        title = self.movies[i]['title']
        year = self.movies[i]['year']
        results = leetx.search('%s %s' % (title, year))
        # { ... title: {'leeches': 'n', 'seeds': 'n', 'link', 'magnet'} ... }

        html = '<table><tr><th>Name</th><th>Seeders</th><th>Leechers</th><th>Magnet</th></tr>'
        for k, v in results.items():
            html += '<tr><th>{}</th><th>{}</th><th>{}</th><th><a href={}>magnet</a></th></tr>'.format(
                k, v['seeds'], v['leeches'], v['link'])
        html += '</table>'

        t = QTextEdit(self.w)
        t.setReadOnly(True)
        t.textCursor().insertHtml(html)
        t.setFixedWidth(780)
        t.setFixedHeight(330)
        t.move(10, 60)
        t.show()
  
        self.current_screen.append(t)
