"""
Repositório Comum (Setup e Relatórios Globais).
Responsabilidade: Criar TODAS as tabelas do sistema, inclusive a nova 'apartamentos'.
Localização: src/repositories/common_repository.py
"""
import sqlite3
from src.repositories.base_repository import BaseRepository
from src.db import queries

class CommonRepository(BaseRepository):
    
    def criar_tabelas(self):
        """Inicializa o esquema do banco de dados (DDL)."""
        try:
            # Se já temos conexão ativa, usa ela. Senão, cria uma temporária.
            manager = self.conn if self.conn else self.db_manager.__enter__()
            
            # 1. Tabelas Independentes (Ordem Importa!)
            manager.execute(queries.CREATE_TABLE_APARTAMENTOS)
            manager.execute(queries.CREATE_TABLE_VISITANTES_CADASTRO)
            
            # 2. Tabelas Dependentes (Com Foreign Keys)
            manager.execute(queries.CREATE_TABLE_MORADORES) # Depende de Apartamentos
            manager.execute(queries.CREATE_TABLE_VEICULOS)  # Depende de Moradores
            manager.execute(queries.CREATE_TABLE_FUNCIONARIOS) # Depende de Moradores
            manager.execute(queries.CREATE_TABLE_TICKETS)
            manager.execute(queries.CREATE_TABLE_HISTORICO)
            
            # 3. Tabela de Usuários (Independente)
            manager.execute(queries.CREATE_TABLE_USUARIOS)

            if not self.conn:
                self.db_manager.__exit__(None, None, None)
                
        except sqlite3.Error as e:
            print(f"❌ Erro fatal ao criar tabelas: {e}")

    def listar_ocupacao_completa(self):
        """
        Gera os dados para o Mapa do Estacionamento.
        Retorna uma lista de Dicionários com as chaves exatas da Query.
        """
        cursor = self._get_cursor()
        lista = []
        try:
            cursor.execute(queries.SELECT_OCUPACAO_COMPLETA)
            
            # A query retorna Tuplas. Vamos converter para Dicionário
            # para facilitar o uso no front-end (mapa.py)
            for row in cursor.fetchall():
                # Ordem definida no SELECT do queries.py:
                # 0:tipo, 1:apto_num, 2:apto_bloco, 3:vaga_vis, 
                # 4:proprietario, 5:placa, 6:modelo, 7:cor
                
                item = {
                    "tipo": row[0],            # 'MORADOR' ou 'VISITANTE'
                    "apto_num": row[1],
                    "apto_bloco": row[2],
                    "vaga_visitante": row[3],
                    "proprietario": row[4],    # Nome do dono
                    "placa": row[5],
                    "modelo": row[6],
                    "cor": row[7]
                }
                lista.append(item)
                
            return lista
        except Exception as e: 
            print(f"Erro ao gerar mapa: {e}") 
            return []

    def buscar_historico_por_placa(self, placa):
        """Filtra logs por placa."""
        cursor = self._get_cursor()
        try:
            cursor.execute(queries.SELECT_HISTORICO_BY_PLACA, (placa,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao buscar histórico da placa: {e}")
            return []
            
    def listar_historico_recente(self):
        """Retorna os últimos 50 eventos de entrada/saída."""
        cursor = self._get_cursor()
        try:
            cursor.execute(queries.SELECT_HISTORICO_RECENTE)
            return cursor.fetchall()
        except Exception as e:
            print(f"❌ Erro ao buscar histórico: {e}")
            return []
            
    def listar_todas_cnhs(self):
        """Busca CNHs em Moradores e Visitantes para evitar duplicidade."""
        cursor = self._get_cursor()
        cnhs = set()
        try:
            cursor.execute("SELECT cnh FROM moradores")
            cnhs.update([r[0] for r in cursor.fetchall()])
            
            cursor.execute("SELECT cnh FROM visitantes_cadastrados")
            cnhs.update([r[0] for r in cursor.fetchall()])
            
            return cnhs
        except Exception: 
            return set()