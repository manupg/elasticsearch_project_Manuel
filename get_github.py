import requests
import json
import time
from pprint import pprint

#PRIMERA CARGA
#Cargamos las tres paginas de eventos (100 cada una)
datos1= requests.get('https://api.github.com/events?per_page=100&page=1',auth=('manupg', 'volvagia9'))
datos2= requests.get('https://api.github.com/events?per_page=100&page=2',auth=('manupg', 'volvagia9'))
datos3= requests.get('https://api.github.com/events?per_page=100&page=3',auth=('manupg', 'volvagia9'))
#Guardamos el ETAG de la primera, asi como el ID del primer evento de la primera pagina. Esto nos evitara cargar eventos repetimos
jsona=datos1.json()
id_evento=jsona[0]["id"]

for i in range(3):	
	if i == 0:
		datos=datos1

	elif i == 1:
		datos=datos2

	elif i == 2:
		datos=datos3

	jsona= datos.json()
	fichero=open("github.json","a")
	##print(len(jsona))
	#print(datos.headers['etag']) 
	#print jsona[1]["id"]

	for i in range(len(jsona)):
		fichero.write(json.dumps(jsona[i]))
		fichero.write("\n")

	fichero.close()

#CARGAS SIGUIENTES
time.sleep(10)
while True:
##comienzo bucle
	datos1= requests.get('https://api.github.com/events?per_page=100&page=1',auth=('manupg', 'volvagia9'))
	datos2= requests.get('https://api.github.com/events?per_page=100&page=2',auth=('manupg', 'volvagia9'))
	datos3= requests.get('https://api.github.com/events?per_page=100&page=3',auth=('manupg', 'volvagia9'))
	quit=False
	for i in range(3):	
		if i == 0:
			datos=datos1
			print("PROCESAMOS LA PAGINA 1")
		elif i == 1:
			datos=datos2
			print("PROCESAMOS LA PAGINA 2")
		elif i == 2:
			datos=datos3
			print("PROCESAMOS LA PAGINA 3")
		jsona= datos.json()
		fichero=open("github.json","a")
		for i in range(len(jsona)):
			if jsona[i]["id"] != id_evento:
				fichero.write(json.dumps(jsona[i]))
				fichero.write("\n")
			else:
				print("EVENTO REPETIDO, NO SE GUARDA A PARTIR DE AQUI: " + jsona[i]["id"] +"=" + id_evento  )
				quit=True
				break
		fichero.close()
		print ("Eventos cargados de esta pagina ==> "+ str(i+1) + "\n")
		print ("Eventos repetidos de esta pagina ==> "+ str(99-i) + "\n")
			
		if quit==True:
			break
##ahora guardamos el primer evento de la nueva primera pagina, ya que hasta ese evento, todos han sido cargados.
	jsona=datos1.json()
	id_evento=jsona[0]["id"]
	fichero=open("ultimo_id.txt","w")
	fichero.write(id_evento)
	fichero.close()
	##time.sleep(10)
##fin bucle
