"""
Classe Estacionamento (Final)
Responsabilidade: Gerenciar limites físicos, regras de tempo e zonas.
Não acessa banco de dados.
"""
from datetime import datetime

class Estacionamento:
    # Correção: Adicionados os argumentos opcionais no __init__ para aceitar o que vem do setup.py
    def __init__(self, nome="Estacionamento Principal", capacidade_visitantes=20, tempo_limite_minutos=120):
        self.nome = nome
        
        
        # --- ZONAS E CAPACIDADES ---
        # Zona A (Visitantes): Vagas rotativas (Agora dinâmico via .env)
        self.capacidade_visitantes = int(capacidade_visitantes)
        
        # Zona B (Moradores): Vagas garantidas
        # (Podemos deixar fixo ou expandir no futuro)
        self.capacidade_moradores = 50 
        
        # Capacidade Total (Informativo)
        self.capacidade_total = self.capacidade_visitantes + self.capacidade_moradores
        
        # Regras de Tempo (Agora dinâmico via .env)
        self.tempo_limite_visitante_minutos = int(tempo_limite_minutos)
        
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
        Descobre qual vaga (1 ao limite) está livre.
        Retorna: int (ex: 5) ou None.
        """
        for i in range(1, self.capacidade_visitantes + 1):
            # Garante comparação segura (String vs String)
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