# Dados de entrada

## ordens.csv

Cada linha = uma ordem de produção/serviço (com ou sem retrabalho).

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id | texto | Identificador da ordem |
| data | data (YYYY-MM-DD) | Data da ordem |
| processo | texto | Processo / etapa |
| produto | texto | Produto ou serviço |
| operador | texto | Quem executou |
| turno | texto | Turno (manhã, tarde, noite) |
| unidades | número | Quantidade produzida |
| unidades_retrabalho | número | Quantidade que precisou retrabalho |
| horas_retrabalho | número | Horas gastas no retrabalho |
| custo_hora | número | Custo da hora de mão de obra (R$) |
| custo_material | número | Material descartado/reposto no retrabalho (R$) |
| causa | texto | Causa-raiz do retrabalho (vazio se não houve) |
| ticket_hora | número | Receita/hora que aquela capacidade poderia gerar (R$) |

## Como o diagnóstico usa

- **Custo direto** = (horas_retrabalho × custo_hora) + custo_material
- **Custo de oportunidade** = horas_retrabalho × ticket_hora
- **FPY** = (unidades − unidades_retrabalho) / unidades
- **Taxa de retrabalho** = ordens com retrabalho / total de ordens
