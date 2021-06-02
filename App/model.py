"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


'''from typing_extensions import TypeVarTuple'''
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf
from DISClib.ADT.graph import gr
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as mp
import datetime
import time
import tracemalloc
import haversine as hs
import sys
sys.setrecursionlimit(15000)


"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newAnalyzer():
    analyzer={'connections':gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=14000,
                                              comparefunction=None),
                'countries':mp.newMap(numelements=480,maptype='PROBING'),
                'landing': mp.newMap(numelements=480,maptype='PROBING'),
                'vertices_paises':mp.newMap(numelements=480,maptype='PROBING')
                
                }
              
    return analyzer
# Funciones para agregar informacion al catalogo

def add_landing_point(analyzer,file):
    for line in file:
        key=str(line['landing_point_id'])
        value=mp.newMap(numelements=10,maptype='PROBING')
        mp.put(value,'name',line['name'])
        mp.put(value,'id',line['id'])
        mp.put(value,'latitude',line['latitude'])
        mp.put(value,'longitude',line['longitude'])
        mp.put(analyzer['landing'],key,value)
    

def add_country(analyzer,file):
    for line in file:
        key=line['CountryName']
        value=mp.newMap(numelements=20,maptype='PROBING')
        mp.put(value,'CapitalName',line['CapitalName'])
        mp.put(value,'CapitalLatitude',line['CapitalLatitude'])
        mp.put(value,'CapitalLongitude',line['CapitalLongitude'])
        mp.put(value,'CountryCode',line['CountryCode'])
        mp.put(value,'ContinentName',line['ContinentName'])
        mp.put(value,'Population',line['Population'])
        mp.put(value,'Internet users',line['Internet users'])
        mp.put(analyzer['countries'],str(key),value)
        gr.insertVertex(analyzer['connections'],(line['CapitalName'],'1'))
    
    

def create_graph(analyzer,file):
     for line in file:
        vertice_origen=(line['\ufefforigin'],line['cable_name'])
        vertice_destino=(line['destination'],line['cable_name'])
        gr.insertVertex(analyzer['connections'],vertice_origen)
        gr.insertVertex(analyzer['connections'],vertice_destino)
        gr.addEdge(analyzer['connections'],vertice_origen,vertice_destino,line['cable_length'])
        
     añadir_capitales(analyzer)
     vertices_por_paises(analyzer)
     conexion_lp(analyzer)

        
def vertices_por_paises(analyzer):
    vertices = gr.vertices(analyzer['connections'])
    for i in range(lt.size(vertices)):
        vertice=(lt.getElement(vertices,i))
        if mp.contains(analyzer['landing'],(vertice[0])) == True:
            lista_interna=me.getValue(mp.get(analyzer['landing'],(vertice[0])))
            pais=((me.getValue(mp.get(lista_interna,'name'))).split(', '))[-1]
            
            if mp.contains(analyzer['vertices_paises'],pais)==False:
                mp.put(analyzer['vertices_paises'],pais,lt.newList('ARRAYLIST'))
                
            if mp.contains(analyzer['vertices_paises'],pais)==True:
                lista=me.getValue(mp.get(analyzer['vertices_paises'],pais))
                lt.addLast(lista,vertice)
    

def conexion_lp(analyzer):
    paises=mp.keySet(analyzer['vertices_paises'])
    for i in range(lt.size(paises)):
        pais=lt.getElement(paises,i)
        lista_vertices=me.getValue(mp.get(analyzer['vertices_paises'],pais))
        for j in range(lt.size(lista_vertices)):
            vertice1=lt.getElement(lista_vertices,j)
            for h in range(lt.size(lista_vertices)):
                vertice2=lt.getElement(lista_vertices,h)
                if vertice1[0] == vertice2[0]:
                    gr.addEdge(analyzer['connections'],vertice1,vertice2,'0.1 km')


def añadir_capitales(analyzer):
    vertices = gr.vertices(analyzer['connections'])
    for i in range(lt.size(vertices)):
        vertice=(lt.getElement(vertices,i))
        if mp.contains(analyzer['landing'],(vertice[0])) == True:
            lista_interna=me.getValue(mp.get(analyzer['landing'],(vertice[0])))
            nombre_pais=((me.getValue(mp.get(lista_interna,'name'))).split(', '))[-1]
            
            lista_int=me.getValue(mp.get(analyzer['countries'],nombre_pais))
            nombre_capital=me.getValue(mp.get(lista_int,'CapitalName'))
            
            largo_cable = largo_cables(analyzer,vertice[0],nombre_pais)
            gr.addEdge(analyzer['connections'],vertice,(nombre_capital,'1'),largo_cable)



def añadir_capitales_aburridas(analyzer):
    pass





















        

def largo_cables(analyzer,vertice,pais):
    interna_vertice=me.getValue(mp.get(analyzer['landing'],vertice))
    interna_capital=me.getValue(mp.get(analyzer['countries'],pais))
    lat_vertice=float(me.getValue(mp.get(interna_vertice,'latitude')))
    lon_vertice=float(me.getValue(mp.get(interna_vertice,'longitude')))
    lat_capital=float(me.getValue(mp.get(interna_capital,'CapitalLatitude')))
    lon_capital=float(me.getValue(mp.get(interna_capital,'CapitalLongitude')))
    loc1=(lat_vertice,lon_vertice)
    loc2=(lat_capital,lon_capital)
    distancia=hs.haversine(loc1,loc2)
    return distancia





# Funciones de consulta






# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
