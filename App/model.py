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

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newAnalyzer():
    analyzer={'connections':gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=NotImplemented),
                'countries':mp.newMap(numelements=480,maptype='PROBING'),
                'landing': mp.newMap(numelements=480,maptype='PROBING')
                }
              
    return analyzer
# Funciones para agregar informacion al catalogo

def add_landing_point(analyzer,file):
    for line in file:
        interno= mp.newMap(numelements=4,maptype='PROBING')
        mp.put(interno,'id',line['id'])
        mp.put(interno,'name',line['name'])
        mp.put(interno,'latitude',line['latitude'])
        mp.put(interno,'longitude',line['longitude'])

        key=line['landing_point_id']
        mp.put(analyzer['landing'],str(key),interno)


def add_country(analyzer,file):
    pass

def create_graph(analyzer,file):
     for line in file:
        print(line['\ufefforigin'])
        if gr.containsVertex(analyzer['connections'],line['\ufefforigin']) != True:
            gr.insertVertex(analyzer['connections'],line['\ufefforigin'])

        if gr.containsVertex(analyzer['connections'],line['destination']) != True:
                gr.insertVertex(analyzer['connections'],line['destination'])

        if gr.containsVertex(analyzer['connections'],line['destination']) == True and gr.containsVertex(analyzer['connections'],line['origin']) == True:
            gr.addEdge(analyzer['connections'],line['\ufefforigin'],line['destination'],line['cable_length'])

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
