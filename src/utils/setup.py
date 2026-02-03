"""
Utilitários de inicialização do sistema.
Carrega variáveis de ambiente e conecta ao banco.
Localização: src/utils/setup.py
"""
import os
import sys
from dotenv import load_dotenv 
from src.repositories.estacionamento_repository import EstacionamentoRepository
from src.classes.Estacionamento import Estacionamento
from src.ui.components import show_error

load_dotenv()

def inicializar_sistema():
    """
    Configura o ambiente.
    Retorna: (repo, estacionamento)
    """
    # 1. Banco de Dados
    db_filename = os.getenv("DB_FILENAME", "estacionamento.db")
    # Ajuste o caminho considerando que o script roda da raiz
    db_path = os.path.join("src", "db", db_filename)
    
    try:
        repo = EstacionamentoRepository(db_path)
    except Exception as e:
        show_error(f"Falha crítica ao conectar no Banco: {e}")
        sys.exit(1)

    # 2. Configurações de Negócio do Estacionamento
    try:
        cap_vis = int(os.getenv("CAPACIDADE_VISITANTES", 20))
        cap_mor = int(os.getenv("CAPACIDADE_MORADORES", 50))
        tempo = int(os.getenv("TIME_LIMIT_MINUTES", 120))
        nome = os.getenv("PARKING_NAME", "Condomínio Solar")
    except ValueError:
        show_error("Erro no .env: Valores numéricos inválidos.")
        sys.exit(1)

    # Cria a instância com os valores lidos
    estacionamento = Estacionamento(
        nome=nome,
        capacidade_visitantes=cap_vis,
        capacidade_moradores=cap_mor, 
        tempo_limite_minutos=tempo
    )
    
    return repo, estacionamento