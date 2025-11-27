"""
Contém a classe base Veiculo.

Esta classe serve como pai para Morador e Visitante, centralizando
os dados comuns de qualquer veículo/motorista (Placa, CNH, Modelo, etc.).
"""

from src.utils.validations import validate_placa, validate_cnh, validate_names

class Veiculo:
    """
    Classe base para todos os veículos (Moradores e Visitantes).
    
    Attributes:
        _id (int): ID do banco de dados (pode ser None se ainda não salvo).
        _nome (str): Nome do proprietário/motorista.
        _placa (str): Placa do veículo.
        _cnh (str): CNH do motorista.
        _modelo (str): Modelo do carro (ex: "Fiat Uno").
        _cor (str): Cor do carro.
    """

    def __init__(self, id=None, nome="", placa="", cnh="", modelo="", cor=""):
        """
        Inicializa os dados básicos do veículo.
        """
        self._id = id
        
        # Setters validarão os dados imediatamente
        self.nome = nome
        self.placa = placa
        self.cnh = cnh
        self.modelo = modelo
        self.cor = cor

    # --- ID (Somente Leitura, gerenciado pelo DB) ---
    @property
    def id(self):
        return self._id

    # --- Nome (Validado) ---
    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        val, erro = validate_names(valor)
        if erro:
            raise ValueError(f"Nome inválido: {erro}")
        self._nome = val

    # --- Placa (Validada) ---
    @property
    def placa(self):
        return self._placa

    @placa.setter
    def placa(self, valor):
        val, erro = validate_placa(valor) 
        if erro:
            raise ValueError(f"Placa inválida: {erro}")
        self._placa = val

    # --- CNH (Validada) ---
    @property
    def cnh(self):
        return self._cnh

    @cnh.setter
    def cnh(self, valor):
        # Assumindo que criaremos validate_cnh
        val, erro = validate_cnh(valor)
        if erro:
            raise ValueError(f"CNH inválida: {erro}")
        self._cnh = val

    # --- Dados Simples (Sem validação complexa por enquanto) ---
    @property
    def modelo(self):
        return self._modelo

    @modelo.setter
    def modelo(self, valor):
        self._modelo = str(valor).strip().upper()

    @property
    def cor(self):
        return self._cor

    @cor.setter
    def cor(self, valor):
        self._cor = str(valor).strip().upper()

    def to_dict(self):
        """Retorna um dicionário com os dados (útil para exportação/DB)."""
        return {
            "id": self.id,
            "nome": self.nome,
            "placa": self.placa,
            "cnh": self.cnh,
            "modelo": self.modelo,
            "cor": self.cor
        }