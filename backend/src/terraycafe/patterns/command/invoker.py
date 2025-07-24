# Classe que invoca os comandos
from terraycafe.patterns.command.command_base import Command


class Invoker():
    def __init__(self):
        self.historico = []

    async def executar(self, comando: Command):
        resultado = await comando.executar()
        self.historico.append(comando)
        return resultado
    