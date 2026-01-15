"""
Representa o cadastro permanente de um visitante frequente.
Herda de Veiculo para reaproveitar nome, placa, cnh, modelo e cor.
"""
from datetime import datetime
from src.classes.Veiculo import Veiculo

class VisitanteCadastro(Veiculo):
    def __init__(self, id=None, nome="", placa="", cnh="", modelo="", cor="", data_cadastro=None):
        # Repassa os dados comuns para a classe pai (Veiculo)
        super().__init__(id, nome, placa, cnh, modelo, cor)
        
        # Adiciona apenas o campo específico deste contexto
        self.data_cadastro = data_cadastro if data_cadastro else datetime.now().isoformat()

    def __repr__(self):
        return f"Cadastro Frequente({self.nome} - {self.placa})"