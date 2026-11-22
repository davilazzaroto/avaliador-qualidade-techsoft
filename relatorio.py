"""Análise das avaliações e geração do relatório em texto simples."""

from processos import classificar_nota


def analisar_processos(processos):
    if not processos:
        raise ValueError("Não há processos para avaliar.")

    # Notas 0 e 1 indicam os processos que precisam de mais atenção.
    prioritarios = [
        (indice, processo)
        for indice, processo in enumerate(processos)
        if processo["nota"] <= 1
    ]
    # A ordenação estável mantém a ordem original nos empates.
    prioritarios.sort(key=lambda item: item[1]["nota"])

    menor_nota = min(processo["nota"] for processo in processos)
    # Mantemos todos os empatados para não destacar apenas o primeiro.
    empatados = [
        processo for processo in processos
        if processo["nota"] == menor_nota
    ]

    return {
        "processos": processos,
        "prioritarios": prioritarios,
        # A média resume as notas, sem indicar um nível oficial de maturidade.
        "media": sum(processo["nota"] for processo in processos) / len(processos),
        "menor_nota": menor_nota,
        "empatados": empatados,
    }


def gerar_texto_relatorio(analise):
    linhas = [
        "RELATÓRIO FINAL - AVALIADOR DE QUALIDADE TECHSOFT",
        "=" * 54,
        "",
        "As notas iniciais são uma proposta de diagnóstico acadêmico editável,",
        "baseada no cenário. Não são uma conclusão determinada pelo enunciado",
        "nem representam certificação ou nível oficial de maturidade CMMI/MPS.BR.",
        "",
        "PROCESSOS AVALIADOS",
    ]
    for processo in analise["processos"]:
        linhas.extend(
            [
                f"- {processo['nome']}: {processo['nota']} - "
                f"{classificar_nota(processo['nota'])}",
                f"  Justificativa: {processo['justificativa']}",
            ]
        )

    linhas.extend(
        [
            "",
            "PROCESSOS PRIORITÁRIOS (nota 0 ou 1)",
        ]
    )
    if analise["prioritarios"]:
        for _, processo in analise["prioritarios"]:
            linhas.extend(
                [
                    f"- {processo['nome']} (nota {processo['nota']}): "
                    f"{processo['recomendacao']}",
                ]
            )
    else:
        linhas.append("Não há processos prioritários nesta avaliação.")

    linhas.extend(
        [
            "",
            f"Média aritmética simples: {analise['media']:.2f}",
            "A média resume as avaliações e não equivale a um nível oficial "
            "de maturidade.",
            f"Menor nota: {analise['menor_nota']}",
            "Processos empatados na menor nota: "
            + ", ".join(processo["nome"] for processo in analise["empatados"])
            + ".",
        ]
    )
    if not analise["prioritarios"]:
        linhas.append(
            "A existência de uma menor nota não significa que haja processos "
            "prioritários."
        )
    return "\n".join(linhas)
