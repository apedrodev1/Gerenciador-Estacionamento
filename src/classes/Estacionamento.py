"""
Contém a classe Estacionamento, responsável pelas regras de negócio.
"""
from datetime import datetime

class Estacionamento:
    """
    Representa as regras do estacionamento (O 'Cérebro').
    Gerencia a alocação dinâmica para visitantes e valida regras de tempo e zoneamento.
    """

    def __init__(self, nome="Condomínio POO", capacidade_total=50, tempo_limite_minutos=120):
        """
        Args:
            nome (str): Nome do estabelecimento.
            capacidade_total (int): Total de vagas ROTATIVAS (para visitantes).
            tempo_limite_minutos (int): Tempo máximo em minutos antes do ticket vencer.
        """
        self._nome = nome
        self._capacidade_total = capacidade_total
        self._tempo_limite_minutos = tempo_limite_minutos
        
        # Hidratado pelo Repositório a cada loop
        self._ocupacao_atual = 0 

    # --- Properties ---

    @property
    def nome(self):
        return self._nome

    @property
    def capacidade_total(self):
        return self._capacidade_total

    @property
    def ocupacao_atual(self):
        return self._ocupacao_atual

    @ocupacao_atual.setter
    def ocupacao_atual(self, valor):
        self._ocupacao_atual = max(0, valor)

    @property
    def vagas_disponiveis(self):
        return self._capacidade_total - self._ocupacao_atual

    @property
    def esta_lotado(self):
        return self._ocupacao_atual >= self._capacidade_total

    # --- Lógica de Entrada (Visitantes) ---

    def verificar_entrada_visitante(self):
        """Verificação rápida de lotação para visitantes."""
        return not self.esta_lotado

    def alocar_vaga_visitante(self, vagas_ocupadas_ids):
        """
        O Cérebro da Alocação: Descobre a próxima vaga livre (1 a 50).
        Retorna: int (vaga livre) ou None (lotado).
        """
        todas_vagas = set(range(1, self._capacidade_total + 1))
        ocupadas = set(vagas_ocupadas_ids)
        livres = list(todas_vagas - ocupadas)
        
        if not livres:
            return None 
            
        return min(livres)

    # --- Lógica de Zoneamento (Moradores) ---
    # ESTES SÃO OS MÉTODOS QUE FALTAVAM:

    def vaga_pertence_a_visitantes(self, numero_vaga):
        """Verifica se o número da vaga cai na zona de rotativos (1 a Capacidade)."""
        return 1 <= numero_vaga <= self._capacidade_total

    def validar_atribuicao_vaga_morador(self, numero_vaga):
        """
        Impede que um morador receba uma vaga destinada a visitantes.
        Retorna: (Bool, Mensagem de Erro)
        """
        if numero_vaga is None:
            return True, None # Morador sem vaga (apenas cadastro) é permitido

        if self.vaga_pertence_a_visitantes(numero_vaga):
            return False, f"A vaga {numero_vaga} pertence à ZONA DE VISITANTES (1-{self._capacidade_total}). Escolha uma vaga acima de {self._capacidade_total}."
        
        return True, None

    # --- Lógica de Tempo (Trigger) ---

    def calcular_tempo_permanencia(self, visitante):
        if not visitante.entrada:
            return 0.0
        agora = datetime.now()
        delta = agora - visitante.entrada
        return delta.total_seconds() / 60

    def verificar_ticket_vencido(self, visitante):
        minutos = self.calcular_tempo_permanencia(visitante)
        return minutos > self._tempo_limite_minutos