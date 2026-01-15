"""
Módulo de utilitários contendo funções de validação para entrada de dados.
"""
import re

# --- Validações Gerais de Entrada ---

def validate_names(name):
    """Valida se o nome contém apenas letras e espaços."""
    cleaned = name.strip().title() # Title deixa a primeira letra Maiúscula
    # Verifica se tem caracteres válidos (letras e espaços)
    if cleaned and all(x.isalpha() or x.isspace() for x in cleaned):
        return cleaned, None
    return None, "O nome deve conter apenas letras."

def validate_yes_no(input_value):
    """Valida entradas 's'/'n' ou 'y'/'n'."""
    cleaned = input_value.strip().lower()
    if cleaned in ['s', 'n', 'y']:
        return cleaned, None
    return None, "Por favor, digite apenas 's' (sim) ou 'n' (não)."

# --- Novas Validações para o Estacionamento ---

def validate_placa(placa_input):
    """
    Valida placas nos formatos:
    - Antigo: AAA-1234 (ou AAA1234)
    - Mercosul: AAA1A23
    """
    # Remove hífens e espaços, e joga para maiúsculo
    limpa = placa_input.replace("-", "").strip().upper()

    # Regex que aceita os dois padrões (3 letras + 4 números OU 3 letras + 1 num + 1 letra + 2 nums)
    # Padrão: ^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$
    padrao_mercosul_ou_antigo = r'^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$'

    if re.match(padrao_mercosul_ou_antigo, limpa):
        return limpa, None # Retorna a placa limpa (sem hífen)
    
    return None, "Placa inválida. Use o formato AAA-1234 ou Mercosul."


# ... (conteúdo anterior de validações de formato) ...

def validate_placa_unica(placa_input, placas_existentes):
    """
    Valida formato E unicidade da placa.
    Args:
        placa_input (str): A placa digitada.
        placas_existentes (list): Lista de strings com todas as placas do banco.
    """
    # 1. Valida Formato
    placa_limpa, erro_formato = validate_placa(placa_input)
    
    if erro_formato:
        return None, erro_formato

    # 2. Valida Unicidade
    if placa_limpa in placas_existentes:
        return None, f"A placa {placa_limpa} JÁ ESTÁ CADASTRADA no sistema."

    return placa_limpa, None

def validate_cnh(cnh_input):
    """
    Valida formato da CNH (apenas dígitos).
    Para este projeto, vamos checar se tem 11 dígitos numéricos.
    """
    limpa = str(cnh_input).strip()
    
    if not limpa.isdigit():
        return None, "A CNH deve conter apenas números."
    
    if len(limpa) != 11:
        return None, f"A CNH deve ter 11 dígitos (você digitou {len(limpa)})."
    
    return limpa, None

def validate_cnh_unica(cnh_input, cnhs_existentes):
    """
    Valida formato E unicidade da CNH.
    Args:
        cnh_input (str): A CNH digitada.
        cnhs_existentes (list): Lista de strings com todas as CNHs do banco.
    """
    # 1. Valida Formato
    cnh_limpa, erro_formato = validate_cnh(cnh_input)
    
    if erro_formato:
        return None, erro_formato

    # 2. Valida Unicidade
    if cnh_limpa in cnhs_existentes:
        return None, f"A CNH {cnh_limpa} JÁ PERTENCE a outro cadastro."

    return cnh_limpa, None


def validate_apartamento(apto_input):
    """
    Valida o número/bloco do apartamento.
    Aceita números ou combinações curtas (ex: '102', '12B', 'Cobertura').
    """
    limpa = str(apto_input).strip().upper()
    
    if not limpa:
        return None, "O apartamento não pode estar vazio."
        
    if len(limpa) > 6:
        return None, "O identificador do apartamento é muito longo (máx 6 chars)."
        
    return limpa, None