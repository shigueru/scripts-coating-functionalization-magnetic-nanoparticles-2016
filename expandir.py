#!/home/shigueru/anaconda3/bin/python

import sys 
import getopt
import math

input_file = " "
output_file = " "
radio = 0.0

try:
    opts, args = getopt.getopt(sys.argv[1:],"hr:i:o:",["help","radio=","input=","output="])
except getopt.GetoptError:
    print("Error en las opciones o argumentos")
    print("h:help r:<radio> i:<input file> o:<output file>")
    sys.exit(2)

for opt, arg in opts:
    if opt in ("-h", "--help"):
        ayuda = """
expandir.py -r <radio> -i <input_file> -o <output_file>

opciones:

-h o --help   : Proporciona ayuda sobre las opciones.

-r o --radio  : radio de separacion entre las capas.
                Se debe indicar la medida en las unidades
                en el archivo original de coordenadas.

-i o --input  : Archivo de entrada con las coordenadas 
                originales.

-o o --output : Archivo de salida donde guardas las 
                nuevas coordenadas.
"""
        print(ayuda)
        sys.exit()
    elif opt in ("-r", "--radio"):
        radio = float(arg)
    elif opt in ("-i", "--input"):
        input_file = arg
    elif opt in ("-o", "--output"):
        output_file = arg
#print("radio input output",radio,input_file,output_file)

data = open(input_file,"r")
salida = open(output_file,"w")

xm = 0.0
ym = 0.0
zm = 0.0
c = 0.0

lineas = data.readlines()

# calculo centro de masa

for j, line in enumerate(lineas):
    if j > 1:
        spl = line.split()
        xm = xm + float(spl[1])
        ym = ym + float(spl[2])
        zm = zm + float(spl[3])
        c = c + 1.0
    else:
        salida.write(line)

xm = xm/c
ym = ym/c
zm = zm/c

print("centro de masa: ", xm, ym, zm)

for j, line in enumerate(lineas):
	if j > 1:
		spl = line.split()
		if spl[0] == "C":
			x = float(spl[1]) - xm
			y = float(spl[2]) - ym
			z = float(spl[3]) - zm

			mod = math.sqrt((0 - x)**2 + (0 -y)**2 + (0 -z)**2)
			
			x = 0 + (radio * (x/mod))
			y = 0 + (radio * (y/mod))
			z = 0 + (radio * (z/mod))

			l = [spl[0],str(x),str(y),str(z)]

			salida.write(str(" ".join(l)))
			salida.write("\n")
		else:
			salida.write(spl[0])
			salida.write(" ")
			x = str(float(spl[1]) - xm)
			y = str(float(spl[2]) - ym)
			z = str(float(spl[3]) - zm)
			salida.write(x+" ")
			salida.write(y+" ")
			salida.write(z+"\n")
	else:
		continue
