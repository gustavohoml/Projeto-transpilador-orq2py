
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
    Booleano
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
        )
    ]

    aprovados = 0

    for nome, codigo, deve_aceitar in testes:
        print("\n" + "=" * 60)
        print(nome)
        print("=" * 60)

        try:
            resultado = analisar_codigo(codigo)
            pprint(resultado, width=80)

            passou = deve_aceitar

        except SyntaxError as erro:
            print(f"ERRO: {erro}")
            # passou = not deve_aceitar

        if passou:
            print("STATUS: APROVADO")
            aprovados += 1
        else:
            print("STATUS: REPROVADO")

    print("\n" + "=" * 60)
    print(f"RESULTADO FINAL: {aprovados}/{len(testes)} testes aprovados")
    print("=" * 60)
