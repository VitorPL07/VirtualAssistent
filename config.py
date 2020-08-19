import NiverData
import datetime
import requests as rq
import webbrowser as web
import os
from youtube_search import YoutubeSearch
import smtplib

listEmail = [
    "gmail.com",
    "yahoo.com",
    "hotmail.com",
    "outlook.com",
    "live.com"
]

listaErros = [
	"Não entendi nada",
	"Desculpe, não entendi",
	"Repita novamente por favor"
]

listaSair = [
	"já pode hibernar",
	"ok obrigado",
	"ok, obrigado",
	"está dispensada"
]

version = 1.0

def Intro():
    msg = f"Assistente - Version {version} / Criador: VitorPL"
    print("~" * len(msg) +  f"\n{msg}\n"  +   "~" * len(msg))


def Calculadora(entrada):
	if "mais" in entrada or "+" in entrada:
		entradas_recebidas = entrada.split(" ")
		resultado = int(entradas_recebidas[0]) + int(entradas_recebidas[2])
	elif "menos" in entrada or "-" in entrada:
		entradas_recebidas = entrada.split(" ")
		resultado = int(entradas_recebidas[0]) - int(entradas_recebidas[2])
	elif "vezes" in entrada or "x" in entrada:
		entradas_recebidas = entrada.split(" ")
		resultado = round(float(entradas_recebidas[0]) * float(entradas_recebidas[2]), 2)
	elif "dividido por" in entrada:
		entradas_recebidas = entrada.split(" ")
		resultado = round(float(entradas_recebidas[0]) / float(entradas_recebidas[3]), 2)
	elif "/" in entrada:
		entradas_recebidas = entrada.split(" ")
		resultado = round(float(entradas_recebidas[0]) / float(entradas_recebidas[2]), 2)
	else:
		resultado = "Operação não encontrada"

	return resultado


def ClimaTempo(cidade):	
	endereco_api = "http://api.openweathermap.org/data/2.5/weather?appid=9e1280f88eef9db700e867bb898fd3ec&q="
	url = endereco_api + cidade

	infos = rq.get(url).json()

	# Coord
	longitude = infos['coord']['lon']
	latitude = infos['coord']['lat']
	# main
	temp = infos['main']['temp'] - 273.15 # Kelvin para Celsius
	pressao = infos['main']['pressure'] / 1013.25 #Libras para ATM
	humidade = infos['main']['humidity'] # Recebe em porcentagem
	temp_max= infos['main']['temp_max'] - 273.15 # Kelvin para Celsius
	temp_min = infos['main']['temp_min'] - 273.15 # Kelvin para Celsius

	#vento
	v_speed = infos['wind']['speed'] # km/ h
	v_direc = infos['wind']['deg'] #Recebe em graus

	#clouds / nuvens
	nebulosidade = infos['clouds']['all']

	#id
	id_da_cidade = infos['id']

	return [longitude, latitude, 
		temp, pressao, humidade, 
		temp_max, temp_min, v_speed, 
		v_direc, nebulosidade, id_da_cidade]


def Abrir(fala):
	try:
		if "google" in fala:
			web.open("https://www.google.com.br/")
			return "Abrindo Google"
		elif "facebook" in fala:
			web.open("https://pt-br.facebook.com/")
			return "Abrindo Facebook"
		elif "instagram" in fala:
			web.open("https://www.instagram.com/?hl=pt-br")
			return "Abrindo Instagram"
		elif "twitter" in fala:
			web.open("https://twitter.com/")
			return "Abrindo Twitter"
		elif "reddit" in fala:
			web.open("https://www.reddit.com/")
			return "Abrindo Reddit"
		elif "whatsapp" in fala:
			web.open("https://web.whatsapp.com/")
			return "Abrindo WhatsApp"
		elif "youtube" in fala:
			web.open("https://www.youtube.com/?hl=pt&gl=BR")
			return "Abrindo Youtube"
		elif "bloco de notas" in fala:
			os.system("notepad")
			return "Abrindo bloco de notas"
		else:
			return "Ainda não sei abrir isso."
	except:
		return "Houve um erro"

def Tocar(msc):
	msc = msc + "Clipe Oficial Música -filme"
	results = YoutubeSearch(msc, max_results=1).to_dict()
	for c in results:
		you = 'https://www.youtube.com'
		tube = c['link']
		youtube = (you + tube)
		web.open(youtube)
	return "Tocando {}".format(c['title'])


def Pesquisa(link):
	url_inicial = "https://www.google.com/search?q="
	purl = (url_inicial + link)
	web.open(purl)
	return f"abrindo {link}"


def NiverDataVerify(UserAtual):
    data = datetime.date.today().strftime('%d/%m')
    NiverData.cursor.execute("""
    SELECT * FROM Aniversario
    WHERE Data = ?
    """, (data,))
    VerifyData = NiverData.cursor.fetchone()
    try:
        if data in VerifyData:
            if data in VerifyData:
                web.open("https://www.youtube.com/watch?v=6FhNsxb0C-k")
                return f"Parabéns {UserAtual}"
            else:
                return f"{VerifyData[1]} está de aniversário hoje"

    except:
        return "Ninguém está completando ano hoje."

def SendEmail(From, Title, Message):
	try:
		smtpObj = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		smtpObj.ehlo()
		msgTo = 'yui.virtualassistent@gmail.com'
		toPass = 'yvzd hmkj aapo bjhj'
		smtpObj.login(msgTo, toPass)
		smtpObj.sendmail(msgTo, From, 'Subject: {}\n{}'.format(Title, Message))
		smtpObj.quit()
		print("Email enviado com sucesso")
	except:
		print("Erro ao enviar o email...")

def AdicionarData(Name, diaNiver, mesNiver):
	if mesNiver == "janeiro":
		mesNiver = "01"
	elif mesNiver == "fevereiro":
		mesNiver = "02"
	elif mesNiver == "março":
		mesNiver = "03"
	elif mesNiver == "abril":
		mesNiver = "04"
	elif mesNiver == "maio":
		mesNiver = "05"
	elif mesNiver == "junho":
		mesNiver = "06"
	elif mesNiver == "julho":
		mesNiver = "07"
	elif mesNiver == "agosto":
		mesNiver = "08"
	elif mesNiver == "setembro":
		mesNiver = "09"
	elif mesNiver == "outubro":
		mesNiver = "10"
	elif mesNiver == "novembro":
		mesNiver = "11"
	elif mesNiver == "dezembro":
		mesNiver = "12"

	try:
		data = diaNiver + "/" + mesNiver
		NiverData.cursor.execute("""
		INSERT INTO Aniversario (Nome, Data) VALUES (?, ?)
		""", (Name, data,))
		NiverData.conn.commit()
		return "Data adicionada com sucesso!"
	except:
		return "Não foi possivel adicionar a data"
