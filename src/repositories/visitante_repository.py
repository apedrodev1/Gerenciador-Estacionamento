"""
Repositório Especializado: Visitantes.
Lida com 'visitantes' (rotativo) e 'visitantes_cadastrados' (frequentes).
Localização: src/repositories/visitante_repository.py
"""
from datetime import datetime
from src.repositories.base_repository import BaseRepository
from src.db import queries

from src.classes.Visitante.VisitanteControle import VisitanteCatraca
from src.classes.Visitante.VisitanteCadastro import VisitanteCadastro

class VisitanteRepository(BaseRepository):
    
    # --- VISITANTES FREQUENTES (CADASTRO) ---

    def adicionar_cadastro(self, v: VisitanteCadastro):
        cursor = self._get_cursor()
        cursor.execute(queries.INSERT_VISITANTE_CADASTRO, (
            v.nome, v.placa, v.cnh, v.modelo, v.cor, v.data_cadastro
        ))

    def listar_cadastros(self):
        cursor = self._get_cursor()
        lista = []
        try:
            cursor.execute(queries.SELECT_ALL_VISITANTES_CADASTRO)
            for row in cursor.fetchall():
                v = VisitanteCadastro(id=row[0], nome=row[1], placa=row[2], cnh=row[3],
                                      modelo=row[4], cor=row[5], data_cadastro=row[6])
                lista.append(v)
            return lista
        except Exception as e:
            print(f"❌ Erro ao listar cadastros: {e}")
            return []

    def buscar_cadastro_por_placa(self, placa):
        cursor = self._get_cursor()
        try:
            cursor.execute(queries.SELECT_VISITANTE_CADASTRO_BY_PLACA, (placa,))
            row = cursor.fetchone()
            if row:
                return VisitanteCadastro(id=row[0], nome=row[1], placa=row[2], cnh=row[3],
                                         modelo=row[4], cor=row[5], data_cadastro=row[6])
            return None
        except Exception as e:
            print(f"❌ Erro ao buscar cadastro: {e}")
            return None

    def atualizar_cadastro(self, v: VisitanteCadastro):
        cursor = self._get_cursor()
        cursor.execute(queries.UPDATE_VISITANTE_CADASTRO, (
            v.nome, v.cnh, v.modelo, v.cor, v.id
        ))

    def remover_cadastro(self, id):
        cursor = self._get_cursor()
        cursor.execute(queries.DELETE_VISITANTE_CADASTRO, (id,))

    # --- VISITANTES ATIVOS (CATRACA) ---

    def registrar_entrada(self, v: VisitanteCatraca):
        cursor = self._get_cursor()
        data_iso = v.entrada.isoformat()
        cursor.execute(queries.INSERT_VISITANTE, (
            v.nome, v.placa, v.cnh, v.modelo, v.cor, data_iso, v.numero_vaga
        ))
        # Log Automático
        self._registrar_log(v.placa, "VISITANTE", "ENTRADA")

    def registrar_saida(self, id):
        # Precisamos buscar a placa antes de deletar para poder logar!
        # Pequena lógica extra aqui:
        cursor = self._get_cursor()
        
        # 1. Descobre a placa
        placa_temp = "DESCONHECIDA"
        try:
            cursor.execute("SELECT placa FROM visitantes WHERE id = ?", (id,))
            row = cursor.fetchone()
            if row: placa_temp = row[0]
        except: pass

        # 2. Deleta
        cursor.execute(queries.DELETE_VISITANTE, (id,))
        
        # 3. Loga
        self._registrar_log(placa_temp, "VISITANTE", "SAIDA")
        
    def listar_ativos(self):
        """Retorna lista de visitantes NO PÁTIO."""
        cursor = self._get_cursor()
        lista = []
        
        # Sem try/except genérico para facilitar o debug
        cursor.execute(queries.SELECT_ALL_VISITANTES)
        rows = cursor.fetchall()
        
        for row in rows:
            # id, nome, placa, cnh, modelo, cor, ent, vaga
            id_db, nome, placa, cnh, modelo, cor, ent, vaga = row
            
            try:
                data_entrada = datetime.fromisoformat(ent)
            except ValueError: 
                data_entrada = datetime.now()

            # Instancia a classe correta: VisitanteCatraca
            v = VisitanteCatraca(
                id=id_db, 
                nome=nome, 
                placa=placa, 
                cnh=cnh, 
                modelo=modelo, 
                cor=cor, 
                entrada=data_entrada, 
                numero_vaga=vaga
            )
            lista.append(v)
            
        return lista

    def buscar_ativos_por_placa(self, placa):
        cursor = self._get_cursor()
        try:
            cursor.execute(queries.SELECT_VISITANTE_BY_PLACA, (placa,))
            row = cursor.fetchone()
            if row:
                id, nome, p_db, cnh, mod, cor, ent, vaga = row
                
                try:
                    data_entrada = datetime.fromisoformat(ent)
                except ValueError:
                    data_entrada = datetime.now()

                # CORREÇÃO AQUI: Usar VisitanteCatraca (igual ao import)
                return VisitanteCatraca(id=id, nome=nome, placa=p_db, cnh=cnh, 
                                        modelo=mod, cor=cor, entrada=data_entrada, numero_vaga=vaga)
            return None
        except Exception as e:
            print(f"❌ Erro ao buscar ativo: {e}")
            return None

    def buscar_vagas_ocupadas(self):
        cursor = self._get_cursor()
        try:
            cursor.execute(queries.SELECT_VAGAS_OCUPADAS)
            return [str(row[0]) for row in cursor.fetchall()]
        except Exception: return []

    def contar_ativos(self):
        cursor = self._get_cursor()
        try:
            cursor.execute(queries.COUNT_VISITANTES)
            return cursor.fetchone()[0]
        except Exception: return 0