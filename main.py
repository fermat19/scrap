import requests
from bs4 import BeautifulSoup
import pandas as pd

clt = requests.Session()
html = clt.get('https://citas.css.gob.pa/admin/index.php').content
soup = BeautifulSoup(html, 'html.parser')

login_info = {
	'correo': 'ferncastillo',
	'clave': 'Admin123',
	'commit': 'ENTRAR'
}

auth = clt.post('https://citas.css.gob.pa/admin/autenticacion.php', data=login_info)
scrap = clt.get('https://citas.css.gob.pa/admin/agenda_confirma.php').content
spu = BeautifulSoup(scrap, 'html.parser')

strTotalRows = str(spu.find('font', attrs={"size":"+1"}).text)
strTotalPages = str(spu.find('div', class_='text-marroncito').text)

strTotalP = strTotalPages.replace(" ", "")
totalPagesby = strTotalP.replace("\n", " ")
tpStart = totalPagesby.index("/")+1
tpEnd = len(totalPagesby)
totalPages = int(totalPagesby[tpStart:tpEnd])

trStart = strTotalRows.index("(")+1
trEnd = strTotalRows.index(")")
totalRows = int(strTotalRows[trStart:trEnd])

header = ["#Control", "CITA PARA", "UNIDAD EJECUTORA", "CONFIRMAR"]
data = []
for i in range(totalPages):
	# i = 0
	urlScrap = f"https://citas.css.gob.pa/admin/agenda_confirma.php?pageNum_Rs={i}&totalRows_Rs={totalRows}"
	htmlStr = clt.get(urlScrap).content
	htmlParsed = BeautifulSoup(htmlStr, 'html.parser')

	table0 = htmlParsed.find('table')
	table1 = table0.find('tr')
	table2 = table1.select_one('table tr:nth-of-type(3)')
	table3 = table2.find('table')
	
	for tr in table3:
		if tr != '\n':
			row = []
			for td in tr:
				if td.find('font'):
					if td.find('font') != -1:
						texto = td.find('font').text
						if texto not in header:
							row.append(texto.replace(',', ' '))
			data.append(row)

df = pd.DataFrame(data)
df.to_csv('data/data1.csv')
print(df.head())
print(f'Se han registrado {totalRows} registros')
print(df.shape)
