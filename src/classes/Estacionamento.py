"""
Contém a classe Estacionamento, responsável pelas regras de negócio.
"""
from datetime import datetime

class Estacionamento:
    """
    Representa as regras do estacionamento.
    """

    def __init__(self, nome="Condomínio POO", capacidade_total=50, tempo_limite_minutos=120):
        """
        Args:
            tempo_limite_minutos (int): Tempo máximo em minutos antes do ticket vencer (Padrão: 2 horas).
        """
        self._nome = nome
        self._capacidade_total = capacidade_total
        self._tempo_limite_minutos = tempo_limite_minutos
        
        # Hidratado pelo Repositório
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

    # --- Lógica de Entrada ---

    def verificar_entrada(self):
        """A Catraca: Retorna True se pode entrar."""
        return not self.esta_lotado

    # --- Lógica de Tempo (O Trigger Lógico) ---

    def calcular_tempo_permanencia(self, visitante):
        """
        Calcula quantos minutos o visitante está no local.
        Args:
            visitante (Visitante): Objeto hidratado com data de entrada.
        Returns:
            float: Minutos passados.
        """
        if not visitante.entrada:
            return 0.0
            
        agora = datetime.now()
        # visitante.entrada é um objeto datetime (convertido pelo Repository)
        delta = agora - visitante.entrada
        return delta.total_seconds() / 60

    def verificar_ticket_vencido(self, visitante):
        """
        Retorna True se o tempo limite foi excedido.
        """
        minutos = self.calcular_tempo_permanencia(visitante)
        return minutos > self._tempo_limite_minutos