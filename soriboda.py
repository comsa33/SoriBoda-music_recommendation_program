import sys
import os
import urllib.request
import webbrowser
import threading
import time
from datetime import date, datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5 import sip
import sqlite3
import pandas as pd
from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView,QWebEnginePage as QWebPage
from PyQt5.QtWebEngineWidgets import QWebEngineSettings as QWebSettings
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import urllib.request

### 광원이 코드
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
# 혹은 options.add_argument("--disable-gpu")
form_class = uic.loadUiType("영상.ui")[0]

wd = webdriver.Chrome('C:\\Users\\user\\PycharmProjects\\PYQT_Project_1\\SoriBoda-main\\chromedriver.exe', options=options)

form_class = uic.loadUiType("soriboda.ui")[0]

class SoribodaApp(QMainWindow, form_class):
    ### 세은이 코드 변수
    members = {}  # 회원 정보 딕셔너리
    # 회원 정보 1개 이상일 때 주석 제거
    con = sqlite3.connect('SBmembers.db')
    cur = con.cursor()
    members_df = pd.read_sql('SELECT * FROM SBmembers', con)
    id_result = list(members_df['id'])
    pw_result = list(members_df['pw'])
    print(id_result)
    print(pw_result)
    print(members_df)

    ### 영완이 코드 변수
    search_year = []    #검색할 년도 리스트
    title_btns=[]       #노래제목이 들어갈 리스트       (프레임안에들어갈리스트)
    artist_btns=[]      #가수가 들어갈 리스트          (프레임안에들어갈리스트)
    images_labels=[]    #앨범 이미지가 들어갈 리스트    (프레임안에들어갈리스트)
    images=[]           #잠시 이미지를 넣어둘 리스트     (db에서 뽑아오기 위함)
    song_name=[]        #잠시 노래제목을 넣어둘 리스트   (db에서 뽑아오기 위함)
    singer=[]           #잠시 가수이름을 넣어둘 리스트   (db에서 뽑아오기 위함)
    con = sqlite3.connect("소리보다_sql.db")        #sql데이터
    music_df = pd.read_sql("SELECT * FROM 노래", con, index_col='index')    #sql판다스식으로 변경

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget_3.setCurrentIndex(0)
        # 세은이 코드
        self.sign_in()

        self.btn_recommend.clicked.connect(lambda: self.stackedWidget_2.setCurrentIndex(0))
        self.btn_search.clicked.connect(lambda: self.stackedWidget_2.setCurrentIndex(1))
        self.btn_logout.clicked.connect(self.logout)
        self.btn_myinfo.clicked.connect(lambda: self.stackedWidget_2.setCurrentIndex(2))

    def logout(self):
        self.stackedWidget.setCurrentIndex(0)
        self.id_lineEdit_1.clear()
        self.pw_lineEdit_1.clear()

    ### 세은이 코드 : 로그인 + 회원관리db
    def sign_in(self):
        self.label_status.clear()
        self.btn_signup.clicked.connect(self.join_move)  # 첫 번째 창 회원가입 btn
        self.join_btn_2.clicked.connect(self.info)  # 두 번째 창 회원가입 btn
        self.id_ck_btn.clicked.connect(self.id_Check)  # id 중복 확인 btn
        self.btn_signin.clicked.connect(self.login)
        self.pw_lineEdit_1.returnPressed.connect(self.login)

    def join_move(self):
        self.stackedWidget_3.setCurrentIndex(1)
        self.id_ck_label.clear()
        self.pw_ck_label.clear()
        self.birth_years()

    def birth_years(self):
        for year in range(1955, 2021):
            self.year_comboBox.addItem(f'{year}')

    def id_Check(self):
        for i in self.id_result:
            if self.id_lineEdit_2.text() == i:
                self.id_ck_label.setText('사용할 수 없는 아이디입니다')
            else:
                self.id_ck_label.setText('사용 가능한 아이디입니다')
                pass

    def login(self):
        for i in self.id_result:
            for j in self.pw_result:
                if self.id_lineEdit_1.text() == i and self.pw_lineEdit_1.text() == j:
                    self.label_status.setText('로그인 성공')
                    self.stackedWidget.setCurrentIndex(1)
                    self.current_user_id = self.id_lineEdit_1.text()
                    self.current_user_df = self.members_df.loc[self.members_df['id'] == self.current_user_id]
                    print('현재 로그인 정보 df\n',self.current_user_df)
                    self.birthday = str(self.current_user_df['birth_year'].values[0])
                    print(self.birthday)
                    self.check_birthday()
                elif self.id_lineEdit_1.text() != i and self.pw_lineEdit_1.text() != j:
                    self.label_status.setText('존재하지 않는 로그인 정보입니다!')
                elif self.id_lineEdit_1.text() != i:
                    self.label_status.setText('아이디가 올바르지 않습니다!')
                elif self.pw_lineEdit_1.text() != j:
                    self.label_status.setText('패스워드가 올바르지 않습니다!')

    def info(self):
        nick = self.nick_lineEdit.text()                 # 닉네임
        birth_year = self.year_comboBox.currentText()    # 출생년도
        id = self.id_lineEdit_2.text()                   # id
        pw = self.pw_lineEdit_2.text()                   # pw
        rpw = self.rpw_lineEdit.text()                   # pw 재확인

        if pw != rpw:
            self.pw_ck_label.setText('패스워드가 일치하지 않습니다!')
        else:
            self.members = {'nick':[nick], 'birth_year':[birth_year], 'id':[id], 'pw':[pw]}

            res = pd.DataFrame(self.members)
            con = sqlite3.connect('SBmembers.db')
            res.to_sql('SBmembers', con, if_exists='append')
            members_df = pd.read_sql('SELECT * FROM SBmembers', con)

            print('\n',members_df)

            self.stackedWidget_3.setCurrentIndex(0)

    ### 영완이 코드 : 노래 추천
    # 생년월일 중 2000년이 넘어가면 2000년생으로 설정해 15개가 무조건 나오는 함수
    def check_birthday(self):
        if int(self.birthday)>=2000:
            self.birthday='2000'
            self.start_year = int(self.birthday) + 15
            self.end_year = int(self.birthday) + 20
            while True:
                if self.start_year != self.end_year:
                    self.search_year.append(str(self.start_year))
                    self.start_year = self.start_year + 1
                else:
                    break
        elif int(self.birthday)<2000:
            self.start_year = int(self.birthday) + 15
            self.end_year = int(self.birthday) + 20
            while True:
                if self.start_year != self.end_year:
                    self.search_year.append(str(self.start_year))
                    self.start_year = self.start_year + 1
                else:
                    break
        self.user_search_result()

    # 사용자 생년월일에 맞춰 이미지,노래,가수를 뽑아 저장하는 함수
    def user_search_result(self):
        for j in range(len(self.search_year)):
            for i in range(len(self.music_df)):
                if self.search_year[j] in self.music_df.loc[i][0]:
                    self.images.append(self.music_df.loc[i][1])
                    self.song_name.append(self.music_df.loc[i][2])
                    self.singer.append(self.music_df.loc[i][3])
        self.labels_produce()

    # 동적 변수로 라벨과 푸시버튼을 15개 생성 및 위에서 뽑아온 데이터 넣어주는 함수
    def labels_produce(self):
        for i in range(15):
            globals()['title_btn{}'.format(i)] = QPushButton()
            globals()['title_btn{}'.format(i)].setStyleSheet('QPushButton {border:None; '
                                                             'text-align:left;'
                                                             'background-color:rgb(230,230,230);'
                                                             '}'
                                                             'QPushButton:hover{'
                                                             'border-radius: 7px;'
                                                             'background-color:rgb(245,245,245);'
                                                             '}')
            globals()['title_btn{}'.format(i)].setCursor(QCursor(QtCore.Qt.PointingHandCursor))
            globals()['title_btn{}'.format(i)].setFont(QFont('나눔스퀘어_ac ExtraBold', 13))
            globals()['title_btn{}'.format(i)].setText(self.song_name[i])
            globals()['title_btn{}'.format(i)].setMinimumSize(250, 30)
            globals()['title_btn{}'.format(i)].setMaximumSize(250, 30)
            self.title_btns.append(globals()['title_btn{}'.format(i)])
            globals()['artist_btn{}'.format(i)] = QPushButton()
            globals()['artist_btn{}'.format(i)].setStyleSheet('QPushButton {border:None; '
                                                              'text-align:left;'
                                                              'background-color:rgb(230,230,230);'
                                                              '}')
            globals()['artist_btn{}'.format(i)].setFont(QFont('나눔스퀘어_ac Light', 10))
            globals()['artist_btn{}'.format(i)].setText(self.singer[i])
            globals()['artist_btn{}'.format(i)].setMinimumSize(250, 30)
            globals()['artist_btn{}'.format(i)].setMaximumSize(250, 30)
            self.artist_btns.append(globals()['artist_btn{}'.format(i)])
            globals()['images_label{}'.format(i)] = QLabel()
            globals()['images_label{}'.format(i)].setStyleSheet('QLabel {border:None;}')
            globals()['images_label{}'.format(i)].setMaximumSize(80, 80)
            globals()['album_image{}'.format(i)]=urllib.request.urlopen(self.images[i]).read()
            globals()['pixmaps{}'.format(i)]=QPixmap()
            globals()['pixmaps{}'.format(i)].loadFromData(globals()['album_image{}'.format(i)])
            globals()['pixmaps{}'.format(i)].scaled(80, 80)
            globals()['images_label{}'.format(i)].setPixmap(globals()['pixmaps{}'.format(i)])
            globals()['images_label{}'.format(i)].setScaledContents(True)
            self.images_labels.append(globals()['images_label{}'.format(i)])
        self.label_contents_produce()

    # 프레임과 그리드 레이아웃을 동적 변수로 만들어서 QT에 추가시켜 보여주는 함수
    def label_contents_produce(self):

        for i in range(15):
            globals()['G_layout{}'.format(i)]=QGridLayout()
            globals()['G_layout{}'.format(i)].setContentsMargins(0, 0, 0, 0)
            globals()['G_layout{}'.format(i)].setHorizontalSpacing(10)
            globals()['G_layout{}'.format(i)].setVerticalSpacing(0)
            globals()['G_layout{}'.format(i)].addWidget(self.title_btns[i], 0, 1, 1, 4)
            globals()['G_layout{}'.format(i)].addWidget(self.artist_btns[i], 1, 1, 1, 4)
            globals()['G_layout{}'.format(i)].addWidget(self.images_labels[i], 0, 0, 2, 2)
            globals()['like_Frame{}'.format(i)]=QFrame()
            globals()['like_Frame{}'.format(i)].setStyleSheet('QFrame {border:none; background-color:rgb(230,230,230);}')
            globals()['like_Frame{}'.format(i)].setMinimumSize(490,80)
            globals()['like_Frame{}'.format(i)].setContentsMargins(0,0,0,0)
            globals()['like_Frame{}'.format(i)].setLayout(globals()['G_layout{}'.format(i)])
            self.verticalLayout_10.addWidget(globals()['like_Frame{}'.format(i)])
            ### 루오 : 버튼마다 '제목+가수이름'별로 링크 걸어두기
            globals()['search_word{}'.format(i)] = str(self.song_name[i]) + "+" + str(self.singer[i])
            print(globals()['search_word{}'.format(i)])

        self.title_btns[0].clicked.connect(lambda: self.youtube(globals()['search_word{}'.format(0)], 0))
        self.title_btns[1].clicked.connect(lambda: self.youtube(globals()['search_word{}'.format(1)], 1))
        self.title_btns[2].clicked.connect(lambda: self.youtube(globals()['search_word{}'.format(2)], 2))
        self.title_btns[3].clicked.connect(lambda: self.youtube(globals()['search_word{}'.format(3)], 3))
        self.title_btns[4].clicked.connect(lambda: self.youtube(globals()['search_word{}'.format(4)], 4))
        self.title_btns[5].clicked.connect(lambda: self.youtube(globals()['search_word{}'.format(5)], 5))
        self.title_btns[6].clicked.connect(lambda: self.youtube(globals()['search_word{}'.format(6)], 6))
        self.title_btns[7].clicked.connect(lambda: self.youtube(globals()['search_word{}'.format(7)], 7))
        self.title_btns[8].clicked.connect(lambda: self.youtube(globals()['search_word{}'.format(8)], 8))
        self.title_btns[9].clicked.connect(lambda: self.youtube(globals()['search_word{}'.format(9)], 9))
        self.title_btns[10].clicked.connect(lambda: self.youtube(globals()['search_word{}'.format(10)], 10))
        self.title_btns[11].clicked.connect(lambda: self.youtube(globals()['search_word{}'.format(11)], 11))
        self.title_btns[12].clicked.connect(lambda: self.youtube(globals()['search_word{}'.format(12)], 12))
        self.title_btns[13].clicked.connect(lambda: self.youtube(globals()['search_word{}'.format(13)], 13))
        self.title_btns[14].clicked.connect(lambda: self.youtube(globals()['search_word{}'.format(14)], 14))


    ### 광원이 코드
    def youtube(self, search_word, order_no):
        print(search_word)
        self.search_lylics(self.song_name[order_no], self.singer[order_no])
        self.deleteLayout(self.frame_25.layout())
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.webview = QWebView(self)
        self.layout.addWidget(self.webview)
        self.frame_25.setLayout(self.layout)
        youtube_url = 'https://www.youtube.com/results?search_query=' + search_word + '노래'
        wd.get(youtube_url)
        # time.sleep(0.3)
        html = wd.page_source
        soupYT = BeautifulSoup(html, 'html.parser')
        ss = soupYT.select_one('#contents > ytd-video-renderer:nth-child(3) > div > ytd-thumbnail > a')
        tail = ss.attrs['href'][9:]
        url = "https://www.youtube.com/embed/" + tail # +'?autoplay=1&mute=1'
        self.webview.setUrl(QUrl(url))
        wd.quit()

    def deleteLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.deleteLayout(item.layout())
            sip.delete(layout)


    ### 용천이 코드
    def search_lylics(self, title, artist):
        naver_URL = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query='
        fullURL = naver_URL + artist + " " + title + " " + '가사'
        naver_wd = webdriver.Chrome('C:\\Users\\user\\PycharmProjects\\PYQT_Project_1\\SoriBoda-main\\chromedriver.exe',
                              options=options)

        naver_wd.get(fullURL)
        time.sleep(1)

        naver_wd.find_element_by_class_name("area_button_arrow").click()
        html = naver_wd.page_source
        soup = BeautifulSoup(html, 'html.parser')
        lylics = soup.select_one(
            '#main_pack > div.sc_new.cs_common_module._au_music_content_wrap.case_empasis.color_23 > div.cm_content_wrap > div.cm_content_area._cm_content_area_song_lyric > div > div.intro_box > p')
        result = lylics.get_text()
        print(result)
        self.textBrowser.setText(result)

    def initUI(self):
        self.setWindowTitle('음악을 눈으로 즐기다! 소리보다!')
        # self.resize(1000, 850)
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = SoribodaApp()
    form.show()
    exit(app.exec_())