from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from pprint import pprint
from typing import List, Optional
from random import choice
from time import sleep
import textwrap


class Agente:
    def __init__(self, nombre: str, profesion: str, alineacion: str = "izquierda") -> None:
        self.nombre = nombre
        self.profesion = profesion
        self.rol = None
        self.instr = []
        self.alineacion = alineacion  # Alineación del texto
        self.llm = ChatOpenAI(model="gpt-4")  # Modelo LLM para obtener argumentos

    def agente_dice(self, mensaje: str) -> None:
        """Muestra el mensaje del agente formateado según su alineación."""
        if self.alineacion == "izquierda":
            texto_formateado = textwrap.fill(mensaje, width=60)
            print(f"[{self.nombre}]:\n{texto_formateado}\n")
        elif self.alineacion == "derecha":
            texto_formateado = textwrap.fill(mensaje, width=60)
            texto_alineado = "\n".join(line.rjust(60) for line in texto_formateado.split("\n"))
            print(f"[{self.nombre}]:\n{texto_alineado}\n")

    def notificacion(self, mensaje: str) -> None:
        """Muestra mensajes del sistema."""
        print(f"[SYSTEM]: {mensaje}")

    def asignar_rol(self, rol: str, instrucciones: List[str]) -> None:
        self.rol = rol
        self.instr = instrucciones
        self.notificacion(f"Rol asignado a {self.nombre}: {self.rol}")

    def generar_argumento(self, tema: str, posicion: str, ultimo_argumento: Optional[str] = None) -> str:
        """Genera un argumento para el agente con base en el tema y la posición."""
        prompt = [
            SystemMessage(content=" ".join(self.instr)),
            HumanMessage(content=f"El tema es: {tema}. Responde en 2 o 3 frases máximo."),
            HumanMessage(content=f"Tienes la posición: {posicion}."),
        ]
        if ultimo_argumento:
            prompt.append(AIMessage(content=f"El último argumento fue: {ultimo_argumento}"))

        # Aquí se llama al modelo de lenguaje usando invoke
        respuesta = self.llm.invoke(prompt).content.strip()
        return respuesta


class AI_Debate:
    def __init__(self, agente1: Agente, agente2: Agente) -> None:
        self.agente1 = agente1
        self.agente2 = agente2
        self.tema = "No definido"
        self.historial = []
        self.turno = choice([agente1, agente2])  # Elegir un agente inicial al azar
        self.posiciones = {}  # Diccionario para almacenar las posiciones de los agentes

    def seleccionar_tema(self, tema: str) -> None:
        self.tema = tema
        print(f"\nTema seleccionado: {self.tema}\n")

    def iniciar_debate(self) -> None:
        print("\nBienvenidos al debate entre:")
        print(f"{self.agente1.nombre} / {self.agente1.profesion}")
        print(f"y {self.agente2.nombre} / {self.agente2.profesion}")
        print(f"El tema a debatir será: {self.tema}\n")

    def establecer_posiciones(self) -> None:
        """Establece las posiciones iniciales de los agentes."""
        posicion_inicial = self.turno.generar_argumento(self.tema, "elige libremente")
        self.posiciones[self.turno] = posicion_inicial
        self.turno.agente_dice(f"Mi posición es: {posicion_inicial}")

        # Cambiar turno para que el segundo agente adopte la posición contraria
        self.cambiar_turno()
        posicion_contraria = f"Estoy en contra de: {posicion_inicial}"
        self.posiciones[self.turno] = posicion_contraria
        self.turno.agente_dice(f"Mi posición es: {posicion_contraria}")

    def turno_actual(self) -> None:
        posicion = self.posiciones[self.turno]
        argumento = self.turno.generar_argumento(
            self.tema, posicion, ultimo_argumento=self.obt_ult_argumento()
        )
        self.turno.agente_dice(argumento)
        self.historial.append({"nombre": self.turno.nombre, "mensaje": argumento})
        self.cambiar_turno()
        sleep(8)  # Espera de 5 segundos entre turnos

    def cambiar_turno(self) -> None:
        self.turno = self.agente1 if self.turno == self.agente2 else self.agente2

    def obt_ult_argumento(self) -> Optional[str]:
        return self.historial[-1]["mensaje"] if self.historial else None

    def iniciar_turnos(self, turnos: int) -> None:
        for _ in range(turnos):
            self.turno_actual()


def main():
    print("Comienza el debate...")
    agente1 = Agente("Lic. Luisa Tyson", "Licenciada en Sociología", alineacion="izquierda")
    agente2 = Agente("Dr. Pedro Subido", "Médico especialista en ética médica", alineacion="derecha")

    debate = AI_Debate(agente1, agente2)

    debate.seleccionar_tema("Debatiremos sobre EL ABORTO. ¿Estás a favor o en contra?")
    print("-" * 40)
    debate.iniciar_debate()
    print("-" * 40)

    rol1 = "Socióloga experta"
    instr1 = [
        "Eres una mujer apasionada, peleona, que le gusta la confrontación.",
        "Debes dar argumentos lógicos, concretos y precisos, sin divagar.",
        "Usa lenguaje coloquial. Sé breve y concisa.",
    ]
    agente1.asignar_rol(rol1, instr1)

    rol2 = "Médico especialista en ética médica"
    instr2 = [
        "Eres un hombre calmado, calculador, sereno, sabio, que evita la confrontación.",
        "Debes usar lenguaje casi inentendible tipo Cantinflas",
        "Usa un lenguaje técnico pero mantén las respuestas breves.",
    ]
    agente2.asignar_rol(rol2, instr2)

    debate.establecer_posiciones()
    debate.iniciar_turnos(5)
    print("-" * 40)
    print("El debate ha concluido. ¡Gracias por su participación!\n")


main()
