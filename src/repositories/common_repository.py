"""
Repositório para consultas globais e utilitários que cruzam tabelas.
Ex: Listar todas as placas (Moradores + Visitantes), Relatórios Gerais.
"""
import sqlite3
from src.repositories.base_repository import BaseRepository
from src.db import queries

class CommonRepository(BaseRepository):
    
    def criar_tabelas(self):
        """Inicializa o banco de dados."""
        try:
            # Para criar tabelas, precisamos garantir uma conexão
            # Se não estiver num 'with', abrimos uma temporária
            manager = self.conn if self.conn else self.db_manager.__enter__()
            
            manager.execute(queries.CREATE_TABLE_MORADORES)
            manager.execute(queries.CREATE_TABLE_VISITANTES)
            manager.execute(queries.CREATE_TABLE_VISITANTES_CADASTRO)
            
            # Se abrimos manualmente aqui, o __exit__ do manager cuidaria do commit/close
            # mas como é execute direto, está ok.
        except sqlite3.Error as e:
            print(f"❌ Erro ao criar tabelas: {e}")

    def listar_todas_placas(self):
        """Unifica placas de Moradores, Visitantes Ativos e Cadastrados."""
        cursor = self._get_cursor()
        placas = set()
        try:
            # 1. Moradores
            cursor.execute("SELECT placa FROM moradores")
            placas.update(row[0] for row in cursor.fetchall())
            
            # 2. Visitantes Ativos
            cursor.execute("SELECT placa FROM visitantes")
            placas.update(row[0] for row in cursor.fetchall())
            
            # 3. Visitantes Cadastrados
            try:
                cursor.execute("SELECT placa FROM visitantes_cadastrados")
                placas.update(row[0] for row in cursor.fetchall())
            except sqlite3.Error: pass # Tabela pode não existir ainda
            
            return placas
        except sqlite3.Error as e:
            print(f"❌ Erro ao listar placas: {e}")
            return set()

    def listar_todas_cnhs(self):
        """Unifica CNHs de Moradores, Visitantes e Cadastrados."""
        cursor = self._get_cursor()
        cnhs = set()
        try:
            cursor.execute("SELECT cnh FROM moradores")
            cnhs.update(row[0] for row in cursor.fetchall())
            
            cursor.execute("SELECT cnh FROM visitantes")
            cnhs.update(row[0] for row in cursor.fetchall())
            
            try:
                cursor.execute("SELECT cnh FROM visitantes_cadastrados")
                cnhs.update(row[0] for row in cursor.fetchall())
            except sqlite3.Error: pass
            
            return cnhs
        except sqlite3.Error as e:
            print(f"❌ Erro ao listar CNHs: {e}")
            return set()
            
    def listar_ocupacao_total(self):
        """Relatório unificado para o Mapa."""
        cursor = self._get_cursor()
        lista = []
        try:
            cursor.execute(queries.SELECT_OCUPACAO_TOTAL)
            for row in cursor.fetchall():
                vaga, tipo, nome, placa, modelo, cor = row
                lista.append({
                    "vaga": vaga, "tipo": tipo, "nome": nome, "placa": placa,
                    "modelo": modelo or "", "cor": cor or ""
                })
            return lista
        except sqlite3.Error: return []