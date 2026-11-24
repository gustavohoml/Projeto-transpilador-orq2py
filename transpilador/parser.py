
import ply.yacc as yacc
from .lexer import tokens, lexer
from .ast_nodes import (
    Programa,
    Atribuicao,
    Imprimir,
    Servico,
    Identificador,
    Numero,
    String,
    Booleano,
    Binaria,
    Unaria,
    Condicional,
    Repeticao
)

# GRAMÁTICA BÁSICA

def p_programa(p):
    'programa : INICIO comandos FIM'
    p[0] = Programa(comandos=p[2])


def p_comandos_unico(p):
    'comandos : comando'
    p[0] = [p[1]]


def p_comandos_lista(p):
    'comandos : comandos comando'
    p[0] = p[1] + [p[2]]


# COMANDOS BÁSICOS

def p_comando_atribuicao(p):
    'comando : VAR ID ATRIBUICAO expr'
    p[0] = Atribuicao(
        nome=Identificador(p[2]),
        valor=p[4]
    )


def p_comando_imprimir(p):
    'comando : IMPRIMIR expr'
    p[0] = Imprimir(expressao=p[2])


def p_comando_servico(p):
    '''comando : SERVICO ID ABRE_PARENTESES argumentos_opcionais FECHA_PARENTESES retorno_opcional'''
    p[0] = Servico(
        nome=p[2],
        argumentos=p[4],
        destino=p[6]
    )


# ARGUMENTOS E RETORNO

def p_argumentos_opcionais(p):
    '''argumentos_opcionais : argumentos
                            | vazio'''
    if p[1] is None:
        p[0] = []
    else:
        p[0] = p[1]


def p_argumentos_unico(p):
    'argumentos : expr'
    p[0] = [p[1]]


def p_argumentos_lista(p):
    'argumentos : argumentos VIRGULA expr'
    p[0] = p[1] + [p[3]]


def p_retorno_opcional(p):
    '''retorno_opcional : SETA ID
                        | vazio'''
    if len(p) == 3:
        p[0] = Identificador(p[2])
    else:
        p[0] = None


def p_vazio(p):
    'vazio :'
    p[0] = None


# EXPRESSÕES SIMPLES

def p_expr_numero(p):
    'expr : NUM'
    p[0] = Numero(valor=p[1])


def p_expr_string(p):
    'expr : STR'
    p[0] = String(valor=p[1][1:-1])


def p_expr_identificador(p):
    'expr : ID'
    p[0] = Identificador(nome=p[1])


def p_expr_booleano(p):
    '''expr : VERDADEIRO
            | FALSO'''
    p[0] = Booleano(valor=(p[1] == 'VERDADEIRO'))

# EXTENSÕES DA GRAMATICA

# CONDICIONAL
def p_comando_se(p):
    'comando : SE expr ENTAO comandos FIM'
    p[0] = Condicional(condicao=p[2], entao=p[4])

def p_comando_se_senao(p):
    'comando : SE expr ENTAO comandos SENAO comandos FIM'
    p[0] = Condicional(condicao=p[2], entao=p[4], senao=p[6])

#REPETIÇÃO
def p_comando_repita(p):
    'comando : REPITA expr VEZES comandos FIM'
    p[0] = Repeticao(quantidade=p[2], comandos=p[4])

#EXPRESSÕES
precedence = (
    ('nonassoc', 'IGUAL', 'DIFERENTE', 'MENOR', 'MAIOR', 'MENOR_IGUAL', 'MAIOR_IGUAL'),
    ('left', 'MAIS', 'MENOS'),
    ('left', 'ASTERISCO', 'BARRA'),
    ('right', 'UMENOS'),
)

def p_expr_binaria(p):
    '''expr : expr MAIS expr
            | expr MENOS expr
            | expr ASTERISCO expr
            | expr BARRA expr
            | expr IGUAL expr
            | expr DIFERENTE expr
            | expr MENOR expr
            | expr MAIOR expr
            | expr MENOR_IGUAL expr
            | expr MAIOR_IGUAL expr'''
    p[0] = Binaria(esquerda=p[1], operador=p[2], direita=p[3])

def p_expr_unaria(p):
    'expr : MENOS expr %prec UMENOS'
    p[0] = Unaria(operador='-', operando=p[2])

def p_expr_parenteses(p):
    'expr : ABRE_PARENTESES expr FECHA_PARENTESES'
    p[0] = p[2]

# TRATAMENTO DE ERROS

def p_error(p):
    if p is None:
        raise SyntaxError(
            "Fim inesperado do programa."
        )

    raise SyntaxError(
        f"Token inesperado '{p.value}' "
        f"({p.type}) na linha {p.lineno}"
    )


# INICIALIZAÇÃO DO PARSER

parser = yacc.yacc(start='programa')


def analisar_codigo(codigo: str) -> Programa:
    lexer.lineno = 1
    return parser.parse(codigo, lexer=lexer)


# TESTES DO PARSER

if __name__ == "__main__":
    from pprint import pprint

    testes = [
        (
            "1. Atribuicao simples",
            "INICIO VAR x = 10 FIM",
            True
        ),
        (
            "2. Multiplos comandos",
            '''
            INICIO
            VAR x = 10
            VAR y = 2.5
            IMPRIMIR x
            IMPRIMIR y
            FIM
            ''',
            True
        ),
        (
            "3. Strings e booleanos",
            '''
            INICIO
            VAR nome = "Ana"
            VAR ativo = VERDADEIRO
            VAR bloqueado = FALSO
            IMPRIMIR nome
            FIM
            ''',
            True
        ),
        (
            "4. Servico sem argumentos",
            "INICIO SERVICO teste() FIM",
            True
        ),
        (
            "5. Servico com um argumento",
            "INICIO SERVICO buscar_preco(10) FIM",
            True
        ),
        (
            "6. Servico com varios argumentos",
            '''
            INICIO
            SERVICO teste(10, 2.5, "Ana", VERDADEIRO, x)
            FIM
            ''',
            True
        ),
        (
            "7. Servico com retorno",
            '''
            INICIO
            SERVICO buscar_preco(10) -> preco
            IMPRIMIR preco
            FIM
            ''',
            True
        ),
        (
            "8. Servico sem argumentos com retorno",
            "INICIO SERVICO teste() -> resultado FIM",
            True
        ),
        (
            "9. Comentarios e reatribuicao",
            '''
            INICIO
            VAR x = 10
            # Atualizando a variavel
            VAR x = 20
            IMPRIMIR x
            FIM
            ''',
            True
        ),
        (
            "10. Programa vazio",
            "INICIO FIM",
            False
        ),
        (
            "11. Falta INICIO",
            "VAR x = 10 FIM",
            False
        ),
        (
            "12. Falta FIM",
            "INICIO VAR x = 10",
            False
        ),
        (
            "13. Atribuicao sem valor",
            "INICIO VAR x = FIM",
            False
        ),
        (
            "14. Servico sem fechar parenteses",
            "INICIO SERVICO teste(10 FIM",
            False
        ),
        (
            "15. Virgula sem argumento",
            "INICIO SERVICO teste(10,) FIM",
            False
        ),
        (
            "16. Seta sem identificador",
            "INICIO SERVICO teste() -> FIM",
            False
        ),
        (
            "17. Caractere ilegal",
            "INICIO VAR x = 10 @ FIM",
            False
        ),

        # EXPRESSOES: o 4o elemento (opcional) e a AST esperada,
        # para conferir precedencia e associatividade, nao so se aceita.
        (
            "18. Precedencia: * antes de +",
            "INICIO IMPRIMIR 2 + 3 * 4 FIM",
            True,
            Binaria(Numero(2), '+', Binaria(Numero(3), '*', Numero(4)))
        ),
        (
            "19. Parenteses mudam a precedencia",
            "INICIO IMPRIMIR (2 + 3) * 4 FIM",
            True,
            Binaria(Binaria(Numero(2), '+', Numero(3)), '*', Numero(4))
        ),
        (
            "20. Associatividade a esquerda na subtracao",
            "INICIO IMPRIMIR 10 - 3 - 2 FIM",
            True,
            Binaria(Binaria(Numero(10), '-', Numero(3)), '-', Numero(2))
        ),
        (
            "21. Associatividade a esquerda na divisao",
            "INICIO IMPRIMIR 8 / 4 / 2 FIM",
            True,
            Binaria(Binaria(Numero(8), '/', Numero(4)), '/', Numero(2))
        ),
        (
            "22. Menos unario antes da multiplicacao",
            "INICIO IMPRIMIR -2 * 3 FIM",
            True,
            Binaria(Unaria('-', Numero(2)), '*', Numero(3))
        ),
        (
            "23. Menos unario seguido de soma",
            "INICIO IMPRIMIR -5 + 8 FIM",
            True,
            Binaria(Unaria('-', Numero(5)), '+', Numero(8))
        ),
        (
            "24. Menos unario em parenteses e variavel",
            "INICIO IMPRIMIR -(2 + 3) - -x FIM",
            True,
            Binaria(
                Unaria('-', Binaria(Numero(2), '+', Numero(3))),
                '-',
                Unaria('-', Identificador('x'))
            )
        ),
        (
            "25. Comparacao tem a menor precedencia",
            "INICIO IMPRIMIR x + 1 >= 2 * y FIM",
            True,
            Binaria(
                Binaria(Identificador('x'), '+', Numero(1)),
                '>=',
                Binaria(Numero(2), '*', Identificador('y'))
            )
        ),
        (
            "26. Todos os operadores de comparacao",
            '''
            INICIO
            IMPRIMIR a == b
            IMPRIMIR a != b
            IMPRIMIR a < b
            IMPRIMIR a <= b
            IMPRIMIR a > b
            IMPRIMIR a >= b
            FIM
            ''',
            True
        ),
        (
            "27. Expressoes em VAR e argumentos de SERVICO",
            '''
            INICIO
            VAR total = preco * quantidade - 10
            SERVICO aplicar_desconto(total / 2, (5 + 5) * 2) -> final
            FIM
            ''',
            True
        ),
        (
            "28. Comparacao encadeada (proibida)",
            "INICIO IMPRIMIR 1 < x < 10 FIM",
            False
        ),
        (
            "29. Operador sem operando a direita",
            "INICIO VAR x = 1 + FIM",
            False
        ),
        (
            "30. Operador sem operando a esquerda",
            "INICIO IMPRIMIR * 2 FIM",
            False
        ),
        (
            "31. Parentese nao fechado",
            "INICIO IMPRIMIR (2 + 3 FIM",
            False
        ),
        (
            "32. Parenteses vazios",
            "INICIO IMPRIMIR () FIM",
            False
        ),

        # CONDICIONAL
        (
            "33. SE sem SENAO",
            '''
            INICIO
            SE x > 10 ENTAO
                IMPRIMIR "grande"
            FIM
            FIM
            ''',
            True
        ),
        (
            "34. SE com SENAO",
            '''
            INICIO
            SE ativo ENTAO
                IMPRIMIR "ativo"
            SENAO
                IMPRIMIR "inativo"
            FIM
            FIM
            ''',
            True
        ),
        (
            "35. SE aninhado: SENAO pertence ao SE mais proximo",
            '''
            INICIO
            SE a ENTAO
                SE b ENTAO
                    IMPRIMIR 1
                SENAO
                    IMPRIMIR 2
                FIM
            FIM
            FIM
            ''',
            True
        ),
        (
            "36. SE aninhado nos dois ramos",
            '''
            INICIO
            SE a ENTAO
                SE b ENTAO IMPRIMIR 1 FIM
            SENAO
                SE c ENTAO IMPRIMIR 2 SENAO IMPRIMIR 3 FIM
            FIM
            FIM
            ''',
            True
        ),
        (
            "37. SE sem ENTAO",
            "INICIO SE x > 1 IMPRIMIR x FIM FIM",
            False
        ),
        (
            "38. SE sem FIM",
            "INICIO SE x > 1 ENTAO IMPRIMIR x FIM",
            False
        ),
        (
            "39. SE com bloco vazio",
            "INICIO SE x ENTAO FIM FIM",
            False
        ),
        (
            "40. SENAO com bloco vazio",
            "INICIO SE x ENTAO IMPRIMIR 1 SENAO FIM FIM",
            False
        ),
        (
            "41. SE sem condicao",
            "INICIO SE ENTAO IMPRIMIR 1 FIM FIM",
            False
        ),
        (
            "42. SENAO solto, sem SE",
            "INICIO IMPRIMIR 1 SENAO IMPRIMIR 2 FIM",
            False
        ),

        # REPETICAO
        (
            "43. REPITA com numero",
            '''
            INICIO
            REPITA 3 VEZES
                IMPRIMIR "Executando"
            FIM
            FIM
            ''',
            True
        ),
        (
            "44. REPITA com expressao e reatribuicao",
            '''
            INICIO
            VAR i = 1
            REPITA n * 2 VEZES
                SERVICO registrar_log("Execucao") -> ok
                IMPRIMIR i
                VAR i = i + 1
            FIM
            FIM
            ''',
            True
        ),
        (
            "45. REPITA aninhado com SE dentro",
            '''
            INICIO
            REPITA 2 VEZES
                REPITA 3 VEZES
                    SE i > 1 ENTAO IMPRIMIR i SENAO IMPRIMIR 0 FIM
                FIM
            FIM
            FIM
            ''',
            True
        ),
        (
            "46. REPITA sem VEZES",
            "INICIO REPITA 3 IMPRIMIR 1 FIM FIM",
            False
        ),
        (
            "47. REPITA sem FIM",
            "INICIO REPITA 3 VEZES IMPRIMIR 1 FIM",
            False
        ),
        (
            "48. REPITA sem contagem",
            "INICIO REPITA VEZES IMPRIMIR 1 FIM FIM",
            False
        ),
        (
            "49. REPITA com bloco vazio",
            "INICIO REPITA 3 VEZES FIM FIM",
            False
        )
    ]

    aprovados = 0

    for nome, codigo, deve_aceitar, *arvore_esperada in testes:
        print("\n" + "=" * 60)
        print(nome)
        print("=" * 60)

        try:
            resultado = analisar_codigo(codigo)
            pprint(resultado, width=80)

            passou = deve_aceitar

            # Se o teste traz a AST esperada, compara a expressao
            # do primeiro comando (IMPRIMIR) com ela
            if passou and arvore_esperada:
                obtida = resultado.comandos[0].expressao
                if obtida != arvore_esperada[0]:
                    print(f"ARVORE ESPERADA: {arvore_esperada[0]}")
                    passou = False

        except SyntaxError as erro:
            print(f"ERRO: {erro}")
            passou = not deve_aceitar

        if passou:
            print("STATUS: APROVADO")
            aprovados += 1
        else:
            print("STATUS: REPROVADO")

    print("\n" + "=" * 60)
    print(f"RESULTADO FINAL: {aprovados}/{len(testes)} testes aprovados")
    print("=" * 60)
