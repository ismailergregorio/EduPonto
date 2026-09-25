# EduPonto

## Sistema Biométrico para Registro de Frequência Docente

O **EduPonto** é um projeto voltado à automatização do controle de frequência docente por meio de autenticação biométrica.

A proposta utiliza um equipamento baseado em **Raspberry Pi**, sensor de impressão digital e uma aplicação de gestão, permitindo registrar automaticamente os horários de entrada e saída dos docentes, além de disponibilizar recursos para consulta, auditoria e geração de relatórios.

---

## 📌 Sobre o Projeto

O projeto surgiu a partir da necessidade de melhorar o processo de controle de frequência docente, atualmente sujeito a procedimentos manuais, como planilhas e assinaturas.

Esses processos podem gerar:

- Demora no processamento dos registros;
- Erros e inconsistências;
- Necessidade de conferência manual;
- Utilização de papel e toner;
- Dificuldade para auditoria;
- Dificuldade para geração de relatórios.

O EduPonto busca automatizar esse processo utilizando biometria e uma plataforma de gestão.

---

## 🎯 Objetivo

Desenvolver e validar um protótipo funcional de um sistema biométrico baseado em Raspberry Pi para controle automatizado da frequência docente.

O sistema deverá permitir:

- Cadastro de docentes;
- Cadastro biométrico;
- Autenticação por impressão digital;
- Registro de entrada;
- Registro de saída;
- Consulta dos registros;
- Geração de relatórios;
- Exportação de dados;
- Registro de auditoria;
- Proteção dos dados biométricos;
- Gestão administrativa.

---

## 🏗️ Arquitetura Proposta

```text
                    ┌──────────────────────┐
                    │       DOCENTE        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  TERMINAL BIOMÉTRICO │
                    │                      │
                    │    Raspberry Pi      │
                    │    Sensor Biométrico │
                    │    Display           │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │       SERVIDOR       │
                    │                      │
                    │ API / Banco de Dados │
                    │ Regras de Negócio    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      PORTAL WEB      │
                    │                      │
                    │ Gestores / Admin     │
                    │ Relatórios           │
                    │ Consultas            │
                    └──────────────────────┘
```

---

# 🔐 Autenticação Biométrica

O registro de frequência será realizado por meio da impressão digital do docente.

### Fluxo básico

```text
Docente
   │
   ▼
Apresenta impressão digital
   │
   ▼
Sensor biométrico realiza leitura
   │
   ▼
Sistema verifica biometria
   │
   ├── Não encontrada
   │       │
   │       ▼
   │   Exibe mensagem de erro
   │
   └── Encontrada
           │
           ▼
      Identifica docente
           │
           ▼
      Registra data/hora
           │
           ▼
      Registra auditoria
           │
           ▼
      Feedback ao usuário
```

---

# 👨‍🏫 Cadastro do Docente

O sistema deverá permitir o cadastro dos docentes que utilizarão o equipamento.

Durante o cadastro biométrico, poderão ser utilizadas duas impressões digitais para aumentar a disponibilidade de autenticação.

Os dados biométricos deverão ser tratados de forma segura, evitando o armazenamento direto da imagem da impressão digital.

---

# 🕐 Registro de Frequência

Após uma autenticação biométrica válida, o sistema deverá registrar:

- Identificação do docente;
- Data;
- Horário;
- Tipo de registro;
- Informações necessárias para auditoria.

O sistema deverá permitir o registro de entrada e saída.

---

# 📊 Portal de Gestão

O projeto prevê uma interface de gestão para usuários autorizados.

Entre as funcionalidades previstas estão:

- Consulta dos registros;
- Dashboard;
- Geração de relatórios;
- Exportação CSV;
- Exportação PDF;
- Gestão de usuários;
- Consulta de informações de frequência;
- Recursos relacionados à auditoria.

---

# 🔒 Segurança e Privacidade

A segurança dos dados é uma parte importante do EduPonto.

O projeto prevê:

- Criptografia dos dados biométricos;
- AES-256;
- HTTPS;
- Autenticação;
- Logs de auditoria;
- Backup criptografado;
- Controle de acesso;
- Proteção dos dados pessoais;
- Princípios de Privacy by Design.

Os dados biométricos não devem ser armazenados como imagens da impressão digital.

---

# 📋 Requisitos Funcionais

| ID | Requisito |
|---|---|
| RF01 | Cadastro de docente |
| RF02 | Cadastro biométrico |
| RF03 | Registro de consentimento |
| RF04 | Criptografia dos dados biométricos |
| RF05 | Autenticação biométrica |
| RF06 | Registro de entrada |
| RF07 | Registro de saída |
| RF08 | Feedback visual/sonoro |
| RF09 | Registro de auditoria |
| RF10 | Consulta de registros |
| RF11 | Dashboard |
| RF12 | Geração de relatórios |
| RF13 | Exportação CSV |
| RF14 | Exportação PDF |
| RF15 | Gestão de usuários |
| RF16 | Gestão dos direitos dos titulares |
| RF17 | Integração com sistemas educacionais |

---

# ⚙️ Requisitos Não Funcionais

| ID | Requisito | Meta |
|---|---|---|
| RNF01 | Tempo de autenticação | ≤ 3 segundos |
| RNF02 | Reconhecimento biométrico | ≥ 95% |
| RNF03 | Falsa aceitação (FAR) | ≤ 0,01% |
| RNF04 | Falsa rejeição (FRR) | ≤ 3% |
| RNF05 | Disponibilidade | ≥ 99% |
| RNF06 | Segurança | AES-256, HTTPS e auditoria |
| RNF07 | Privacidade | LGPD / Privacy by Design |
| RNF08 | Armazenamento biométrico | Templates protegidos |
| RNF09 | Usabilidade | ≥ 4,2/5 |
| RNF10 | Escalabilidade | Arquitetura modular |
| RNF11 | Manutenibilidade | Documentação técnica |
| RNF12 | Resiliência | Tolerância a falhas |

---

# 🖥️ Hardware

A proposta inicial considera:

- Raspberry Pi 4 Model B ou superior;
- Sensor biométrico AS608 ou R307;
- Display touchscreen;
- Câmera para Raspberry Pi;
- Cartão microSD;
- Fonte de alimentação;
- Gabinete/proteção física.

---

# 💻 Software

A proposta inicial considera:

- Raspberry Pi OS Lite 64-bit;
- Python 3.11+;
- Flask;
- SQLite;
- Biblioteca de comunicação com sensor biométrico;
- Biblioteca de criptografia;
- Biblioteca para geração de PDF;
- HTTPS;
- Autenticação por token;
- Sistema de logs de auditoria.

> As tecnologias podem ser alteradas durante a implementação conforme as decisões técnicas do projeto.

---

# 🔄 Funcionamento Offline

Uma questão de arquitetura que está sendo validada para o projeto é o funcionamento dos terminais sem conexão com a rede.

```text
             SEM INTERNET / REDE
                     │
                     ▼
          ┌─────────────────────┐
          │ Terminal biométrico │
          └──────────┬──────────┘
                     │
                     ▼
          Registro armazenado
             localmente
                     │
                     │
             Rede restaurada
                     │
                     ▼
          ┌─────────────────────┐
          │ Sincronização com   │
          │ servidor            │
          └──────────┬──────────┘
                     │
                     ▼
              Dados atualizados
```

A estratégia definitiva de sincronização e tratamento de conflitos ainda deverá ser definida durante a análise e validação dos requisitos.

---

# 🔋 Continuidade de Energia

Também está sendo avaliada a utilização de uma solução de alimentação de emergência, como bateria ou nobreak.

O objetivo seria permitir que o equipamento continue funcionando durante interrupções de energia e preserve os registros realizados.

A solução definitiva de alimentação ainda deverá ser definida na etapa de projeto do hardware.

---

# 👥 Histórias de Usuário

### Docente

> Como docente, quero utilizar minha impressão digital para me identificar, para realizar meu registro de frequência de forma automatizada.

### Administrador

> Como administrador, quero cadastrar um docente no sistema, para que ele possa utilizar o registro biométrico de frequência.

### Gestor

> Como gestor, quero consultar os registros de frequência, para acompanhar as marcações realizadas pelos docentes.

### Gestor

> Como gestor, quero gerar relatórios dos registros de frequência, para utilizar essas informações na gestão administrativa.

### Titular dos Dados

> Como titular dos dados, quero exercer os direitos relacionados aos meus dados pessoais, para ter controle sobre o tratamento das informações.

---

# 🧩 Stakeholders

| Stakeholder | Participação |
|---|---|
| Docentes | Utilização do sistema de registro |
| Gestores | Consulta e acompanhamento |
| Administradores | Administração do sistema |
| Instituição de ensino | Utilização da solução |
| Equipe de desenvolvimento | Desenvolvimento e manutenção |
| Responsável por dados | Questões de privacidade |
| Setor administrativo | Utilização dos registros |

---

# 📈 Indicadores do Projeto

As principais metas definidas para avaliação do projeto incluem:

- Reconhecimento biométrico ≥ 95%;
- Tempo médio de autenticação ≤ 3 segundos;
- FAR ≤ 0,01%;
- FRR ≤ 3%;
- Disponibilidade ≥ 99%;
- Redução do tempo de processamento;
- Redução das inconsistências;
- Redução do trabalho administrativo;
- Facilidade de uso ≥ 4,2/5.

---

# 🗂️ Documentação do Projeto

```text
Documentação
│
├── Canvas
├── SWOT / FOFA
├── Análise de Requisitos
├── Requisitos Funcionais
├── Requisitos Não Funcionais
├── Requisitos de Negócio
├── Requisitos de Hardware
├── Requisitos de Software
├── Histórias de Usuário
├── Critérios de Aceitação
├── Fluxos do Sistema
├── Casos de Uso
├── Diagramas UML
├── Arquitetura do Sistema
├── Documentação da API
├── Documentação do Hardware
└── Manual do Usuário
```

---

# 🚧 Status do Projeto

**Em desenvolvimento**

O projeto encontra-se na etapa de levantamento, análise e validação dos requisitos, seguida pelo desenvolvimento do protótipo e dos componentes de software.

### Etapas previstas

- [x] Definição do problema
- [x] Canvas
- [x] SWOT / FOFA
- [x] Levantamento inicial de requisitos
- [x] Requisitos funcionais
- [x] Requisitos não funcionais
- [x] Histórias de usuário
- [x] Fluxo principal
- [ ] Validação dos requisitos
- [ ] Arquitetura definitiva
- [ ] Desenvolvimento do protótipo
- [ ] Desenvolvimento da aplicação
- [ ] Integração hardware/software
- [ ] Testes
- [ ] Teste piloto
- [ ] Documentação final

---

# ❓ Questões em Validação

1. Um docente cadastrado em um terminal poderá registrar o ponto em outro terminal utilizando a mesma biometria?

2. Os terminais deverão compartilhar a mesma base biométrica entre si ou todos os dados deverão ser sincronizados com um servidor central?

3. O sistema deverá funcionar totalmente offline quando não houver conexão com a rede?

4. Quando estiver offline, o equipamento deverá armazenar os registros localmente e, após o restabelecimento da conexão, sincronizar automaticamente os dados com o servidor?

5. Como deverá funcionar a sincronização dos dados em caso de falha de rede ou conflito entre registros?

6. O equipamento terá bateria, nobreak ou algum outro sistema de alimentação de emergência para continuar funcionando durante uma queda de energia?

7. Em caso de queda de energia, o equipamento deverá continuar realizando os registros normalmente?

8. Haverá um portal web para que os gestores possam acessar e acompanhar as informações e os registros de frequência?

9. Quais informações e quais níveis de acesso estarão disponíveis para os gestores nesse portal?

10. O sistema permitirá que um gestor conteste um registro de ponto?

11. Como deverá funcionar o processo de contestação, análise e aprovação de um registro de ponto?

12. Os registros originais deverão permanecer imutáveis, sendo as alterações ou contestações registradas separadamente para fins de auditoria?

---

# 🎓 Projeto Acadêmico

O EduPonto está sendo desenvolvido como projeto acadêmico com foco em:

- Inovação tecnológica;
- IoT;
- Biometria;
- Automação;
- Segurança da informação;
- Gestão educacional;
- Privacidade de dados;
- Desenvolvimento de software e hardware.

---

# 📄 Licença

Projeto acadêmico desenvolvido para fins educacionais.

---

# 👨‍💻 Equipe

**Projeto:** EduPonto  
**Instituição:** UniSales  
**Curso:** Engenharia de Software

> Integrantes e demais informações da equipe devem ser adicionados conforme a composição oficial do projeto.
