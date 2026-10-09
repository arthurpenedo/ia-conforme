"""Classificação de risco por regras explicáveis.

Cada regra que dispara vira um motivo legível. Os níveis seguem a lógica do Marco Legal da IA
(PL 2338/2023) e do AI Act europeu: vedado/inaceitável, alto, limitado, mínimo. É uma triagem
técnica para priorizar trabalho, não um parecer jurídico.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .ficha import Ficha

NIVEIS = ["minimo", "limitado", "alto", "vedado"]

DOMINIOS_ALTO_RISCO = {
    "credito": "avalia crédito ou capacidade de pagamento",
    "emprego": "seleção, avaliação ou gestão de trabalhadores",
    "educacao": "acesso ou avaliação em educação",
    "saude": "diagnóstico, triagem ou tratamento em saúde",
    "seguranca_publica": "segurança pública ou investigação",
    "justica": "apoio a decisão judicial ou administrativa",
    "servicos_essenciais": "acesso a serviços públicos ou essenciais",
}


@dataclass
class Resultado:
    nivel: str
    motivos: list[str] = field(default_factory=list)


def classificar(f: Ficha) -> Resultado:
    # 1. Práticas vedadas
    vedados = []
    if f.manipulacao:
        vedados.append("usa técnicas subliminares ou manipuladoras que podem causar dano")
    if f.pontuacao_social:
        vedados.append("faz pontuação social de pessoas pelo poder público ou com efeito discriminatório")
    if f.biometria_identificacao and f.dominio == "seguranca_publica":
        vedados.append("identificação biométrica à distância em segurança pública (em regra vedada)")
    if f.reconhecimento_emocoes and f.dominio in {"emprego", "educacao"}:
        vedados.append("reconhece emoções no trabalho ou na escola")
    if vedados:
        return Resultado("vedado", vedados)

    # 2. Alto risco
    altos = []
    if f.dominio in DOMINIOS_ALTO_RISCO and f.decisao != "nenhuma":
        altos.append(f"domínio sensível: {DOMINIOS_ALTO_RISCO[f.dominio]}, e a IA participa da decisão")
    if f.biometria_identificacao:
        altos.append("faz identificação ou autenticação biométrica")
    if f.decisao == "automatica" and f.dados_pessoais:
        altos.append("decide sozinha sobre pessoas usando dados pessoais")
    if f.dados_sensiveis and f.decisao != "nenhuma":
        altos.append("usa dado pessoal sensível (saúde, biometria, raça etc.) para decidir ou apoiar decisão")
    if f.criancas and f.dados_pessoais and f.decisao != "nenhuma":
        altos.append("trata dados de crianças ou adolescentes em decisão")
    if altos:
        return Resultado("alto", altos)

    # 3. Limitado
    limitados = []
    if f.publico in {"clientes", "publico_geral"}:
        limitados.append("conversa ou entrega conteúdo diretamente a pessoas fora da empresa")
    if f.dados_pessoais:
        limitados.append("trata dados pessoais (LGPD se aplica)")
    if f.reconhecimento_emocoes:
        limitados.append("reconhece emoções")
    if f.decisao == "apoia":
        limitados.append("apoia decisões humanas")
    if limitados:
        return Resultado("limitado", limitados)

    return Resultado("minimo", ["uso interno, sem dado pessoal e sem decisão sobre pessoas"])
