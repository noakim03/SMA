#Visualizador del modelo 
#Autoras:
#Abigail Donají Chavez Rubio A01747423
#Noh Ah Kim Kwon A01747512
#Fecha de creación: 09/11/2023

from ActividadM1 import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

#Muestra el drid y losagentes de forma circular y con diferente color de acuerdo a su valor
def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 0.5}

    if agent.valor == 1: 
        portrayal["Color"] = "red" #agente
        portrayal["Layer"] = 0
    elif agent.valor == 2: 
        portrayal["Color"] = "gray" #limpio
        portrayal["Layer"] = 0
    else:
        portrayal["Color"] = "blue" #sucio
        portrayal["Layer"] = 0 

    return portrayal

num_agentes = 30
ancho = 40
alto = 40
porcentaje = 50
tiempo_max = 50
grid = CanvasGrid(agent_portrayal, ancho, alto, 750, 750)
server = ModularServer(LimpiadorModel,
                       [grid],
                       "Cleaning Model",
                       {"num_agentes":num_agentes,"width":ancho, "height":alto,"porcentaje":porcentaje, "tiempo_max":tiempo_max})

server.port = 8521 # The default
server.launch()
