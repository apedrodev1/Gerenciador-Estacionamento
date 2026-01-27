"""
Repositório Especializado: Moradores.
Lida apenas com a tabela 'moradores' (Dados Pessoais).
Localização: src/repositories/morador_repository.py
"""
from src.repositories.base_repository import BaseRepository
from src.db import queries
from src.classes.Morador import Morador

class MoradorRepository(BaseRepository):
    
    def adicionar(self, morador: Morador):
        """
        Salva um novo morador no banco.
        Retorna: O ID (int) gerado pelo banco de dados.
        """
        cursor = self._get_cursor()
        cursor.execute(queries.INSERT_MORADOR, (
            morador.nome, 
            morador.cnh, 
            morador.id_apartamento # AGORA USAMOS O ID (FK)
        ))
        # Importante: Retornamos o ID para vincular o veículo em seguida
        return cursor.lastrowid

    def listar(self):
        """Retorna lista de objetos Morador."""
        cursor = self._get_cursor()
        lista = []
        try:
            cursor.execute(queries.SELECT_ALL_MORADORES)
            for row in cursor.fetchall():
                # Row: (id, nome, cnh, id_apartamento)
                m = Morador(
                    id=row[0], 
                    nome=row[1], 
                    cnh=row[2], 
                    id_apartamento=row[3] # Mapeando a FK
                )
                lista.append(m)
            return lista
        except Exception as e:
            print(f"Erro ao listar moradores: {e}")
            return []

    def buscar_por_id(self, id_morador):
        """Busca um morador específico pelo ID."""
        cursor = self._get_cursor()
        cursor.execute(queries.SELECT_MORADOR_BY_ID, (id_morador,))
        row = cursor.fetchone()
        
        if row:
            return Morador(
                id=row[0], 
                nome=row[1], 
                cnh=row[2], 
                id_apartamento=row[3]
            )
        return None

    def buscar_por_id_apartamento(self, id_apartamento):
        """
        Retorna uma lista de Moradores vinculados a um ID de Apartamento.
        Nota: Recebe o ID do banco (ex: 5), não o número (ex: 101).
        """
        cursor = self._get_cursor()
        cursor.execute(queries.SELECT_MORADORES_BY_APTO_ID, (id_apartamento,))
        
        lista = []
        for row in cursor.fetchall():
            m = Morador(
                id=row[0], 
                nome=row[1], 
                cnh=row[2], 
                id_apartamento=row[3]
            )
            lista.append(m)
        return lista

    def listar_ids_apartamentos_ocupados(self):
        """
        Retorna um SET com os IDs de apartamentos que possuem moradores.
        Útil para saber quais unidades estão habitadas.
        """
        cursor = self._get_cursor()
        try:
            cursor.execute("SELECT DISTINCT id_apartamento FROM moradores")
            return {row[0] for row in cursor.fetchall()}
        except Exception:
            return set()

    def atualizar(self, morador: Morador):
        """Atualiza dados pessoais e vínculo de moradia."""
        cursor = self._get_cursor()
        cursor.execute(queries.UPDATE_MORADOR, (
            morador.nome, 
            morador.cnh, 
            morador.id_apartamento, # Atualiza a FK se ele mudar de apto
            morador.id
        ))

    def remover(self, id):
        """Remove o morador (Cascade apaga veículos)."""
        cursor = self._get_cursor()
        cursor.execute(queries.DELETE_MORADOR, (id,))