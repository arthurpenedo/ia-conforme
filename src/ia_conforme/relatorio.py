"""Relatório em Markdown do inventário."""

from __future__ import annotations

from dataclasses import dataclass

from .checklist import Item, montar, pendencias
from .ficha import Ficha
from .risco import NIVEIS, Resultado, classificar

ROTULO = {"vedado": "VEDADO", "alto": "ALTO", "limitado": "LIMITADO", "minimo": "MÍNIMO"}


@dataclass
class Avaliacao:
    ficha: Ficha
    risco: Resultado
    itens: list[Item]

    @property
    def pendencias(self) -> list[Item]:
        return pendencias(self.itens)


def avaliar(f: Ficha) -> Avaliacao:
    r = classificar(f)
    return Avaliacao(f, r, montar(f, r.nivel))


def avaliar_todas(fichas: list[Ficha]) -> list[Avaliacao]:
    return sorted(
        (avaliar(f) for f in fichas),
        key=lambda a: (-NIVEIS.index(a.risco.nivel), -len(a.pendencias), a.ficha.nome),
    )


def ficha_md(a: Avaliacao) -> str:
    f = a.ficha
    linhas = [
        f"### {f.nome}: risco {ROTULO[a.risco.nivel]}",
        "",
        f"**Finalidade:** {f.finalidade}",
        "",
        "**Por que esse nível:**",
        *[f"- {m}" for m in a.risco.motivos],
        "",
    ]
    if a.risco.nivel == "vedado":
        linhas += ["**Ação:** não colocar em produção; rever o desenho do sistema.", ""]
    elif a.itens:
        linhas.append("**Checklist:**")
        linhas += [f"- [{'x' if i.ok else ' '}] {i.descricao}" for i in a.itens]
        linhas.append("")
    else:
        linhas += ["**Checklist:** sem exigência adicional neste nível.", ""]
    return "\n".join(linhas)


def relatorio_md(avaliacoes: list[Avaliacao]) -> str:
    contagem = {n: sum(1 for a in avaliacoes if a.risco.nivel == n) for n in reversed(NIVEIS)}
    total_itens = sum(len(a.itens) for a in avaliacoes)
    total_pend = sum(len(a.pendencias) for a in avaliacoes)
    linhas = [
        "# Inventário de sistemas de IA",
        "",
        f"{len(avaliacoes)} sistemas avaliados. Pendências no checklist: {total_pend} de {total_itens} controles exigidos.",
        "",
        "| Sistema | Risco | Pendências |",
        "|---|---|---:|",
        *[
            f"| {a.ficha.nome} | {ROTULO[a.risco.nivel]} | {len(a.pendencias)}/{len(a.itens)} |"
            for a in avaliacoes
        ],
        "",
        "Resumo: " + ", ".join(f"{contagem[n]} {ROTULO[n].lower()}" for n in reversed(NIVEIS)) + ".",
        "",
        "## Detalhe",
        "",
        *[ficha_md(a) for a in avaliacoes],
        "> Triagem técnica por regras. Não substitui parecer jurídico.",
        "",
    ]
    return "\n".join(linhas)
