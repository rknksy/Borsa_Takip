import json
import os.path
import matplotlib.dates as mdates
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import sys, matplotlib.pyplot as plt
from PyQt5 import QtGui,QtWidgets
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox
from Borsa_Takip_form import Ui_MainWindow
from Borsa_Takip_data_collect import *


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Ui elemanların listesi

        # self.setWindowTitle("SBroker")
        # self.setWindowIcon(QtGui.QIcon('The_Great_Wave_off_Kanagawa.jpg'))


        # self.setWindowOpacity(0.5)
        # self.ui.graph_Coin.setWindowOpacity(0)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_NoSystemBackground, True)

        # self.setWindowOpacity(0.5)
        # self.ui.graph_Coin.setAutoFillBackground(True)


        coin_list = self.ui.lW_coin_list

        al_bar = self.ui.pB_AL
        sat_bar = self.ui.pB_SAT

        start = self.ui.pb_Start
        start.clicked.connect(self.alarm_check)

        set_alarm_Start = self.ui.pB_set_Alarm
        set_alarm_Stop = self.ui.pB_set_Alarm_stop
        set_alarm_Start.clicked.connect(self.alarm_set_enter)
        set_alarm_Stop.clicked.connect(self.alarm_set_exit)

        ara_btn_coin = self.ui.btn_ARA_coin

        listele_btn = self.ui.btn_Listele
        Load_btn = self.ui.btn_Load
        delete_btn = self.ui.btn_Delete
        ort_ciz = self.ui.btn_Ortalama_Ciz
        satin_alma_listesi = self.ui.tW_yaplan_alis_listesi



        # Gerekli Değişkenler listesi ********************

        self.ort=0
        self.alis_data = []
        self.liste_row = 0
        self.coin = 'Decentraland'
        self.current = 0
        self.alarm_stop_float, self.alarm_start_float = 0, 0



        # Grafikler ******************************

        self.plot_tuval_coin()
        # self.plot_tuval_analiz()
        self.data = coin_data_collect()
        self.current = self.data["open"][-1]
        print('self.current: ', self.current)

        self.plot_figure(self.data["date"],self.data["open"])


        # Listeler *******************************

        # self.fav_coin_list = cyropto_currency_list['currency name']
        # self.fav_coin_code = cyropto_currency_list['currency code']
        self.fav_coin_list = ['Decenterland','Bitcoin','Ethereum','Shiba Inu', 'DogeCoin','Polkadot','Ripple']
        self.fav_coin_code = ['MANA','BTC', 'ETH', 'SHIB', 'DOGE', 'DOT', 'XRP']
        self.fav_coin_list_with_codes = []
        for i in range(len(self.fav_coin_list)):
            self.fav_coin_list_with_codes.append(self.fav_coin_list[i]+" ---> "+ self.fav_coin_code[i])

        self.fav_analiz_list = ['lolo', 'mama', 'dada', 'Bitcoin']

        coin_list.addItems(self.fav_coin_list_with_codes)
        coin_list.setCurrentItem(self.ui.lW_coin_list.item(0))
        coin_list.currentItemChanged.connect(self.selectedCoinChanged)

        # analiz_list.addItems(self.fav_analiz_list)
        # analiz_list.setCurrentItem(self.ui.lW_Analiz_list.item(0))
        # analiz_list.currentItemChanged.connect(self.selectedAnalizChanged)

        ara_btn_coin.clicked.connect(self.arama_coin_list)
        # ara_btn_analiz.clicked.connect(self.arama_analiz_list)

        # ALım-Satım Listesi **********************

        satin_alma_listesi.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)  # listeyi kilitleme
        listele_btn.clicked.connect(self.listeleme)
        Load_btn.clicked.connect(self.update)
        delete_btn.clicked.connect(self.delete)
        ort_ciz.clicked.connect(self.orta_ciz)



        # AL-Sat Barlar ***************************

        sat_bar.setStyleSheet("QProgressBar"
            "{"
                             "border: 2px solid grey;"
                             "border-radius: 5px;"
                             "text-align: center;"
                             "}""QProgressBar::chunk "
                          "{"
                              "background-color: red;"
                              
                          "}")
        al_bar.setStyleSheet("QProgressBar"
            "{"
                             "border: 2px solid grey;"
                             "border-radius: 5px;"
                             "text-align: center;"
                             "}"
                             "QProgressBar::chunk"
            "{"
                             "background-color: # 05B8CC;"
                             
                             "}")

        self.Self_Update()


    # ******************* Fonksiyonlar ****************************

    # Grafik fonksiyonları ****************

    def plot_tuval_coin(self):
        self.figure_coin = plt.figure()
        self.canvas_coin = FigureCanvas(self.figure_coin)
        self.toolbar_coin = NavigationToolbar(self.canvas_coin, self)

        layout = QVBoxLayout()
        layout.addWidget(self.toolbar_coin)
        layout.addWidget(self.canvas_coin)
        self.ui.graph_Coin.setLayout(layout)

    def plot_figure(self,x,y):
        self.figure_coin.clear()

        self.ax = self.figure_coin.add_subplot(111)

        self.ax.grid(True)

        # date axis için
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
        plt.gcf().autofmt_xdate()
        x.reverse()
        y.reverse()
        try:
            plt.axis([x[-14],x[-1],min(y),max(y)]) #zoom ayarı için ama pek sağlıklı değil
        except Exception as error:
            print(error)

        print(x)
        self.ax.plot(x,y,'r.-',mec='black')


        self.canvas_coin.draw()

    # Liste Fonksiyonları *******************

    def selectedCoinChanged(self, selected_coin):

        self.ui.lW_coin_list.setCurrentItem(selected_coin)
        row =self.ui.lW_coin_list.currentRow()
        code = self.fav_coin_code[row]
        self.coin = self.fav_coin_list[row]
        print('new coin: ',code)
        print('selected coin:', self.coin)
        self.data_refresh(code)


    def arama_coin_list(self ):

        for index, item in enumerate(self.fav_coin_list):

            if item == self.ui.le_Coi_Arama.text():
                self.coin = item
                print('listede bulundu')
                print(item)
                self.ui.lW_coin_list.setCurrentItem(self.ui.lW_coin_list.item(index))
                # code = self.fav_coin_code[index]
                # self.data_refresh(code)
                self.ui.le_Coi_Arama.setText('')
                break

            else:
                print('listede bulunamadı')
                pass



    #     Alım-Satım Listeleme fonksiyonları *******************************

    def listeleme(self):

        miktar = self.ui.le_Miktar.text()
        fiyat = self.ui.le_Fiyat.text()


        self.create_alis_data(miktar,fiyat)

        self.yazdir()

        self.ui.le_Fiyat.setText('')
        self.ui.le_Miktar.setText('')

    def create_alis_data(self, miktar,fiyat):

        miktar_float = float(miktar)
        fiyat_float = float(fiyat)
        alis_maliyet_float = miktar_float*fiyat_float
        tm=0
        tmf=0
        ort = 0

        self.alis_data.append({"tarih": str(datetime.datetime.now().date()), "miktar": str(miktar_float), "fiyat": str(fiyat_float),
                     "alis_maliyet": str(alis_maliyet_float), "ort_fiyat": str(round(ort,2))})

        for index,item in enumerate(self.alis_data):
            tmf += float(item["alis_maliyet"])
            tm += float(item["miktar"])
            ort = tmf / tm

            self.alis_data[index]["ort_fiyat"] = str(ort)
        self.ort = ort
        self.tm = tm
        print('self.ort=',self.ort)
        print('self.coin:',self.coin)

        jsonString = json.dumps(self.alis_data)
        jsonFile = open(f"{self.coin}_alis_maliyet_data_json.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()



    def load_alis_data(self,coni='Bitcoin'):
        print("yazdır köpek")
        try:
            fileObject = open(f"{coni}_alis_maliyet_data_json.json", "r")
            jsonContent = fileObject.read()
            self.alis_data = json.loads(jsonContent)
        except Exception as error:
            print(error)
        print(self.alis_data)
        self.liste_row = len(self.alis_data)-1
        self.yazdir()



    def delete(self):
        try:
            if len(self.alis_data)>0:
                self.alis_data.pop(-1)
                print(self.alis_data)
                self.liste_row -= 1
                self.yazdir()
                self.ui.tW_yaplan_alis_listesi.removeRow(1)
                self.ui.tW_yaplan_alis_listesi.setRowCount(len(self.alis_data))
            else:
                print(self.ui.tW_yaplan_alis_listesi.rowCount())

        except EOFError as error:
            print('error:', error)
        jsonString = json.dumps(self.alis_data)
        jsonFile = open(f"{self.coin}_alis_maliyet_data_json.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()



    def orta_ciz(self):
        ort = self.ort
        print('ortlar: ',ort,self.ort)
        self.data_ort = []
        print('ort_ciz: ',ort,len(self.data["date"]))
        for i in range(len(self.data["date"])):
            self.data_ort.append([ort,self.data["open"][i]])
        print('data_ort: ',self.data_ort)
        print(type(self.data["date"][5]),self.data["date"][5])
        try:
            self.plot_figure(self.data["date"],self.data_ort)
        except Exception as error:
            print(error)
        self.canvas_coin.draw()
        self.canvas_coin.show()



    def yazdir(self):
        self.alis_data.reverse()
        self.liste_row +=1
        self.ui.tW_yaplan_alis_listesi.setRowCount(self.liste_row)
        print(self.liste_row)
        for index_y,item_y in enumerate(self.alis_data):
            self.ui.tW_yaplan_alis_listesi.setVerticalHeaderItem(index_y, QTableWidgetItem(self.alis_data[index_y]["tarih"]))
            self.ui.tW_yaplan_alis_listesi.setItem(index_y, 0, QTableWidgetItem(self.alis_data[index_y]["miktar"]))
            self.ui.tW_yaplan_alis_listesi.setItem(index_y, 1, QTableWidgetItem(self.alis_data[index_y]["fiyat"]))
            self.ui.tW_yaplan_alis_listesi.setItem(index_y, 2, QTableWidgetItem(self.alis_data[index_y]["alis_maliyet"]))
            self.ui.tW_yaplan_alis_listesi.setItem(index_y, 3, QTableWidgetItem(self.alis_data[index_y]["ort_fiyat"]))
        self.alis_data.reverse()

    # Data Yenileme ******************************

    def data_refresh(self,code):

        self.data = coin_data_collect(str(code))
        print('yenilenmiş ort',self.ort)

        print(code,'\n data_refreshed: ', self.data)

        self.plot_figure(self.data["date"], self.data["open"])
        self.canvas_coin.draw()
        self.canvas_coin.show()


        try:
            self.ui.tW_yaplan_alis_listesi.setRowCount(1)
            self.load_alis_data(self.coin)
        except Exception as error:
            print(error)

        data = 0
# datayı da sıfırlamak lazım yoksa eski datayı ekliyor. satırları da silmek lazım. ortalama 2 bas olmalı




    # Alarm ******************************

    def alarm_Play(self,song_wav):
        CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
        # filename = os.path.join(CURRENT_DIR, "sell-alarm.wav")

        full_path = os.path.join(CURRENT_DIR, song_wav)
        url = QUrl.fromLocalFile(full_path)
        content = QMediaContent(url)
        self.player = QMediaPlayer()
        self.player.setMedia(content)
        self.player.setVolume(80)
        self.player.play()
        print('played dude')

    def alarm_Stop(self):
        self.player.stop()

    def alarm_set_enter(self):
        try:
            dada = float(self.ui.le_Alarm.text())
            self.alarm_start_float = 0
            self.ui.lb_Alarm.setText(f'Kar alarmı, %{dada} olarak ayarlandı.')
            self.alarm_start_float = dada / 100
            self.ui.le_Alarm.setText(' ')
        except Exception as error:
            self.ui.lb_Alarm_stop.setText('Lütfen sayı giriniz')
            print(error)

    def alarm_set_exit(self):
        try:
            dada = float(self.ui.le_Alarm_stop.text())
            self.alarm_stop_float = 0
            self.ui.lb_Alarm_stop.setText(f'Zarar alarmı, %{dada} olarak ayarlandı.')
            self.alarm_stop_float = dada/100
            self.ui.le_Alarm_stop.setText(' ')
        except Exception as error:
            self.ui.lb_Alarm_stop.setText('Lütfen sayı giriniz')
            print(error)


    def alarm_check(self):

        if self.ort:
            try:
                dart = (self.current - self.ort) / self.ort
                print('dart: ', dart)
                print(self.alarm_stop_float, self.alarm_start_float)
                if dart >= self.alarm_start_float and dart > 0:
                    print('here we are')
                    self.alarm_Play('buy-alarm.wav')
                    self.pop_up('Kar alınabilir')
                    self.ui.lb_Status.setText('Çıkış yap kanki düşüyoruz')

                elif -dart >= self.alarm_stop_float and dart < 0:
                    print('here not we are')
                    self.alarm_Play('sell-alarm.wav')
                    self.pop_up('Çıkış yap kanki düşüyoruz')
                    self.ui.lb_Status.setText('Çıkış yap kanki düşüyoruz')
                else:
                    print('Wait for it!')
                    self.ui.lb_Status.setText('Wait for it!')

            except Exception as error:
                print(error)
        else:
            self.ui.lb_Status.setText("Alarm Kur Kardeş Önce")


    def pop_up(self,text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(text)
        msg.setInformativeText(f" Ort: {self.ort} \n Anlık: {self.current} \n Toplam Miktar: {self.tm} \n Net kazanç: {self.tm*(self.current-self.ort)} ")
        msg.setWindowTitle(" Uyarı")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.buttonClicked.connect(self.alarm_Stop)

        retval = msg.exec_()
        print("value of pressed message box button:", retval)

    #     Self_Update *******************

    def Self_Update(self):
        timer = QTimer()
        timer.timeout.connect(self.update)
        timer.setInterval(30000) #5min =300.000 msn
        timer.start()
        print('UPDATED BROOO')

    def update(self):
        self.ort = self.data["ort_fiyat"][-1]
        print(self.ort)
        self.data = coin_data_collect(self.fav_coin_code[self.fav_coin_list.index(self.coin)])

        if self.data_ort:
            for i in range(len(self.data["date"])):
                self.data_ort.append([self.ort, self.data["open"][i]])

            try:
                self.plot_figure(self.data["date"], self.data_ort)
            except Exception as error:
                print(error)

            self.canvas_coin.draw()
            self.canvas_coin.show()

        try:
            self.ui.tW_yaplan_alis_listesi.setRowCount(1)
            self.load_alis_data(self.coin)
        except Exception as error:
            print(error)

        self.alarm_check()
        print('update lo update')




"""
*********************Main Start***********************
"""

def Borsa_Takip():
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())

Borsa_Takip()
