from pathlib import Path

import pytest

from ia_conforme.checklist import montar, pendencias
from ia_conforme.cli import main
from ia_conforme.ficha import FichaInvalida, carregar_pasta, de_dict
from ia_conforme.relatorio import avaliar, avaliar_todas, relatorio_md
from ia_conforme.risco import classificar

EXEMPLOS = Path(__file__).resolve().parent.parent / "exemplos"


def ficha(**kw):
    base = {"nome": "x", "finalidade": "y"}
    base.update(kw)
    return de_dict(base)


def test_minimo():
    assert classificar(ficha()).nivel == "minimo"


def test_dados_pessoais_viram_limitado():
    assert classificar(ficha(dados_pessoais=True)).nivel == "limitado"


def test_publico_externo_limitado():
    assert classificar(ficha(publico="clientes")).nivel == "limitado"


def test_dominio_sensivel_com_decisao_e_alto():
    r = classificar(ficha(dominio="credito", decisao="apoia"))
    assert r.nivel == "alto"
    assert "crédito" in r.motivos[0]


def test_dominio_sensivel_sem_decisao_nao_e_alto():
    assert classificar(ficha(dominio="saude")).nivel == "minimo"


def test_decisao_automatica_com_dados_pessoais_e_alto():
    assert classificar(ficha(decisao="automatica", dados_pessoais=True)).nivel == "alto"


def test_pontuacao_social_e_vedado():
    assert classificar(ficha(pontuacao_social=True)).nivel == "vedado"


def test_emocoes_no_trabalho_vedado_mas_em_atendimento_limitado():
    assert classificar(ficha(reconhecimento_emocoes=True, dominio="emprego")).nivel == "vedado"
    assert classificar(ficha(reconhecimento_emocoes=True, dominio="atendimento")).nivel == "limitado"


def test_vedado_vence_alto():
    r = classificar(ficha(manipulacao=True, decisao="automatica", dados_pessoais=True))
    assert r.nivel == "vedado"


def test_checklist_alto_cobra_todos_os_controles():
    f = ficha(dominio="emprego", decisao="automatica", dados_pessoais=True)
    itens = montar(f, "alto")
    assert len(itens) == 7
    assert len(pendencias(itens)) == 7


def test_checklist_supervisao_so_vale_antes_da_decisao():
    f = ficha(dominio="credito", decisao="apoia", supervisao_humana="amostral")
    sup = [i for i in montar(f, "alto") if i.campo == "supervisao_humana"][0]
    assert not sup.ok
    f2 = ficha(dominio="credito", decisao="apoia", supervisao_humana="antes_da_decisao")
    assert [i for i in montar(f2, "alto") if i.campo == "supervisao_humana"][0].ok


def test_checklist_vedado_vazio_e_minimo_sem_exigencia():
    assert montar(ficha(), "minimo") == []
    assert montar(ficha(pontuacao_social=True), "vedado") == []


def test_ficha_invalida():
    with pytest.raises(FichaInvalida):
        de_dict({"nome": "x"})
    with pytest.raises(FichaInvalida):
        de_dict({"nome": "x", "finalidade": "y", "decisao": "talvez"})
    with pytest.raises(FichaInvalida):
        de_dict({"nome": "x", "finalidade": "y", "dados_pessoais": "sim"})
    with pytest.raises(FichaInvalida):
        de_dict({"nome": "x", "finalidade": "y", "campo_novo": 1})


def test_exemplos_classificacao_esperada():
    por_nome = {a.ficha.nome: a for a in map(avaliar, carregar_pasta(EXEMPLOS))}
    esperado = {
        "agente-banco": "alto",
        "lgpd-guard": "limitado",
        "triagem-curriculos": "alto",
        "score-credito": "alto",
        "resumo-reunioes": "minimo",
        "pontuacao-moral": "vedado",
    }
    assert {n: a.risco.nivel for n, a in por_nome.items()} == esperado
    assert por_nome["score-credito"].pendencias == []
    assert len(por_nome["triagem-curriculos"].pendencias) == 5


def test_ordenacao_pior_primeiro():
    ordem = [a.ficha.nome for a in avaliar_todas(carregar_pasta(EXEMPLOS))]
    assert ordem[0] == "pontuacao-moral"
    assert ordem[-1] == "resumo-reunioes"


def test_relatorio_tem_tabela_e_checklist():
    md = relatorio_md(avaliar_todas(carregar_pasta(EXEMPLOS)))
    assert "| triagem-curriculos | ALTO | 5/7 |" in md
    assert "- [ ] Avaliação de impacto" in md
    assert "6 sistemas avaliados" in md


def test_cli_saida_e_falhar_se(tmp_path, capsys):
    saida = tmp_path / "r.md"
    assert main(["avaliar", str(EXEMPLOS), "--saida", str(saida)]) == 0
    assert saida.read_text(encoding="utf-8").startswith("# Inventário")
    assert main(["avaliar", str(EXEMPLOS), "--falhar-se", "vedado"]) == 1
    assert main(["avaliar", str(EXEMPLOS / "resumo-reunioes.toml"), "--falhar-se", "alto"]) == 0


def test_cli_erros(tmp_path, capsys):
    assert main(["avaliar", str(tmp_path)]) == 2
    ruim = tmp_path / "ruim.toml"
    ruim.write_text('nome = "x"\n', encoding="utf-8")
    assert main(["avaliar", str(ruim)]) == 2
