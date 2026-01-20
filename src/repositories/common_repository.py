"""
Repositório Comum (Base e Compartilhado).
Localização: src/repositories/common_repository.py
"""
import sqlite3
from src.repositories.base_repository import BaseRepository
from src.db import queries

class CommonRepository(BaseRepository):
    
    def criar_tabelas(self):
        try:
            manager = self.conn if self.conn else self.db_manager.__enter__()
            manager.execute(queries.CREATE_TABLE_MORADORES)
            manager.execute(queries.CREATE_TABLE_VISITANTES)
            manager.execute(queries.CREATE_TABLE_VISITANTES_CADASTRO)
            manager.execute(queries.CREATE_TABLE_HISTORICO)
        except sqlite3.Error as e:
            print(f"❌ Erro ao criar tabelas: {e}")

    def listar_todas_placas(self):
        cursor = self._get_cursor()
        placas = []
        try:
            cursor.execute(queries.SELECT_ALL_PLACAS_MORADORES)
            placas.extend([r[0] for r in cursor.fetchall()])
            
            cursor.execute(queries.SELECT_ALL_PLACAS_VISITANTES)
            placas.extend([r[0] for r in cursor.fetchall()])
            
            cursor.execute(queries.SELECT_ALL_PLACAS_VISITANTES_CADASTRO)
            placas.extend([r[0] for r in cursor.fetchall()])
            return set(placas)
        except Exception: return set()

    def listar_todas_cnhs(self):
        cursor = self._get_cursor()
        cnhs = []
        try:
            cursor.execute("SELECT cnh FROM moradores")
            cnhs.extend([r[0] for r in cursor.fetchall()])
            cursor.execute("SELECT cnh FROM visitantes_cadastrados")
            cnhs.extend([r[0] for r in cursor.fetchall()])
            return set(cnhs)
        except Exception: return set()

    def listar_ocupacao_total(self):
        """Relatório unificado para o Mapa."""
        cursor = self._get_cursor()
        lista = []
        try:
            cursor.execute(queries.SELECT_OCUPACAO_TOTAL)
            for row in cursor.fetchall():
                # Agora desempacotamos 7 itens
                vaga, tipo, nome, placa, modelo, cor, apto = row
                
                if tipo == 'MORADOR':
                    identificador = f"Apto {apto}"
                else:
                    identificador = f"Vaga {vaga}"

                lista.append({
                    "vaga": identificador,
                    "tipo": tipo,
                    "nome": nome,
                    "placa": placa,
                    "modelo": modelo or "",
                    "cor": cor or ""
                })
            return lista
        except Exception as e: 
            print(f"Erro: {e}") 
            return []

    # Métodos de histórico (Mantenha igual)
    def buscar_historico_geral(self):
        cursor = self._get_cursor()
        try:
            cursor.execute(queries.SELECT_HISTORICO_GERAL)
            return cursor.fetchall()
        except Exception as e:
            print(f"❌ Erro ao buscar histórico: {e}")
            return []

    def buscar_historico_por_placa(self, placa):
        cursor = self._get_cursor()
        try:
            cursor.execute(queries.SELECT_HISTORICO_POR_PLACA, (placa,))
            return cursor.fetchall()
        except Exception as e:
            print(f"❌ Erro ao buscar histórico da placa: {e}")
            return []