# importing required modules
import sys
import time
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QScrollBar, QSplitter, QTableWidgetItem, QTableWidget, QComboBox, QVBoxLayout, QGridLayout, QDialog, QWidget, QPushButton, QApplication, QMainWindow, QAction, QMessageBox, QLabel, QTextEdit, QProgressBar, QLineEdit
from PyQt5.QtCore import QCoreApplication
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os
from gtts import gTTS
from pygame import mixer
from tempfile import TemporaryFile

# defining global variable for response from trained bot
global response
response = ''

# class for main Window which has QDialog inheritance


class Window(QDialog):
    def __init__(self):
        # multiple inheritance
        super().__init__()
        # creating widgets for chatBody layout which uses splitter2 to combine the Send Button and splitter; splitter combines Chat History and Chat Text Field
        self.chatTextField = QLineEdit(self)
        self.chatTextField.resize(480, 100)
        self.chatTextField.move(10, 350)

        self.btnSend = QPushButton("Send", self)
        self.btnSend.resize(480, 30)
        self.btnSendFont = self.btnSend.font()
        self.btnSendFont.setPointSize(15)
        self.btnSend.setFont(self.btnSendFont)
        self.btnSend.move(10, 460)
        self.btnSend.setStyleSheet("background-color: #86f715")
        self.btnSend.clicked.connect(self.send)

        self.chat = QTextEdit()
        self.chat.setReadOnly(True)

        splitter = QSplitter(QtCore.Qt.Vertical)
        splitter.addWidget(self.chat)
        splitter.addWidget(self.chatTextField)
        splitter.setSizes([400, 100])

        splitter2 = QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(splitter)
        splitter2.addWidget(self.btnSend)
        splitter2.setSizes([200, 10])

        self.chatBody = QVBoxLayout(self)
        self.chatBody.addWidget(splitter2)

        self.setWindowTitle("Chat Application")
        self.resize(500, 500)

    # method for sending chat which displays input and gets reponse using getResponse() function and displays the response as well
    def send(self):
        text = self.chatTextField.text()
        font = self.chat.font()
        font.setPointSize(13)
        self.chat.setFont(font)
        textFormatted = '{:>80}'.format(text)
        self.chat.append("Me: " + textFormatted)
        self.chatTextField.setText("")
        response = getResponse(text)
        self.chat.append("Bot: " + response)
        talkToMe(response)

# function to train the bot form chatterbot


def trainBot():
    global bot
    bot = ChatBot('Bot')
    bot.set_trainer(ListTrainer)
    dirname = '/Users/tanvirniaz/Documents/Python/anaconda3/lib/python3.6/site-packages/chatterbot_corpus/data/english'
    for filename in os.listdir(dirname):
        with open(os.path.join(dirname, filename), "rt") as f:
            data = f.readlines()
        bot.train(data)

# function to get reponse from trained bot given a text string input


def getResponse(text):
    reply = bot.get_response(text)
    return str(reply)

# function to convert input string into audio file using gTTS and plays the file using pygame mixer


def talkToMe(audioString):
    tts = gTTS(text=audioString, lang='en')
    mixer.init()
    sf = TemporaryFile()
    tts.write_to_fp(sf)
    sf.seek(0)
    mixer.music.load(sf)
    mixer.music.play()


# main function in QApplication form which trains the bot and then executes the main window
if __name__ == '__main__':
    app = QApplication(sys.argv)
    trainBot()
    window = Window()
    window.exec()

    sys.exit(app.exec_())
