"""
Repositório Especializado: Visitantes Cadastrados.
Responsabilidade: CRUD de PESSOAS (Visitantes Frequentes/Prestadores).
Não lida com veículos ou tickets de catraca.
Localização: src/repositories/visitante_repository.py
"""
from src.repositories.base_repository import BaseRepository
from src.db import queries
from src.classes.visitante.Visitante import Visitante

class VisitanteRepository(BaseRepository):
    
    def adicionar(self, visitante: Visitante):
        """
        Salva um novo visitante (pessoa) no banco.
        Retorna: O ID (int) gerado, necessário para vincular veículos.
        """
        cursor = self._get_cursor()
        
        # O ID é None na entrada, gerado pelo banco
        # A data_cadastro já vem preenchida pelo __init__ da classe se não informada
        cursor.execute(queries.INSERT_VISITANTE_CADASTRO, (
            visitante.nome,
            visitante.cnh,
            visitante.data_cadastro
        ))
        return cursor.lastrowid

    def listar(self):
        """Retorna lista de todos os visitantes cadastrados."""
        cursor = self._get_cursor()
        lista = []
        try:
            cursor.execute(queries.SELECT_ALL_VISITANTES)
            for row in cursor.fetchall():
                # Row: id, nome, cnh, data_cadastro
                v = Visitante(
                    id=row[0],
                    nome=row[1],
                    cnh=row[2],
                    data_cadastro=row[3]
                )
                lista.append(v)
            return lista
        except Exception as e:
            print(f"Erro ao listar visitantes: {e}")
            return []

    def buscar_por_id(self, id_visitante):
        """Busca um visitante específico pelo ID."""
        cursor = self._get_cursor()
        cursor.execute(queries.SELECT_VISITANTE_BY_ID, (id_visitante,))
        row = cursor.fetchone()
        
        if row:
            return Visitante(
                id=row[0],
                nome=row[1],
                cnh=row[2],
                data_cadastro=row[3]
            )
        return None

    def atualizar(self, visitante: Visitante):
        """Atualiza dados pessoais (Nome, CNH)."""
        cursor = self._get_cursor()
        cursor.execute(queries.UPDATE_VISITANTE, (
            visitante.nome,
            visitante.cnh,
            visitante.id
        ))

    def remover(self, id_visitante):
        """
        Remove o cadastro da pessoa.
        Graças ao ON DELETE CASCADE no banco, os veículos vinculados
        a este ID também serão removidos automaticamente.
        """
        cursor = self._get_cursor()
        cursor.execute(queries.DELETE_VISITANTE, (id_visitante,))