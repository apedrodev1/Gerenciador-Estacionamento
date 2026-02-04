"""
Classe Visitante (Entidade)
Responsabilidade: Representar a Pessoa (Cadastro).
Nota: Não guarda dados do carro. O vínculo é feito na classe Veiculo (campo visitante_id).
"""
from datetime import datetime
from src.utils.validations import validate_names, validate_cnh

class Visitante:
    def __init__(self, id=None, nome="", cnh="", data_cadastro=None):
        self._id = id
        self.nome = nome
        self.cnh = cnh
        self.data_cadastro = data_cadastro if data_cadastro else datetime.now().isoformat()

    # --- ID (Leitura) ---
    @property
    def id(self):
        return self._id

    # --- NOME (Validado) ---
    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        val, erro = validate_names(valor)
        if erro:
            raise ValueError(f"Nome inválido: {erro}")
        self._nome = val

    # --- CNH (Validada) ---
    @property
    def cnh(self):
        return self._cnh

    @cnh.setter
    def cnh(self, valor):
        val, erro = validate_cnh(valor)
        if erro:
            raise ValueError(f"CNH inválida: {erro}")
        self._cnh = val

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cnh": self.cnh,
            "data_cadastro": self.data_cadastro
        }

    def __repr__(self):
        return f"<Visitante {self.nome}>"