from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, \
    QSlider, QStyle, QSizePolicy, QFileDialog
import sys
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtCore import Qt, QUrl
 
 
 
class Window(QWidget):
    def __init__(self):
        super().__init__()
 
        self.setWindowTitle("PyMusic") #название окна
        self.setGeometry(350, 100, 700, 100) #размеры окна
        self.setFixedSize(700, 100)
 
        # цвет окна
        p =self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)
 
        self.init_ui()
 
 
        self.show()
 
 
    def init_ui(self):
 
        #создание объекта медиаплеера
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
 
 
        #создание виджета видеоплеера
 
        videowidget = QVideoWidget()
 
 
        #создание кнопки "открыть музыку"
        openBtn = QPushButton('Open Music')
        openBtn.clicked.connect(self.open_file)
 
 
 
        #функционал кнопки воспроизведения
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)
 
 
 
        #создание слайдера перемотки
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0,0)
        self.slider.sliderMoved.connect(self.set_position)
 
 
 
        #create label
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
 
 
        #create hbox layout
        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(50,0,50,0)
 
        #set widgets to the hbox layout
        hboxLayout.addWidget(openBtn)
        hboxLayout.addWidget(self.playBtn)
        hboxLayout.addWidget(self.slider)
 
 
 
        #create vbox layout
        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(videowidget)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(self.label)
 
        # установка макета для окна (иначе не будут выходных данных)
        self.setLayout(vboxLayout)
 
        self.mediaPlayer.setVideoOutput(videowidget)
 
 
        #media player signals
 
        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)
 
        # функция открытия файла
    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Выбрать файл")
 
        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)
 
    # функция воспроизведения
    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
 
        else:
            self.mediaPlayer.play()
 
    # функция проверки состояния мультимедия (изменение значка воспроизведения при паузе и воспроизведении)
    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)
 
            )
 
        else:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)
 
            )
 
    # позиция слайдера
    def position_changed(self, position):
        self.slider.setValue(position)
 
 
    def duration_changed(self, duration):
        self.slider.setRange(0, duration)
 
 
    def set_position(self, position):
        self.mediaPlayer.setPosition(position)
 
    # обработка ошибок (вывод в консоль)
    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.mediaPlayer.errorString())
 
 
 
 
 
app = QApplication(sys.argv)
window = Window()
# основной цикл приложения. Получение события из окна и отправление в приложение
sys.exit(app.exec_())