"""Apresentação e interação no terminal com Rich."""

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from processos import (
    alterar_avaliacao,
    classificar_nota,
    converter_entrada_inteira,
    validar_justificativa,
    validar_nota,
    validar_numero_processo,
)
from relatorio import analisar_processos, gerar_texto_relatorio

console = Console()


def mostrar_menu():
    opcoes = (
        "1. Listar processos e avaliações\n"
        "2. Alterar a avaliação de um processo\n"
        "3. Exibir relatório final\n"
        "4. Salvar relatório final em TXT\n"
        "5. Sair"
    )
    console.print(
        Panel(Text(opcoes), title="Avaliador de Qualidade TechSoft", border_style="blue")
    )
    console.print(
        Text("As alterações ficam apenas nesta execução e serão perdidas ao sair.",
             style="yellow")
    )


def solicitar_texto(mensagem):
    console.print(Text(mensagem, style="cyan"))
    return input("> ")


def ler_opcao_menu():
    """Lê uma opção válida do menu."""
    while True:
        entrada = solicitar_texto("Escolha uma opção (1 a 5):")
        try:
            opcao = converter_entrada_inteira(entrada)
        except ValueError:
            console.print(Text("Erro: informe um número inteiro de 1 a 5.",
                               style="red"))
            continue
        if 1 <= opcao <= 5:
            return opcao
        console.print(Text("Erro: a opção deve estar entre 1 e 5.", style="red"))


def listar_processos(processos):
    tabela = Table(title="Processos e avaliações", box=box.SIMPLE)
    tabela.add_column("Nº", justify="right", style="cyan")
    tabela.add_column("Processo", style="bold")
    tabela.add_column("Nota", justify="center")
    tabela.add_column("Classificação")
    tabela.add_column("Justificativa", overflow="fold")
    for indice, processo in enumerate(processos, start=1):
        estilo = "red" if processo["nota"] <= 1 else "green"
        tabela.add_row(
            str(indice),
            Text(processo["nome"]),
            str(processo["nota"]),
            Text(classificar_nota(processo["nota"]), style=estilo),
            Text(processo["justificativa"]),
        )
    console.print(tabela)


def selecionar_indice_processo(processos):
    """Lê um número que corresponda a um processo."""
    while True:
        entrada = solicitar_texto(
            f"Informe o número do processo (1 a {len(processos)}):"
        )
        try:
            return validar_numero_processo(entrada, len(processos))
        except ValueError as erro:
            console.print(Text(f"Erro: {erro}", style="red"))


def ler_nota():
    """Lê uma nota válida na escala de 0 a 3."""
    while True:
        entrada = solicitar_texto("Nova nota (0 a 3):")
        try:
            return validar_nota(entrada)
        except ValueError as erro:
            console.print(Text(f"Erro: {erro}", style="red"))


def ler_justificativa():
    """Lê uma justificativa não vazia."""
    while True:
        justificativa = solicitar_texto("Nova justificativa:")
        try:
            return validar_justificativa(justificativa)
        except ValueError as erro:
            console.print(Text(f"Erro: {erro}", style="red"))


def alterar_processo(processos):
    """Coleta os dados e atualiza o processo após validá-los."""
    listar_processos(processos)
    indice = selecionar_indice_processo(processos)
    nota = ler_nota()
    justificativa = ler_justificativa()
    alterar_avaliacao(processos, indice, nota, justificativa)
    console.print(Text("Avaliação atualizada com sucesso.", style="green"))


def exibir_relatorio(processos):
    """Mostra o relatório com os mesmos cálculos usados no TXT."""
    analise = analisar_processos(processos)

    tabela = Table(title="Relatório final - processos", box=box.SIMPLE)
    tabela.add_column("Processo", style="bold")
    tabela.add_column("Nota", justify="center")
    tabela.add_column("Classificação")
    tabela.add_column("Justificativa", overflow="fold")
    for processo in analise["processos"]:
        estilo = "red" if processo["nota"] <= 1 else "green"
        tabela.add_row(
            Text(processo["nome"]),
            str(processo["nota"]),
            Text(classificar_nota(processo["nota"]), style=estilo),
            Text(processo["justificativa"]),
        )
    console.print(tabela)

    titulo = (
        f"Média aritmética: {analise['media']:.2f}\n"
        f"Menor nota: {analise['menor_nota']} — "
        + ", ".join(p["nome"] for p in analise["empatados"])
    )
    console.print(Panel(Text(titulo), title="Resumo", border_style="blue"))

    linhas_prioritarios = []
    for _, processo in analise["prioritarios"]:
        linhas_prioritarios.append(
            f"{processo['nome']} (nota {processo['nota']}): "
            f"{processo['recomendacao']}"
        )
    if linhas_prioritarios:
        texto_prioritarios = "\n".join(linhas_prioritarios)
    else:
        texto_prioritarios = "Não há processos prioritários nesta avaliação."
    console.print(
        Panel(
            Text(texto_prioritarios),
            title="Prioridades e recomendações (notas 0 ou 1)",
            border_style="yellow",
        )
    )
    console.print(
        Text(
            "A média resume as avaliações e não equivale a um nível oficial "
            "de maturidade. A avaliação é acadêmica, não uma certificação "
            "CMMI ou MPS.BR.",
            style="dim",
        )
    )
    if not analise["prioritarios"]:
        console.print(
            Text(
                "Uma menor nota sempre existe; isso não significa que haja "
                "processos prioritários.",
                style="dim",
            )
        )
    return analise


def montar_relatorio_textual(processos):
    """Gera o relatório em texto simples para exportação."""
    analise = analisar_processos(processos)
    return gerar_texto_relatorio(analise)


def mostrar_mensagem(mensagem, estilo="green"):
    console.print(Text(mensagem, style=estilo))
