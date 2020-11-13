#!/home/shigueru/anaconda3/bin/python

import sys
import getopt
import math

file_in = " "
file_ou = " "
ini = 1
fin = 1
pas = 1

try:
	opts, args = getopt.getopt(sys.argv[1:],"hi:o:s:e:p:",["help","input=","output=","start=","end=","pass="])
except:
	print("ERROR!!!")
	sys.exit(2)

for opt, arg in opts:
	if opt in ("-h","--help"):
		ayuda="""
msd.py -i <input_file> -o <output_file> s <start> e <end> -p <pass>

NOTA: El archivo a procesar debe estar escrito en formato de 
      "VECTOR" por LAMMPS.

opciones:

-h o --help   : Proporciona ayuda

-i o --input  : Archivo de entrada original del MSD obtenido de
                la simulacion.

-o o --output : Archivo donde van a ser escritos los registros
                del MSD ardenados con el siguiente formato:

                time_step msd[1] msd[2] msd[2]

-s o --start  : Paso de tiempo inicial registrado en el archivo
                MSD original.

-e o --end    : Paso final registrado en el archivo MSD 
                original.

-p o --pass   : Paso de tiempo usado para registrar el MSD 
                en el archivo original.

===> EJEMPLO:

Se tiene un archivo llamado "msd.out" escrito en modo vector,
con el siguiente contenido: 

# Time-average data for fix msd1
# Time Number-of-rows
# Row c_msd11
120 4      <--- paso de tiempo 120
1 0.02      |
2 0.98      | componentes del vector MSD 
3 0.00      |
4 0.78      |
240 4      <---  paso de tiempo 240
1 0.76
2 0.89
3 0.65
4 0.65
.
.
.
9960 4     <--- paso de tiempo 9960
1 0.78
2 0.65
3 0.66
4 0.88

Por lo que el comando a usar seria:

msd.py -i msd.ou -o msd.dat -s 120 -e 9960 -p 120

donde:
       -i -> indica el archivo msd.out como entrada a procesar.
       -o -> nombre del archivo donde guardar el resultado.
       -s -> paso inicial de tiempo 120
       -e -> paso final de tiempo 9960
       -p -> paso de tiempo o cada cuanto se produjo un
             registro de datos: 120
"""
		print(ayuda)
		sys.exit()
	elif opt in ("-i", "--input"):
		file_in = arg
	elif opt in ("-o", "--output"):
		file_ou = arg
	elif opt in ("-s", "start"):
		ini = int(arg)
	elif opt in ("-e", "--end"):
		fin = int(arg)
	elif opt in ("-p", "--pass"):
		pas = int(arg)

data = open(file_in,"r")
salida = open(file_ou,"w")

linea = data.readlines()

rango = range(ini,fin+pas,pas)

lista = ["#TimeStep","c_msd[1]","c_msd[2]","c_msd[3]"]

for j, line in enumerate(linea):
	if j > 2:
		spl = line.split()
		it = int(spl[0])
		if it in rango:
			salida.write(str(" ".join(lista)))
			salida.write("\n")
			lista.clear()
			lista.append(spl[0])
		else:
			lista.append(spl[1])
	else:
		continue

salida.write(str(" ".join(lista)))

data.close()
salida.close()
