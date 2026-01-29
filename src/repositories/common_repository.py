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
            manager.execute(queries.CREATE_TABLE_APARTAMENTOS) # <--- FALTAVA ESSA LINHA!
            manager.execute(queries.CREATE_TABLE_VISITANTES_CADASTRO)
            
            # 2. Tabelas Dependentes (Com Foreign Keys)
            manager.execute(queries.CREATE_TABLE_MORADORES) # Depende de Apartamentos
            manager.execute(queries.CREATE_TABLE_VEICULOS)  # Depende de Moradores
            manager.execute(queries.CREATE_TABLE_TICKETS)
            manager.execute(queries.CREATE_TABLE_HISTORICO)
            
            if not self.conn:
                self.db_manager.__exit__(None, None, None)
                
        except sqlite3.Error as e:
            print(f"❌ Erro fatal ao criar tabelas: {e}")

    def listar_ocupacao_completa(self):
        """
        Gera o relatório do Mapa do Estacionamento.
        """
        cursor = self._get_cursor()
        lista = []
        try:
            cursor.execute(queries.SELECT_OCUPACAO_COMPLETA)
            # Colunas da Query: tipo, apto_num, apto_bloco, vaga_visitante, proprietario, placa, modelo, cor
            
            for row in cursor.fetchall():
                tipo, apto_num, apto_bloco, vaga_vis, prop, placa, modelo, cor = row
                
                # Lógica de Exibição
                if tipo == 'MORADOR':
                    # Monta "101-A" ou só "101"
                    bloco_str = f"-{apto_bloco}" if apto_bloco else ""
                    identificador = f"Apto {apto_num}{bloco_str}"
                else:
                    identificador = f"Vaga {vaga_vis}"

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