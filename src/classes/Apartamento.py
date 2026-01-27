"""
Classe Apartamento (Entidade).
Responsabilidade: Representar a unidade física.
Contém a lógica matemática das vagas baseada no número da porta.
Localização: src/classes/Apartamento.py
"""

class Apartamento:
    def __init__(self, id=None, numero="", bloco="", vagas=2):
        self._id = id
        self.numero = str(numero) # Ex: "102"
        self.bloco = str(bloco).upper() if bloco else "" 
        self.vagas = int(vagas) # Limite físico de vagas

    @property
    def id(self):
        return self._id

    @property
    def rotulo(self):
        """Retorna representação legível (Ex: 102-A ou apenas 102)"""
        if self.bloco:
            return f"{self.numero}-{self.bloco}"
        return self.numero

    def get_vagas_teoricas(self):
        """
        Calcula quais seriam as vagas baseadas na regra matemática do condomínio.
        Regra: Apto N -> Vagas (N*2)-1 e (N*2)
        Nota: Só funciona se o número do apto for numérico.
        """
        try:
            num = int(self.numero)
            vaga2 = num * 2
            vaga1 = vaga2 - 1
            return [f"M{vaga1}", f"M{vaga2}"]
        except ValueError:
            # Caso o apto seja "Térreo" ou alfanumérico, não calcula auto
            return []

    def __repr__(self):
        return f"<Apto {self.rotulo} | Vagas: {self.vagas}>"

    def to_dict(self):
        return {
            "id": self.id,
            "numero": self.numero,
            "bloco": self.bloco,
            "vagas": self.vagas,
            "vagas_calculadas": self.get_vagas_teoricas()
        }