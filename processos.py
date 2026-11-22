"""Dados iniciais e validação das avaliações."""

import re


def converter_entrada_inteira(entrada):
    """Aceita somente números inteiros em notação decimal."""
    if not isinstance(entrada, str) or not re.fullmatch(
        r"[+-]?[0-9]+", entrada.strip()
    ):
        raise ValueError
    return int(entrada.strip())


def obter_processos_iniciais():
    return [
        {
            "nome": "Requisitos",
            "nota": 1,
            "justificativa": (
                "Os requisitos são levantados, mas a aprovação do cliente "
                "nem sempre é registrada."
            ),
            "recomendacao": (
                "Registrar critérios de aceitação e aprovação do cliente."
            ),
        },
        {
            "nome": "Desenvolvimento",
            "nota": 1,
            "justificativa": (
                "O desenvolvimento ocorre, mas cada desenvolvedor trabalha "
                "de uma maneira."
            ),
            "recomendacao": (
                "Adotar padrões simples de código e vincular alterações "
                "às solicitações."
            ),
        },
        {
            "nome": "Revisão de código",
            "nota": 1,
            "justificativa": (
                "A revisão não é obrigatória, portanto não existe garantia "
                "de aplicação consistente."
            ),
            "recomendacao": (
                "Exigir revisão por outro desenvolvedor e registrar "
                "sua aprovação."
            ),
        },
        {
            "nome": "Testes",
            "nota": 1,
            "justificativa": (
                "Os testes são realizados, mas nem sempre possuem resultados "
                "e evidências registrados."
            ),
            "recomendacao": (
                "Padronizar os testes e registrar resultados e evidências."
            ),
        },
        {
            "nome": "Implantação",
            "nota": 1,
            "justificativa": (
                "Algumas versões são liberadas sem homologação e o controle "
                "de versões por cliente é insuficiente."
            ),
            "recomendacao": (
                "Exigir homologação e registrar a versão instalada "
                "por cliente."
            ),
        },
        {
            "nome": "Suporte",
            "nota": 1,
            "justificativa": (
                "Atende e corrige problemas, mas nem todas as solicitações "
                "são registradas e as causas raramente são investigadas."
            ),
            "recomendacao": (
                "Centralizar solicitações e analisar as causas dos problemas "
                "recorrentes."
            ),
        },
    ]


def classificar_nota(nota):
    classificacoes = {
        0: "Não atende",
        1: "Atende parcialmente",
        2: "Atende em grande parte",
        3: "Atende completamente",
    }
    if nota not in classificacoes:
        raise ValueError("A nota deve ser um inteiro entre 0 e 3.")
    return classificacoes[nota]


def validar_nota(entrada):
    """Converte a entrada e aceita apenas notas inteiras de 0 a 3."""
    # A nota precisa estar na escala antes de ser usada na avaliação.
    try:
        nota = converter_entrada_inteira(entrada)
    except ValueError:
        raise ValueError("Informe uma nota inteira entre 0 e 3.") from None

    if nota < 0 or nota > 3:
        raise ValueError("A nota deve estar entre 0 e 3.")
    return nota


def validar_justificativa(justificativa):
    """Rejeita justificativas vazias ou compostas por espaços."""
    if not isinstance(justificativa, str) or not justificativa.strip():
        raise ValueError("A justificativa não pode ficar vazia.")
    return justificativa.strip()


def validar_numero_processo(entrada, quantidade):
    """Converte a seleção em índice e confere se há processo correspondente."""
    try:
        numero = converter_entrada_inteira(entrada)
    except ValueError:
        raise ValueError("Informe um número inteiro de processo.") from None

    if numero < 1 or numero > quantidade:
        raise ValueError(f"Escolha um processo entre 1 e {quantidade}.")
    return numero - 1


def alterar_avaliacao(processos, indice, nota, justificativa):
    """Atualiza a avaliação só depois de validar nota e justificativa."""
    if not isinstance(indice, int) or indice < 0 or indice >= len(processos):
        raise ValueError("O processo selecionado é inválido.")

    nota_validada = validar_nota(str(nota))
    justificativa_validada = validar_justificativa(justificativa)
    processos[indice]["nota"] = nota_validada
    processos[indice]["justificativa"] = justificativa_validada
