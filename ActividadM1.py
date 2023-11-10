#Este programa crea un sistema de multiagentes los cuales limpian celdas sucias
#Autoras:
#Abigail Donají Chavez Rubio A01747423
#Noh Ah Kim Kwon A01747512
#Fecha de creación: 09/11/2023

from typing import Any
from mesa import Agent, Model
from mesa.space import MultiGrid #Permite varios agentes en celdas
from mesa.time import SimultaneousActivation #Agentes se activan de manera simultanea

#Regresa la cantidad de pasos por agente
def graficas(model):
    pasos = [agent.pasos for agent in model.schedule.agents] 
    return pasos

#Clase que implemente al agente, recibe el modelo y unique id
#Su valor varia entre 1 y 0, 1 significa que es un agente limpiador y 0 significa que la celda está sucia
class Agente_Limpiador(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.valor = None
        self.pasos = 0

    # Mueve el agente de manera aleatoria
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        self.pasos += 1

    # Revisa la celda en la que se movió, si está sucia (valor = 0) entonces la limpia (valor = 2) y se suman las celdas limpiadas
    def step(self):
        x, y = self.pos
        valor_celda = self.model.grid.get_cell_list_contents((x,y))
        if len(valor_celda) > 1:
            for ag in valor_celda:
                if ag != self:  # Verificar si el agente actual no es el agente que estamos revisando
                    if ag.valor == 0:
                        ag.valor = 2
                        self.model.celdas_limpiadas += 1
                        self.move()
        self.move()

#Clase que implementa el modelo, este recibe el número de agentes, alto, ancho, porcentaje de celdas sucias y el tiempo máximo de ejecución
class LimpiadorModel(Model):
    def __init__(self, num_agentes, width, height, porcentaje, tiempo_max):
        self.celdas_sucias = int((width * height * porcentaje) / 100)
        self.total = width * height
        self.tiempo_max = tiempo_max
        self.num_agents = num_agentes
        self.grid = MultiGrid(width, height, False)
        self.schedule = SimultaneousActivation(self)
        self.running = True
        self.contador = 0
        self.celdas_limpiadas = (width * height) - self.celdas_sucias

        
        #Se inicializan celdas sucias de manera aleatoria considerando el porcentaje de celdas sucias 
        for _ in range(self.celdas_sucias):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            newPos = (x,y)
            while self.grid.is_cell_empty(newPos) == False:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                newPos = (x,y)
            a = Agente_Limpiador(newPos, self)
            a.valor = 0
            self.grid.place_agent(a, newPos)

        #Se inicializan los agentes limpiadores en la posición (1,1)
        for i in range(self.num_agents):
            b = Agente_Limpiador(i,self)
            if self.grid.is_cell_empty(newPos) == False:
                self.grid.place_agent(b, (1,1))
            b.valor = 1
            self.schedule.add(b)

    #Mueve a los agentes y para la simulación cuando se pasa el tiempo especificado
    # Por alguna razón hace 2 pasos de más     
    def step(self):

        if self.contador < self.tiempo_max and (self.celdas_limpiadas != self.total):
            self.schedule.step()
            self.contador += 1
        else:
            self.running = False
            print("Total de agentes: " + str(self.num_agents) +
                  "\nTiempo: " + str(self.contador) +
                  "\nCeldas limpiadas: " + str((self.celdas_limpiadas * 100)/ self.total) + "%"
                  "\nMovimientos realizados por cada agente: " + str(graficas(self)) +
                  "\nMovimiento total: " + str(sum(graficas(self)))
                  )
            

            
        
        