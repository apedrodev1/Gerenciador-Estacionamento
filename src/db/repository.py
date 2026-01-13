"""
Módulo de Repositório para o Sistema de Estacionamento.
Gerencia a persistência de Moradores e Visitantes usando SQLite.
"""

import sqlite3
from datetime import datetime
from . import queries
from src.utils.db_connection import DatabaseManager
from src.classes.Morador import Morador
from src.classes.Visitante import Visitante

class EstacionamentoRepository:
    """
    Gerencia todas as operações de banco de dados.
    """

    def __init__(self, db_path: str):
        self.db_manager = DatabaseManager(db_path)
        self.conn = None
        self._create_tables()

    # --- Protocolo Context Manager (para usar 'with repo:') ---
    def __enter__(self):
        self.conn = self.db_manager.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db_manager.__exit__(exc_type, exc_val, exc_tb)
        self.conn = None

    def _get_cursor(self):
        """Retorna o cursor da conexão ativa ou cria uma temporária."""
        if self.conn:
            return self.conn.cursor()
        return self.db_manager.__enter__().cursor()

    # --- Inicialização ---

    def _create_tables(self):
        """Cria as tabelas se não existirem."""
        try:
            # Usa uma conexão temporária para garantir a criação
            with self.db_manager as conn:
                conn.execute(queries.CREATE_TABLE_MORADORES)
                conn.execute(queries.CREATE_TABLE_VISITANTES)
        except sqlite3.Error as e:
            print(f"❌ Erro ao criar tabelas: {e}")

    # --- CRUD Moradores ---

    def adicionar_morador(self, morador: Morador):
        cursor = self._get_cursor()
        try:
            cursor.execute(queries.INSERT_MORADOR, (
                morador.nome,
                morador.placa,
                morador.cnh,
                morador.modelo,
                morador.cor,
                morador.apartamento,
                morador.vaga_id
            ))
            # O commit é feito automaticamente pelo __exit__ do context manager
        except sqlite3.Error as e:
            print(f"❌ Erro ao adicionar morador: {e}")
            raise

    def listar_moradores(self):
        """Retorna uma lista de objetos Morador."""
        cursor = self._get_cursor()
        lista_moradores = []
        try:
            cursor.execute(queries.SELECT_ALL_MORADORES)
            rows = cursor.fetchall()
            
            for row in rows:
                # Desempacota a tupla do banco
                id_db, nome, placa, cnh, modelo, cor, apto, vaga, est_int = row
                
                estacionado_bool = bool(est_int)

                # Instancia o objeto (Dumb Class)
                m = Morador(id=id_db, nome=nome, placa=placa, cnh=cnh, 
                            modelo=modelo, cor=cor, apartamento=apto, vaga_id=vaga,estacionado=estacionado_bool)
                lista_moradores.append(m)
                
            return lista_moradores
        except sqlite3.Error as e:
            print(f"❌ Erro ao listar moradores: {e}")
            return []

    def buscar_morador_por_placa(self, placa):
        """Busca um morador específico pela placa."""
        cursor = self._get_cursor()
        try:
            cursor.execute(queries.SELECT_MORADOR_BY_PLACA, (placa,))
            row = cursor.fetchone()
            
            if row:
                # Reconstrói o objeto Morador com os dados do banco
                return Morador(
                    id=row[0],
                    nome=row[1],
                    placa=row[2],
                    cnh=row[3],
                    modelo=row[4],
                    cor=row[5],
                    apartamento=row[6],
                    vaga_id=row[7],
                    estacionado=bool(row[8])
                )
            return None
            
        except sqlite3.Error as e:
            print(f"❌ Erro ao buscar morador por placa: {e}")
            return None
                    

    def remover_morador(self, morador_id):
        cursor = self._get_cursor()
        try:
            cursor.execute(queries.DELETE_MORADOR, (morador_id,))
        except sqlite3.Error as e:
            print(f"❌ Erro ao remover morador: {e}")
            raise

    def atualizar_morador(self, morador: Morador):
        """Atualiza todos os dados do morador no banco."""
        cursor = self._get_cursor()
        try:
            cursor.execute(queries.UPDATE_MORADOR, (
                morador.nome,
                morador.placa,
                morador.cnh,
                morador.modelo,
                morador.cor,
                morador.apartamento,
                morador.vaga_id,
                morador.id # O ID vai no WHERE
            ))
        except sqlite3.Error as e:
            print(f"❌ Erro ao atualizar morador: {e}")
            raise

    # --- CONTROLE DE ACESSO MORADORES ---

    def registrar_entrada_morador(self, placa):
        """Marca o morador como estacionado usando a PLACA."""
        cursor = self._get_cursor()
        try:
            cursor.execute(queries.REGISTRAR_ENTRADA_MORADOR, (placa,))
            
            if cursor.rowcount == 0:
                print(f"⚠️  Aviso: Nenhuma placa '{placa}' encontrada para registrar entrada.")
                
        except sqlite3.Error as e:
            print(f"❌ Erro ao registrar entrada de morador: {e}")
            raise

    def registrar_saida_morador(self, placa):
        """Marca o morador como ausente usando a PLACA."""
        cursor = self._get_cursor()
        try:
            cursor.execute(queries.REGISTRAR_SAIDA_MORADOR, (placa,))
            
            if cursor.rowcount == 0:
                print(f"⚠️  Aviso: Nenhuma placa '{placa}' encontrada para registrar saída.")
                
        except sqlite3.Error as e:
            print(f"❌ Erro ao registrar saída de morador: {e}")
            raise

    # --- CRUD Visitantes (Entrada/Saída) ---

    def registrar_entrada(self, visitante: Visitante):
        cursor = self._get_cursor()
        try:
            # Converte datetime para string ISO para salvar no SQLite
            data_iso = visitante.entrada.isoformat()
            
            cursor.execute(queries.INSERT_VISITANTE, (
                visitante.nome,
                visitante.placa,
                visitante.cnh,
                visitante.modelo,
                visitante.cor,
                data_iso,
                visitante.numero_vaga
            ))
        except sqlite3.Error as e:
            print(f"❌ Erro ao registrar entrada: {e}")
            raise

    def registrar_saida(self, visitante_id):
        """Remove o visitante da tabela de ativos."""
        cursor = self._get_cursor()
        try:
            cursor.execute(queries.DELETE_VISITANTE, (visitante_id,))
        except sqlite3.Error as e:
            print(f"❌ Erro ao registrar saída: {e}")
            raise

    def listar_visitantes_ativos(self):
        """Retorna lista de objetos Visitante que estão no estacionamento."""
        cursor = self._get_cursor()
        lista = []
        try:
            cursor.execute(queries.SELECT_ALL_VISITANTES)
            rows = cursor.fetchall()
            
            for row in rows:
                # Agora recuperamos numero_vaga
                id_db, nome, placa, cnh, modelo, cor, entrada_iso, num_vaga = row
                
                data_entrada = datetime.fromisoformat(entrada_iso)
                
                # CORREÇÃO: Removida a vírgula extra e movido o parêntese para o final
                v = Visitante(
                    id=id_db, 
                    nome=nome, 
                    placa=placa, 
                    cnh=cnh,
                    modelo=modelo, 
                    cor=cor, 
                    entrada=data_entrada,
                    numero_vaga=num_vaga 
                )
                lista.append(v)
            return lista
        except sqlite3.Error as e:
            print(f"❌ Erro ao listar visitantes: {e}")
            return []


    def buscar_vagas_ocupadas_visitantes(self):
        """Retorna lista de STRINGS das vagas ocupadas."""
        cursor = self._get_cursor()
        try:
            cursor.execute(queries.SELECT_VAGAS_OCUPADAS)
            rows = cursor.fetchall()
            # Garante que seja string (caso o banco tenha salvo algo estranho)
            vagas = [str(row[0]) for row in rows] 
            return vagas
        except sqlite3.Error as e:
            print(f"❌ Erro ao buscar vagas: {e}")
            return []

    def contar_visitantes_ativos(self):
        cursor = self._get_cursor()
        try:
            cursor.execute(queries.COUNT_VISITANTES)
            return cursor.fetchone()[0]
        except sqlite3.Error:
            return 0

    
    def listar_ocupacao_total(self):
        """
        Retorna uma lista unificada de todos os veículos no pátio.
        Retorna: Lista de dicionários {'vaga', 'tipo', 'nome', 'placa', 'modelo', 'cor'}
        """
        cursor = self._get_cursor()
        lista_unificada = []
        try:
            cursor.execute(queries.SELECT_OCUPACAO_TOTAL)
            rows = cursor.fetchall()
            
            for row in rows:
                vaga, tipo, nome, placa, modelo, cor = row
                
                # Criamos um dicionário simples para o relatório
                veiculo_dict = {
                    "vaga": vaga,
                    "tipo": tipo,
                    "nome": nome,
                    "placa": placa,
                    "modelo": modelo if modelo else "---",
                    "cor": cor if cor else "---"
                }
                lista_unificada.append(veiculo_dict)
            
            return lista_unificada
        except sqlite3.Error as e:
            print(f"❌ Erro ao gerar relatório geral: {e}")
            return []