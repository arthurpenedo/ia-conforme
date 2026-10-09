# Inventário de sistemas de IA

6 sistemas avaliados. Pendências no checklist: 12 de 22 controles exigidos.

| Sistema | Risco | Pendências |
|---|---|---:|
| pontuacao-moral | VEDADO | 0/0 |
| agente-banco | ALTO | 6/7 |
| triagem-curriculos | ALTO | 5/7 |
| score-credito | ALTO | 0/7 |
| lgpd-guard | LIMITADO | 1/1 |
| resumo-reunioes | MÍNIMO | 0/0 |

Resumo: 1 vedado, 3 alto, 1 limitado, 1 mínimo.

## Detalhe

### pontuacao-moral: risco VEDADO

**Finalidade:** Dá nota de comportamento a moradores para liberar ou negar benefícios

**Por que esse nível:**
- faz pontuação social de pessoas pelo poder público ou com efeito discriminatório

**Ação:** não colocar em produção; rever o desenho do sistema.

### agente-banco: risco ALTO

**Finalidade:** Agente de atendimento bancário que consulta saldo, bloqueia cartão, emite segunda via e contesta cobrança via tool calling

**Por que esse nível:**
- decide sozinha sobre pessoas usando dados pessoais

**Checklist:**
- [ ] Base legal da LGPD documentada para o tratamento de dados pessoais
- [ ] Pessoa é avisada de que fala com IA ou de que há decisão automatizada
- [ ] Supervisão humana antes da decisão (humano no circuito)
- [ ] Canal para a pessoa contestar e pedir revisão da decisão
- [x] Registro (log) das decisões e das entradas para auditoria
- [ ] Avaliação de impacto algorítmico feita e atualizada
- [ ] Teste de viés e desempenho por grupo

### triagem-curriculos: risco ALTO

**Finalidade:** Ranqueia candidatos e descarta automaticamente os abaixo da nota de corte

**Por que esse nível:**
- domínio sensível: seleção, avaliação ou gestão de trabalhadores, e a IA participa da decisão
- decide sozinha sobre pessoas usando dados pessoais

**Checklist:**
- [x] Base legal da LGPD documentada para o tratamento de dados pessoais
- [ ] Pessoa é avisada de que fala com IA ou de que há decisão automatizada
- [ ] Supervisão humana antes da decisão (humano no circuito)
- [ ] Canal para a pessoa contestar e pedir revisão da decisão
- [x] Registro (log) das decisões e das entradas para auditoria
- [ ] Avaliação de impacto algorítmico feita e atualizada
- [ ] Teste de viés e desempenho por grupo

### score-credito: risco ALTO

**Finalidade:** Calcula limite de crédito de pessoas físicas com modelo de machine learning

**Por que esse nível:**
- domínio sensível: avalia crédito ou capacidade de pagamento, e a IA participa da decisão

**Checklist:**
- [x] Base legal da LGPD documentada para o tratamento de dados pessoais
- [x] Pessoa é avisada de que fala com IA ou de que há decisão automatizada
- [x] Supervisão humana antes da decisão (humano no circuito)
- [x] Canal para a pessoa contestar e pedir revisão da decisão
- [x] Registro (log) das decisões e das entradas para auditoria
- [x] Avaliação de impacto algorítmico feita e atualizada
- [x] Teste de viés e desempenho por grupo

### lgpd-guard: risco LIMITADO

**Finalidade:** Firewall que troca CPF, cartão e nomes por marcadores antes do texto ir ao provedor de IA

**Por que esse nível:**
- trata dados pessoais (LGPD se aplica)

**Checklist:**
- [ ] Base legal da LGPD documentada para o tratamento de dados pessoais

### resumo-reunioes: risco MÍNIMO

**Finalidade:** Resume atas de reuniões internas, sem dado de clientes

**Por que esse nível:**
- uso interno, sem dado pessoal e sem decisão sobre pessoas

**Checklist:** sem exigência adicional neste nível.

> Triagem técnica por regras. Não substitui parecer jurídico.
