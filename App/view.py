"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
from DISClib.ADT import list as lt
from DISClib.ADT.graph import gr
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as mp
import datetime
import time
import tracemalloc

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Inicializar catálogo")
    print("2- Cargar información en el catálogo ")
    print("3- Identificar clusteres de información ")
    print("4- Identificar puntos de conexión críticos ")
    print("5- Ruta de menor distancia ")
    print("6- Identificar infraestructura crítica ")
    print("7- Análisis de fallas ")
   


catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        #------------------------------------------------
        filename='connections.csv'
        filename2='landing_points.csv'
        filename3='countries.csv'
        '''tracemalloc.start()
        start_time = getTime()
        start_memory = getMemory()'''
        #***************************************
        cont = controller.init()
        #**************************************
        '''stop_memory = getMemory()
        stop_time = getTime()
        tracemalloc.stop()
        delta_time = round(stop_time - start_time,2)
        delta_memory = round(deltaMemory(start_memory, stop_memory),2)
        print("Tiempo [ms]:",delta_time)
        print("Memoria [kB]:",delta_memory,)
        print('-'*80)'''
    elif int(inputs[0]) == 2:
        #------------------------------------------------
        '''tracemalloc.start()
        start_time = getTime()
        start_memory = getMemory()'''
        #***************************************
        analyzer=controller.loadData(cont,filename,filename2,filename3)
        #**************************************
        '''stop_memory = getMemory()
        stop_time = getTime()
        tracemalloc.stop()
        delta_time = round(stop_time - start_time,2)
        delta_memory = round(deltaMemory(start_memory, stop_memory),2)'''
        #-------------------------------------------------
        print("El numero de landing points es de: "+ str(gr.numVertices(analyzer['connections'])))
        print("El total de conexiones entre landing points es de: "+ str((gr.numEdges(analyzer['connections']))))
        print("El total de paises es de: " + str(mp.size(analyzer['countries'])))
        print()
        


    
    elif int(inputs[0]) == 3:
        #Requerimeinto 1



        pass

    elif int(inputs[0]) == 4:
        #Requerimeinto 2



        pass

    elif int(inputs[0]) == 5:
        #Requerimeinto 3



        pass

    elif int(inputs[0]) == 6:
        #Requerimeinto 4



        pass

    elif int(inputs[0]) == 7:
        #Requerimeinto 5




        pass

    else:
        sys.exit(0)
sys.exit(0)
