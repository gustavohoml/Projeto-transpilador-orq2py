from .ast_nodes import (
    Programa,
    Atribuicao,
    Imprimir,
    Servico,
    Numero,
    String,
    Booleano,
    Identificador,
    Binaria,
    Unaria,
    Condicional,
)

CABECALHO = "from runtime.servicos import *"

def gerar_expr(expr, nivel: int = 0) -> str:
    indentacao = "    " * nivel

    if isinstance(expr, Numero):
        return repr(expr.valor)

    if isinstance(expr, String):
        return repr(expr.valor)

    if isinstance(expr, Booleano):
        return "True" if expr.valor else "False"

    if isinstance(expr, Identificador):
        return expr.nome

    if isinstance(expr, Unaria):
        return f"(-{gerar_expr(expr.operando)})"

    if isinstance(expr, Binaria):
        esquerda = gerar_expr(expr.esquerda)
        direita = gerar_expr(expr.direita)
        return f"({esquerda} {expr.operador} {direita})"

    raise TypeError(f"Expressão desconhecida: {expr!r}")

def gerar_chamada(servico: Servico) -> str:
    argumentos = ", ".join(gerar_expr(arg) for arg in servico.argumentos)
    chamada = f"{servico.nome}({argumentos})"

    if servico.destino is not None:
        return f"{servico.destino.nome} = {chamada}"
    return chamada

def gerar_comando(comando, nivel: int = 0) -> str:
    indentacao = "    " * nivel

    if isinstance(comando, Atribuicao):
        return f"{indentacao}{comando.nome.nome} = {gerar_expr(comando.valor)}"

    if isinstance(comando, Imprimir):
        return f"{indentacao}print({gerar_expr(comando.expressao)})"

    if isinstance(comando, Servico):
        return indentacao + gerar_chamada(comando)

    if isinstance(comando, Condicional):
        condicao = gerar_expr(comando.condicao)
        linhas = [f"{indentacao}if {condicao}:"]

        for interno in comando.entao:
            linhas.append(gerar_comando(interno, nivel + 1))

        if comando.senao is not None:
            linhas.append(f"{indentacao}else:")

            for interno in comando.senao:
                linhas.append(gerar_comando(interno, nivel + 1))

        return "\n".join(linhas)

    raise TypeError(f"Comando desconhecido: {comando!r}")

def gerar_programa(programa: Programa) -> str:
    linhas = [CABECALHO, ""]

    for comando in programa.comandos:
        linhas.append(gerar_comando(comando))

    return "\n".join(linhas) + "\n"




if __name__ == "__main__":
    from .parser import analisar_codigo

    codigo = '''
    INICIO
    VAR x = 10

    SE x > 5 ENTAO
        IMPRIMIR "Maior que 5"

        SE x == 10 ENTAO
            IMPRIMIR "Igual a 10"
        SENAO
            IMPRIMIR "Diferente de 10"
        FIM

    SENAO
        IMPRIMIR "Menor ou igual a 5"
    FIM

    SE x > 0 ENTAO
        IMPRIMIR "Positivo"
    FIM

    IMPRIMIR "Finalizado"
    FIM
    '''

    python_gerado = gerar_programa(analisar_codigo(codigo))
    print(python_gerado)

    print("--- executando ---")
    exec(python_gerado)   # roda o código gerado aqui mesmo
