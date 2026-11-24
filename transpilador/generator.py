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
)

CABECALHO = "from runtime.servicos import *"

def gerar_expr(expr) -> str:
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

def gerar_comando(comando) -> str:
    if isinstance(comando, Atribuicao):
        return f"{comando.nome.nome} = {gerar_expr(comando.valor)}"

    if isinstance(comando, Imprimir):
        return f"print({gerar_expr(comando.expressao)})"

    if isinstance(comando, Servico):
        return gerar_chamada(comando)

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
    VAR x = 2 + 3 * 4
    VAR nome = "Ana"
    VAR ativo = VERDADEIRO
    VAR y = -x / 2
    IMPRIMIR x >= 10
    IMPRIMIR nome
    SERVICO registrar_log("Inicio")
    SERVICO buscar_usuario(1) -> usuario
    SERVICO buscar_preco(10) -> preco
    SERVICO calcular_total(preco, x - 10) -> total
    SERVICO aplicar_desconto(total, (5 + 5) * 1) -> final
    IMPRIMIR usuario
    IMPRIMIR final
    FIM
    '''

    python_gerado = gerar_programa(analisar_codigo(codigo))
    print(python_gerado)

    print("--- executando ---")
    exec(python_gerado)   # roda o código gerado aqui mesmo
