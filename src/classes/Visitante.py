"""
Contém a classe Visitante, que herda de Veiculo.
"""

from datetime import datetime
from src.classes.Veiculo import Veiculo

class Visitante(Veiculo):
    """
    Representa um visitante.
    
    Além dos dados do veículo, armazena o momento da entrada para controle.
    """

    def __init__(self, id=None, nome="", placa="", cnh="", modelo="", cor="", entrada=None, numero_vaga=None):
        super().__init__(id, nome, placa, cnh, modelo, cor)
        
        # Se nenhuma data for passada, assume-se "agora" (momento da criação do objeto)
        self._entrada = entrada if entrada else datetime.now()
        self.numero_vaga = numero_vaga

    @property
    def entrada(self):
        return self._entrada
    
    # Geralmente não alteramos a data de entrada manualmente, 
    # mas podemos adicionar um setter se necessário no futuro.

    def to_dict(self):
        data = super().to_dict()
        data['entrada'] = self.entrada.isoformat() 
        data['numero_vaga'] = self.numero_vaga
        return data