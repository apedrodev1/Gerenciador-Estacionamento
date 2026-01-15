"""
Repositório Especializado: Moradores.
Lida apenas com a tabela 'moradores'.
"""
from src.repositories.base_repository import BaseRepository
from src.db import queries
from src.classes.Morador import Morador

class MoradorRepository(BaseRepository):
    
    def adicionar(self, morador: Morador):
        cursor = self._get_cursor()
        cursor.execute(queries.INSERT_MORADOR, (
            morador.nome, morador.placa, morador.cnh, 
            morador.modelo, morador.cor, morador.apartamento, morador.vaga_id
        ))

    def listar(self):
        cursor = self._get_cursor()
        lista = []
        try:
            cursor.execute(queries.SELECT_ALL_MORADORES)
            for row in cursor.fetchall():
                id_db, nome, placa, cnh, modelo, cor, apto, vaga, est_int = row
                m = Morador(id=id_db, nome=nome, placa=placa, cnh=cnh,
                            modelo=modelo, cor=cor, apartamento=apto, vaga_id=vaga, estacionado=bool(est_int))
                lista.append(m)
            return lista
        except Exception: return []

    def buscar_por_placa(self, placa):
        cursor = self._get_cursor()
        cursor.execute(queries.SELECT_MORADOR_BY_PLACA, (placa,))
        row = cursor.fetchone()
        if row:
            return Morador(id=row[0], nome=row[1], placa=row[2], cnh=row[3],
                           modelo=row[4], cor=row[5], apartamento=row[6], 
                           vaga_id=row[7], estacionado=bool(row[8]))
        return None

    def atualizar(self, morador: Morador):
        cursor = self._get_cursor()
        cursor.execute(queries.UPDATE_MORADOR, (
            morador.nome, morador.placa, morador.cnh, morador.modelo, 
            morador.cor, morador.apartamento, morador.vaga_id, morador.id
        ))

    def remover(self, id):
        cursor = self._get_cursor()
        cursor.execute(queries.DELETE_MORADOR, (id,))

    def registrar_entrada(self, placa):
        cursor = self._get_cursor()
        cursor.execute(queries.REGISTRAR_ENTRADA_MORADOR, (placa,))

    def registrar_saida(self, placa):
        cursor = self._get_cursor()
        cursor.execute(queries.REGISTRAR_SAIDA_MORADOR, (placa,))