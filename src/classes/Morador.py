"""
Classe Morador (Entidade)
Responsabilidade: Representar a Pessoa e seu Vínculo Imobiliário (Apartamento).
Regra de Negócio: As vagas são calculadas matematicamente baseadas no Apartamento.
"""
from src.utils.validations import validate_apartamento

class Morador:
    def __init__(self, id=None, nome="", cnh="", apartamento=None):
        self.id = id
        self.nome = nome
        self.cnh = cnh
        # Ao atribuir aqui, o @apartamento.setter já é acionado para validar
        self.apartamento = apartamento 

    # --- PROPRIEDADE: APARTAMENTO (Com Validação) ---
    @property
    def apartamento(self):
        return self._apartamento

    @apartamento.setter
    def apartamento(self, valor):
        """
        Valida e define o apartamento.
        Se mudar o apartamento, as vagas calculadas mudarão automaticamente.
        """
        if valor is None:
            self._apartamento = None
            return

        val_formatado, erro = validate_apartamento(valor)
        
        if erro:
            raise ValueError(f"Erro ao definir apartamento: {erro}")
        
        # Salvamos como inteiro para poder fazer a conta das vagas
        self._apartamento = int(val_formatado)

    # --- PROPRIEDADE CALCULADA: VAGAS ---
    @property
    def vagas_vinculadas(self):
        """
        Calcula as vagas baseadas no número do apartamento.
        Regra: Apto N -> Vagas (N*2)-1 e (N*2)
        Ex: Apto 10 -> M19 e M20
        """
        if self._apartamento is None:
            return []

        vaga2 = self._apartamento * 2
        vaga1 = vaga2 - 1
        return [f"M{vaga1}", f"M{vaga2}"]

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cnh": self.cnh,
            "apartamento": self.apartamento,
            "vagas_direito": self.vagas_vinculadas # Retorna a lista calculada
        }

    def __repr__(self):
        return f"<Morador {self.nome} - Apto {self.apartamento}>"