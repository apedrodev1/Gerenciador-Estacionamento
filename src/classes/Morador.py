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

    def __init__(self, id=None, nome="", placa="", cnh="", modelo="", cor="", apartamento="", vaga_id=None):
        # Chama o construtor do Pai (Veiculo) para lidar com a parte "comum"
        super().__init__(id, nome, placa, cnh, modelo, cor)
        

        self.apartamento = apartamento
        self.vaga_id = vaga_id


    # --- Apartamento (Novo) ---
    @property
    def apartamento(self):
        return self._apartamento

    @apartamento.setter
    def apartamento(self, valor):
        val, erro = validate_apartamento(valor)
        if erro:
            raise ValueError(f"Erro no Apartamento: {erro}")
        self._apartamento = val

    
    @property
    def vaga_id(self):
        return self._vaga_id
    
    @vaga_id.setter
    def vaga_id(self, valor):
        # Simples validação para garantir que é inteiro ou None
        if valor is None:
            self._vaga_id = None
        else:
            try:
                self._vaga_id = int(valor)
            except ValueError:
                raise ValueError("O ID da vaga deve ser um número inteiro.")


    def to_dict(self):
        """Sobrescreve to_dict para incluir a vaga."""
        data = super().to_dict() # Pega os dados do pai
        data['apartamento'] = self.apartamento
        data['vaga_id'] = self.vaga_id

        return data