"""Página de demo estática: o inventário dos sistemas de exemplo, com nível de risco, motivos e checklist."""
from __future__ import annotations

from html import escape
from pathlib import Path

from .ficha import carregar_pasta
from .relatorio import ROTULO, Avaliacao, avaliar_todas
from .risco import NIVEIS

CSS = (
    "body{font-family:system-ui,sans-serif;max-width:900px;margin:2rem auto;padding:0 1rem}"
    "table{border-collapse:collapse;width:100%;font-size:.9rem;margin-bottom:1.5rem}"
    "td,th{border-bottom:1px solid #eee;padding:.3rem;text-align:left}"
    ".sistema{border:1px solid #ddd;border-radius:6px;padding:.8rem;margin-bottom:1rem}"
    ".vedado{color:#b00020;font-weight:700}.alto{color:#b25b00;font-weight:700}"
    ".limitado{color:#8a6d00;font-weight:600}.minimo{color:#0a6b2d;font-weight:600}"
    "ul{margin:.3rem 0}.pend{color:#b00020}"
)


def _sistema(a: Avaliacao) -> str:
    motivos = "".join(f"<li>{escape(m)}</li>" for m in a.risco.motivos)
    if a.risco.nivel == "vedado":
        checklist = "<p><b>Ação:</b> não colocar em produção; rever o desenho do sistema.</p>"
    elif a.itens:
        itens = "".join(
            f"<li class='{'' if i.ok else 'pend'}'>{'✔' if i.ok else '✘'} {escape(i.descricao)}</li>" for i in a.itens)
        checklist = f"<p>Checklist:</p><ul>{itens}</ul>"
    else:
        checklist = "<p>Checklist: sem exigência adicional neste nível.</p>"
    return (
        f"<div class='sistema'><h3>{escape(a.ficha.nome)}: risco "
        f"<span class='{a.risco.nivel}'>{ROTULO[a.risco.nivel]}</span></h3>"
        f"<p><b>Finalidade:</b> {escape(a.ficha.finalidade)}</p>"
        f"<p>Por que esse nível:</p><ul>{motivos}</ul>{checklist}</div>"
    )


def gerar_html(pasta: str | Path) -> str:
    """Avalia todas as fichas .toml de `pasta` e monta a página."""
    fichas = carregar_pasta(Path(pasta))
    if not fichas:
        raise FileNotFoundError(f"nenhuma ficha .toml encontrada em {pasta}")
    avaliacoes = avaliar_todas(fichas)
    total_itens = sum(len(a.itens) for a in avaliacoes)
    total_pend = sum(len(a.pendencias) for a in avaliacoes)
    contagem = {n: sum(1 for a in avaliacoes if a.risco.nivel == n) for n in reversed(NIVEIS)}
    resumo = ", ".join(f"{contagem[n]} {ROTULO[n].lower()}" for n in reversed(NIVEIS))
    linhas = "".join(
        f"<tr><td>{escape(a.ficha.nome)}</td><td class='{a.risco.nivel}'>{ROTULO[a.risco.nivel]}</td>"
        f"<td>{len(a.pendencias)}/{len(a.itens)}</td></tr>" for a in avaliacoes
    )
    return (
        "<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'>"
        f"<title>ia-conforme: demo</title><style>{CSS}</style></head><body>"
        "<h1>ia-conforme: demo</h1>"
        f"<p>Inventário de {len(avaliacoes)} sistemas de IA <b>fictícios</b>, classificados por risco com regras "
        "inspiradas no AI Act e na LGPD. "
        f"Pendências: {total_pend} de {total_itens} controles exigidos. Resumo: {resumo}. "
        "<a href='https://github.com/arthurpenedo/ia-conforme'>Código no GitHub</a>.</p>"
        "<table><tr><th>Sistema</th><th>Risco</th><th>Pendências</th></tr>" + linhas + "</table>"
        + "".join(_sistema(a) for a in avaliacoes)
        + "<p><small>Triagem técnica por regras. Não substitui parecer jurídico.</small></p></body></html>"
    )
