#!/home/shigueru/anaconda3/bin/python

import sys
import getopt
import math

file_core = " "
file_ring = " "
file_out = " "
radio = 1.0

try:
	opts, args = getopt.getopt(sys.argv[1:],"hd:c:r:o:",["help","dis=","core=","ring=","output="])
except:
	print("Error en las opciones o argumentos")
	print("h:help r=<radio> c:<core> s:<shell> o:<output>")
	sys.exit(2)

for opt, arg in opts:
	if opt in ("-h", "--help"):
		ayuda="""
anillo.py -r <radio> c <core> s <shell> -o <output>

opciones:

-h o --help    : Proporciona ayuda sobre las opciones.

-d o --dis   : Radio desde el centro del core hasta 
                 el shell, en las unidades usadas en los
                 archivos. (ver dibujo)
                                         
                           |#############|  
                       |==|               |==|
                      |==|     _______     |==|
                     |==|     /     / \     |==|
                    |==|     /     / x \   y |==| 
                   |==|     |     o     |-----|==|
                    |==|     \         /     |==| 
                     |==|     \_______/     |==|
                      |==|                 |==|
                       |==|               |==| 
                           |#############|
                           
                 el radio debe ser "R" siendo este:
                                 R = x + y
                    donde:
                          y : es la separacion entre el 
                              core y el shell.
                          x : radio del core

-c o --core    : Archivo conteniendo las coordenadas
                 cartesianas X Y Z del core esferico.

-r o --ring   : Archivo conteniendo las coordenadas 
                 cartesianas X Y Z del anillo a ser
                 usado.

-o o --output  : Archivo de salida donde guardar el sistema
                 ensamblado.
"""

		print(ayuda)
		sys.exit()
	elif opt in ("-d", "--dis"):
		radio = float(arg)
	elif opt in ("-c", "--core"):
		file_core = arg
	elif opt in ("-r", "--ring"):
		file_ring = arg
	elif opt in ("-o", "--output"):
		file_out = arg

data_core = open(file_core,"r")
data_ring = open(file_ring,"r")
salida = open(file_out,"w")

# centro de masa del core
xm_c = 0.0
ym_c = 0.0
zm_c = 0.0
c_c = 0.0 # contador
#centro de masa del ring
xm_r = 0.0
ym_r = 0.0
zm_r = 0.0
c_r = 0.0 #contador

lines_c = data_core.readlines()
lines_r = data_ring.readlines()

#calculo centro de masa core
for j, line_c in enumerate(lines_c):
	if j > 1:
		spl = line_c.split()
		xm_c = xm_c + float(spl[1])
		ym_c = ym_c + float(spl[2])
		zm_c = zm_c + float(spl[3])
		c_c = c_c + 1.0
	else:
		continue

xm_c = xm_c/c_c
ym_c = ym_c/c_c
zm_c = zm_c/c_c

#calculo centro de masa ring
for k, line_r in enumerate(lines_r):
	if k > 1:
		spl = line_r.split()
		xm_r = xm_r + float(spl[1])
		ym_r = ym_r + float(spl[2])
		zm_r = zm_r + float(spl[3])
		c_r = c_r + 1.0
	else:
		continue

xm_r = xm_r/c_r
ym_r = ym_r/c_r
zm_r = zm_r/c_r

salida.write(str(int(c_c + c_r)))
salida.write("\n")
salida.write("#Ensamblado con anillo.py \n")

for j, line_c in enumerate(lines_c):
	if j > 1:
		spl = line_c.split()
		salida.write(spl[0])
		salida.write(" ")
		x_c = str(float(spl[1]) - xm_c)
		y_c = str(float(spl[2]) - ym_c)
		z_c = str(float(spl[3]) - zm_c)
		salida.write(x_c+" ")
		salida.write(y_c+" ")
		salida.write(z_c+"\n")
	else:
		continue

for k, line_r in enumerate(lines_r):
	if k > 1:
		spl = line_r.split()
		salida.write(spl[0])
		salida.write(" ")
		x_r = str(float(spl[1]) - xm_r)
		y_r = str(float(spl[2]) - ym_r)
		z_r = str(float(spl[3]) - zm_r + radio)
		salida.write(x_r+" ")
		salida.write(y_r+" ")
		salida.write(z_r+"\n")
	else:
		continue

print("Ensamblado exitoso!!")

data_core.close()
data_ring.close()
salida.close()
