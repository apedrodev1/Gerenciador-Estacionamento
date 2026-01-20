"""
Repositório Especializado: Moradores.
Lida apenas com a tabela 'moradores'.
Localização: src/repositories/morador_repository.py
"""
from src.repositories.base_repository import BaseRepository
from src.db import queries
from src.classes.Morador import Morador

class MoradorRepository(BaseRepository):
    
    def adicionar(self, morador: Morador):
        cursor = self._get_cursor()
        # Nota: Passamos vaga_id como None se não existir, ou o valor que tiver
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
        # Log Automático
        self._registrar_log(placa, "MORADOR", "ENTRADA")

    def registrar_saida(self, placa):
        cursor = self._get_cursor()
        cursor.execute(queries.REGISTRAR_SAIDA_MORADOR, (placa,))
        # Log Automático
        self._registrar_log(placa, "MORADOR", "SAIDA")

    # --- MÉTODOS NOVOS (COTA E CONTAGEM) ---

    def contar_carros_no_apto(self, numero_apto):
        """Conta quantos carros deste apartamento estão NO PÁTIO (estacionado=1)."""
        cursor = self._get_cursor()
        try:
            query = "SELECT COUNT(*) FROM moradores WHERE apartamento = ? AND estacionado = 1"
            cursor.execute(query, (numero_apto,))
            return cursor.fetchone()[0]
        except Exception as e:
            print(f"❌ Erro ao contar carros do apto: {e}")
            return 0

    def contar_moradores_estacionados(self):
        """Conta o total GERAL de moradores dentro do estacionamento."""
        cursor = self._get_cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM moradores WHERE estacionado = 1")
            return cursor.fetchone()[0]
        except Exception:
            return 0