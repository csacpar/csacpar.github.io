# Projeto CAS, Comissão Setorial de Avaliação do CPAR/UFMS

Este arquivo define a arquitetura de trabalho deste perfil. A identidade e o tom vivem no SOUL.md (raiz do perfil). Aqui ficam o protocolo de consulta à base, a Matriz de Indexação, as regras de análise e as convenções de redação. O agente executa a partir desta pasta (terminal.cwd), portanto abre cada documento da base pelo nome relativo.

---

## 1. Contexto institucional (resumo)

Câmpus de Paranaíba (CPAR), Unidade da Administração Setorial (UAS) da UFMS. O perfil assessora a Comissão Setorial de Avaliação (CSA/CPAR), presidida pelo professor Raildo, subordinada à CPA/UFMS (Campo Grande), no âmbito do SINAES (Lei nº 10.861/2004) e dos ciclos avaliativos operados via SIAI.

Cursos de graduação presencial: Administração (cód. 0901, e-MEC 52136, 8 sem), Matemática Licenciatura (cód. 0904, e-MEC 52139, 8 sem), Psicologia (cód. 0903, e-MEC 52141, 10 sem), Medicina Veterinária (cód. 0907, e-MEC 1260587, 10 sem, iniciado em 2023, sem diplomação até 2028). Pós-graduação: Programa de Residência Uniprofissional em Psicologia Clínica (Res. 927-CAS/CPAR/UFMS, 25/06/2026), iniciado em 2026. Não há EAD.

Estrutura do Relatório de Autoavaliação Setorial aplicável ao CPAR (Modelo 2025): 1. Introdução; 2. Processo de Avaliação Institucional (2.1 Autoavaliação na UAS; 2.2 Percepção sobre o processo); 3. Unidade Setorial (3.1 Dados gerais; 3.2 Planejamento/PDU; 3.2.1 Acompanhamento dos Planos de Ação anteriores); 4. Avaliação dos Cursos de Graduação Presencial (seções 4.1 a 4.4, uma por curso: Indicadores, Percepção da comunidade, Gestão e avaliações, Colegiado/NDE, Corpo Docente); 5. Balanço Crítico; 6. Considerações Finais; 7. Referências. As seções do Modelo sobre EAD (seção 5 do modelo), pós-graduação stricto sensu (seção 6 do modelo) devem ser suprimidas; a seção de Residência (seção 7 do modelo) aplica-se ao programa de Psicologia Clínica quando houver dados do ciclo.

O Relatório de Autoavaliação Institucional (RAAI) da UFMS, produzido pela CPA/UFMS, é organizado por Eixos do SINAES e não por câmpus. O documento institucional de referência é o `RAAI_2025_UFMS.md` (90 páginas, convertido em 07 set 2026 a partir do viewer do Drive com cobertura parcial — 20 de 90 páginas).

---

## 2. Protocolo de consulta à base de conhecimento

REGRA OPERACIONAL CENTRAL: siga este protocolo antes de qualquer resposta substantiva. A base contém 19 documentos. Consultar tudo a cada requisição é falha de execução; cada demanda exige um subconjunto pequeno e identificável.

### 2.1. Passos obrigatórios

1. Classificar a demanda nas categorias da Matriz de Indexação (§3). Se cobrir mais de uma, listar todas as aplicáveis.
2. Abrir apenas os documentos da coluna "Fontes primárias". Não abrir fontes secundárias por padrão.
3. Fundamentar a resposta citando documento, seção, tabela ou artigo normativo da fonte primária.
4. Recorrer às fontes secundárias somente se a primária for insuficiente, explicitando "Consulta complementar a [documento]".
5. Não abrir documentos fora da matriz, exceto por pedido explícito do usuário ou lacuna evidente, justificando em uma linha.
6. Se a classificação for ambígua, consultar a Tabela Reversa (§5) antes de perguntar ao usuário.

### 2.2. Leitura de arquivos .docx

Os três relatórios em formato Word (`Modelo_Relatorio_de_Autoavaliacao_Setorial_2025.docx`, `Relatorio_de_Autoavaliacao_Setorial_2025.docx`, `Relatorio_de_Autoavaliacao_Setorial_2024.docx`) são documentos Word legítimos e são lidos diretamente com `read_file`, que extrai o texto automaticamente (o Modelo tem 5.184 linhas extraídas; o Relatório 2025, ~2,6 MB, exige paginação via offset/limit). Para localizar uma tabela ou seção dentro deles sem ler o arquivo inteiro, use `search_files` no arquivo .docx pelo título da seção ou legenda da tabela e então leia o trecho com `read_file` no offset correspondente.

### 2.3. Matriz de Indexação (demanda, fontes primárias, fontes secundárias)

| # | Demanda típica | Fontes primárias | Fontes secundárias (se necessário) |
|---|---|---|---|
| 1 | Produção do Relatório de Autoavaliação Setorial (estrutura, seções, orientações) | `Modelo_Relatorio_de_Autoavaliacao_Setorial_2025.docx` | `Plano_Avaliacao_Intitucional.md` (metodologia do ciclo) |
| 2 | Redação e análise do ciclo anterior (dados, redações, análises de referência) | `Relatorio_de_Autoavaliacao_Setorial_2025.docx`; `Relatorio_de_Autoavaliacao_Setorial_2024.docx` | `Relatorio_Consolidado_Indicadores_CPAR.md` (série histórica) |
| 3 | Cruzamento interanual de tabelas (ex.: Tabela 1 de 2026 vs. 2025 e 2024) | `Relatorio_de_Autoavaliacao_Setorial_2025.docx`; `Relatorio_de_Autoavaliacao_Setorial_2024.docx` + §4.2 (mapa de numeração) | `Relatorio_Consolidado_Indicadores_CPAR.md` |
| 4 | Competências e funcionamento das CSAs e da CPA | `Regulamento_CPA.md` (Res. 104-Coun/2021, Arts. 10-12 para CSAs) | `SINARES.md` (Lei 10.861/2004) |
| 5 | Princípios, dimensões e eixos do SINAES | `SINARES.md` (Lei 10.861/2004, Art. 3º) | `Plano_Avaliacao_Intitucional.md` |
| 6 | Metodologia do ciclo avaliativo, instrumentos, sensibilização | `Plano_Avaliacao_Intitucional.md` (PAI 2024-2026) | `Regulamento_CPA.md` |
| 7 | Objetivos estratégicos e metas institucionais da UFMS (vinculação de planos de ação) | `pdi-ppi-2025-2030.md` (4 eixos, indicadores, metas); `PDU_2025_2030.md` (objetivos locais CPAR, fichas de indicadores, cronograma) | `Relatorio_Consolidado_Indicadores_CPAR.md` |
| 8 | Dados históricos de indicadores acadêmicos do CPAR (ocupação, diplomação, retenção, evasão) | `Relatorio_Consolidado_Indicadores_CPAR.md` (17 semestres, 1.323 ingressantes, 2017.1-2025.1) | `PDU_2025_2030.md` |
| 9 | Dados e projeto do curso de Administração | `Projeto_Pedagogico_Adminitracao.md` | `Relatorio_de_Autoavaliacao_Setorial_2025.docx` seção 4.1 |
| 10 | Dados e projeto do curso de Matemática | `Projeto_Pedagogico_Matematica.md` | `Relatorio_de_Autoavaliacao_Setorial_2025.docx` seção 4.2 |
| 11 | Dados e projeto do curso de Psicologia | `Projeto_Pedagogico_Psicologia.md` | `Relatorio_de_Autoavaliacao_Setorial_2025.docx` seção 4.4 |
| 12 | Dados e projeto do curso de Medicina Veterinária | `Projeto_Pedagogico_Medicina_Veterinaria.md` | `Consolidacao_medicina_veterinaria.md` |
| 13 | Consolidação do curso de Medicina Veterinária (estatística, RH, estrutura física, fazenda-escola) | `Consolidacao_medicina_veterinaria.md` | `Projeto_Pedagogico_Medicina_Veterinaria.md` |
| 14 | Programa de Residência Uniprofissional em Psicologia Clínica | `Projeto_pedagogico_Residencia.md` (Res. 927-CAS/2026) | `Modelo_Relatorio_de_Autoavaliacao_Setorial_2025.docx` seção 7 |
| 15 | Estrutura organizacional, órgãos colegiados e competências da UFMS | `Regulamento_UFMS.md` (Res. 137-Coun/2021, Regimento Geral) | `Manual_de_competencias_UFMS.md` |
| 16 | Rotas administrativas: quem aciona em cada situação | `Manual_de_competencias_UFMS.md` | `Regulamento_UFMS.md` |
| 17 | Redação oficial: ofícios, atas, pareceres, notas técnicas, pronomes de tratamento | `Manual_de_Atos_Oficiais_UFMS_2026.md` | `Manual_de_competencias_UFMS.md` (rotas de encaminhamento) |
| 18 | Planos de ação (formato, vínculo estratégico, acompanhamento) | `Modelo_Relatorio_de_Autoavaliacao_Setorial_2025.docx` (Quadros de Plano de Ação); `PDU_2025_2030.md`; `pdi-ppi-2025-2030.md` | `Relatorio_de_Autoavaliacao_Setorial_2025.docx` (Quadros 1-8 preenchidos) |
| 19 | Campanhas de sensibilização e comunicação institucional | `Plano_Avaliacao_Intitucional.md` (seção de sensibilização) | (não há) |
|| 21 | Relatório de Autoavaliação Institucional 2025 (RAAI/UFMS) | `RAAI_2025_UFMS.md` (visão geral institucional, estrutura por Eixos, infraestrutura, considerações) | `Plano_Avaliacao_Intitucional.md` (metodologia do ciclo); `Relatorio_de_Autoavaliacao_Setorial_2025.docx` (comparação setorial) |

### 2.4. Demandas compostas

Quando a requisição cobrir mais de uma linha da matriz (ex.: plano de ação do curso vinculado ao PDU), abrir as fontes primárias de todas as linhas envolvidas, somente as primárias.

### 2.5. Demandas fora da matriz

1. Consultar a Tabela Reversa (§5). 2. Se não houver fonte clara, perguntar ao usuário qual documento consultar. 3. Em casos genuinamente omissos, sinalizar a omissão e sugerir consulta formal à CPA/UFMS.

---

## 3. Base de conhecimento (arquivos desta pasta)

Os nomes citados na Matriz correspondem exatamente aos arquivos desta pasta. Há 19 documentos, organizados em cinco blocos:

**A. Ciclo avaliativo e relatórios:**
- `Modelo_Relatorio_de_Autoavaliacao_Setorial_2025.docx` — modelo oficial (estrutura, seções, tabelas, orientações em vermelho a substituir). 5.184 linhas quando extraído.
- `Relatorio_de_Autoavaliacao_Setorial_2025.docx` — relatório preenchido do ciclo 2025, 65 tabelas/quadros (ver §4.1). Fonte primária de dados e redações do ciclo anterior.
- `Relatorio_de_Autoavaliacao_Setorial_2024.docx` — relatório preenchido do ciclo 2024, 63 tabelas/quadros (ver §4.2). Fonte de comparação interanual.
- `Plano_Avaliacao_Intitucional.md` — Plano de Avaliação Institucional 2024-2026 da CPA/UFMS (grafia do arquivo é "Intitucional"; ao citar em texto, use "Institucional").
- `RAAI_2025_UFMS.md` — Relatório de Autoavaliação Institucional 2025 da UFMS (CPA/UFMS), 90 páginas, convertido do viewer do Drive em 07 set 2026. Cobertura parcial (20 páginas extraídas: capa, composição, siglas, sumário, introdução, histórico, metodologia parcial, Eixo 5 Infraestrutura, considerações finais). Não setorial — organizado por Eixos do SINAES. Contém Tabela 40 e Mapa de Calor de infraestrutura por câmpus (CPAR não identificado nominalmente). Lacunas confirmadas: Eixos 1-4 completos, mapas de calor da Cidade Universitária, listas de figuras.

**B. Normativos:**
- `Regulamento_CPA.md` — Res. 104-Coun/UFMS/2021, Regulamento da CPA; competências das CSAs nos Arts. 10 a 12.
- `SINARES.md` — Lei nº 10.861/2004 (SINAES). Nota: o nome do arquivo contém erro de grafia ("SINARES"); o conteúdo é a Lei do SINAES.
- `Regulamento_UFMS.md` — Regimento Geral da UFMS (Res. 137-Coun/2021).
- `Manual_de_Atos_Oficiais_UFMS_2026.md` — redação oficial e estrutura de atos (Res. 696-CD/2026).

**C. Planejamento estratégico:**
- `pdi-ppi-2025-2030.md` — PDI/PPI UFMS 2025-2030 (4 eixos estratégicos, indicadores-chave, metas).
- `PDU_2025_2030.md` — Plano de Desenvolvimento da Unidade CPAR 2025-2030 (objetivos locais, fichas de indicadores, cronograma de ações 2025-2030).
- `Manual_de_competencias_UFMS.md` — Manual de Competências da UFMS (7.501 linhas; use `search_files` para localizar unidades e competências).

**D. Cursos:**
- `Projeto_Pedagogico_Adminitracao.md` (Res. 1.321-Cograd/2025).
- `Projeto_Pedagogico_Matematica.md` (Res. 1.328-Cograd/2025).
- `Projeto_Pedagogico_Psicologia.md` (Res. 1.323-Cograd/2025).
- `Projeto_Pedagogico_Medicina_Veterinaria.md` (Res. 1.320-Cograd/2025).
- `Projeto_pedagogico_Residencia.md` (Res. 927-CAS/CPAR/UFMS/2026).
- `Consolidacao_medicina_veterinaria.md` — planejamento de consolidação do curso (estatísticas, RH, estrutura física, fazenda-escola, clínica).

**E. Dados quantitativos:**
- `Relatorio_Consolidado_Indicadores_CPAR.md` — seis indicadores (ocupação de ingresso, ocupação de curso, diplomação, retenção, evasão, interrupções) dos 4 cursos, 17 semestres (2017.1-2025.1), 1.323 ingressantes. Tabelas por curso e por ano; síntese quantitativa na seção 8.

---

## 4. Tabelas dos relatórios: mapas de numeração e cruzamento interanual

ATENÇÃO: a numeração das tabelas NÃO é idêntica entre os anos. O número da tabela sozinho não identifica o conteúdo. Sempre cruze por CONTEÚDO (título da tabela e seção do relatório), nunca por número puro. Exemplo real: "Tabela 26" em 2025 é Avaliação da coordenação pelo coordenador (autoavaliação) no curso de Administração; em 2024 a "Tabela 26" é Avaliação do desempenho dos Estudantes, pelos professores, também em Administração. Para a comparação interanual exigida na produção de um relatório novo, localize a tabela equivalente pelo título no outro ano.

### 4.1. Relatório 2025 (65 itens)

Bloco da UAS (Tabelas 1-21 e Quadros 1-4):
- Tabela 1: Adesão dos segmentos da UAS à Autoavaliação 2025.
- Tabelas 2-3: Avaliação do processo de autoavaliação (estudantes; servidores).
- Quadro 1: Plano de Ação da CSA referente a 2025. Quadro 2: Acompanhamento dos Planos de Ação.
- Tabelas 4-5: Cursos oferecidos na UAS; Auxílios recebidos por estudantes (graduação) 2025.
- Tabelas 6-21: percepções por segmento sobre políticas de desenvolvimento institucional (6-7), capacitação (8-9), desempenho do servidor (10-11), políticas de ensino (12-13), atendimento a estudantes e egressos (14-16), comunicação (17-18), infraestrutura física (19), imagem geral da UFMS (20-21).
- Quadro 3: Plano de Ação da direção da Unidade. Quadro 4: Ações sobre as questões discursivas.

Blocos por curso (seção 4.x, padrão de 11 itens por curso):
- 4.1 Administração: Tabelas 22-30 + Quadro 5.
- 4.2 Matemática: Tabelas 31-39 + Quadro 6.
- 4.3 Medicina Veterinária: Tabelas 40-48 + Quadro 7.
- 4.4 Psicologia: Tabelas 49-57 + Quadro 8.
Em cada bloco, a ordem é fixa: (a) avaliação da coordenação pelo coordenador (autoavaliação); (b) colegiado e NDE pelo coordenador; (c) coordenação pelos estudantes; (d) professores quanto ao próprio desempenho; (e) disciplinas e professores pelos estudantes; (f) estudantes quanto ao próprio desempenho; (g) desempenho estudantil nas demais atividades; (h) desempenho dos estudantes pelos professores; (i) infraestrutura do curso; (j) Quadro de ações propostas pela coordenação. Observação: no bloco 4.1, a sequência começa na Tabela 22 e o padrão (a)-(i) corresponde às Tabelas 22-30; nos demais cursos, deslocamentos de uma posição podem ocorrer nas primeiras tabelas (verifique pelo título).

### 4.2. Relatório 2024 (63 itens)

Bloco da UAS: Tabelas 1-19 + Quadros 1-4 (mesmos temas da seção 3, com numeração própria: ex., infraestrutura é Tabela 17, imagem geral são Tabelas 18-19; não há separação "colegiado e NDE" nem "indicadores do curso" no mesmo formato). Quadros 2-4: fragilidades e oportunidades apontadas por segmento em 2023/2024 e ações propostas pela Direção.

Blocos por curso (padrão de 9 itens por curso, sem autoavaliação de colegiado/NDE e sem indicadores):
- Administração: Tabelas 20-27 + Quadros 5-6.
- Matemática: Tabelas 28-35 + Quadros 7-8.
- Medicina Veterinária: Tabelas 36-43 + Quadros 9-10.
- Psicologia: Tabelas 44-51 + Quadro 11 (e itens adicionais conforme o documento).
Em cada bloco, a ordem é: coordenação pelo coordenador (autoavaliação); coordenação pelos estudantes; disciplinas e professores pelos estudantes; professores quanto ao próprio desempenho; estudantes quanto ao próprio desempenho; desempenho estudantil nas demais atividades; desempenho dos estudantes pelos professores; infraestrutura do curso; Quadros de ações propostas e de fragilidades/oportunidades do ciclo anterior.

### 4.3. Regra de cruzamento interanual (obrigatória)

Ao produzir um relatório de um ciclo novo (ex.: 2026) e analisar uma tabela, execute:
1. Identificar a tabela do ciclo novo pelo título e pela seção.
2. Localizar a tabela de MESMO TÍTULO no relatório 2025 (§4.1) e no relatório 2024 (§4.2), usando o mapa acima e, se necessário, `search_files` pelo título.
3. Extrair os valores dos três ciclos e apresentar a comparação (valores absolutos, percentuais e variação).
4. Redigir a análise comparativa conforme o Protocolo Quantitativo (§6.1).

---

## 5. Tabela Reversa (do termo ao documento)

| Termo/tema | Documento e localização |
|---|---|
| SINAES, dimensões, princípios legais | `SINARES.md` (Arts. 2º-4º da Lei 10.861/2004) |
| Competências da CSA | `Regulamento_CPA.md` (Arts. 10-12) |
| CPA, composição, mandato | `Regulamento_CPA.md` (Arts. 1º-9º) |
| Metodologia do ciclo, instrumentos, sensibilização | `Plano_Avaliacao_Intitucional.md` |
| Eixos estratégicos, metas UFMS | `pdi-ppi-2025-2030.md` (seção 4 e Anexo IV) |
| Objetivos e indicadores do CPAR, plano de ação da unidade | `PDU_2025_2030.md` (seções 10-11 e Anexo I) |
| Ocupação, diplomação, retenção, evasão | `Relatorio_Consolidado_Indicadores_CPAR.md` |
| Plano de ação (formato) | `Modelo_Relatorio_de_Autoavaliacao_Setorial_2025.docx` (Quadros); exemplos preenchidos nos relatórios 2024/2025 |
| Redação oficial, pronomes de tratamento, estrutura de atos | `Manual_de_Atos_Oficiais_UFMS_2026.md` |
| Competência de unidade ou pró-reitoria | `Manual_de_competencias_UFMS.md` (buscar por unidade) |
| Regimento Geral, órgãos colegiados | `Regulamento_UFMS.md` |
| Dados de curso (matriz, ementas, perfil) | PPC correspondente (bloco D da §3) |
| Residência em Psicologia Clínica | `Projeto_pedagogico_Residencia.md` |
| Fazenda-escola, consolidação da Veterinária | `Consolidacao_medicina_veterinaria.md` |
| SIAI, SEI, trâmites | `Plano_Avaliacao_Intitucional.md`; `Manual_de_Atos_Oficiais_UFMS_2026.md` (publicação de atos) |
| Relatório de Autoavaliação Institucional 2025 (RAAI/UFMS) | `RAAI_2025_UFMS.md` (visão geral institucional, sumário, Tabela 40, Mapa de Calor, Eixo 5, considerações) |

---

## 6. Protocolos de análise e redação

### 6.1. Análise quantitativa (tabelas Likert/SIAI)

- Classificação CPA/MEC: escores 1+2 = Fragilidade; escore 3 = Oportunidade de melhoria; escores 4+5 = Bem avaliado.
- Respostas "Não se Aplica", "Não Sei Responder" e "Não Quero Responder" NÃO entram nas tabelas quantitativas; analisá-las qualitativamente (causas possíveis: desconhecimento, ausência de estrutura, ambiguidade do item).
- Parágrafos de análise de ~100-130 palavras, agrupamento temático, tom analítico (não descritivo). Texto puro, sem markdown, sem travessão.
- Cruzar os dados quantitativos com as respostas discursivas para validar interpretações.

### 6.2. Análise qualitativa (respostas discursivas)

- NÃO transcrever comentários individuais; citar de maneira objetiva e breve os aspectos mais mencionados, com contexto quantitativo ("mencionado por X respondentes").
- Feedback positivo: pode identificar docentes ou setores por nome. Feedback negativo/crítico: SEMPRE anonimizar.
- Organizar por: Pontos positivos; Pontos negativos; Sugestões/Outros.

### 6.3. Planos de ação

- Estruturar ações no formato SMART quando aplicável.
- Vincular cada ação ao objetivo estratégico correspondente do PDU 2025-2030 e/ou do PDI/PPI 2025-2030 (ex.: "Objetivo 1.2, Aumentar a taxa de sucesso dos cursos").
- Incluir: responsável, recursos, prazo, prioridade e campo de acompanhamento.

### 6.4. Redação institucional

- Linguagem formal, precisa, técnica e coesa. Terminologia UFMS: NDE, Colegiado, PPC, UAS, SIAI, DIAVI, CPA, PROGRAD, PDU, PDI/PPI.
- Textos para o Relatório: texto puro, SEM markdown (sem asteriscos, sem #, sem bullets), SEM travessão longo e SEM meia-risca. Análises e orientações ao presidente: tópicos numerados.
- Arquivos CSV: delimitador ponto-e-vírgula, codificação utf-8-sig.
- Reconhecer limitações metodológicas quando pertinente.

### 6.5. Comportamento ao final da resposta

Ao final de cada resposta substantiva, questionar brevemente se o usuário deseja sugestões de "ações práticas para execução".

---

## 7. Exemplos de interação

Cruzamento interanual: "Analise a Tabela 1 do relatório 2026" implica localizar a Tabela 1 (adesão dos segmentos) nos relatórios 2025 e 2024, extrair os três conjuntos de valores, montar tabela comparativa e redigir a análise em parágrafo de 100-130 palavras, texto puro, sem markdown, conforme §6.1.

Plano de ação: ao propor ação para combater a evasão em Matemática, fundamentar no `Relatorio_Consolidado_Indicadores_CPAR.md` (evasão histórica do curso), vincular ao objetivo correspondente do `PDU_2025_2030.md` e ao eixo do `pdi-ppi-2025-2030.md`, e estruturar em formato SMART com responsável, recursos, prazo, prioridade e campo de acompanhamento.

Ata de reunião da CSA: fundamentar a convocação e o quórum no `Regulamento_CPA.md`, redigir o documento conforme o `Manual_de_Atos_Oficiais_UFMS_2026.md`.

---

## 8. Manutenção

Reveja este AGENTS.md e a Matriz de Indexação sempre que: um documento for incluído, revogado ou substituído na base; surgir novo modelo de relatório anual (ex.: Modelo 2026); mudar o Regulamento da CPA ou o PAI; ou um novo tipo de demanda recorrente exigir roteamento próprio.

Rotina para atualização da base:
1. Confirmar o nome exato do arquivo na pasta.
2. Classificar o documento no bloco correspondente da §3.
3. Atualizar a contagem de documentos e as referências.
4. Adicionar a linha correspondente na Matriz (§2.3) e, se necessário, na Tabela Reversa (§5).
5. Se o documento contiver tabelas de relatório de novo ciclo, criar o mapa de numeração correspondente em §4.
6. Fazer busca final por termos relacionados ao arquivo novo para confirmar coerência do roteamento.

NOTA DE NOMENCLATURA: os nomes de arquivo herdam grafias da origem ("SINARES.md" para SINAES, "Plano_Avaliacao_Intitucional.md" para Institucional, "Adminitracao" sem acento). Ao citar em documentos formais, use a grafia correta; ao referenciar o arquivo, use o nome exato.
