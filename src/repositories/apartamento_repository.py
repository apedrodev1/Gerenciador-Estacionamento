"""
Repositório Especializado: Apartamentos.
Responsabilidade: Gerenciar a tabela 'apartamentos' e garantir unicidade das unidades.
Localização: src/repositories/apartamento_repository.py
"""
from src.repositories.base_repository import BaseRepository
from src.db import queries
from src.classes.Apartamento import Apartamento

class ApartamentoRepository(BaseRepository):
    
    def adicionar(self, apto: Apartamento):
        """
        Cadastra um novo apartamento no sistema.
        Retorna o ID gerado ou None se houver erro (ex: duplicidade).
        """
        cursor = self._get_cursor()
        try:
            cursor.execute(queries.INSERT_APARTAMENTO, (
                apto.numero, 
                apto.bloco, 
                apto.vagas
            ))
            return cursor.lastrowid
        except Exception as e:
            # Geralmente erro de UNIQUE constraint (Já existe esse Número+Bloco)
            print(f"⚠️ Erro ao criar apartamento {apto.numero}-{apto.bloco}: {e}")
            return None

    def listar(self):
        """Retorna todos os apartamentos cadastrados, ordenados por número."""
        cursor = self._get_cursor()
        lista = []
        try:
            cursor.execute(queries.SELECT_ALL_APARTAMENTOS)
            for row in cursor.fetchall():
                # Row: id, numero, bloco, vagas
                lista.append(Apartamento(id=row[0], numero=row[1], bloco=row[2], vagas=row[3]))
            return lista
        except Exception as e:
            print(f"Erro ao listar apartamentos: {e}")
            return []

    def buscar_por_rotulo(self, numero, bloco=""):
        """
        Busca um apartamento pela sua identificação visual (Número + Bloco).
        Essencial para o cadastro de moradores: "Se já existe, usa esse ID".
        """
        cursor = self._get_cursor()
        
        # Garante que None vire string vazia para bater com o banco
        b = bloco if bloco else ""
        
        cursor.execute(queries.SELECT_APARTAMENTO_BY_NUM_BLOCO, (str(numero), str(b)))
        row = cursor.fetchone()
        
        if row:
            return Apartamento(id=row[0], numero=row[1], bloco=row[2], vagas=row[3])
        return None
        
    def buscar_por_id(self, id_apto):
        """Busca pelo ID interno (FK)."""
        cursor = self._get_cursor()
        cursor.execute(queries.SELECT_APARTAMENTO_BY_ID, (id_apto,))
        row = cursor.fetchone()
        
        if row:
            return Apartamento(id=row[0], numero=row[1], bloco=row[2], vagas=row[3])
        return None


    def contar_vagas_ocupadas(self, id_apartamento):
        """
        Retorna o número total de veículos vinculados a este apartamento.
        Faz um JOIN direto no banco, muito mais rápido e limpo que loops em Python.
        """
        cursor = self._get_cursor()
        try:
            cursor.execute(queries.SELECT_COUNT_VEICULOS_BY_APTO_ID, (id_apartamento,))
            row = cursor.fetchone()
            return row[0] if row else 0
        except Exception as e:
            print(f"Erro ao contar vagas do apto {id_apartamento}: {e}")
            return 0