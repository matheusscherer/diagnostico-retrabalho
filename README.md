# Diagnóstico de Retrabalho

<p align="left">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas" />
  <img src="https://img.shields.io/badge/pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white" alt="pytest" />
  <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white" alt="GitHub Actions" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT" />
</p>

**Problema de negócio:** a operação produz duas vezes o que deveria produzir uma.  
Mão de obra, material e capacidade são consumidos de novo — e o faturamento não acompanha.

Este projeto transforma a planilha de ordens em um diagnóstico objetivo:

- **Custo direto** do retrabalho (mão de obra + material)
- **Custo de oportunidade** (horas que poderiam faturar)
- **First Pass Yield (FPY)**
- Onde o problema se concentra (processo, produto, causa, operador, turno)

> Feito para ser lido por gestor e executado por analista.

---

## O que ele entrega

| Saída | Descrição |
|-------|-----------|
| Resumo executivo | Custo direto, oportunidade, FPY, taxa de retrabalho |
| Ranking por processo | Qual etapa mais custa |
| Ranking por produto | Quais SKUs/serviços mais falham |
| Ranking por causa-raiz | Onde atacar primeiro |
| Ranking por operador / turno | Padrões operacionais |
| Relatório Markdown | Pronto para WhatsApp/e-mail |
| Excel detalhado | Abas por dimensão + resumo |

---

## Como rodar (3 minutos)

```bash
git clone https://github.com/matheusscherer/diagnostico-retrabalho.git
cd diagnostico-retrabalho

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

python -m diagnostico_retrabalho
pytest -v
```

Arquivos gerados em `outputs/`:
- `diagnostico_retrabalho.md`
- `diagnostico_retrabalho.xlsx`

### Com seus dados

```bash
python -m diagnostico_retrabalho \
  --ordens caminho/suas_ordens.csv \
  --fpy-target 0.95
```

---

## Formato do arquivo

### ordens.csv
```text
id,data,processo,produto,operador,turno,unidades,unidades_retrabalho,horas_retrabalho,custo_hora,custo_material,causa,ticket_hora
ORD-001,2026-08-15,Montagem,Produto A,João,manhã,100,12,3.5,35,45,Ajuste dimensional,90
```

---

## Lógica do diagnóstico

1. **Custo direto** = (horas_retrabalho × custo_hora) + custo_material
2. **Custo de oportunidade** = horas_retrabalho × ticket_hora
3. **FPY** = (unidades − unidades_retrabalho) ÷ unidades
4. **Taxa de retrabalho** = ordens com retrabalho ÷ total de ordens
5. Rankings por custo total (direto + oportunidade)

---

## Estrutura do projeto

```text
diagnostico-retrabalho/
├── data/raw/
├── src/diagnostico_retrabalho/
│   ├── analyzer.py
│   ├── loader.py
│   ├── metrics.py
│   ├── models.py
│   ├── report.py
│   └── cli.py
├── tests/
└── outputs/
```

---

## Testes

```bash
pytest -v
```

CI em Python 3.10, 3.11 e 3.12 a cada push.

---

## Por que este projeto importa

A maioria dos relatórios de qualidade mostra “% de rejeição”.  
Este mostra **dinheiro**:

- Quanto saiu em retrabalho
- Quanto deixou de entrar por capacidade consumida de novo
- Qual causa atacar primeiro

---

## Premissas e limites

- Dados de exemplo são sintéticos
- ticket_hora é a receita/hora estimada da capacidade (proxy de oportunidade)
- Não substitui sistema de qualidade — é um **diagnóstico** de ciclo fechado
- Não conecta em ERP/MES — lê CSV

---

## Autor

**Matheus Scherer** · Porto Alegre, RS  
Diagnóstico de custo operacional com Python

[GitHub](https://github.com/matheusscherer) · [LinkedIn](https://linkedin.com/in/scherermatheus) · [Site](https://mtsch-site.vercel.app)
