"""Checklist de governança: o que falta, conforme o nível de risco."""

from __future__ import annotations

from dataclasses import dataclass

from .ficha import Ficha

# (campo da ficha, descrição, níveis em que é exigido)
CONTROLES = [
    ("base_legal_lgpd", "Base legal da LGPD documentada para o tratamento de dados pessoais",
     {"limitado", "alto"}, "dados_pessoais"),
    ("transparencia_usuario", "Pessoa é avisada de que fala com IA ou de que há decisão automatizada",
     {"limitado", "alto"}, "publico_externo_ou_decisao"),
    ("supervisao_humana", "Supervisão humana antes da decisão (humano no circuito)",
     {"alto"}, None),
    ("canal_contestacao", "Canal para a pessoa contestar e pedir revisão da decisão",
     {"alto"}, "decisao"),
    ("registro_decisoes", "Registro (log) das decisões e das entradas para auditoria",
     {"alto"}, None),
    ("avaliacao_impacto", "Avaliação de impacto algorítmico feita e atualizada",
     {"alto"}, None),
    ("teste_vies", "Teste de viés e desempenho por grupo",
     {"alto"}, "decisao"),
]


@dataclass
class Item:
    campo: str
    descricao: str
    ok: bool


def _aplica(f: Ficha, condicao: str | None) -> bool:
    if condicao is None:
        return True
    if condicao == "dados_pessoais":
        return f.dados_pessoais
    if condicao == "decisao":
        return f.decisao != "nenhuma"
    if condicao == "publico_externo_ou_decisao":
        return f.publico != "interno" or f.decisao != "nenhuma"
    return True


def _atendido(f: Ficha, campo: str) -> bool:
    if campo == "supervisao_humana":
        return f.supervisao_humana == "antes_da_decisao"
    return bool(getattr(f, campo))


def montar(f: Ficha, nivel: str) -> list[Item]:
    if nivel == "vedado":
        return []
    itens = []
    for campo, descricao, niveis, condicao in CONTROLES:
        if nivel in niveis and _aplica(f, condicao):
            itens.append(Item(campo, descricao, _atendido(f, campo)))
    return itens


def pendencias(itens: list[Item]) -> list[Item]:
    return [i for i in itens if not i.ok]
