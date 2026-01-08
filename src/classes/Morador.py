"""
Contém a classe Morador, que herda de Veiculo.
"""
from src.utils.validations import validate_apartamento
from src.classes.Veiculo import Veiculo

class Morador(Veiculo):
    """
    Representa um morador do condomínio.
    
    Herda todos os atributos de veículo e adiciona a Vaga vinculada e Apartamento.
    """

    def __init__(self, id=None, nome="", placa="", cnh="", modelo="", cor="", apartamento="", vaga_id=None, estacionado=False):
        # Chama o construtor do Pai (Veiculo) para lidar com a parte "comum"
        super().__init__(id, nome, placa, cnh, modelo, cor)
        
        self.apartamento = apartamento
        self.vaga_id = vaga_id
        self.estacionado = estacionado

    # --- Apartamento ---
    @property
    def apartamento(self):
        return self._apartamento

    @apartamento.setter
    def apartamento(self, valor):
        val, erro = validate_apartamento(valor)
        if erro:
            raise ValueError(f"Erro no Apartamento: {erro}")
        self._apartamento = val

    # --- Vaga (Agora aceita TEXTO para lógica "10-1") ---
    @property
    def vaga_id(self):
        return self._vaga_id
    
    @vaga_id.setter
    def vaga_id(self, valor):
        # Se for vazio ou None, fica None
        if valor is None or valor == "":
            self._vaga_id = None
        else:
            # Aceita string e converte para maiúsculo (ex: "10-1")
            self._vaga_id = str(valor).strip().upper()

    def to_dict(self):
        """Sobrescreve to_dict para incluir apartamento e vaga."""
        data = super().to_dict() # Pega os dados do pai
        data['apartamento'] = self.apartamento
        data['vaga_id'] = self.vaga_id
        data['estacionado'] = self.estacionado
        return data