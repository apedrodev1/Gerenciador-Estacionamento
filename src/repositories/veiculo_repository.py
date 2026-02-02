"""
Repositório Especializado: Veículos.
Responsabilidade: CRUD de carros e Execução de Movimentação (Entrada/Saída).
Lida com a tabela 'veiculos' e registra logs em 'historico_movimentacao'.
Localização: src/repositories/veiculo_repository.py
"""
from datetime import datetime
from src.repositories.base_repository import BaseRepository
from src.db import queries
from src.classes.Veiculo import Veiculo

class VeiculoRepository(BaseRepository):
    
    def adicionar(self, veiculo: Veiculo):
        """
        Salva um veículo novo e vincula ao ID do dono.
        """
        cursor = self._get_cursor()
        cursor.execute(queries.INSERT_VEICULO, (
            veiculo.placa,
            veiculo.modelo,
            veiculo.cor,
            veiculo.morador_id,   # Pode ser int ou None
            veiculo.visitante_id, # Pode ser int ou None
            int(veiculo.estacionado)
        ))

    def buscar_por_placa(self, placa):
        """
        Busca veiculo pela placa.
        Retorna: Objeto Veiculo (se cadastrado) ou None (se não existir).
        """
        cursor = self._get_cursor()
        cursor.execute(queries.SELECT_VEICULO_BY_PLACA, (placa,))
        row = cursor.fetchone()
        
        if row:
            # Mapeamento do banco para o objeto
            return Veiculo(
                id=row[0],
                placa=row[1],
                modelo=row[2],
                cor=row[3],
                estacionado=bool(row[4]),
                morador_id=row[5],
                visitante_id=row[6]
            )
        return None

    def listar_por_morador(self, id_morador):
        """Retorna lista de veículos de um morador específico."""
        cursor = self._get_cursor()
        cursor.execute(queries.SELECT_VEICULOS_BY_MORADOR_ID, (id_morador,))
        lista = []
        for row in cursor.fetchall():
            v = Veiculo(
                id=row[0], placa=row[1], modelo=row[2], cor=row[3],
                estacionado=bool(row[4]), morador_id=row[5], visitante_id=row[6]
            )
            lista.append(v)
        return lista

    def listar_por_visitante(self, id_visitante):
        """Retorna lista de veículos de um visitante específico."""
        cursor = self._get_cursor()
        cursor.execute(queries.SELECT_VEICULOS_BY_VISITANTE_ID, (id_visitante,))
        lista = []
        for row in cursor.fetchall():
            v = Veiculo(
                id=row[0], 
                placa=row[1], 
                modelo=row[2], 
                cor=row[3],
                estacionado=bool(row[4]), 
                morador_id=row[5], 
                visitante_id=row[6]
            )
            lista.append(v)
        return lista

    def listar_todas_placas(self):
        """Retorna lista de placas (strings) para validação de unicidade."""
        cursor = self._get_cursor()
        cursor.execute(queries.SELECT_ALL_PLACAS)
        return [row[0] for row in cursor.fetchall()]

    def atualizar(self, veiculo: Veiculo):
        """Atualiza dados do carro (modelo, cor, vínculos)."""
        cursor = self._get_cursor()
        cursor.execute(queries.UPDATE_VEICULO, (
            veiculo.modelo,
            veiculo.cor,
            veiculo.morador_id,
            veiculo.visitante_id,
            veiculo.placa # WHERE placa = ?
        ))

    def remover(self, placa):
        """Remove o veículo do banco."""
        cursor = self._get_cursor()
        cursor.execute(queries.DELETE_VEICULO, (placa,))

    # --- MÉTODOS DE MOVIMENTAÇÃO (COM LOG) ---

    def registrar_entrada(self, placa, tipo_dono="DESCONHECIDO"):
        """
        Altera status para Estacionado e gera log de Histórico.
        Nota: Só deve ser chamado se o carro JÁ existir no banco.
        """
        cursor = self._get_cursor()
        
        # 1. Atualiza Status na tabela Veiculos
        cursor.execute(queries.SET_VEICULO_ESTACIONADO, (placa,))
        
        # 2. Grava Log na tabela Histórico
        self._registrar_log(placa, tipo_dono, "ENTRADA")

    def registrar_saida(self, placa, tipo_dono="DESCONHECIDO"):
        """
        Altera status para Fora e gera log de Histórico.
        """
        cursor = self._get_cursor()
        
        # 1. Atualiza Status na tabela Veiculos
        cursor.execute(queries.SET_VEICULO_SAIDA, (placa,))
        
        # 2. Grava Log na tabela Histórico
        self._registrar_log(placa, tipo_dono, "SAIDA")

    # --- MÉTODO PRIVADO AUXILIAR ---

    def registrar_log_visitante(self, placa, evento):
        """
        Apenas grava o histórico (Usado para visitantes com ou sem cadastro).
        Não tenta atualizar status na tabela veiculos para evitar erros com avulsos.
        """
        # Define se é VISITANTE ou AVULSO (apenas para ficar bonito no relatório)
        # Se quiser simplificar, pode mandar sempre "VISITANTE"
        tipo = "VISITANTE" 
        self._registrar_log(placa, tipo, evento)
    
    def _registrar_log(self, placa, tipo_veiculo, evento):
        """Insere registro na tabela de auditoria."""
        try:
            cursor = self._get_cursor()
            agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(queries.INSERT_HISTORICO, (
                agora, 
                placa, 
                tipo_veiculo, # Ex: "MORADOR", "VISITANTE"
                evento        # "ENTRADA" ou "SAIDA"
            ))
        except Exception as e:
            print(f"⚠️ Erro ao gravar log de histórico: {e}")