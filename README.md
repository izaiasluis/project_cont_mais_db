# ContMais DB – DRE Dinâmica

## 1. Visão Geral do Projeto

O **ContMais DB – DRE Dinâmica** é uma solução Full-Stack desenvolvida para automatizar a leitura, processamento e visualização da **Demonstração do Resultado do Exercício (DRE)**. O projeto integra o processamento de dados transacionais armazenados em um banco de dados MySQL a um Dashboard web moderno e responsivo, demonstrando a comunicação eficiente entre as camadas.

---

## 2. Tecnologias Envolvidas

| Foco | Tecnologia |
| :--- | :--- |
| **Backend / Lógica** | Python (Cálculo, Serialização JSON, `mysql.connector`) |
| **Dados** | MySQL (Estrutura `lancamentos` e `plano_de_contas`) |
| **Frontend / Visual** | HTML, CSS (Responsividade via Flexbox e Media Queries), JavaScript (Manipulação DOM, `fetch`) |

---

## 3. Estrutura de Diretórios

O projeto segue uma arquitetura modular, separando a lógica de dados da apresentação:

project_CONT_MAIS_DB/ ├── .env # Credenciais de acesso ao MySQL. ├── calcular_dre.py # Script principal de backend e exportação de dados. ├── data/ │ └── dre_resultado.json # Arquivo de saída com a DRE para o Frontend. └── frontend/ ├── index.html # Estrutura do Dashboard com IDs para injeção de dados. ├── style.css # Estilização com design profissional e responsivo. └── app.js # Lógica JavaScript (fetch e DOM manipulation).
---

## 4. Análise da Complexidade Algorítmica (Big O)

A complexidade de tempo da aplicação é dominada pelo acesso ao banco de dados:

* **Complexidade Dominante:** **$O(N)$ (Tempo Linear)**, onde $N$ é o número de registros na tabela `lancamentos`. O custo reside nas consultas SQL de agregação (`SUM()`), que escalam linearmente com o volume de dados.
* **Complexidade Constante:** O código Python (cálculo do lucro) e o Frontend (leitura e exibição do JSON) operam em **$O(1)$ (Tempo Constante)**, pois realizam um número fixo de passos.

Esta arquitetura garante que a solução seja escalável e eficiente, delegando o processamento pesado ao MySQL.

---

## 5. Guia de Execução

1.  **Geração de Dados:** Garanta que a pasta `data/` exista. Execute o script Python para consultar o banco e gerar o JSON:
    ```bash
    python calcular_dre.py
    ```
2.  **Visualização:** Abra o `frontend/index.html` utilizando a extensão **Live Server** no VS Code para garantir que o JavaScript possa ler o `dre_resultado.json` sem falhas de segurança do navegador.

---

## 6. Relatório de Desafios e Soluções (Troubleshooting)

Este relatório documenta as dificuldades técnicas superadas e as soluções implementadas, demonstrando a robustez da solução:

| Desafio Encontrado | Solução Implementada | Conceito-Chave |
| :--- | :--- | :--- |
| **Falha na Criação de Pasta** | Uso de **`os.makedirs(..., exist_ok=True)`** no Python para garantir que o diretório `data/` fosse criado antes da exportação JSON. | Robustez de Caminhos |
| **Erro de Leitura `fetch()`** | Utilização do **Live Server** para contornar as restrições de segurança (CORS) do navegador ao tentar ler arquivos locais. | Ambiente de Desenvolvimento |
| **Dessincronização de Chaves** | Correção no Python para usar chaves em *CamelCase* (`ReceitaBruta`, etc.) no dicionário `dre_data`, sincronizando com a expectativa do JavaScript. | Sincronização API/Frontend |
| **Falha Crítica na Serialização** | Implementação de **`float(valor) if valor is not None else 0.0`** no Python. Esta adaptação resolveu o erro do `json.dump` ao tentar serializar tipos de dados como `Decimal` (do MySQL) para `float` padrão. | **Type Casting (Serialização)** |
