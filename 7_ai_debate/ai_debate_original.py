from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from pprint import pprint
from typing import List, Union, Optional
from random import random

class Agente:
    def __init__(self, nombre: str, profesion: str) -> None:
        self.nombre = nombre
        self.profesion = profesion
        self.instr = ['Cada agente o participante del debate debe hacerlo de forma respetuosa con los demas',
                      'Cada agente debe respetar que los demás contrincantes den completamente su opinión sin interrumpirlo y procurando leer la totalidad de cada argumento',
                      'El debate debe ser constructivo siempre, con el fin de llegar acuerdos y conclusiones que puedan eventualmente llegar al mayor consenso posible']
        
    def agente_dice(self, mensaje) -> None:
        pprint(f'[{self.nombre}]: {mensaje}')

    def notificacion(self, mensaje) -> None:
        pprint(f'[SYSTEM]: {mensaje}')
        
    def asignar_rol(self, rol) -> None:
        self.notificacion(f'Asignado rol a agente: {self.nombre}...')

    def asignar_instrucciones(self) -> None:
        self.notificacion(f'Asignado instrucciones a agente: {self.nombre}...')
    
        
class Rol:
    def __init__(self, titulo: str, instrucciones: str = '') -> None:
        self.titulo = titulo
        self.instrucciones = instrucciones

class AI_Debate:
    def __init__(self, agente1, agente2) -> None:
        self.agente1 = agente1
        self.agente2 = agente2
        self.instr_generales = ['Cada agente o participante del debate debe hacerlo de forma respetuosa con los demas',
                                'Cada agente debe respetar que los demás contrincantes den completamente su opinión sin interrumpirlo y procurando leer la totalidad de cada argumento',
                                'El debate debe ser constructivo siempre, con el fin de llegar acuerdos y conclusiones que puedan eventualmente llegar al mayor consenso posible']

        self.historial = []

    def seleccionar_tema(self, tema='Nada. Vamos a hablar sobre la nada') -> Optional[str]:
        pprint('Escogiendo tema...')
        self.tema = tema

    def iniciar_debate(self) -> None:
        pprint(f'Bienvenidos al debate entre nuestros invitados de lujo que tenemos para hoy:')
        pprint(f'{self.agente1.nombre} / {self.agente1.profesion} y...')
        pprint(f'{self.agente2.nombre} / {self.agente2.profesion}')
        pprint(f'El tema que estaremos debatiendo será: {self.tema}')

    def display_chat(self) -> None:
        pprint(f'Actualizando display de conversacion...')

    def obt_ult_argumento(self) -> Optional[str]:
        # Simplified return logic
        return self.historial[-1].content if self.historial else None

        rol1  = 'Socióloga experta'
        rol2  = 'Médico especialista en ética médica'
        instr1 = ['Eres una mujer apasionada, peleona, que le gusta la confrontacion',
                 'Debes dar argumentos logicos, concretos y precisos, sin divagar',
                 'Te gusta usar un lenguaje coloquial, sin tecnicismos',
                 'Reconoces una buena argumentacion y eres capaz de revisar tus postulados',
                 f'En este debate asumiras una posicion con respecto al {self.tema} y la debatiras con tu contrincante'
        ]
        instr2 = ['Eres una hombre calmado, calculador, sereno, sabio, que evita la confrontacion',
                 'Debes dar argumentos logicos, concretos y precisos, sin divagar',
                 'Te gusta usar un lenguaje rebuscado, lleno de jerga tecnica, te gusta impresionar con el lenguaje',
                 'Consideras que eres superior a los demas y te cuesta aceptar posiciones divergentes a la tuya',
                 f'En este debate asumiras una posicion con respecto al {self.tema} y la debatiras con tu contrincante'
        ]        
        agente1.asignar_rol('Eres un: {rol1}', intr1)
        agente2.asignar_rol('Eres un: {rol2}', intr2)
        
        
def main():
    print('Comienza el debate...')
    agente1 = Agente('Lic. Luisa Tyson', 'Licencia en Sociologia')
    agente2 = Agente('Dr. Pedro Subido', 'Medico especialista en medicina etica')
    
    debate = AI_Debate(agente1, agente2)
    debate.seleccionar_tema('Debatiremos sobre EL ABORTO. Estas a favor o en contra?')
    pprint('-'*40)
    debate.iniciar_debate()
    pprint('-'*40)
    pprint('Ha concluido el debate. Gracias por su participacion')
    
main()