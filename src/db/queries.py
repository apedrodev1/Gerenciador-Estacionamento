"""
Módulo de Queries SQL (Refatorado).
Reflete a nova arquitetura: Morador (Pessoa) | Veículo (Carro) | Ticket (Catraca).
"""

# ==============================================================================
# 1. CRIAÇÃO DE TABELAS (DDL)
# ==============================================================================

# Agora só guarda a PESSOA e o IMÓVEL
CREATE_TABLE_MORADORES = """
CREATE TABLE IF NOT EXISTS moradores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cnh TEXT NOT NULL,
    apartamento INTEGER NOT NULL
);
"""

# Tabela nova para as PESSOAS visitantes (Parentes, Prestadores)
CREATE_TABLE_VISITANTES_CADASTRO = """
CREATE TABLE IF NOT EXISTS visitantes_cadastrados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cnh TEXT NOT NULL,
    data_cadastro TEXT
);
"""

# A Tabela Central: Liga o carro ao dono (Morador ou Visitante)
CREATE_TABLE_VEICULOS = """
CREATE TABLE IF NOT EXISTS veiculos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    placa TEXT UNIQUE NOT NULL,
    modelo TEXT,
    cor TEXT,
    estacionado INTEGER DEFAULT 0, -- 0=Fora, 1=Dentro
    morador_id INTEGER,
    visitante_id INTEGER,
    FOREIGN KEY(morador_id) REFERENCES moradores(id) ON DELETE CASCADE,
    FOREIGN KEY(visitante_id) REFERENCES visitantes_cadastrados(id) ON DELETE CASCADE
);
"""

# Tabela de Operação (Quem está na vaga rotativa AGORA)
CREATE_TABLE_TICKETS = """
CREATE TABLE IF NOT EXISTS tickets_visitantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    placa TEXT NOT NULL,
    numero_vaga INTEGER,
    entrada TEXT NOT NULL,      -- ISO Format
    id_visitante INTEGER,       -- Opcional: Link se for alguém cadastrado
    FOREIGN KEY(id_visitante) REFERENCES visitantes_cadastrados(id)
);
"""

CREATE_TABLE_HISTORICO = """
CREATE TABLE IF NOT EXISTS historico_movimentacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_hora TEXT NOT NULL,
    placa TEXT NOT NULL,
    tipo_veiculo TEXT,  -- 'MORADOR', 'VISITANTE_CADASTRO', 'AVULSO'
    tipo_evento TEXT    -- 'ENTRADA' ou 'SAIDA'
);
"""


# ==============================================================================
# 2. MORADORES (CRUD)
# ==============================================================================

INSERT_MORADOR = "INSERT INTO moradores (nome, cnh, apartamento) VALUES (?, ?, ?);"

SELECT_ALL_MORADORES = "SELECT * FROM moradores ORDER BY apartamento;"

SELECT_MORADOR_BY_ID = "SELECT * FROM moradores WHERE id = ?;"

# Busca útil para validação de cadastro (evitar duplicidade no apto se for regra)
SELECT_MORADORES_BY_APTO = "SELECT * FROM moradores WHERE apartamento = ?;"

UPDATE_MORADOR = "UPDATE moradores SET nome=?, cnh=?, apartamento=? WHERE id=?;"

DELETE_MORADOR = "DELETE FROM moradores WHERE id=?;"


# ==============================================================================
# 3. VISITANTES (CADASTRO PESSOA)
# ==============================================================================

INSERT_VISITANTE_CADASTRO = "INSERT INTO visitantes_cadastrados (nome, cnh, data_cadastro) VALUES (?, ?, ?);"

SELECT_ALL_VISITANTES = "SELECT * FROM visitantes_cadastrados ORDER BY nome;"

SELECT_VISITANTE_BY_ID = "SELECT * FROM visitantes_cadastrados WHERE id = ?;"

UPDATE_VISITANTE = "UPDATE visitantes_cadastrados SET nome=?, cnh=? WHERE id=?;"

DELETE_VISITANTE = "DELETE FROM visitantes_cadastrados WHERE id=?;"


# ==============================================================================
# 4. VEÍCULOS (CRUD + OPERAÇÃO)
# ==============================================================================

INSERT_VEICULO = """
INSERT INTO veiculos (placa, modelo, cor, morador_id, visitante_id, estacionado)
VALUES (?, ?, ?, ?, ?, ?);
"""

SELECT_VEICULO_BY_PLACA = "SELECT * FROM veiculos WHERE placa = ?;"

# Listar todos os carros de um morador específico
SELECT_VEICULOS_BY_MORADOR_ID = "SELECT * FROM veiculos WHERE morador_id = ?;"

# Listar todas as placas (para validação de unicidade)
SELECT_ALL_PLACAS = "SELECT placa FROM veiculos;"

UPDATE_VEICULO = """
UPDATE veiculos SET modelo=?, cor=?, morador_id=?, visitante_id=? WHERE placa=?;
"""

DELETE_VEICULO = "DELETE FROM veiculos WHERE placa=?;"

# --- Operação de Catraca (Status) ---
SET_VEICULO_ESTACIONADO = "UPDATE veiculos SET estacionado = 1 WHERE placa = ?;"
SET_VEICULO_SAIDA = "UPDATE veiculos SET estacionado = 0 WHERE placa = ?;"


# ==============================================================================
# 5. TICKETS (CATRACA VISITANTE)
# ==============================================================================

INSERT_TICKET = """
INSERT INTO tickets_visitantes (placa, numero_vaga, entrada, id_visitante)
VALUES (?, ?, ?, ?);
"""

# Verifica se existe ticket aberto para esta placa
SELECT_TICKET_ATIVO = "SELECT * FROM tickets_visitantes WHERE placa = ?;"

SELECT_ALL_TICKETS = "SELECT * FROM tickets_visitantes;"

SELECT_VAGAS_OCUPADAS_VISITANTES = "SELECT numero_vaga FROM tickets_visitantes;"

DELETE_TICKET = "DELETE FROM tickets_visitantes WHERE id=?;"


# ==============================================================================
# 6. RELATÓRIOS E MAPA (SUPER QUERY)
# ==============================================================================
# Esta query "monta" o cenário atual unindo as duas tabelas principais

SELECT_OCUPACAO_COMPLETA = """
-- 1. Veículos de Moradores (Estacionados)
SELECT 
    ('M' || (m.apartamento * 2) - 1) as vaga_ref, -- Apenas referência visual, lógica no código
    'MORADOR' as tipo,
    m.nome as proprietario,
    m.apartamento,
    v.placa,
    v.modelo,
    v.cor
FROM veiculos v
JOIN moradores m ON v.morador_id = m.id
WHERE v.estacionado = 1

UNION ALL

-- 2. Visitantes (Tickets Ativos)
SELECT 
    t.numero_vaga as vaga_ref,
    'VISITANTE' as tipo,
    COALESCE(vc.nome, 'AVULSO') as proprietario, -- Pega nome se tiver cadastro, senão 'Avulso'
    NULL as apartamento,
    t.placa,
    '---' as modelo, -- Ticket não guarda modelo obrigatoriamente
    '---' as cor
FROM tickets_visitantes t
LEFT JOIN visitantes_cadastrados vc ON t.id_visitante = vc.id;
"""

# ==============================================================================
# 7. HISTÓRICO
# ==============================================================================

INSERT_HISTORICO = """
INSERT INTO historico_movimentacao (data_hora, placa, tipo_veiculo, tipo_evento)
VALUES (?, ?, ?, ?);
"""

SELECT_HISTORICO_RECENTE = "SELECT * FROM historico_movimentacao ORDER BY id DESC LIMIT 50;"