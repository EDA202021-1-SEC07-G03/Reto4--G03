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
 """

import config as cf
import model
import csv
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as mp
import datetime
import time
import tracemalloc


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo
def init():
    analyzer = model.newAnalyzer()
    return analyzer
# Funciones para la carga de datos
def loadData(analyzer, filename, filename2,filename3):
    filename = cf.data_dir + filename
    input_file = csv.DictReader(open(filename, encoding="utf-8"),delimiter=",")
    
    filename2 = cf.data_dir + filename2
    input_file2 = csv.DictReader(open(filename2, encoding="utf-8"),delimiter=",")
    filename3 = cf.data_dir + filename3
    input_file3 = csv.DictReader(open(filename3, encoding="utf-8"),delimiter=",")
    
    landing_points=model.add_landing_point(analyzer,input_file2)
    countries=model.add_country(analyzer,input_file3)
    connection=model.create_graph(analyzer,input_file)
    

    return analyzer


# Funciones de ordenamiento



# Funciones de consulta sobre el catálogo
def clusteres(analyzer,lp1,lp2):
    return model.clusteres(analyzer,lp1,lp2)

def landing_principales(analyzer):
    return model.landing_principales(analyzer)

def ruta_minima(analyzer,pais1,pais2):
    return model.ruta_minima(analyzer,pais1,pais2)

def infraestructura_critica(analyzer):
    return model.infraestructura_critica(analyzer)

def impacto_fallo(analyzer,lp):
    return model.impacto_fallo(analyzer,lp)

def ancho_banda(analyzer,pais,cable):
    return model.ancho_banda(analyzer,pais,cable)