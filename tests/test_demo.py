from pathlib import Path

from ia_conforme.cli import main
from ia_conforme.demo import gerar_html

EXEMPLOS = Path(__file__).resolve().parent.parent / "exemplos"


def test_demo_html_lista_sistemas_e_riscos():
    html = gerar_html(EXEMPLOS)
    assert "ia-conforme: demo" in html
    assert "VEDADO" in html or "ALTO" in html
    assert "Não substitui parecer jurídico" in html


def test_cli_demo_grava_arquivo(tmp_path):
    saida = tmp_path / "site" / "index.html"
    assert main(["demo", str(EXEMPLOS), "--saida", str(saida)]) == 0
    assert "<table>" in saida.read_text(encoding="utf-8")


def test_cli_demo_pasta_inexistente(tmp_path):
    assert main(["demo", str(tmp_path / "nada"), "--saida", str(tmp_path / "x.html")]) == 2
