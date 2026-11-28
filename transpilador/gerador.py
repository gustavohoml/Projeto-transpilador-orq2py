from ast_nodes import Programa, Atribuicao, Imprimir

def gerar_codigo(ast: Programa):
    codigo_python = 'from runtime.servicos import *\n\n'
    for comando in ast.comandos:
        if isinstance(comando, Atribuicao):
            nome = comando.nome.nome
            valor = comando.valor.valor

            codigo_python += f'{nome} = {valor}'

    return codigo_python
      