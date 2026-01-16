"""
Classe Estacionamento.
Gerencia a capacidade, contagem de vagas e regras de negócio de limites.
Localização: src/classes/Estacionamento.py
"""
class Estacionamento:
    # CORREÇÃO 1: Adicionado tempo_limite_minutos aqui
    def __init__(self, nome="Estacionamento Principal", capacidade_visitantes=20, capacidade_total=100, tempo_limite_minutos=120):
        self.nome = nome
        self.capacidade_visitantes = int(capacidade_visitantes)
        self.capacidade_total = int(capacidade_total)
        self.tempo_limite_minutos = int(tempo_limite_minutos) # CORREÇÃO: Salvamos a config
        
        # --- NOVA REGRA: Cota por Apartamento ---
        self.limite_carros_por_apto = 2  
        
        # Cache de ocupação
        self.ocupacao_atual = 0

    @property
    def vagas_disponiveis(self):
        """Retorna quantas vagas de VISITANTE ainda restam."""
        return self.capacidade_visitantes - self.ocupacao_atual

    @property
    def esta_lotado(self):
        """Verifica se a área de visitantes está cheia."""
        return self.vagas_disponiveis <= 0

    def alocar_vaga_visitante(self, vagas_ocupadas_set):
        """
        Encontra a primeira vaga livre (1..Capacidade) para visitantes.
        """
        for i in range(1, self.capacidade_visitantes + 1):
            if str(i) not in vagas_ocupadas_set:
                return i
        return None

    def calcular_tempo_permanencia(self, visitante):
        """Retorna o tempo em minutos que o visitante está no pátio."""
        from datetime import datetime
        agora = datetime.now()
        delta = agora - visitante.entrada
        return delta.total_seconds() / 60

    # CORREÇÃO 2: Usamos self.tempo_limite_minutos em vez de passar parâmetro opcional fixo
    def verificar_ticket_vencido(self, visitante):
        """Retorna True se o visitante excedeu o tempo limite configurado."""
        tempo = self.calcular_tempo_permanencia(visitante)
        return tempo > self.tempo_limite_minutos

    # --- NOVOS MÉTODOS DE VALIDAÇÃO (Regra de Negócio) ---

    def validar_cota_morador(self, morador, repositorio):
        """
        Verifica se o apartamento do morador ainda tem 'crédito' para entrar.
        """
        # 1. Consulta o banco
        qtd_no_patio = repositorio.moradores.contar_carros_no_apto(morador.apartamento)
        
        # 2. Verifica limite
        if qtd_no_patio >= self.limite_carros_por_apto:
            return False, (
                f"⛔ LIMITE ATINGIDO! O Apto {morador.apartamento} já possui {qtd_no_patio} carros no pátio.\n"
                f"   Limite permitido: {self.limite_carros_por_apto} veículos simultâneos."
            )
        
        # 3. Calcula saldo
        saldo = self.limite_carros_por_apto - qtd_no_patio
        restantes_apos_entrar = saldo - 1
        
        return True, (
            f"✅ Entrada Liberada!\n"
            f"   Cota do Apto {morador.apartamento}: {qtd_no_patio}/{self.limite_carros_por_apto} em uso.\n"
            f"   Vagas restantes para este apto: {restantes_apos_entrar}"
        )