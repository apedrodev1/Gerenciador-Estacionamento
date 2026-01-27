"""
Classe Morador (Entidade).
Responsabilidade: Representar a Pessoa e seu Vínculo (Foreign Key) com o Apartamento.
Localização: src/classes/Morador.py
"""
from src.utils.validations import validate_names, validate_cnh

class Morador:
    def __init__(self, id=None, nome="", cnh="", id_apartamento=None):
        self._id = id
        # Usamos os setters para validar desde a criação
        self.nome = nome
        self.cnh = cnh
        
        # VÍNCULO: Agora guardamos apenas o ID (Chave Estrangeira)
        self.id_apartamento = int(id_apartamento) if id_apartamento else None

    # --- ID (Leitura) ---
    @property
    def id(self):
        return self._id

    # --- NOME (Com Validação) ---
    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        val, erro = validate_names(valor)
        if erro: raise ValueError(erro)
        self._nome = val

    # --- CNH (Com Validação) ---
    @property
    def cnh(self):
        return self._cnh

    @cnh.setter
    def cnh(self, valor):
        val, erro = validate_cnh(valor)
        if erro: raise ValueError(erro)
        self._cnh = val

    # --- APARTAMENTO (Vínculo FK) ---
    # Nota: Não validamos formato "101" aqui, pois aqui entra o ID (1, 2, 50...)
    @property
    def id_apartamento(self):
        return self._id_apartamento

    @id_apartamento.setter
    def id_apartamento(self, valor):
        if valor is None:
            self._id_apartamento = None
            return
        try:
            self._id_apartamento = int(valor)
        except ValueError:
            raise ValueError("O ID do apartamento deve ser um número inteiro.")

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cnh": self.cnh,
            "id_apartamento": self.id_apartamento
        }

    def __repr__(self):
        return f"<Morador {self.nome} | ID_Apto: {self.id_apartamento}>"