# 📋 Report da Sprint 06 - Automação de Processos

## 🗓 Período da Sprint

**De:** 20 de maio de 2025  
**Até:** 03 de junho de 2025  
**Duração:** 2 semanas

---

## 🎯 Objetivo da Sprint

- Realizar melhorias no monitoramento das VMs do ambiente RPA.
- Implementar log estruturado no sistema de coleta.
- Corrigir falha intermitente no serviço de extração de PDFs.

---

## ✅ Itens Entregues (Done)

| ID         | Título                                                           | Responsável  | Status       | Observações                                        |
|------------|------------------------------------------------------------------|--------------|--------------|----------------------------------------------------|
| HIST-220   | Criar rotina de monitoramento de ocupação das VMs                | João         | Concluído    | Publicado em produção                              |
| HIST-225   | Ajustar extrator de PDF para lidar com páginas rotacionadas      | Fernando     | Concluído    | 100% testado com novos arquivos                    |
| BUG-108    | Corrigir erro de "NoneType" no envio para Graylog                | Amanda       | Concluído    | Corrigido e validado com logs reais                |
| DOC-005    | Documentar processo de envio de logs para Graylog                | Rafael       | Concluído    | Aprovado na revisão técnica                        |

---

## ❌ Itens Não Concluídos (Carry Over)

| ID         | Título                                      | Motivo do atraso                           | Situação atual |
|------------|---------------------------------------------|--------------------------------------------|----------------|
| HIST-227   | Integração com sistema legado via SQS       | Aguardando acesso à fila                   | Replanejado ⏭ |
| HIST-229   | Dashboard de visualização no Grafana        | Falta de tempo e dependência do time de BI | Em andamento 🔄 |

---

## 📊 Métricas da Sprint

- **Pontos planejados**: 34  
- **Pontos concluídos**: 21  
- **Velocidade do time (últimas 3 sprints)**: 24 / 27 / 21  
- **Taxa de entrega**: 62%

---

## 🧠 Aprendizados / Melhorias

- A definição antecipada dos acessos (ex: SQS) evita bloqueios técnicos.
- A automação de testes nos scripts de PDF reduziu erros em produção.
- Melhor comunicação com o time de BI para sincronizar demandas visuais.

---

## 🚧 Impedimentos

- A fila SQS da AWS ainda não foi liberada pelo time de infraestrutura.
- Os dados de uso das VMs estão inconsistentes — investigação em andamento.

---

## 🔮 Próximos Passos (Planejamento da Sprint 07)

- Finalizar integração com sistema legado via SQS.
- Desenvolver painel de uso de VMs com gráficos por horário.
- Iniciar testes A/B nos extratores com OCR otimizado.
