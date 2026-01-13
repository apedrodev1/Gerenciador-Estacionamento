"""
Contém a classe Estacionamento, responsável pelas regras de negócio.
"""
from datetime import datetime

class Estacionamento:
    """
    Representa as regras do estacionamento (O 'Cérebro').
    Gerencia a alocação de vagas de visitantes (V01-V20) e validação de moradores.
    """

    def __init__(self, nome="Condomínio Solar", capacidade_visitantes=20, tempo_limite_minutos=120):
        # parametros já são pré definidos / ver co-relação com o .env
        
        """
        Args:
            nome (str): Nome do estabelecimento.
            capacidade_visitantes (int): Quantidade de vagas para visitantes (V01 até Vxx).
            tempo_limite_minutos (int): Tempo máximo em minutos antes do ticket vencer.
        """
        self._nome = nome
        self._capacidade_visitantes = capacidade_visitantes
        self._tempo_limite_minutos = tempo_limite_minutos
        
        # Hidratado pelo Repositório a cada loop
        self._ocupacao_atual = 0 

    # --- Properties ---

    @property
    def nome(self):
        return self._nome

    @property
    def capacidade_total(self):
        return self._capacidade_visitantes

    @property
    def ocupacao_atual(self):
        return self._ocupacao_atual

    @ocupacao_atual.setter
    def ocupacao_atual(self, valor):
        self._ocupacao_atual = max(0, valor)

    @property
    def vagas_disponiveis(self):
        return self._capacidade_visitantes - self._ocupacao_atual

    @property
    def esta_lotado(self):
        return self._ocupacao_atual >= self._capacidade_visitantes

    # --- Lógica de Entrada (Visitantes) ---

    def verificar_entrada_visitante(self):
        """Verificação rápida de lotação para visitantes."""
        return not self.esta_lotado

    # --- GERADOR DE VAGAS DE VISITANTE (V01 ... Vxx) ---
    def _gerar_lista_vagas_visitantes(self):
        """Gera lista de strings ['V01', 'V02', ..., 'V20']"""
        lista = []
        for i in range(1, self._capacidade_visitantes + 1):
            lista.append(f"V{i:02d}") # Formata com zero à esquerda
        return lista

    def alocar_vaga_visitante(self, vagas_ocupadas_ids):
        """
        Retorna a primeira vaga 'Vxx' livre.
        Args: vagas_ocupadas_ids (list[str]): ex ['V01', '101-1']
        """
        # Conjunto com todas as vagas possíveis de visitante
        todas_vagas = set(self._gerar_lista_vagas_visitantes())
        
        # Conjunto das vagas que já estão ocupadas no banco
        ocupadas = set(vagas_ocupadas_ids)
        
        # Filtra apenas as vagas de visitante que estão livres
        livres = list(todas_vagas - ocupadas)
        
        if not livres:
            return None 
            
        livres.sort() # Garante ordem alfabética (V01, V02...)
        return livres[0]

    # --- Lógica de Moradores (Regra: 2 Vagas por Apto) ---

    def validar_atribuicao_vaga_morador(self, apartamento, vaga_escolhida):
        """
        Valida se a vaga escolhida pertence ao apartamento.
        Regra: Apto '101' -> Vagas permitidas: '101-1' e '101-2'
        """
        if not vaga_escolhida:
            return True, None # Permite morador sem vaga cadastrada

        vaga_escolhida = vaga_escolhida.upper().strip()
        apartamento = str(apartamento).strip()
        
        # 1. Gera as vagas permitidas para este apto
        vaga_permitida_1 = f"{apartamento}-1"
        vaga_permitida_2 = f"{apartamento}-2"
        
        permitidas = [vaga_permitida_1, vaga_permitida_2]
        
        if vaga_escolhida in permitidas:
            return True, None
        else:
            return False, f"Vaga inválida para o Apto {apartamento}. As vagas exclusivas deste apartamento são: {permitidas}"

    # --- Lógica de Tempo (Trigger) ---

    def calcular_tempo_permanencia(self, visitante):
        """Calcula minutos passados desde a entrada."""
        if not visitante.entrada:
            return 0.0
        agora = datetime.now()
        delta = agora - visitante.entrada
        return delta.total_seconds() / 60

    def verificar_ticket_vencido(self, visitante):
        """Retorna True se o tempo limite foi excedido."""
        minutos = self.calcular_tempo_permanencia(visitante)
        return minutos > self._tempo_limite_minutos