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
from DISClib.Algorithms.Sorting import mergesort as mrg
assert cf
from DISClib.ADT.graph import gr
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import prim
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
                                              directed=True,
                                              size=14000,
                                              comparefunction=None),
                'countries':mp.newMap(numelements=480,maptype='PROBING'),
                'landing': mp.newMap(numelements=480,maptype='PROBING'),
                'vertices_paises':mp.newMap(numelements=480,maptype='PROBING'),
                'capital_pais':mp.newMap(numelements=480,maptype='PROBING'),
                'pais_capital':mp.newMap(numelements=480,maptype='PROBING'),
                'nombrelp_codigo':mp.newMap(numelements=480,maptype='PROBING'),
                'vertice_pais':mp.newMap(numelements=480,maptype='PROBING'),
                'cable_capacidad':mp.newMap(numelements=480,maptype='PROBING')
                
                
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
        usuarios=line['Internet users'].replace('.','')
        mp.put(value,'Internet users',usuarios)
        mp.put(analyzer['countries'],str(key),value)
        gr.insertVertex(analyzer['connections'],(line['CapitalName'],'1'))
        key2=line['CapitalName']
        value2=line['CountryName']
        mp.put(analyzer['capital_pais'],key2,value2)
        mp.put(analyzer['pais_capital'],value2,key2)
    
    

def create_graph(analyzer,file):
     for line in file:
        key=line['cable_name']
        value=line['capacityTBPS']
        mp.put(analyzer['cable_capacidad'],str(key),float(value))
        vertice_origen=(line['\ufefforigin'],line['cable_name'])
        vertice_destino=(line['destination'],line['cable_name'])
        if gr.containsVertex(analyzer['connections'],vertice_origen) == False:
            gr.insertVertex(analyzer['connections'],vertice_origen)
        if gr.containsVertex(analyzer['connections'],vertice_destino) == False:
            gr.insertVertex(analyzer['connections'],vertice_destino)
            
        distancia=(line['cable_length'].replace(' km','')).replace(',','')
        if distancia == 'n.a.':
            distancia=500
        else:
            distancia=float(distancia)
            
        gr.addEdge(analyzer['connections'],vertice_origen,vertice_destino,distancia)
        
     añadir_capitales(analyzer)
     vertices_por_paises(analyzer)
     nombre_codigo(analyzer)
     conexion_lp(analyzer)
     añadir_capitales_aburridas(analyzer)
     vertice_pais(analyzer)

        
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


def nombre_codigo(analyzer):
    vertices = gr.vertices(analyzer['connections'])
    for i in range(lt.size(vertices)):
        vertice=(lt.getElement(vertices,i))
        if mp.contains(analyzer['landing'],(vertice[0])) == True:
            lista_interna=me.getValue(mp.get(analyzer['landing'],(vertice[0])))
            nombre=((me.getValue(mp.get(lista_interna,'name'))).split(', '))[0]
            mp.put(analyzer['nombrelp_codigo'],nombre,vertice)
    
            
        

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
                    if gr.getEdge(analyzer['connections'],vertice1,vertice2)==None:
                        gr.addEdge(analyzer['connections'],vertice1,vertice2,0.1)
                        gr.addEdge(analyzer['connections'],vertice2,vertice1,0.1)


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
            gr.addEdge(analyzer['connections'],vertice,(nombre_capital,'1'),float(largo_cable))
            gr.addEdge(analyzer['connections'],(nombre_capital,'1'),vertice,float(largo_cable))



def añadir_capitales_aburridas(analyzer):
    vertices = gr.vertices(analyzer['connections'])
    
    for i in range(lt.size(vertices)):
        vertice=(lt.getElement(vertices,i))
        mas_corto=10000000
        vertice_mas_cercano=('a',1)
        if gr.degree(analyzer['connections'],vertice)==0 and len(vertice[0]) > 0 and vertice[1]=='1':
            for j in range(lt.size(vertices)):
                vertice2=(lt.getElement(vertices,j))
                if mp.contains(analyzer['landing'],(vertice2[0])) == True:
                    pais=me.getValue(mp.get(analyzer['capital_pais'],vertice[0]))
                    largo_cable = largo_cables(analyzer,vertice2[0],pais)
                    if largo_cable < mas_corto:
                        vertice_mas_cercano = vertice2
                        mas_corto=largo_cable
            gr.addEdge(analyzer['connections'],vertice_mas_cercano,vertice,float(mas_corto))
            gr.addEdge(analyzer['connections'],vertice,vertice_mas_cercano,float(mas_corto))

def vertice_pais(analyzer):
    vertices = gr.vertices(analyzer['connections'])
    for i in range(lt.size(vertices)):
        vertice=(lt.getElement(vertices,i))
        if mp.contains(analyzer['landing'],(vertice[0])) == True:
            lista_interna=me.getValue(mp.get(analyzer['landing'],(vertice[0])))
            pais=((me.getValue(mp.get(lista_interna,'name'))).split(', '))[-1]
            mp.put(analyzer['vertice_pais'],vertice,pais)
            


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

#---------------------------------------REQUERIMIENTO 1 ----------------------------------------
def clusteres(analyzer,lp1,lp2):
    cfc=scc.KosarajuSCC(analyzer['connections'])
    numero=scc.connectedComponents(cfc)
    vertice1=me.getValue(mp.get(analyzer['nombrelp_codigo'],lp1))
    vertice2=me.getValue(mp.get(analyzer['nombrelp_codigo'],lp2))
    conectados=scc.stronglyConnected(cfc,vertice1,vertice2)
    return(numero,conectados)


#---------------------------------------REQUERIMIENTO 2 ----------------------------------------
def landing_principales(analyzer):
    vertices = gr.vertices(analyzer['connections'])
    max=0
    lista=lt.newList('ARRAYLIST')
    
    for i in range(lt.size(vertices)):
        vertice=lt.getElement(vertices,i)
        grado=gr.degree(analyzer['connections'],vertice)
        
        if grado == max:
            lt.addLast(lista,vertice)

        if grado > max:
            max=grado
            lista=lt.newList('ARRAYLIST')
            lt.addFirst(lista,vertice)
    vermax=lt.getElement(lista,0)
 
    return vermax[0], max


#---------------------------------------REQUERIMIENTO 3 ----------------------------------------
def ruta_minima(analyzer,pais1,pais2):
    capital1=me.getValue(mp.get(analyzer['pais_capital'],pais1))
    capital2=me.getValue(mp.get(analyzer['pais_capital'],pais2))
    search=djk.Dijkstra(analyzer['connections'],(capital1,'1'))
    distancia_total=djk.distTo(search,(capital2,'1'))
    camino=djk.pathTo(search,(capital2,'1'))

    return camino,distancia_total

#---------------------------------------REQUERIMIENTO 4 ----------------------------------------

def infraestructura_critica(analyzer):
    mst=prim.PrimMST(analyzer['connections'])
    cantidad_nodos=(mst['marked']['size'])
    peso=prim.weightMST(analyzer['connections'],mst)
    
    return cantidad_nodos,peso

#---------------------------------------REQUERIMIENTO 5 ----------------------------------------

def impacto_fallo(analyzer,lp):
    vertices=gr.vertices(analyzer['connections'])
    codigolp=me.getValue(mp.get(analyzer['nombrelp_codigo'],lp))
    
    lista=lt.newList('ARRAYLIST')
    lista2=lt.newList('ARRAYLIST')
    for i in range(lt.size(vertices)):
        vertice=lt.getElement(vertices,i)
        if vertice[0]==codigolp[0]:
            lista_adyacentes=gr.adjacents(analyzer['connections'],vertice)
            for j in range(lt.size(lista_adyacentes)):
                ver=lt.getElement(lista_adyacentes,j)
                if mp.contains(analyzer['landing'],ver[0]) == True:
                    pais=me.getValue(mp.get(analyzer['vertice_pais'],ver))
                    
        
                    if lt.isPresent(lista,pais)==False:
                        lt.addLast(lista,pais)
                        distancia=gr.getEdge(analyzer['connections'],vertice,ver)['weight']
                        lt.addLast(lista2,(pais,float(distancia)))

    lista2=mrg.sort(lista2,cmp5)

    return lista2,lt.size(lista2)

#---------------------------------------REQUERIMIENTO 6 ----------------------------------------


def ancho_banda(analyzer,pais,cable):
    vertices=gr.vertices(analyzer['connections'])
    lista_paises=lt.newList('ARRAYLIST')
    lista_pais_nu=lt.newList('ARRAYLIST')
    lista_final=lt.newList('ARRAYLIST')
    capacidad =float(me.getValue(mp.get(analyzer['cable_capacidad'],cable)))
    for i in range(lt.size(vertices)):

        vertice=lt.getElement(vertices,i)
        if vertice[1]==cable:
            pais2=me.getValue(mp.get(analyzer['vertice_pais'],vertice))
            if pais2 != pais and lt.isPresent(lista_paises,pais2) == 0:
                
                interna=me.getValue(mp.get(analyzer['countries'],pais2))
                numero_usuarios=float(me.getValue(mp.get(interna,'Internet users')))
                x=(pais2,numero_usuarios)
                
                lt.addLast(lista_pais_nu,x)
                lt.addLast(lista_paises,pais2)
    
                

    for j in range(1,lt.size(lista_pais_nu)+1):
        tupla=lt.getElement(lista_pais_nu,j)
        
        ancho=(capacidad/tupla[1])*1000000
        valor=(tupla[0],ancho)
        if lt.isPresent(lista_final,valor)==0:
            
            lt.addFirst(lista_final,valor)


    return lista_final



# Funciones utilizadas para comparar elementos dentro de una lista

def cmp5(tupla1,tupla2):
    return(tupla1[1]>=tupla2[1])

# Funciones de ordenamiento
