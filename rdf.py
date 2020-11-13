#!/home/shigueru/anaconda3/bin/python

import os
import sys
import getopt
import shutil

file_in = " "
carp = " "
ini = 1
fin = 1
pas = 1
cut = 1

try:
	opts, args = getopt.getopt(sys.argv[1:],"hi:o:s:e:p:c:",["help","input=","output=","start=","end=","pass=","cut="])
except:
	print("Error !!")
	sys.exit(2)

for opt, arg in opts:
	if opt in ("-h", "--help"):
		ayuda="""
rdf.py -i <input> -o <output> -s <start> -e <end> -p <pass> -c <cut>

opciones:

-h o --help : Proporciona ayuda de las opciones.

-i o --input : Indica el nombre del archivo producido por 
               LAMMPS en formato vector, conteniendo el RDF.

-o o --output : Indica el nombre de la carpeta donde guardar
                los archivos procesados. El programa produce
                un archivo por cada paso de tiempo, que se 
                encuentre dentro del rango especificado y con
                el paso de tiempo indicado.

-s o --start : Paso de tiempo inicial, o el paso de tiempo 
               donde se tenga interes.

-e o --end : Paso de tiempo final, o paso de tiempo donde se 
             desee que termine el procesamiento.

-p o --pass : Paso de tiempo usado por LAMMPS, o intervalo 
              deseado para el procesamiento.

-c o --cut : Indica corte, es decir si existen valores de RDF
             que no sean de interes, estos pueden ser ignorados
             durante el proceso.

=======> EJEMPLO:

Se tiene un archivo llamado rdf1.out con el siguiente contenido

# Time-averaged data for fix myfix
# TimeStep Number-of-rows
# Row c_rdf1[1] c_rdf1[2] c_rdf1[3]
1000 200                  <---- Paso de tiempo 1000
1 0.345 0.0 0.0           |
2 0.456 0.0 0.0           |
...                       | Contenido del RDF
199 0.45 0.56 0.567       |
200 0.02 0.56 0.674       |
2000 200                  <---- Paso de tiempo 2000
1 0.785 0.0 0.0
2 0.352 0.0 0.0
...
199 0.367 0.356 0.783
200 0.456 0.672 0.678
.
.
.
20000 200                 <---- Paso de tiempo 20000
1 0.345 0.0 0.0
2 0.785 0.0 0.0
...
199 0.567 0.345 0.456
200 0.345 0.678 0.123

El comando seria:

rdf.py -i rdf1.out -o rdf -s 1000 -e 20000 -p 1000 -c 2

donde:
      -i -> nos indica cual archivo vamos a leer para procesar.
      -o -> indicamos el nombre de la carpeta que contendra
            todos los archivos, que resultan del procesamiento.
            Esta carpeta es creada durante el proceso. 
            ¡No es necesario crearla previamente!
      -s -> indicamos a partir de que paso de tiempo empezar
            el procesamiento.
      -e -> indicamos hasta que paso de tiempo procesar.
      -p -> indicamos cual es el intervalo entre pasos.
      -c -> esto nos sive para ignorar datos del RDF, por 
            ejemplo, en nuestro ejemplo los primeros datos 
            contienen ceros, asi que podrian ignorarse.
"""

		print(ayuda)
		sys.exit()
	elif opt in ("-i", "--input"):
		file_in = arg	
	elif opt in ("-o", "--output"):
		carp = arg
	elif opt in ("-s", "--start"):
		ini = int(arg)
	elif opt in ("-e", "--end"):
		fin = int(arg)
	elif opt in ("-p", "--pass"):
		pas = int(arg)
	elif opt in ("-c", "--cut"):
		cut = int(arg)

data = open(file_in,"r")

g = os.getcwd()


tempo = g + "/" + carp + "/" + "temp/"
perm = g + "/" + carp + "/" + "rdf/"

if os.path.exists(tempo):
	shutil.rmtree(tempo)
if os.path.exists(perm):
	shutil.rmtree(perm)
if os.path.exists(g+"/"+carp+"/"):
	shutil.rmtree(g+"/"+carp+"/")

os.mkdir(g+"/"+carp+"/")
os.mkdir(tempo)

linea = data.readlines()

rango = range(ini,fin+pas,pas)

ar = open("no_valido.txt","w")
ar.write("BORRAR: NO TIENE CONTENIDO NI IMPORTANCIA")

for j, line in enumerate(linea):
	if j > 2:
		spl = line.split()
		it = int(spl[0])
		if it in rango:
			if float(spl[1]) < 200.0:
				ar.write(line)
			else:
				ar.close()
				ar = open(tempo+spl[0]+".txt","w")
		else:
			ar.write(line)

ar.close()
data.close()

os.mkdir(perm)

ar2 = open("no_vale.txt","w")
ar2.write("BORRAR: NO TIENE CONTENIDO NI IMPORTANCIA")

for h in rango:
	arc = open(tempo+str(h)+".txt","r")
	lin = arc.readlines()
	ar2.close()
	ar2 = open(perm+str(h)+".txt","w")
	for t, li in enumerate(lin):
		if t > cut:
			ar2.write(li)
		else:
			continue
	arc.close()

shutil.rmtree(tempo)
