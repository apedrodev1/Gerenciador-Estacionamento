"""
Classe Veiculo (Entidade Relacional Universal)
Responsabilidade: Representar o automóvel físico.
Vínculo: Possui campos explícitos para ligar a diferentes tipos de proprietários (Morador, Visitante, etc).
"""
from src.utils.validations import validate_placa

class Veiculo:
    def __init__(self, id=None, placa="", modelo="", cor="", morador_id=None, visitante_id=None, funcionario_id=None, estacionado=False):
        self._id = id
        
        # --- Atributos Físicos ---
        self.placa = placa
        self.modelo = modelo
        self.cor = cor
        
        # --- Vínculos de Propriedade (Explícitos) ---
        # Permite integridade referencial no banco e expansão futura (ex: funcionario_id)
        self.morador_id = morador_id
        self.visitante_id = visitante_id
        self.funcionario_id = funcionario_id
        
        # --- Estado ---
        self.estacionado = estacionado

    # --- ID (Leitura) ---
    @property
    def id(self):
        return self._id

    # --- PLACA (Com Validação) ---
    @property
    def placa(self):
        return self._placa

    @placa.setter
    def placa(self, valor):
        if not valor:
            self._placa = ""
            return
            
        val, erro = validate_placa(valor)
        if erro:
            raise ValueError(f"Placa inválida: {erro}")
        self._placa = val

    # --- MODELO (Formatação) ---
    @property
    def modelo(self):
        return self._modelo

    @modelo.setter
    def modelo(self, valor):
        self._modelo = str(valor).strip().upper() if valor else ""

    # --- COR (Formatação) ---
    @property
    def cor(self):
        return self._cor

    @cor.setter
    def cor(self, valor):
        self._cor = str(valor).strip().upper() if valor else ""

    # --- VÍNCULOS (Validação de Tipo) ---
    @property
    def morador_id(self):
        return self._morador_id

    @morador_id.setter
    def morador_id(self, valor):
        if valor is not None and not isinstance(valor, int):
            raise ValueError("ID do morador deve ser um número inteiro.")
        self._morador_id = valor

    @property
    def visitante_id(self):
        return self._visitante_id

    @visitante_id.setter
    def visitante_id(self, valor):
        if valor is not None and not isinstance(valor, int):
            raise ValueError("ID do visitante deve ser um número inteiro.")
        self._visitante_id = valor

    # --- ESTADO ---
    @property
    def estacionado(self):
        return self._estacionado

    @estacionado.setter
    def estacionado(self, valor):
        self._estacionado = bool(valor)

    def to_dict(self):
        """Retorna dicionário completo para persistência."""
        return {
            "id": self.id,
            "placa": self.placa,
            "modelo": self.modelo,
            "cor": self.cor,
            "morador_id": self.morador_id,
            "visitante_id": self.visitante_id,
            "estacionado": self.estacionado
        }

    def __repr__(self):
        dono = f"Morador:{self.morador_id}" if self.morador_id else f"Visitante:{self.visitante_id}"
        return f"<Veiculo {self.placa} | {dono}>"