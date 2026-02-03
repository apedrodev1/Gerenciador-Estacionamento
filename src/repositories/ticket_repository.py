"""
Repositório Especializado: Tickets (Catraca).
Responsabilidade: Gerenciar a ocupação das vagas rotativas (Zona A).
Lida com a tabela 'tickets_visitantes'.
Localização: src/repositories/ticket_repository.py
"""
from datetime import datetime
from src.repositories.base_repository import BaseRepository
from src.db import queries
from src.classes.Visitante.TicketVisitante import TicketVisitante

class TicketRepository(BaseRepository):
    
    def criar_ticket(self, ticket: TicketVisitante):
        """
        Gera um novo ticket de entrada.
        Retorna o ID gerado.
        """
        cursor = self._get_cursor()
        
        # Garante formato de data string para o SQLite
        data_iso = ticket.entrada.isoformat() if isinstance(ticket.entrada, datetime) else ticket.entrada
        
        cursor.execute(queries.INSERT_TICKET, (
            ticket.placa,
            ticket.numero_vaga,
            data_iso,
            ticket.id_visitante # Opcional (int ou None)
        ))
        return cursor.lastrowid

    def vincular_cadastro_a_ticket(self, placa, id_visitante):
        """
        Atualiza tickets ativos desta placa, vinculando-os ao visitante recém-criado.
        Usado quando um visitante se cadastra após entrar com veículo.
        """
        cursor = self._get_cursor()
        sql = "UPDATE tickets_visitantes SET id_visitante = ? WHERE placa = ?"
        cursor.execute(sql, (id_visitante, placa))
        self.conn.commit()

    def buscar_ticket_ativo(self, placa):
        """
        Verifica se existe um ticket ABERTO para esta placa.
        Usado na saída para calcular o tempo.
        """
        cursor = self._get_cursor()
        cursor.execute(queries.SELECT_TICKET_ATIVO, (placa,))
        row = cursor.fetchone()
        
        if row:
            # Row: id, placa, numero_vaga, entrada, id_visitante
            return TicketVisitante(
                id=row[0],
                placa=row[1],
                numero_vaga=row[2],
                entrada=row[3], # A classe já trata a conversão de str->datetime
                id_visitante=row[4]
            )
        return None

    def listar_tickets_ativos(self):
        """
        Retorna todos os carros que estão ocupando vagas rotativas agora.
        """
        cursor = self._get_cursor()
        cursor.execute(queries.SELECT_ALL_TICKETS)
        lista = []
        
        for row in cursor.fetchall():
            t = TicketVisitante(
                id=row[0],
                placa=row[1],
                numero_vaga=row[2],
                entrada=row[3],
                id_visitante=row[4]
            )
            lista.append(t)
        return lista

    def listar_vagas_ocupadas(self):
        """
        Retorna uma lista (set) de strings com os números das vagas ocupadas.
        Ex: {'1', '5', '12'}
        Vital para o Estacionamento saber onde alocar o próximo.
        """
        cursor = self._get_cursor()
        cursor.execute(queries.SELECT_VAGAS_OCUPADAS_VISITANTES)
        # Retorna lista de strings para facilitar a comparação no Estacionamento
        return {str(row[0]) for row in cursor.fetchall()}

    def remover_ticket(self, id_ticket):
        """
        Remove o ticket (Processo de Saída).
        Nota: O log de histórico e a atualização do veículo são feitos 
        pelo VeiculoRepository, chamado pelo Controller.
        """
        cursor = self._get_cursor()
        cursor.execute(queries.DELETE_TICKET, (id_ticket,))