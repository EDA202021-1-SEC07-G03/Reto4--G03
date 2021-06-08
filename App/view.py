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
def getTime():
    return float(time.perf_counter()*1000)
def getMemory():
    return tracemalloc.take_snapshot()
def deltaMemory(start_memory, stop_memory):
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    delta_memory = delta_memory/1024.0
    return delta_memory

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
    print("8- Ancho de banda")
   


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
        tracemalloc.start()
        start_time = getTime()
        start_memory = getMemory()
        #***************************************
        cont = controller.init()
        #**************************************
        stop_memory = getMemory()
        stop_time = getTime()
        tracemalloc.stop()
        delta_time = round(stop_time - start_time,2)
        delta_memory = round(deltaMemory(start_memory, stop_memory),2)
        print("Tiempo [ms]:",delta_time)
        print("Memoria [kB]:",delta_memory,)
        print('-'*80)
    elif int(inputs[0]) == 2:
        #------------------------------------------------
        tracemalloc.start()
        start_time = getTime()
        start_memory = getMemory()
        #***************************************
        analyzer=controller.loadData(cont,filename,filename2,filename3)
        #**************************************
        stop_memory = getMemory()
        stop_time = getTime()
        tracemalloc.stop()
        delta_time = round(stop_time - start_time,2)
        delta_memory = round(deltaMemory(start_memory, stop_memory),2)
        #-------------------------------------------------
        print("El numero de landing points es de: "+ str(gr.numVertices(analyzer['connections'])))
        print("El total de conexiones entre landing points es de: "+ str((gr.numEdges(analyzer['connections']))))
        print("El total de paises es de: " + str(mp.size(analyzer['countries'])))
        interno=me.getValue(mp.get(analyzer['landing'],'3316'))
        nombre=me.getValue(mp.get(interno,'name'))
        longitud=me.getValue(mp.get(interno,'longitude'))
        latitud=me.getValue(mp.get(interno,'latitude'))
        print('El primer landing point cargado es: codigo: 3316  nombre: ' + nombre + '  longitud: ' + longitud + '  latitud: ' + latitud )
        pais=lt.getElement(mp.keySet(analyzer['countries']),-1)
        interno2=me.getValue(mp.get(analyzer['countries'],pais))
        poblacion=me.getValue(mp.get(interno2,'Population'))
        usuarios=me.getValue(mp.get(interno2,'Internet users'))
        print('El último país cargado es ' + pais + ' con una población de ' + poblacion + ' y ' + usuarios + ' usuarios de internet.')
        print("Tiempo [ms]:",delta_time)
        print("Memoria [kB]:",delta_memory,)
        print('-'*80)
    
    elif int(inputs[0]) == 3:
        #Requerimiento 1
        tracemalloc.start()
        start_time = getTime()
        start_memory = getMemory()
        #***************************************
        lp1=str(input('Ingrese el landing point 1: '))
        lp2=str(input('Ingrese el landing point 2: '))
        clusteres=controller.clusteres(analyzer,lp1,lp2)
        #**************************************
        stop_memory = getMemory()
        stop_time = getTime()
        tracemalloc.stop()
        delta_time = round(stop_time - start_time,2)
        delta_memory = round(deltaMemory(start_memory, stop_memory),2)
        print('La cantidad de clusteres en el grafo es de: ' + str(clusteres[0]))
        print('El landing point ' + lp1 + ' y el landing point ' + lp2 + ' estan en el mismo cluster: '+str(clusteres[1]))
        print("Tiempo [ms]:",delta_time)
        print("Memoria [kB]:",delta_memory,)
        print('-'*80)

    elif int(inputs[0]) == 4:
        #Requerimiento 2
        tracemalloc.start()
        start_time = getTime()
        start_memory = getMemory()
        #***************************************
        lp=controller.landing_principales(analyzer)
        #**************************************
        stop_memory = getMemory()
        stop_time = getTime()
        tracemalloc.stop()
        delta_time = round(stop_time - start_time,2)
        delta_memory = round(deltaMemory(start_memory, stop_memory),2)
        print('El landing point que sirve de interconexión a más cables en la red es '+ str(lp[0])+ ' con ' +str(lp[1])+' conexiones')
        print("Tiempo [ms]:",delta_time)
        print("Memoria [kB]:",delta_memory,)
        print('-'*80)
        
    elif int(inputs[0]) == 5:
        #Requerimiento 3
        tracemalloc.start()
        start_time = getTime()
        start_memory = getMemory()
        #***************************************
        pais1=input('Ingrese el pais origen: ')
        pais2=input('Ingrese el pais destino: ')
        ruta=controller.ruta_minima(analyzer,pais1,pais2)
        #**************************************
        stop_memory = getMemory()
        stop_time = getTime()
        tracemalloc.stop()
        delta_time = round(stop_time - start_time,2)
        delta_memory = round(deltaMemory(start_memory, stop_memory),2)
        print('El camino entre los paises es: ')
        for i in range(1,lt.size(ruta[0])+1):
            print(str(i+1)+'.  Vertice 1: ' +str(lt.getElement(ruta[0],i)['vertexA'])+ ' Vertice 2: ' + str(lt.getElement(ruta[0],i)['vertexB'])+ ' Distancia: '+ str(lt.getElement(ruta[0],i)['weight'])+ ' km')
        print('El camino es de '+str(ruta[1])+' km  de largo.')
        print("Tiempo [ms]:",delta_time)
        print("Memoria [kB]:",delta_memory,)
        print('-'*80)

    elif int(inputs[0]) == 6:
        #Requerimiento 4
        tracemalloc.start()
        start_time = getTime()
        start_memory = getMemory()
        #***************************************
        infraestructura=controller.infraestructura_critica(analyzer)
        #**************************************
        stop_memory = getMemory()
        stop_time = getTime()
        tracemalloc.stop()
        delta_time = round(stop_time - start_time,2)
        delta_memory = round(deltaMemory(start_memory, stop_memory),2)
        print('El numero de nodos conectados a la red de expansión mínima es de: '+ str(infraestructura[0]))
        print('El largo total de la red de expansión mínima es de: '+ str(infraestructura[1])+' km')
        print("Tiempo [ms]:",delta_time)
        print("Memoria [kB]:",delta_memory,)
        print('-'*80)

    elif int(inputs[0]) == 7:
        #Requerimiento 5
        tracemalloc.start()
        start_time = getTime()
        start_memory = getMemory()
        #***************************************
        lp=input('Introduzca el vertice que falla: ')
        impacto=controller.impacto_fallo(analyzer,lp)
        #**************************************
        stop_memory = getMemory()
        stop_time = getTime()
        tracemalloc.stop()
        delta_time = round(stop_time - start_time,2)
        delta_memory = round(deltaMemory(start_memory, stop_memory),2)    
        
        for i in range(1,lt.size(impacto[0])+1):
            tupla=lt.getElement(impacto[0],i)
            print('Pais: ' + tupla[0] + ' ||   Distancia: ' + str(tupla[1])+ 'km')
        print('El numero de paises afectados es de: ' + str(impacto[1]))
        print("Tiempo [ms]:",delta_time)
        print("Memoria [kB]:",delta_memory,)
        print('-'*80)
    
    elif int(inputs[0]) == 8:
        #Requerimiento 6
        tracemalloc.start()
        pais=input('Ingrese el pais de su interés: ')
        cable=input('Ingrese el cable de su interés: ')
        start_time = getTime()
        start_memory = getMemory()
        #***************************************
        ancho=controller.ancho_banda(analyzer,pais,cable)
        #**************************************
        stop_memory = getMemory()
        stop_time = getTime()
        tracemalloc.stop()
        delta_time = round(stop_time - start_time,2)
        delta_memory = round(deltaMemory(start_memory, stop_memory),2)
        print('El ancho de banda en '+ pais + ' con el cable ' + cable+ ' desde: ')
        for i in range(1,lt.size(ancho)+1):
            pais=lt.getElement(ancho,i)
            print(pais[0]+' es de: '+str(pais[1])+' mbps')
        print("Tiempo [ms]:",delta_time)
        print("Memoria [kB]:",delta_memory,)
        print('-'*80)
        
    else:
        sys.exit(0)
sys.exit(0)
