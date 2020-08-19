from PyQt5 import QtWidgets, uic, QtCore, QtGui
import sys
from threading import Thread
import DataBase
import config
import random
import pyttsx3
import speech_recognition as sr
import tkinter
from tkinter import ttk
import NiverData

en = pyttsx3.init('sapi5')

def saiSom(fala):
    en.say(fala)
    en.runAndWait()


def Assistent(UserVA, CityVA, VozVA):
    config.Intro()
    saiSom("Iniciando")
    print("=" * len(f"Bem vindo {UserVA}."))
    print(f"Bem vindo {UserVA}!")
    print("=" * len(f"Bem vindo {UserVA}."))
    saiSom(f"Bem vindo {UserVA}")
    print(config.NiverDataVerify(UserVA))
    saiSom(config.NiverDataVerify(UserVA))
    print("Ouvindo...")

    while True:
        erro = random.choice(config.listaErros)
        sair = False

        def entrada(talk=False):
            if VozVA:
                rec = sr.Recognizer()

                with sr.Microphone() as source:
                    rec.adjust_for_ambient_noise(source)
                    while True:
                        try:
                            audio = rec.listen(source)
                            if talk:
                                ent = rec.recognize_google(audio, language='en-US')
                            else:
                                ent = rec.recognize_google(audio, language='pt-BR')
                            return ent
                        except sr.UnknownValueError:
                            if talk:
                                pass
                            else:
                                saiSom(erro)
            else:
                ent = input("Digite: ")
                return ent
        
        fala = entrada(talk=True).lower()

        if 'zoe' in fala:
            print("Estou ouvindo...")
            saiSom("Estou ouvindo")

            while True:
                try:
                    comando = entrada().lower()
                    print(f"User: {comando.capitalize()}")

                    # Sair do loop
                    if comando in config.listaSair:
                        print("Ok, quando precisar é só chamar!")
                        saiSom("Okey, quando precisar é só chamar")
                        break

                    # Comando Sair
                    if "sair" in comando:
                        try:
                            global janelaAberta
                            if janelaAberta:
                                resposta = "Uma janela aberta não foi fechada, feche-a para sair!"
                            else:
                                print("Saindo...")
                                saiSom("Saindo")
                                sair = True
                                break
                        except:
                            print("Saindo...")
                            saiSom("Saindo")
                            sair = True
                            break
                    
                    # Comando para mostrar as informações da cidade
                    elif "informações" in comando and "cidade" in comando:
                        resposta = "Mostrar informações da cidade"

                    elif "adicionar" in comando and "aniversário" in comando:
                        resposta = "Adicionar aniversário"


                    # Abrir sites e programas
                    elif "abrir" in comando:
                        resposta = config.Abrir(comando)
                    
                    # Tocar música
                    elif comando.startswith("tocar"):
                        comando = comando.replace("tocar ", "")
                        resposta = config.Tocar(comando)

                    # Pesquisar
                    elif comando.startswith("pesquisar"):
                        comando = comando.replace("pesquisar ", "")
                        if comando.startswith("por"):
                            comando.replace("por ", "")
                        resposta = config.Pesquisa(comando)

                    # Calcular
                    elif comando.startswith("quanto é"):
                        comando = comando.replace("quanto é ", "")
                        resposta = config.Calculadora(comando)

                    else:
                        resposta = "Ainda não aprendi a fazer isso."

                    if resposta == "Mostrar informações da cidade":
                            
                        lista_infos = config.ClimaTempo(CityVA)
                        longitude = lista_infos[0]
                        latitude = lista_infos[1]
                        temp = lista_infos[2]
                        pressao = lista_infos[3]
                        humidade = lista_infos[4]
                        temp_max = lista_infos[5]
                        temp_min = lista_infos[6]
                        v_speed = lista_infos[7]
                        v_direc = lista_infos[8]
                        nebulosidade = lista_infos[9]
                        id_da_cidade = lista_infos[10]

                        saiSom("Mostrando informações de {}".format(CityVA))
                        textoTitle = "Informações de {}".format(CityVA).upper()
                        textoLongLat = "Longitude: {}, Latitude: {}".format(longitude, latitude)
                        textoID = "Id: {}".format(id_da_cidade)
                        textoTemp = "Temperatura: {:.2f}º".format(temp)
                        textoTempMax = "Temperatura máxima: {:.2f}º".format(temp_max)
                        textoTempMin = "Temperatura minima: {:.2f}º".format(temp_min)
                        textoHum = "Humidade: {}".format(humidade)
                        textoNeb = "Nebulosidade: {}".format(nebulosidade)
                        textoPress = "Pressao atmosférica: {}".format(round(pressao))
                        textoVec = "Velocidade do vento: {}m/s".format(v_speed)
                        textoDir = "Direção do vento: {}°".format(v_direc)

                        def InfoCityWindow():
                            jan_tk = tkinter.Tk()
                            jan_tk.geometry("600x400+700+50")
                            jan_tk.title("Informações de sua Cidade")
                            jan_tk.resizable(width=False, height=False)
                            jan_tk.config(bg='#6A5ACD')

                            lb1 = tkinter.Label(jan_tk, text=textoTitle, font=("Comic Sans", 20, 'bold'), bg='#6A5ACD')
                            lb1.place(x=100, y=20)
                            lb2 = tkinter.Label(jan_tk, text=textoLongLat, font=("Comic Sans", 12, 'bold'), bg='#6A5ACD')
                            lb2.place(x=10, y=80)
                            lb3 = tkinter.Label(jan_tk, text=textoID, font=("Comic Sans", 12, 'bold'), bg='#6A5ACD')
                            lb3.place(x=10, y=110)
                            lb4 = tkinter.Label(jan_tk, text=textoTemp, font=("Comic Sans", 12, 'bold'), bg='#6A5ACD')
                            lb4.place(x=10, y=140)
                            lb5 = tkinter.Label(jan_tk, text=textoTempMax, font=("Comic Sans", 12, 'bold'), bg='#6A5ACD')
                            lb5.place(x=10, y=170)
                            lb6 = tkinter.Label(jan_tk, text=textoTempMin, font=("Comic Sans", 12, 'bold'), bg='#6A5ACD')
                            lb6.place(x=10, y=200)
                            lb7 = tkinter.Label(jan_tk, text=textoHum, font=("Comic Sans", 12, 'bold'), bg='#6A5ACD')
                            lb7.place(x=10, y=230)
                            lb8 = tkinter.Label(jan_tk, text=textoNeb, font=("Comic Sans", 12, 'bold'), bg='#6A5ACD')
                            lb8.place(x=10, y=260)
                            lb9 = tkinter.Label(jan_tk, text=textoPress, font=("Comic Sans", 12, 'bold'), bg='#6A5ACD')
                            lb9.place(x=10, y=290)
                            lb10 = tkinter.Label(jan_tk, text=textoVec, font=("Comic Sans", 12, 'bold'), bg='#6A5ACD')
                            lb10.place(x=10, y=320)
                            lb11 = tkinter.Label(jan_tk, text=textoDir, font=("Comic Sans", 12, 'bold'), bg='#6A5ACD')
                            lb11.place(x=10, y=350)

                            global janelaAberta
                            janelaAberta = True

                            jan_tk.mainloop()

                            janelaAberta = False


                        threadCity = Thread(target=InfoCityWindow)
                        threadCity.start()

                    elif resposta == "Adicionar aniversário":
                        janTk = tkinter.Tk()
                        janTk.geometry("300x200+400+300")
                        janTk.config(bg='#191970')
                        janTk.resizable(width=False, height=False)

                        dias = []
                        for c in range(1, 32):
                            dias.append(c)

                        def ButtonOk():
                            diaOk = dia.get()
                            mesOk = mes.get()
                            nomeOk = nome.get()
                            if diaOk == "" or mesOk == "" or nomeOk == "":
                                tkinter.messagebox.showerror("Error", "Preencha todos os dados!")
                            else:
                                janTk.destroy()
                                retorno = config.AdicionarData(nomeOk, diaOk, mesOk.lower())
                                print(retorno)
                                saiSom(retorno)


                        def Cancel():
                            janTk.destroy()
                            print("Tudo bem, estarei aqui caso precise!")
                            saiSom("Tudo bem, estarei aqui caso precise")

                        frame = tkinter.Frame(janTk, width=300, height=40)
                        frame.pack(side=tkinter.TOP)

                        titulo = tkinter.Label(frame, text="Coloque a data de aniversário!", font=("Calibri", 14, "bold"))
                        titulo.place(x=20, y=5)

                        frameBaixo = tkinter.Frame(janTk, width=300, height=158)
                        frameBaixo.pack(side=tkinter.BOTTOM)

                        lb = ttk.Label(frameBaixo, text="Dia:", font=("Calibri", 15, "bold"))
                        lb.place(x=20, y=15)

                        dia = ttk.Combobox(frameBaixo, values=dias, font=("Calibri", 12, "bold"))
                        dia.place(x=90, y=20)

                        lb2 = ttk.Label(frameBaixo, text="Mês:", font=("Calibri", 15, "bold"))
                        lb2.place(x=20, y=45)

                        mes = ttk.Combobox(frameBaixo, values=["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"], font=("Calibri", 12, "bold"))
                        mes.place(x=90, y=50)

                        lb3 = tkinter.Label(frameBaixo, text="Nome: ", font=("Calibri", 15, "bold"))
                        lb3.place(x=20, y=75)

                        nome = tkinter.Entry(frameBaixo, width=22, font=("Calibri", 12, "bold"))
                        nome.place(x=90, y=80)

                        bt1 = tkinter.Button(frameBaixo, text="OK", width=7, command=ButtonOk)
                        bt1.place(x=230, y=120)
                        bt2 = tkinter.Button(frameBaixo, text="Cancel", width=7, command=Cancel)
                        bt2.place(x=20, y=120)
                        
                        janTk.mainloop()
                    else:
                        print(f"Assistent: {resposta}")
                        saiSom(resposta)
                        resposta = "Desculpe, você não me mandou fazer nada"
                except:
                    pass
        if sair:
            break
            

countUp = 0
CheckBoxThread = ""

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        uic.loadUi("jan.ui", self)

        threadCheck = Thread(target=self.CheckBox)
        threadCheck.start()

        self.Next.clicked.connect(self.ButtonNext)
        self.Register.clicked.connect(self.ButtonRegister)
        self.Back.clicked.connect(self.ButtonBack)
        self.Forgot.clicked.connect(self.ButtonForgot)


        self.show()

    def closeEvent(self, event):
        global CheckBoxThread
        CheckBoxThread = "Yes"

    def ButtonNext(self):
        UserNext = self.EntryUser.text()
        PasswordNext = self.EntryPass.text()
        DataBase.cursor.execute("""
        SELECT * FROM Login
        WHERE (User = ? and Password = ?)
        """, (UserNext, PasswordNext,))
        Verify = DataBase.cursor.fetchone()
        try:
            if UserNext in Verify and PasswordNext in Verify:
                print("Acesso confirmado...\n\n")
                Voz = self.Voice.isChecked()
                self.close()
                Assistent(UserNext, Verify[4], Voz)
        except:
            print("Erro! Verifique suas informações e tente novamente!")

    def ButtonRegister(self):
        global countUp
        if countUp % 2 == 0:
            self.Logo.move(5000, 5000)
            self.Voice.move(5000, 5000)
            self.Forgot.move(5000, 5000)
            self.Username.move(10, 70)
            self.EntryUser.move(30, 100)
            self.Password.move(10, 150)
            self.EntryPass.move(30, 180)
            self.Show.move(240, 180)
            self.Email.move(10, 220)
            self.EntryEmail.move(30, 250)
            self.City.move(10, 285)
            self.EntryCity.move(30, 320)
            self.LabelRegister.move(50, -10)
            self.Next.move(5000, 5000)
            self.Register.move(220, 390)
            self.Back.move(10, 390)
        elif countUp % 2 == 1:
            UserRegister = self.EntryUser.text()
            PassRegister = self.EntryPass.text()
            EmailRegister = self.EntryEmail.text()
            CityRegister = self.EntryCity.text()

            if UserRegister == "" or PassRegister == "" or EmailRegister == "" or CityRegister == "":
                print("Error! Fill in all fields!")
            else:
                DataBase.cursor.execute("""
                SELECT * FROM Login
                WHERE (User = ?)
                """, (UserRegister,))
                VerifyReplyUser = DataBase.cursor.fetchone()
                DataBase.cursor.execute("""
                SELECT * FROM Login
                WHERE (Email = ?)
                """, (EmailRegister,))
                VerifyReplyEmail = DataBase.cursor.fetchone()
                try:
                    if UserRegister in VerifyReplyUser:
                        print("User already registered!")
                except:
                    try:
                        if EmailRegister in VerifyReplyEmail:
                            print("Email already registered!")
                    except:
                        EmailSliced = EmailRegister.split("@")
                        try:
                            if EmailSliced[1] in config.listEmail:
                                code = ""
                                for c in range(0, 6):
                                    digit = random.randint(0, 9)
                                    code += str(digit)
                                    c += 1
                                
                                MensagemCode = f"Hello, we received a request to register for our program.\nIf it wasn't you, please ignore this email.\nBut if it was you, type the following code into the program.\nCode: {code}"

                                SendEmailThread = Thread(target=config.SendEmail, args=(EmailRegister, "Code Pass", MensagemCode))
                                SendEmailThread.start()

                                # Funções Da Nova Janela

                                def ButtonConfirmCode():
                                    NewCode = EntryCode.text()
                                    if NewCode == code:
                                        DataBase.cursor.execute("INSERT INTO Login (User, Password, Email, City) VALUES (?, ?, ?, ?)", (UserRegister, PassRegister, EmailRegister, CityRegister,))
                                        DataBase.conn.commit()
                                        NewWindow.close()
                                        self.LabelRegister.move(5000, 5000)
                                        self.City.move(5000, 5000)
                                        self.EntryCity.move(5000, 5000)
                                        self.Email.move(5000, 5000)
                                        self.EntryEmail.move(5000, 5000)
                                        self.Back.move(5000, 5000)
                                        self.Logo.move(80, 0)
                                        self.Username.move(10, 170)
                                        self.EntryUser.move(30, 200)
                                        self.Password.move(10, 260)
                                        self.EntryPass.move(30, 290)
                                        self.Show.move(240, 290)
                                        self.Voice.move(50, 340)
                                        self.Next.move(220, 390)
                                        self.Register.move(10, 390)
                                        self.Forgot.move(90, 400)

                                        global countUp
                                        countUp = 0
                                    else:
                                        print("Código incorreto...")

                                def ButtonBackCode():
                                    NewWindow.close()

                                # Criar Nova Janela
                                NewWindow = QtWidgets.QMainWindow(self)
                                NewWindow.resize(307, 166)

                                # Label "BackGround"
                                BackgroundLabel = QtWidgets.QLabel(NewWindow)
                                BackgroundLabel.setGeometry(QtCore.QRect(0, 0, 307, 166))
                                BackgroundLabel.setPixmap(QtGui.QPixmap('image/fundo.png'))
                                BackgroundLabel.setScaledContents(True)

                                # Label "Code:"
                                CodeLabel = QtWidgets.QLabel(NewWindow)
                                CodeLabel.setGeometry(QtCore.QRect(10, 10, 151, 31))
                                fontLabel = QtGui.QFont()
                                fontLabel.setFamily("Calibri")
                                fontLabel.setBold(True)
                                fontLabel.setItalic(True)
                                fontLabel.setPointSize(16)
                                fontLabel.setWeight(75)
                                CodeLabel.setFont(fontLabel)
                                CodeLabel.setText("Code:")
                                CodeLabel.setStyleSheet("background-color: none;")

                                # Entry or LineEdit
                                EntryCode = QtWidgets.QLineEdit(NewWindow)
                                EntryCode.setGeometry(QtCore.QRect(40, 50, 231, 31))
                                fontEntry = QtGui.QFont()
                                fontEntry.setFamily("Calibri")
                                fontEntry.setBold(True)
                                fontEntry.setItalic(False)
                                fontEntry.setPointSize(16)
                                fontEntry.setWeight(75)
                                EntryCode.setFont(fontEntry)
                                EntryCode.setStyleSheet("background-color: rgb(255, 255, 255); border-radius: 10px;")
                                EntryCode.setAlignment(QtCore.Qt.AlignCenter)

                                # PuchButton "Confirm"
                                ConfirmCode = QtWidgets.QPushButton(NewWindow)
                                ConfirmCode.setGeometry(QtCore.QRect(180, 120, 101, 31))
                                fontConfirm = QtGui.QFont()
                                fontConfirm.setFamily("Calibri")
                                fontConfirm.setBold(True)
                                fontConfirm.setItalic(False)
                                fontConfirm.setPointSize(13)
                                fontConfirm.setWeight(75)
                                ConfirmCode.setFont(fontConfirm)
                                ConfirmCode.setStyleSheet("background-color: rgb(0, 0, 255); color: rgb(255, 255, 255); border-radius: 10px;")
                                ConfirmCode.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                                ConfirmCode.setText("Confirm")
                                ConfirmCode.clicked.connect(ButtonConfirmCode)

                                # PushButton "Back"
                                BackCode = QtWidgets.QPushButton(NewWindow)
                                BackCode.setGeometry(QtCore.QRect(20, 120, 101, 31))
                                fontBack = QtGui.QFont()
                                fontBack.setFamily("Calibri")
                                fontBack.setBold(True)
                                fontBack.setItalic(False)
                                fontBack.setPointSize(13)
                                fontBack.setWeight(75)
                                BackCode.setFont(fontBack)
                                BackCode.setStyleSheet("background-color: rgb(0, 0, 255); color: rgb(255, 255, 255); border-radius: 10px;")
                                BackCode.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                                BackCode.setText("<-Back")
                                BackCode.clicked.connect(ButtonBackCode)

                                # Mostrar Nova Janela
                                NewWindow.show()

                        except:
                            print("Email invalid!")
            countUp += 1
        
        countUp += 1

    def ButtonBack(self):
        global countUp
        self.LabelRegister.move(5000, 5000)
        self.City.move(5000, 5000)
        self.EntryCity.move(5000, 5000)
        self.Email.move(5000, 5000)
        self.EntryEmail.move(5000, 5000)
        self.Back.move(5000, 5000)
        self.Logo.move(80, 0)
        self.Username.move(10, 170)
        self.EntryUser.move(30, 200)
        self.Password.move(10, 260)
        self.EntryPass.move(30, 290)
        self.Show.move(240, 290)
        self.Voice.move(50, 340)
        self.Next.move(220, 390)
        self.Register.move(10, 390)
        self.Forgot.move(90, 400)

        countUp = 0
    
    def ButtonForgot(self):
        def ButtonBackForgot():
            WindowForgot.close()

        def ButtonConfirmForgot():
            EmailForgot = EntryEmailForgot.text()
            DataBase.cursor.execute("""
            SELECT * FROM Login
            WHERE Email = ?
            """, (EmailForgot,))
            VerifyEmailForgot = DataBase.cursor.fetchone()
            try:
                if EmailForgot in VerifyEmailForgot:
                    MensagemForgot = f"Hello, we received a request that you forgot your password in our program.\nIf not, ignore this email.\nBut if it was you, here is your password.\nPassword: {VerifyEmailForgot[2]}"

                    SendEmailForgotThread = Thread(target=config.SendEmail, args=[EmailForgot,"Forgot Password" , MensagemForgot])
                    SendEmailForgotThread.start()
            except:
                print("Esse email não está cadastrado!")


        # Criar Nova Janela
        WindowForgot = QtWidgets.QMainWindow(self)
        WindowForgot.resize(307, 166)

        # Label "BackGround"
        BackgroundLabelForgot = QtWidgets.QLabel(WindowForgot)
        BackgroundLabelForgot.setGeometry(QtCore.QRect(0, 0, 307, 166))
        BackgroundLabelForgot.setPixmap(QtGui.QPixmap('image/fundo.png'))
        BackgroundLabelForgot.setScaledContents(True)

        # Label "Code:"
        ForgotLabel = QtWidgets.QLabel(WindowForgot)
        ForgotLabel.setGeometry(QtCore.QRect(10, 10, 151, 31))
        fontLabelForgot = QtGui.QFont()
        fontLabelForgot.setFamily("Calibri")
        fontLabelForgot.setBold(True)
        fontLabelForgot.setItalic(True)
        fontLabelForgot.setPointSize(16)
        fontLabelForgot.setWeight(75)
        ForgotLabel.setFont(fontLabelForgot)
        ForgotLabel.setText("E-mail:")
        ForgotLabel.setStyleSheet("background-color: none;")

        # Entry or LineEdit
        EntryEmailForgot = QtWidgets.QLineEdit(WindowForgot)
        EntryEmailForgot.setGeometry(QtCore.QRect(40, 50, 231, 31))
        fontEntryEmailForgot = QtGui.QFont()
        fontEntryEmailForgot.setFamily("Calibri")
        fontEntryEmailForgot.setBold(True)
        fontEntryEmailForgot.setItalic(False)
        fontEntryEmailForgot.setPointSize(16)
        fontEntryEmailForgot.setWeight(75)
        EntryEmailForgot.setFont(fontEntryEmailForgot)
        EntryEmailForgot.setStyleSheet("background-color: rgb(255, 255, 255); border-radius: 10px;")
        EntryEmailForgot.setAlignment(QtCore.Qt.AlignCenter)

        # PuchButton "Confirm"
        ConfirmForgot = QtWidgets.QPushButton(WindowForgot)
        ConfirmForgot.setGeometry(QtCore.QRect(180, 120, 101, 31))
        fontConfirmForgot = QtGui.QFont()
        fontConfirmForgot.setFamily("Calibri")
        fontConfirmForgot.setBold(True)
        fontConfirmForgot.setItalic(False)
        fontConfirmForgot.setPointSize(13)
        fontConfirmForgot.setWeight(75)
        ConfirmForgot.setFont(fontConfirmForgot)
        ConfirmForgot.setStyleSheet("background-color: rgb(0, 0, 255); color: rgb(255, 255, 255); border-radius: 10px;")
        ConfirmForgot.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        ConfirmForgot.setText("Confirm")
        ConfirmForgot.clicked.connect(ButtonConfirmForgot)

        # PushButton "Back"
        BackForgot = QtWidgets.QPushButton(WindowForgot)
        BackForgot.setGeometry(QtCore.QRect(20, 120, 101, 31))
        fontBackForgot = QtGui.QFont()
        fontBackForgot.setFamily("Calibri")
        fontBackForgot.setBold(True)
        fontBackForgot.setItalic(False)
        fontBackForgot.setPointSize(13)
        fontBackForgot.setWeight(75)
        BackForgot.setFont(fontBackForgot)
        BackForgot.setStyleSheet("background-color: rgb(0, 0, 255); color: rgb(255, 255, 255); border-radius: 10px;")
        BackForgot.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        BackForgot.setText("<-Back")
        BackForgot.clicked.connect(ButtonBackForgot)

        # Mostrar Nova Janela
        WindowForgot.show()
    
    def CheckBox(self):
        while True:
            global CheckBoxThread
            if CheckBoxThread == 'Yes':
                break
            if self.Show.isChecked():
                self.EntryPass.setEchoMode(QtWidgets.QLineEdit.Normal)
            else:
                self.EntryPass.setEchoMode(QtWidgets.QLineEdit.Password)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    WindowMain = Window()
    app.exec_()