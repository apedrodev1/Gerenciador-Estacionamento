"""
Módulo de Exibição de Relatórios.
Localização: src/functions/relatorios/exibir_relatorios.py
"""
from datetime import datetime
from src.ui.tables import criar_tabela
from src.ui.colors import Colors
from src.ui.components import header, show_warning, menu_option
from src.utils.input_handler import get_valid_input
from src.utils.validations import validate_placa

def _renderizar_tabela_historico(dados, titulo="HISTÓRICO"):
    """Função auxiliar para desenhar a tabela de histórico."""
    if not dados:
        show_warning("Nenhum registro encontrado para este filtro.")
        return

    linhas_formatadas = []
    for row in dados:
        # row = (data_iso, placa, tipo, evento)
        data_iso, placa, tipo, evento = row
        
        try:
            dt = datetime.fromisoformat(data_iso)
            data_fmt = dt.strftime("%d/%m/%Y %H:%M")
        except:
            data_fmt = data_iso

        evento_fmt = f"[green]{evento}[/green]" if evento == "ENTRADA" else f"[red]{evento}[/red]"
        tipo_fmt = f"[cyan]{tipo}[/cyan]" if tipo == "MORADOR" else f"[yellow]{tipo}[/yellow]"

        linhas_formatadas.append([data_fmt, placa, tipo_fmt, evento_fmt])

    criar_tabela(
        titulo=titulo,
        colunas=["Data/Hora", "Placa", "Tipo", "Evento"],
        linhas=linhas_formatadas
    )
    input(f"\n{Colors.DIM}Pressione Enter para voltar...{Colors.RESET}")

def relatorio_geral(repositorio):
    """Mostra as últimas movimentações do estacionamento."""
    header("RELATÓRIO DE MOVIMENTAÇÃO (ÚLTIMOS 50)")
    dados = repositorio.common.buscar_historico_geral()
    _renderizar_tabela_historico(dados, titulo="EXTRATO GERAL")

def relatorio_por_placa(repositorio):
    """Filtra o histórico por uma placa."""
    header("BUSCAR HISTÓRICO POR PLACA")
    placa, _ = get_valid_input("Digite a Placa: ", validate_placa)
    
    dados = repositorio.common.buscar_historico_por_placa(placa)
    _renderizar_tabela_historico(dados, titulo=f"EXTRATO: {placa}")

def menu_relatorios(repositorio):
    """Sub-menu de relatórios padronizado."""
    while True:
        header("RELATÓRIOS E AUDITORIA 📋")
        menu_option("1", "Histórico Geral (Últimos 50)")
        menu_option("2", "Filtrar por Placa")
        print("-" * 30)
        menu_option("0", "Voltar")
        
        opcao = input(f"\n{Colors.CYAN}➤ Opção: {Colors.RESET}").strip()
        
        if opcao == '1':
            relatorio_geral(repositorio)
        elif opcao == '2':
            relatorio_por_placa(repositorio)
        elif opcao == '0':
            break
        else:
            show_warning("Opção inválida.")