import ply.lex as lex

def t_comentario(t):
    r'\#.*'
    pass

def t_nova_linha(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reservadas.get(t.value, 'ID')
    return t

def t_error(t):
    raise SyntaxError(
        f"Caractere ilegal '{t.value[0]}' na linha {t.lineno}"
    )

def t_NUM(t):
    r'[0-9]+(\.[0-9]+)?'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

def t_STR(t):
    r'"[^"\n]*"'
    return t

reservadas = {
    'INICIO': 'INICIO',
    'FIM': 'FIM',
    'VAR': 'VAR',
    'SERVICO': 'SERVICO',
    'IMPRIMIR': 'IMPRIMIR',
    'PARALELO': 'PARALELO', 
    'E': 'E', 
    'OU': 'OU',
    'SE': 'SE',
    'SENAO': 'SENAO',
    'ENTAO': 'ENTAO',
    'REPITA': 'REPITA',
    'VEZES': 'VEZES',
    'VERDADEIRO': 'VERDADEIRO',
    'FALSO': 'FALSO',
    'NAO': 'NAO'
}

tokens = [
    'ID',
    'NUM',
    'STR',
    'MAIS',
    'MENOS',
    'ASTERISCO',
    'BARRA',
    'ATRIBUICAO',
    'IGUAL',
    'DIFERENTE',
    'MENOR',
    'MAIOR', 
    'MENOR_IGUAL',
    'MAIOR_IGUAL',
    'ABRE_PARENTESES', 
    'FECHA_PARENTESES',
    'VIRGULA', 
    'SETA' 
] + list(reservadas.values())

t_MAIS = r'\+'
t_MENOS = r'-'
t_ASTERISCO = r'\*'
t_BARRA = r'/'
t_ABRE_PARENTESES = r'\('
t_FECHA_PARENTESES = r'\)'
t_ATRIBUICAO = r'='
t_IGUAL = r'=='
t_DIFERENTE = r'!='
t_MENOR = r'<' 
t_MAIOR = r'>'
t_MENOR_IGUAL = r'<='
t_MAIOR_IGUAL = r'>='
t_VIRGULA = r','
t_SETA = r'->'
t_ignore = ' \t'

lexer = lex.lex()

# TESTES DO LEXER
if __name__ == "__main__":

    testes = {
        "1. Palavras reservadas": '''
            INICIO FIM VAR SERVICO IMPRIMIR
            SE SENAO ENTAO REPITA VEZES
            VERDADEIRO FALSO
            PARALELO E OU NAO
        ''',

        "2. Identificadores": '''
            x preco valor123 _resultado buscar_preco
            inicio var servico
        ''',

        "3. Números": '''
            0 10 123 2.5 0.75 100.0
        ''',

        "4. Strings": '''
            "" "Ola mundo" "Preco: 25" "123"
        ''',

        "5. Operadores aritméticos": '''
            + - * /
        ''',

        "6. Operadores de comparação": '''
            = == != < > <= >=
        ''',

        "7. Símbolos": '''
            ( ) , ->
        ''',

        "8. Comentários": '''
            INICIO
            # Este comentario deve ser ignorado
            VAR x = 10 # Comentario na mesma linha
            IMPRIMIR x
            FIM
        ''',

        "9. Programa completo": '''
            INICIO
            VAR x = 10
            VAR y = 2.5
            SERVICO buscar_preco(x) -> preco

            SE preco >= y ENTAO
                IMPRIMIR "Preco maior"
            SENAO
                IMPRIMIR "Preco menor"
            FIM

            REPITA 3 VEZES
                IMPRIMIR x + y * 2
            FIM
            FIM
        ''',

        "10. Caracteres ilegais": '''
            INICIO
            VAR x = 10 @ 5
            FIM
        '''
    }

    for nome, codigo in testes.items():
        print(f"\n{'=' * 50}")
        print(nome)
        print('=' * 50)

        lexer.lineno = 1
        lexer.input(codigo)

        try:
            for token in lexer:
                print(
                    f"Tipo: {token.type:<20} "
                    f"Valor: {str(token.value):<20} "
                    f"Linha: {token.lineno}"
                )
        except SyntaxError as erro:
            print(f"ERRO LEXICO: {erro}")