from ia_conforme.ficha import de_dict
from ia_conforme.relatorio import avaliar, ficha_md


def _ficha(**kw):
    base = {"nome": "Sistema X", "finalidade": "Testar"}
    base.update(kw)
    return de_dict(base)


def test_ficha_md_traz_titulo_finalidade_e_motivos():
    md = ficha_md(avaliar(_ficha(dados_pessoais=True)))
    assert md.startswith("### Sistema X: risco ")
    assert "**Finalidade:** Testar" in md
    assert "**Por que esse nível:**" in md


def test_ficha_md_sistema_de_risco_minimo_nao_vira_vedado():
    md = ficha_md(avaliar(_ficha()))
    assert "não colocar em produção" not in md


def test_modelos_terceiros_precisa_ser_lista_de_textos():
    import pytest

    from ia_conforme.ficha import FichaInvalida, de_dict

    base = {"nome": "x", "finalidade": "y"}
    with pytest.raises(FichaInvalida, match="modelos_terceiros"):
        de_dict({**base, "modelos_terceiros": "gpt"})
    with pytest.raises(FichaInvalida, match="modelos_terceiros"):
        de_dict({**base, "modelos_terceiros": [1]})
    assert de_dict({**base, "modelos_terceiros": ["gpt"]}).modelos_terceiros == ["gpt"]
