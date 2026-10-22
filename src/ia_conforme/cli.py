"""Linha de comando: ia-conforme avaliar <pasta|ficha.toml> [--saida relatorio.md] [--falhar-se alto]."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .ficha import FichaInvalida, carregar, carregar_pasta
from .relatorio import avaliar_todas, relatorio_md
from .risco import NIVEIS

MODELO = '''nome = "nome do sistema"
finalidade = "o que ele faz, em uma frase"
dominio = "atendimento"      # credito, emprego, educacao, saude, seguranca_publica, justica,
                             # servicos_essenciais, atendimento, marketing, interno, outro
publico = "clientes"         # interno, clientes, publico_geral
dados_pessoais = true
dados_sensiveis = false
criancas = false
decisao = "apoia"            # nenhuma, apoia, automatica
supervisao_humana = "amostral"  # nenhuma, amostral, antes_da_decisao
avaliacao_impacto = false
registro_decisoes = false
teste_vies = false
transparencia_usuario = false
canal_contestacao = false
base_legal_lgpd = false
'''


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="ia-conforme", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("avaliar", help="avalia uma ficha ou uma pasta de fichas .toml")
    a.add_argument("caminho")
    a.add_argument("--saida", help="grava o relatório neste arquivo .md")
    a.add_argument("--falhar-se", choices=NIVEIS, help="sai com código 1 se algum sistema atingir este nível ou pior")
    sub.add_parser("modelo", help="imprime uma ficha em branco")
    d = sub.add_parser("demo", help="gera a página HTML de demo a partir de uma pasta de fichas")
    d.add_argument("pasta", nargs="?", default="exemplos")
    d.add_argument("--saida", default="site/index.html")
    args = p.parse_args(argv)

    if args.cmd == "modelo":
        print(MODELO, end="")
        return 0

    if args.cmd == "demo":
        from .demo import gerar_html
        try:
            html = gerar_html(args.pasta)
        except (FichaInvalida, FileNotFoundError) as e:
            print(f"erro: {e}", file=sys.stderr)
            return 2
        saida = Path(args.saida)
        saida.parent.mkdir(parents=True, exist_ok=True)
        saida.write_text(html, encoding="utf-8")
        print(f"página gravada em {saida}")
        return 0

    alvo = Path(args.caminho)
    try:
        fichas = [carregar(alvo)] if alvo.is_file() else carregar_pasta(alvo)
    except (FichaInvalida, FileNotFoundError) as e:
        print(f"erro: {e}", file=sys.stderr)
        return 2
    if not fichas:
        print("erro: nenhuma ficha .toml encontrada", file=sys.stderr)
        return 2

    avaliacoes = avaliar_todas(fichas)
    texto = relatorio_md(avaliacoes)
    if args.saida:
        Path(args.saida).write_text(texto, encoding="utf-8")
        print(f"relatório gravado em {args.saida}")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(texto)

    if args.falhar_se:
        limite = NIVEIS.index(args.falhar_se)
        if any(NIVEIS.index(a.risco.nivel) >= limite for a in avaliacoes):
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
