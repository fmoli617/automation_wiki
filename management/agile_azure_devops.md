# 🎯 Análise Estratégica: Escolha do Processo "Agile", implementado com o Azure DevOps.

## 🔍 Organização

### O que?

- Raspagem de Dados:
  - Com interação visual.
  - Com interação baseada em componentes mapeados.

- Mapeamento de processos voltados a automação. (BPM-(N)):
  - Analise de requisitos
  - Documentacao de desenvolvimento
  - Mapeamento técnico
  - Desenvolvimento
  - Revisão de Desenvolvimento
  - Documentacao de Produção
  - Plano de Sustentação
  - Plano de movimentação de dados

## 🧠 Matriz SWOT - Equipe de Automação

### Forças (Strengths)

- ✅ Forte conhecimento técnico em RPA, scraping e APIs
- ✅ Capacidade de entregar automações rapidamente
- ✅ Visão integrada de processos e dados
- ✅ Capacidade de integração com APIs REST/JSON
- ✅ Domínio de ferramentas como Python, Selenium, FastAPI

### Fraquezas (Weaknesses)

- ⚠️ Dependência de sistemas externos instáveis
- ⚠️ Documentação nem sempre acompanha o ritmo das entregas
- ⚠️ Dificuldade de escalar soluções em ambientes pouco governados
- ⚠️ Baixa visibilidade estratégica fora da equipe técnica
- ⚠️ Monitoramento e manutenção nem sempre automatizados

### Oportunidades (Opportunities)

- 🚀 Aumento da demanda por automação e eficiência operacional
- 📈 Uso de dados capturados para BI e tomada de decisão
- 🤝 Integração com IA (OCR, NLP, decisão automatizada)
- 💼 Crescente reconhecimento da RPA nas áreas de negócio
- 🧩 Possibilidade de escalar automações com filas e containers

### Ameaças (Threats)

- 🔒 Mudanças em sites que afetam scraping (ex: CAPTCHA)
- 🛑 APIs externas que mudam sem aviso
- ⚙️ Processos manuais mal definidos que geram retrabalho
- 🔐 Restrições legais (ex: LGPD) e barreiras técnicas de acesso
- 💣 Falta de envolvimento da área de negócio na validação

---

## 🔗 Relacionando SWOT à Escolha do Processo Azure DevOps

| Fator | Impacto na Escolha |
|-------|---------------------|
| ✅ Entregas rápidas e técnicas | ✔️ Requer flexibilidade → **Agile** |
| ⚠️ Dependência de sistemas instáveis | ✔️ Necessita gestão visual de impedimentos → **Agile com Kanban** |
| 🚀 Demanda crescente | ✔️ Exige backlog claro e incremental → **Agile** |
| 🔐 Questões legais e estabilidade | ✔️ Precisa de etapas de validação bem definidas → **Agile com colunas customizadas** |
| ⚠️ Baixa visibilidade externa | ✔️ Agile permite uso de **Epics e Features** visíveis no backlog |
| ⚠️ Validações manuais | ✔️ Agile permite separar fases no board (ex: Validação Técnica x Negócio) |
| 🧠 Múltiplas automações simultâneas | ✔️ Hierarquia Agile organiza modularmente por processo |

---

## Decisão

**Agile** baseado na plataforma da Azure* DevOps.

### Justificativas

- Hierarquia clara: `Epic → Feature → User Story → Task`
- Suporte a **Kanban Boards personalizados**
- Flexibilidade para criar colunas específicas para o projeto de automacao
- Acompanhamento da vida útil de cada iniciativa

---

## 🧩 Exemplo Prático com Agile

``` estrutura
     Epic: Revisar projeto de automacao *xyz* em status de produção
      └── Feature: Documentação
            └── User Story: Mapear a lista de documentacao atual
                ├── Task: Validar PDD 
                ├── Task: Verificar documentos auxiliares
                └── Task: Verificar repositório do projeto

      └── Feature: Plano de Sustentação
            └── User Story: Mapear a lista de documentacao atual
                ├── Task: Validar Instruções para Acompanhamento
                ├── Task: Número de incidentes
                └── Task: Levantamento de melhoria contínua

            └── User Story: Mapear intervenção técnica
                ├── Task: O que precisa ser feito (classificar por prioridade)
                ├── Task: Como será implementado (exemplo de epico de implementacao revisao de projeto)
                └── Task: Tempo
    
    Epic: Implementar revisão do projeto de automacao *xyz* em status de produção
      └── Feature: 
            └── User Story: Verificar READE-ME da automação
                ├── Task: As informaçòes contidas estão corretas.
                ├── Task: Adicionar ou alterar as informações definidas na revisão
                └── Task: Verificar repositório do projeto

      └── Feature: Revisão do ambiente de processamento
            └── User Story: Logs
                ├── Task: Monitoramento de registro
                ├── Task: Versionamento correto
                └── Task: Alguma necessidade precisa ser atendida na versão atual

            └── User Story: Arquivos de requisitos para o projeto
                ├── Task: Quais libs externas são usadas
                ├── Task: As libs estão documentadas de forma correta
                ├── Task: Versionamento correto
                └── Task: Alguma necessidade precisa ser atendida na versão atual

            └── User Story: Configuração
                ├── Task: Credenciais
                ├── Task: Variáveis de Ambiente
                ├── Task: Versionamento correto
                └── Task: Alguma necessidade precisa ser atendida na versão atual

            └── User Story: Teste
                ├── Task: Verificar a possibilidade de testar, sem a necessidade da intervenção da área
                ├── Task: Realizar um debug das etapas possíveis, sem a necessidade da intervenção da área
                ├── Task: Executar um teste ponta a ponta
                └── Task: Validar os pontos de implementação
```

> Tags como `bloqueado`, `urgente`, `externo` ajudam a identificar impedimentos

---

## ✅ Conclusão

A estrutura Agile proporciona o equilíbrio ideal entre:

- organização
- lexibilidade
- visibilidade

apoiando as entregas técnicas e a evolução estratégica da equipe de automação.

## Observações

- A Azure fornece, ou pelo menos deveria fornecer metódos para auditoria dos dados.
  - Entendo que exista a possibilidade de extrair os dados
