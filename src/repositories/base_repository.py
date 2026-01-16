"""
Classe Base para Repositórios.
Gerencia o acesso ao cursor e conexão compartilhada.
"""
from datetime import datetime
from src.utils.db_connection import DatabaseManager
from src.db import queries 

class BaseRepository:
    def __init__(self, db_manager: DatabaseManager):
        """
        Recebe o gerenciador de banco.
        A conexão (self.conn) será injetada pelo Facade quando entrarmos no 'with'.
        """
        self.db_manager = db_manager
        self.conn = None

    def set_connection(self, conn):
        """Define a conexão ativa (usado pelo Context Manager do Facade)."""
        self.conn = conn

    def _get_cursor(self):
        """
        Retorna o cursor da conexão ativa (transação) 
        ou cria uma conexão temporária (leitura rápida).
        """
        if self.conn:
            return self.conn.cursor()
        # Se não houver transação aberta, abre uma rápida e fecha (para leituras simples)
        return self.db_manager.__enter__().cursor()
    
    def _registrar_log(self, placa, tipo_veiculo, tipo_evento):
        """
        Grava uma linha no histórico silenciosamente.
        Não deve parar o sistema se der erro (try/except seguro).
        """
        try:
            cursor = self._get_cursor()
            agora = datetime.now().isoformat()
            cursor.execute(queries.INSERT_HISTORICO, (agora, placa, tipo_veiculo, tipo_evento))
        except Exception as e:
            print(f"⚠️ Erro ao gravar log de auditoria: {e}")