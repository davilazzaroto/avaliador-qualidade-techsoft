"""Menu principal do Avaliador de Qualidade TechSoft."""

from datetime import datetime
from pathlib import Path

from interface import (
    alterar_processo,
    exibir_relatorio,
    ler_opcao_menu,
    listar_processos,
    montar_relatorio_textual,
    mostrar_menu,
    mostrar_mensagem,
)
from processos import obter_processos_iniciais


def salvar_relatorio(processos):
    """Salva o relatório TXT em UTF-8 na pasta do projeto."""
    # Assim, o destino não depende da pasta atual do terminal.
    pasta_relatorios = Path(__file__).resolve().parent / "relatorios"
    nome_arquivo = datetime.now().strftime(
        "relatorio_%Y%m%d_%H%M%S_%f.txt"
    )
    caminho = pasta_relatorios / nome_arquivo
    try:
        pasta_relatorios.mkdir(parents=True, exist_ok=True)
        caminho.write_text(
            montar_relatorio_textual(processos),
            encoding="utf-8",
        )
    except OSError as erro:
        mostrar_mensagem(
            f"Não foi possível salvar o relatório: {erro}", estilo="red"
        )
        return
    mostrar_mensagem(f"Relatório salvo em: {caminho}")


def executar():
    """Controla as opções do menu."""
    processos = obter_processos_iniciais()
    mostrar_mensagem(
        "As notas iniciais são uma proposta de diagnóstico acadêmico editável, "
        "não uma conclusão determinada pelo enunciado.",
        estilo="yellow",
    )
    while True:
        mostrar_menu()
        opcao = ler_opcao_menu()
        if opcao == 1:
            listar_processos(processos)
        elif opcao == 2:
            alterar_processo(processos)
        elif opcao == 3:
            exibir_relatorio(processos)
        elif opcao == 4:
            salvar_relatorio(processos)
        else:
            mostrar_mensagem("Programa encerrado. Até mais.", estilo="blue")
            return


if __name__ == "__main__":
    try:
        executar()
    except (KeyboardInterrupt, EOFError):
        mostrar_mensagem("\nPrograma encerrado. Até mais.", estilo="blue")
