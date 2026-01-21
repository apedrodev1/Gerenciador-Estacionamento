"""
Classe Estacionamento (Final)
Responsabilidade: Gerenciar limites físicos, regras de tempo e zonas.
Não acessa banco de dados.
"""
from datetime import datetime

class Estacionamento:
    def __init__(self, nome="Estacionamento Principal"):
        self.nome = nome
        
        # --- ZONAS E CAPACIDADES ---
        # Zona A (Visitantes): Vagas rotativas 01-20
        self.capacidade_visitantes = 20
        
        # Zona B (Moradores): Vagas garantidas 21-70
        self.capacidade_moradores = 50 
        
        # Capacidade Total (Apenas informativo)
        self.capacidade_total = self.capacidade_visitantes + self.capacidade_moradores
        
        # Regras de Tempo
        self.tempo_limite_visitante_minutos = 120
        
        # Cache de estado (Visitantes)
        self._ocupacao_visitantes = 0

    # --- PROPRIEDADES (Visitantes) ---

    @property
    def vagas_visitantes_disponiveis(self):
        """Calcula vagas restantes na Zona A."""
        return self.capacidade_visitantes - self._ocupacao_visitantes

    @property
    def visitante_esta_lotado(self):
        """Booleano para travar catraca de visitante."""
        return self.vagas_visitantes_disponiveis <= 0

    # --- MÉTODOS DE REGRA DE NEGÓCIO ---

    def alocar_vaga_visitante(self, vagas_ocupadas_set):
        """
        Descobre qual vaga (1-20) está livre.
        Retorna: int (ex: 5) ou None.
        """
        for i in range(1, self.capacidade_visitantes + 1):
            # Converte para string pois o set geralmente vem do banco como strings
            if str(i) not in vagas_ocupadas_set:
                return i
        return None

    def verificar_ticket_vencido(self, hora_entrada):
        """
        Calcula se o tempo de permanência excedeu o limite.
        """
        if not hora_entrada:
            return False
            
        agora = datetime.now()
        delta = agora - hora_entrada
        minutos = delta.total_seconds() / 60
        
        return minutos > self.tempo_limite_visitante_minutos