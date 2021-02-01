import argparse
import os
import time

start = time.time()
macrodata=[]
pila=0

def find_between( s, first, last, inicio=0 ):
    try:
        start = s.index(first, inicio) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""

def c_bin_divide_conquer(num, cat, inicio, final):
	"""funcion bin"""
	try:
		mitad = (final+inicio)//2
		if final - inicio == 1 :
			if (final==num or inicio==num):
				return num
			else:
				return "0"
		if num == int(cat[mitad]):
			return num
		elif num < int(cat[mitad]):
			return c_bin_divide_conquer(num, cat, inicio, mitad)
		else:
			return c_bin_divide_conquer(num, cat, mitad, final)
	except ValueError:
		return""

def b_alertados(a, cat):
	"""verifica que no se hayan alertado durante la semana"""
	try:
		for l in  range(0,len(cat)):
			if int(a) == int(cat[l]):
				return str(a) + " - Ya Alertado"
		return str(a)
	except ValueError:
		return""

def blanca(a, b, cat):
	"""verifica la lista blanca"""
	try:
		if str(a) in cat:
			if cat[a] == b:
				return str(a) + " - Lista Blanca "
			return str(a) + " - Lista solo usuario"
		return str(a)
	except ValueError:
		return""

def imprmir_bines():
	"""imprimir bines"""
	try:
		for i in range(0,(len(archivomacro)-1)/3):
			id = i*3
			for j in range(0,2):
				print str(macrodata[i][j])
			#print ""
	except ValueError:
		return""

parser = argparse.ArgumentParser(description='Ingresa el nombre del archivo xml')
parser.add_argument('xml', type=str, help='Nombre del archivo de entrada (en xml)')
parser.add_argument('-a', '--alertados', help='Da el nombre del archivo de bines alertados (default = bines_alertados.txt)', default='bines_alertados.txt')
parser.add_argument('-c', '--catalogo', help='Da el nombre del archivo "catalogo de bines", txt con todos los bines (default = catalogo.txt)', default='catalogo.txt')
parser.add_argument('-l', '--lista', help='Da el nombre del archivo de lista blanca, separado por comas sin espacios los equipos (default = lista_blanca2.txt)', default='lista_blanca2.txt')
parser.add_argument('-o', '--output', help='Da el nombre del archivo de salida (default = Alerta5.txt)', default='Alerta5.txt')
args = parser.parse_args()

with open(args.xml, 'r') as f:
	archivomacro = f.readlines()
	#Elimina el salto de linea en cada elemento de la lista
	archivomacro = [x.strip('\n') for x in archivomacro]
f.close()

with open(args.catalogo, 'r') as f:
	catalogo = f.readlines()
	#Elimina el salto de linea en cada elemento de la lista
	catalogo = [x.strip('\n') for x in catalogo]
f.close()

with open(args.lista, 'r') as f:
	lista = f.readlines()
	#Elimina el salto de linea en cada elemento de la lista
	lista = [x.strip('\n').split(":") for x in lista]
f.close()
lista[12].append(lista[12].pop(1).split(","))
lista[24].append(lista[24].pop(1).split(","))
lista = dict(lista)

if os.stat(args.alertados).st_size != 0:
	with open(args.alertados, 'r') as f:
		alertados = f.readlines()
		#Elimina el salto de linea en cada elemento de la lista
		alertados = [x.strip('\n') for x in alertados]
	f.close()

#------------------------------------------------------------------------------------------------------------------------------
for i in range((len(archivomacro)-1)/3):
	id = i*3
	num_temp = int(find_between(archivomacro[id],"<ns3:matchCount>","</ns3:matchCount>"))+4
	macrodata.append([0]*num_temp)
#
	macrodata[i][0] = find_between(archivomacro[id],"<ns3:incidentId>","</ns3:incidentId>")
	if os.stat(args.alertados).st_size != 0:
		macrodata[i][0] = b_alertados(macrodata[i][0], alertados)
	macrodata[i][1] = find_between(archivomacro[id],"<ns3:matchCount>","</ns3:matchCount>")
	macrodata[i][2] = find_between(archivomacro[id+3],"<ns3:userName>","</ns3:userName>")
	macrodata[i][3] = find_between(archivomacro[id+3],"<ns3:machineName>","</ns3:machineName>")
	macrodata[i][3] = macrodata[i][3].replace('LAP-', '').replace('DT-', '').replace('PC-', '')
	macrodata[i][2] = blanca(macrodata[i][2], macrodata[i][3], lista)
	if '- Lista Blanca' in macrodata[i][2]:
		macrodata[i][0] = macrodata[i][0] + '- Lista Blanca'
	if 'usuario' in macrodata[i][2]:
		macrodata[i][0] = macrodata[i][0] + '- Lista blanca solo usuario'

	for j in range(int(find_between(archivomacro[id],"<ns3:matchCount>","</ns3:matchCount>"))):
		final = (j*83)+archivomacro[id].index("<ns2:violationText>")
		macrodata[i][j+4] = find_between(archivomacro[id],"<ns2:violationText>","</ns2:violationText>",final).replace('-', '').replace(' ', '')
#------------------------------------------------------------------------------------------------------------------------------
o=0
with open(args.output, 'w') as outf:
	with open('detalle.txt', 'w') as detall:
		for i in range(0,(len(archivomacro)-1)/3):
			id = i*3
			pila = 0
			for j in range(0,int(find_between(archivomacro[id],"<ns3:matchCount>","</ns3:matchCount>"))+4):
				if j > 3:
					flag = 0
					if '- Ya Alertado' in macrodata[i][0] or '- Lista Blanca' in macrodata[i][2]:
						"""alertado anteriormente en la semana"""
					else:
						if len(macrodata[i][j]) == 15 or len(macrodata[i][j]) == 16:
							flag = c_bin_divide_conquer(int(macrodata[i][j][:6]),catalogo,0,len(catalogo))
							if flag != "0":
								detall.write(macrodata[i][j] + '\n')
								pila = pila + 1
			macrodata[i][1] = macrodata[i][1] + " - " + str(pila)
			if pila != 0:
				outf.write(macrodata[i][0].replace("- Lista blanca solo usuario", '') + '\n')
				macrodata[i][0] = macrodata[i][0] + " - Alertar"
				detall.write(macrodata[i][0] + '\n' + macrodata[i][1] + '\n')
			else:
				macrodata[i][0] = macrodata[i][0] + " - NO"
	detall.close()
outf.close()

imprmir_bines()
end = time.time()
print (end - start)
