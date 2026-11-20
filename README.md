# OrqLang — Transpilador para Python

**INF1022 — Analisadores Léxicos e Sintáticos | PUC-Rio | 2026.2**

**Professor:** Vitor Pinheiro de Almeida  
**Modalidade:** dupla

## Integrantes

| Nome | Git User |
| --- | --- |
| Gustavo Martins | gustavohoml |
| David Pinheiro | XXX |

## Sobre o projeto

Este repositório reúne o desenvolvimento de um **transpilador da linguagem OrqLang para Python**, como trabalho final da disciplina INF1022.

OrqLang é uma linguagem de domínio específico (DSL) para orquestração de tarefas e serviços. O transpilador deve ler um arquivo `.orq`, realizar **análise léxica e sintática** e produzir um arquivo `.py` executável, utilizando as funções de serviço fornecidas pelo professor.

```text
programa.orq → analisador léxico → analisador sintático → gerador → programa.py
                                                                  ↓
                                                         runtime.servicos
```

O foco do trabalho é a implementação do analisador e da tradução. **Os serviços Python já são fornecidos** no `orqlang-kit`.

## Tecnologias e ambiente

- **Python 3** para implementar o transpilador e executar o código gerado.
- **PLY (Python Lex-Yacc)** como ferramenta planejada para o lexer e o parser.
- **Git e GitHub** para versionamento.
- **GitHub Codespaces e Live Share** para desenvolvimento colaborativo.

Não é obrigatório criar um ambiente virtual ao trabalhar no mesmo Codespace. Se cada integrante criar seu próprio Codespace, deverá instalar as dependências nesse ambiente.

## Estrutura prevista

A estrutura abaixo é a **organização planejada** para o repositório. Ela poderá ser ajustada durante o desenvolvimento.

```text
.
├── enunciado/
├── exemplos/                    # exemplos fornecidos pelo professor
├── gerado/                      # arquivos Python gerados (quando aplicável)
├── orqlang-kit/                 # arquivos restantes da pasta disponibilizada pelo professor
├── runtime/
│   ├── __init__.py
│   ├── servicos.py
│   └── orqlang_runtime.py       # auxiliar para o bônus
├── testes/                      # testes e saídas esperadas do kit
├── transpilador/
│   ├── __init__.py
│   ├── lexer.py
│   ├── parser.py
│   ├── ast_nodes.py
│   ├── generator.py
│   └── main.py                     
├── .gitignore
├── README.md
└── requirements.txt
```

O kit original também inclui `docs/servicos.md`, com documentação dos serviços. Os arquivos fornecidos pelo professor devem ser preservados.

## Instalação

Abra o repositório no GitHub Codespaces (ou em um ambiente com Python 3 instalado) e execute, **na raiz do projeto**:

```bash
python --version
python -m pip install -r requirements.txt
```

O arquivo `requirements.txt` deverá conter, no mínimo:

```text
ply
```

Para verificar a instalação:

```bash
python -c "import ply; print('PLY funcionando!')"
```

### Verificar o kit de serviços

O kit inclui testes próprios da biblioteca de serviços. Execute:

```bash
python -m unittest discover -s testes -p "test_*.py"
```

Esse comando **testa os serviços fornecidos**, não a implementação do transpilador.

## Como usar o transpilador

> **Em desenvolvimento:** a interface de linha de comando ainda será implementada. Os comandos abaixo descrevem a interface que pretendemos adotar; poderão ser atualizados conforme o projeto evoluir.

A proposta é receber um arquivo OrqLang e gerar o Python correspondente:

```bash
python -m transpilador.main exemplos/01_basico.orq gerado/01_basico.py
```

Para executar o Python gerado no terminal Linux do Codespaces, a partir da raiz do repositório:

```bash
PYTHONPATH=. python gerado/01_basico.py
```

O `PYTHONPATH=.` permite localizar o pacote `runtime` durante a execução. No PowerShell, a configuração equivalente é:

```powershell
$env:PYTHONPATH="."
python gerado/01_basico.py
```

## Funcionalidades previstas

### Requisitos obrigatórios

- Reconhecimento de palavras reservadas, identificadores, números inteiros e decimais, strings, booleanos e comentários iniciados por `#`.
- Comandos `VAR`, `SERVICO` (com ou sem retorno) e `IMPRIMIR`.
- Expressões aritméticas (`+`, `-`, `*`, `/`), comparações (`==`, `!=`, `<`, `<=`, `>`, `>=`), parênteses e menos unário, respeitando a precedência e a associatividade especificadas.
- Condicionais `SE ... ENTAO ... [SENAO ...] FIM`, inclusive aninhados.
- Repetições `REPITA ... VEZES ... FIM`, com avaliação única da expressão de contagem e quantidade inteira não negativa.
- Reatribuição de variáveis com `VAR`.
- Geração de Python válido, preservando o comportamento dos programas OrqLang.
- Rejeição de programas com erros léxicos ou sintáticos, informando linha e token quando possível.

### Extensão opcional: operadores lógicos

Está prevista a possibilidade de adicionar `E`, `OU` e `NAO`, traduzidos para `and`, `or` e `not` em Python. Caso seja implementada, a precedência adotada será documentada.

### Bônus opcional: paralelismo

O enunciado prevê até **10 pontos percentuais adicionais** pela implementação correta de `PARALELO ... FIM`, respeitando a nota máxima da disciplina. Nesse bloco, deverão existir pelo menos duas chamadas `SERVICO` com variáveis de saída distintas. A execução concorrente poderá utilizar `runtime/orqlang_runtime.py`, fornecido pelo professor.

Essas extensões são opcionais e **não devem ser consideradas implementadas até serem concluídas e testadas**.

## Exemplo de programa OrqLang

```text
INICIO
    VAR usuario = 1
    VAR quantidade = 2
    SERVICO buscar_usuario(usuario) -> nome
    SERVICO buscar_preco(10) -> preco
    SERVICO calcular_total(preco, quantidade) -> total
    SE total >= 150 ENTAO
        SERVICO aplicar_desconto(total, 10) -> final
        IMPRIMIR final
    SENAO
        IMPRIMIR total
    FIM
FIM
```

Esse exemplo consta do enunciado do trabalho. A saída esperada indicada pelo professor é `180.0`.

## Testes e validação

A validação do transpilador deverá contemplar:

1. Transpilação dos programas válidos presentes em `exemplos/` (exceto o exemplo de paralelismo, caso o bônus não seja implementado).
2. Execução dos arquivos `.py` gerados e comparação com as saídas em `testes/*.esperado.txt`.
3. Testes de precedência, condicionais, repetições e aninhamentos.
4. Rejeição de programas inválidos, como ausência de `FIM` ou `ENTAO`, parênteses não fechados, caracteres ilegais e operadores sem operandos.
5. Criação de **pelo menos cinco programas `.orq` próprios**, incluindo ao menos um inválido, com registro das saídas esperadas ou resultados.

Os resultados dos testes serão documentados à medida que a implementação avançar.

## Organização do desenvolvimento

As atividades são acompanhadas em um quadro do Trello, com tarefas numeradas, pré-requisitos e acompanhamento de status. O desenvolvimento é realizado em dupla, utilizando GitHub Codespaces, Live Share e commits no repositório.

## Entrega

Conforme o enunciado, a entrega final será um único arquivo ZIP contendo:

- Código-fonte do lexer, parser e gerador;
- Instruções de instalação e execução;
- Pelo menos cinco programas de teste `.orq`, incluindo um inválido;
- Saídas esperadas e/ou resultados dos testes;
- Relatório curto com gramática final, decisões de tradução, testes e limitações;
- Nomes e matrículas dos dois integrantes.

**Estado atual:** projeto em desenvolvimento. 
