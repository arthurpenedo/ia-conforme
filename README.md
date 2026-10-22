# ia-conforme

[![CI](https://github.com/arthurpenedo/ia-conforme/actions/workflows/ci.yml/badge.svg)](https://github.com/arthurpenedo/ia-conforme/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

> **Inventário de sistemas de IA com classificação de risco explicável.** Uma ficha TOML por sistema, regras em
> Python que dizem o nível de risco **e por quê**, um checklist do que falta e um relatório em Markdown. Zero
> dependências, zero custo, sem modelo.

## O problema

Empresas usam IA em vários lugares e quase nunca sabem **quais** sistemas têm nem o risco de cada um. O Marco Legal
da IA no Brasil (PL 2338/2023) e o AI Act europeu classificam sistemas por nível de risco e exigem controles
proporcionais (avaliação de impacto, registro de decisões, revisão humana). O primeiro passo de qualquer governança
é o inventário, e isso cabe num repositório de arquivos de texto versionados.

## O que faz

1. **Ficha** (`exemplos/*.toml`): finalidade, domínio, público, dados pessoais, decisão automatizada, supervisão
   humana e os controles que já existem.
2. **Classificação** em quatro níveis (`vedado`, `alto`, `limitado`, `mínimo`), cada um com os motivos que o
   dispararam. Sem caixa-preta: cada regra é uma linha em `risco.py`.
3. **Checklist** proporcional ao nível: o que falta para um sistema de alto risco (7 controles) ou limitado (2).
4. **Relatório** em Markdown, ordenado do pior para o melhor, e `--falhar-se alto` para usar como etapa de CI.

## Resultado nos exemplos

`exemplos/` traz 6 fichas: `agente-banco` e `lgpd-guard` (preenchidas a partir do README de dois projetos meus,
que são de portfólio e não estão em produção) e 4 fictícias. Saída real (`exemplos/RELATORIO.md`):

| Sistema | Risco | Controles pendentes |
|---|---|---:|
| pontuacao-moral (fictício) | VEDADO | n/a |
| agente-banco | ALTO | 6/7 |
| triagem-curriculos (fictício) | ALTO | 5/7 |
| score-credito (fictício) | ALTO | 0/7 |
| lgpd-guard | LIMITADO | 1/1 |
| resumo-reunioes (fictício) | MÍNIMO | n/a |

No total, 12 de 22 controles exigidos estavam pendentes. O `agente-banco` cai em alto risco porque bloqueia cartão e
estorna valores sem humano (decisão automatizada sobre dados pessoais): é exatamente o tipo de achado que o
inventário existe para trazer à tona.

## Como rodar

```bash
pip install -e ".[dev]"
ia-conforme modelo > minha-ficha.toml          # ficha em branco
ia-conforme avaliar exemplos                   # imprime o relatório
ia-conforme avaliar exemplos --saida relatorio.md --falhar-se alto   # código 1 se houver alto risco ou pior
pytest                                         # 18 testes
```

## Página de demo
`ia-conforme demo exemplos --saida site/index.html` gera uma página estática com o inventário dos sistemas de exemplo (risco, motivos e checklist). O workflow `.github/workflows/pagina.yml` publica no GitHub Pages a cada push na `main` (ativar uma vez em Settings → Pages → Source = GitHub Actions). Link: https://arthurpenedo.github.io/ia-conforme/ (vale depois da primeira execução).

## Limites honestos

- **É triagem técnica, não parecer jurídico.** As regras são uma leitura simplificada do PL 2338/2023 e do AI Act,
  feita por um estudante de engenharia, e não foram revisadas por advogado.
- Não verifiquei o estágio atual de tramitação do PL 2338/2023 ao escrever; confira antes de citar como lei vigente.
- A ficha é autodeclarada: a ferramenta confia no que você escreve.
- Os níveis do checklist (quais controles em quais níveis) são uma escolha minha de prioridade, não uma lista legal.
- Os exemplos `agente-banco` e `lgpd-guard` foram preenchidos por mim com base nos respectivos READMEs; controles
  marcados como ausentes significam "não documentados", não "inexistentes".

## Licença

MIT.
