from src.utils.input_handler import get_valid_input
from src.utils.validations import validate_placa  # <--- CORREÇÃO: Usamos a validação de formato simples
from src.ui.components import header, show_success, show_error, show_warning

def registrar_entrada_morador(repositorio):
    header("CATRACA: ENTRADA MORADOR 🏡")
    
    # 1. Busca por Placa (Valida apenas se é AAA-0000)
    placa_busca, _ = get_valid_input("Digite a placa do morador: ", validate_placa)
    
    # Busca na lista (simulando leitura de tag/câmera)
    todos = repositorio.listar_moradores()
    
    # Procura o morador na lista
    morador = next((m for m in todos if m.placa == placa_busca), None)
    
    if not morador:
        show_warning("❌ Morador não encontrado no cadastro.")
        return

    # 2. Validação Lógica (Regra de Negócio: Já está dentro?)
    if morador.estacionado:
        show_warning(f"⚠️  O morador {morador.nome} já consta como DENTRO.")
        return

    # 3. Registro no Banco
    try:
        repositorio.registrar_entrada_morador(morador.placa) 
        
        vaga_msg = morador.vaga_id if morador.vaga_id else "Rotativa/Não atribuída"
        
        # O show_success fará a pausa necessária
        show_success(f"✅ Bem-vindo, {morador.nome}!\n   Vaga Fixa: {vaga_msg}")
        
    except Exception as e:
        show_error(f"❌ Erro ao registrar entrada: {e}")