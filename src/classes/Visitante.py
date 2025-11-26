"""
Contém a classe Estacionamento, responsável pelas regras de negócio.

Esta classe define a capacidade, controla a lotação e valida
se novos veículos (especialmente visitantes) podem entrar.
"""

class Estacionamento:
    """
    Representa o sistema de regras do estacionamento (A 'Árvore' lógica).
    
    Não armazena os dados individuais de cada carro permanentemente (isso é função do DB),
    mas mantém o estado atual de ocupação para validar entradas (Lógica da Catraca).

    Atributos:
        _nome (str): Nome do condomínio/estacionamento.
        _capacidade_total (int): Lotação máxima (padrão 50, conforme esboço).
        _ocupacao_atual (int): Quantos carros (visitantes) estão dentro agora.
    """

    def __init__(self, nome="Condomínio POO", capacidade_total=50):
        """
        Inicializa as regras do estacionamento.

        Args:
            nome (str): Nome do estabelecimento.
            capacidade_total (int): Limite máximo de vagas para visitantes.
        """
        self._nome = nome
        self._capacidade_total = capacidade_total
        
        # Este atributo será "hidratado" pelo Repositório com dados do Banco
        self._ocupacao_atual = 0 

    # --- Properties (Getters & Setters) ---

    @property
    def nome(self):
        return self._nome

    @property
    def capacidade_total(self):
        return self._capacidade_total

    @capacidade_total.setter
    def capacidade_total(self, valor):
        """Define a capacidade, garantindo que seja um número positivo."""
        try:
            val = int(valor)
            if val < 0:
                raise ValueError("A capacidade não pode ser negativa.")
            self._capacidade_total = val
        except ValueError:
            raise ValueError("A capacidade deve ser um número inteiro.")

    @property
    def ocupacao_atual(self):
        return self._ocupacao_atual

    @ocupacao_atual.setter
    def ocupacao_atual(self, valor):
        """
        Atualiza a contagem atual (usado pelo Repositório ao carregar dados).
        """
        if valor < 0:
            # Pode acontecer se houver erro de sincronia no DB, então tratamos
            self._ocupacao_atual = 0 
        else:
            self._ocupacao_atual = valor

    # --- Lógica de Negócio ("A Catraca") ---

    @property
    def vagas_disponiveis(self):
        """Retorna quantas vagas restam."""
        return self._capacidade_total - self._ocupacao_atual

    @property
    def esta_lotado(self):
        """Retorna True se não houver mais vagas."""
        return self._ocupacao_atual >= self._capacidade_total

    def verificar_entrada(self):
        """
        Verifica se é permitido registrar uma nova entrada.
        
        Returns:
            bool: True se pode entrar, False se estiver lotado.
        """
        if self.esta_lotado:
            return False
        return True