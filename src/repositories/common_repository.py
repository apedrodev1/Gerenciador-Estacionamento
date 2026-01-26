"""
Repositório Comum (Setup e Relatórios Globais).
Responsabilidade: Criar tabelas e executar queries que cruzam múltiplos contextos.
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
            
            # Ordem de criação importa (Tabelas independentes primeiro)
            manager.execute(queries.CREATE_TABLE_MORADORES)
            manager.execute(queries.CREATE_TABLE_VISITANTES_CADASTRO)
            
            # Tabelas dependentes (Foreign Keys)
            manager.execute(queries.CREATE_TABLE_VEICULOS)
            manager.execute(queries.CREATE_TABLE_TICKETS)
            manager.execute(queries.CREATE_TABLE_HISTORICO)
            
            if not self.conn:
                self.db_manager.__exit__(None, None, None)
                
        except sqlite3.Error as e:
            print(f"❌ Erro fatal ao criar tabelas: {e}")

    def listar_ocupacao_completa(self):
        """
        Gera o relatório do Mapa do Estacionamento.
        Une carros de Moradores (estacionados) com Tickets de Visitantes.
        """
        cursor = self._get_cursor()
        lista = []
        try:
            cursor.execute(queries.SELECT_OCUPACAO_COMPLETA)
            # Colunas da Query: vaga_ref, tipo, proprietario, apto, placa, modelo, cor
            
            for row in cursor.fetchall():
                vaga_ref, tipo, prop, apto, placa, modelo, cor = row
                
                # Formata identificador visual
                identificador = f"Apto {apto}" if tipo == 'MORADOR' else f"Vaga {vaga_ref}"

                lista.append({
                    "vaga": identificador,
                    "tipo": tipo,
                    "nome": prop,
                    "placa": placa,
                    "modelo": modelo or "---",
                    "cor": cor or "---"
                })
            return lista
        except Exception as e: 
            print(f"Erro ao gerar mapa: {e}") 
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
            
    # --- MÉTODOS DE VALIDAÇÃO (Para evitar duplicidade) ---
    
    def listar_todas_cnhs(self):
        """
        Busca CNHs em Moradores e Visitantes.
        Usado para garantir que uma pessoa não tenha cadastro duplicado.
        """
        cursor = self._get_cursor()
        cnhs = set()
        try:
            # 1. Moradores
            cursor.execute("SELECT cnh FROM moradores")
            cnhs.update([r[0] for r in cursor.fetchall()])
            
            # 2. Visitantes Cadastrados
            cursor.execute("SELECT cnh FROM visitantes_cadastrados")
            cnhs.update([r[0] for r in cursor.fetchall()])
            
            return cnhs
        except Exception: 
            return set()