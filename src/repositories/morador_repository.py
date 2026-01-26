"""
Repositório Especializado: Moradores.
Lida apenas com a tabela 'moradores' (Dados Pessoais).
Não manipula veículos ou catraca.
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
            morador.apartamento
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
                # Row: (id, nome, cnh, apartamento)
                m = Morador(
                    id=row[0], 
                    nome=row[1], 
                    cnh=row[2], 
                    apartamento=row[3]
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
                apartamento=row[3]
            )
        return None

    def buscar_por_apartamento(self, numero_apto):
        """
        Retorna uma lista de Moradores vinculados a este apartamento.
        Útil para saber quem é o dono atual do imóvel.
        """
        cursor = self._get_cursor()
        # Nota: A query SELECT_MORADORES_BY_APTO precisa existir no queries.py
        # Vou assumir que ela é: "SELECT * FROM moradores WHERE apartamento = ?"
        cursor.execute(queries.SELECT_MORADORES_BY_APTO, (int(numero_apto),))
        
        lista = []
        for row in cursor.fetchall():
            m = Morador(id=row[0], nome=row[1], cnh=row[2], apartamento=row[3])
            lista.append(m)
        return lista

    def listar_apartamentos_ocupados(self):
        """
        Retorna um SET com todos os números de apartamentos que já possuem cadastro.
        Ex: {101, 102, 504}
        Similar ao listar_todas_cnhs(), usado para validação rápida.
        """
        cursor = self._get_cursor()
        try:
            cursor.execute("SELECT DISTINCT apartamento FROM moradores")
            # Retorna um conjunto de inteiros
            return {row[0] for row in cursor.fetchall()}
        except Exception:
            return set()

    def atualizar(self, morador: Morador):
        """Atualiza apenas os dados pessoais e endereço."""
        cursor = self._get_cursor()
        cursor.execute(queries.UPDATE_MORADOR, (
            morador.nome, 
            morador.cnh, 
            morador.apartamento, 
            morador.id
        ))

    def remover(self, id):
        """
        Remove o morador.
        Nota: O banco está configurado com CASCADE, então 
        os veículos deste morador serão apagados automaticamente.
        """
        cursor = self._get_cursor()
        cursor.execute(queries.DELETE_MORADOR, (id,))