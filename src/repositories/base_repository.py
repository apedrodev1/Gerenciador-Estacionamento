"""
Classe Base para Repositórios.
Responsabilidade: Gerenciar a injeção de dependência da conexão.
Nota: Não contém lógica de negócio (Logs movidos para VeiculoRepository).
Localização: src/repositories/base_repository.py
"""
from src.utils.db_connection import DatabaseManager

class BaseRepository:
    def __init__(self, db_manager: DatabaseManager):
        """
        Recebe o gerenciador de banco.
        A conexão (self.conn) será injetada pelo Facade (EstacionamentoRepository).
        """
        self.db_manager = db_manager
        self.conn = None

    def set_connection(self, conn):
        """Define a conexão ativa (usado pelo Context Manager do Facade)."""
        self.conn = conn

    def _get_cursor(self):
        """
        Retorna o cursor da conexão ativa.
        """
        if self.conn:
            return self.conn.cursor()
        
        # Alteração de Segurança: 
        # Removemos a criação automática de conexão "fantasma" para forçar 
        # o uso correto do padrão Facade (with repository:).
        raise RuntimeError("Erro Crítico: Tentativa de acessar o banco sem conexão ativa. Envolva a chamada em um bloco 'with repository:'.")