# Classe que invoca os comandos
from backend.src.terraycafe.patterns.command.command_base import Command


class Invoker():
    def __init__(self):
        self.historico = []

    def executar(self, comando: Command):
        resultado = comando.executar()
        self.historico.append(comando)
        return resultado
