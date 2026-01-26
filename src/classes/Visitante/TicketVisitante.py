"""
Classe TicketVisitante (Antigo VisitanteCatraca)
Responsabilidade: Controlar o evento de ocupação de vaga (Entrada/Saída).
Localização: src/classes/visitantes/TicketVisitante.py
"""
from datetime import datetime
from src.utils.validations import validate_placa

class TicketVisitante:
    def __init__(self, id=None, placa="", numero_vaga=None, entrada=None, id_visitante=None):
        self._id = id
        self.placa = placa 
        self.numero_vaga = int(numero_vaga) if numero_vaga else None
        
        # Link opcional: Se for visitante cadastrado, guardamos o ID dele aqui
        self.id_visitante = id_visitante

        # Tratamento da Data de Entrada
        if isinstance(entrada, str):
            self.entrada = datetime.fromisoformat(entrada)
        else:
            self.entrada = entrada if entrada else datetime.now()

    # --- ID (Leitura) ---
    @property
    def id(self):
        return self._id

    # --- PLACA (Validada) ---
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
            raise ValueError(f"Erro no Ticket: {erro}")
        self._placa = val

    def to_dict(self):
        """Serializa para salvar no banco/json."""
        return {
            "id": self.id,
            "placa": self.placa,
            "numero_vaga": self.numero_vaga,
            "entrada": self.entrada.isoformat(),
            "id_visitante": self.id_visitante 
        }

    def __repr__(self):
        tipo = "Cadastrado" if self.id_visitante else "Avulso"
        return f"<Ticket {self.placa} | Vaga {self.numero_vaga} | {tipo}>"