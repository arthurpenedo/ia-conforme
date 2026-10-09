"""Ficha padrão de um sistema de IA, lida de um arquivo TOML."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path

DOMINIOS = {
    "credito",
    "emprego",
    "educacao",
    "saude",
    "seguranca_publica",
    "justica",
    "servicos_essenciais",
    "atendimento",
    "marketing",
    "interno",
    "outro",
}

DECISOES = {"nenhuma", "apoia", "automatica"}
SUPERVISAO = {"nenhuma", "amostral", "antes_da_decisao"}
PUBLICOS = {"interno", "clientes", "publico_geral"}


class FichaInvalida(ValueError):
    """A ficha não segue o formato esperado."""


@dataclass
class Ficha:
    nome: str
    finalidade: str
    dominio: str = "outro"
    publico: str = "interno"
    dados_pessoais: bool = False
    dados_sensiveis: bool = False
    criancas: bool = False
    decisao: str = "nenhuma"
    supervisao_humana: str = "nenhuma"
    # práticas vedadas ou sensíveis
    manipulacao: bool = False
    pontuacao_social: bool = False
    biometria_identificacao: bool = False
    reconhecimento_emocoes: bool = False
    # controles já existentes
    avaliacao_impacto: bool = False
    registro_decisoes: bool = False
    teste_vies: bool = False
    transparencia_usuario: bool = False
    canal_contestacao: bool = False
    base_legal_lgpd: bool = False
    modelo_proprio: bool = False
    modelos_terceiros: list[str] = field(default_factory=list)
    arquivo: str = ""


_BOOLS = [
    "dados_pessoais", "dados_sensiveis", "criancas", "manipulacao", "pontuacao_social",
    "biometria_identificacao", "reconhecimento_emocoes", "avaliacao_impacto",
    "registro_decisoes", "teste_vies", "transparencia_usuario", "canal_contestacao",
    "base_legal_lgpd", "modelo_proprio",
]


def _checar_enum(campo: str, valor: str, validos: set[str]) -> None:
    if valor not in validos:
        raise FichaInvalida(f"{campo}={valor!r} inválido; use um de: {', '.join(sorted(validos))}")


def carregar(caminho: str | Path) -> Ficha:
    caminho = Path(caminho)
    with caminho.open("rb") as f:
        try:
            bruto = tomllib.load(f)
        except tomllib.TOMLDecodeError as e:
            raise FichaInvalida(f"{caminho.name}: TOML inválido ({e})") from e
    return de_dict(bruto, arquivo=caminho.name)


def de_dict(bruto: dict, arquivo: str = "") -> Ficha:
    for obrigatorio in ("nome", "finalidade"):
        if not str(bruto.get(obrigatorio, "")).strip():
            raise FichaInvalida(f"{arquivo or 'ficha'}: campo obrigatório ausente: {obrigatorio}")
    desconhecidos = set(bruto) - set(Ficha.__dataclass_fields__) - {"arquivo"}
    if desconhecidos:
        raise FichaInvalida(f"{arquivo or 'ficha'}: campos desconhecidos: {', '.join(sorted(desconhecidos))}")
    for campo in _BOOLS:
        if campo in bruto and not isinstance(bruto[campo], bool):
            raise FichaInvalida(f"{arquivo or 'ficha'}: {campo} deve ser true ou false")
    ficha = Ficha(**{k: v for k, v in bruto.items() if k != "arquivo"}, arquivo=arquivo)
    _checar_enum("dominio", ficha.dominio, DOMINIOS)
    _checar_enum("decisao", ficha.decisao, DECISOES)
    _checar_enum("supervisao_humana", ficha.supervisao_humana, SUPERVISAO)
    _checar_enum("publico", ficha.publico, PUBLICOS)
    return ficha


def carregar_pasta(pasta: str | Path) -> list[Ficha]:
    arquivos = sorted(Path(pasta).glob("*.toml"))
    return [carregar(a) for a in arquivos]
