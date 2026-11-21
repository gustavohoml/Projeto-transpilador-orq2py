from __future__ import annotations
from dataclasses import dataclass
from typing import TypeAlias

# EXPRESSÕES SIMPLES

@dataclass
class Numero:
    valor: int | float


@dataclass
class String:
    valor: str


@dataclass
class Booleano:
    valor: bool


@dataclass
class Identificador:
    nome: str

# EXPRESSÕES COM OPERADORES

@dataclass
class Binaria:
    esquerda: Expressao
    operador: str
    direita: Expressao


@dataclass
class Unaria:
    operador: str
    operando: Expressao


# Tipos de expressões aceitos pela linguagem
Expressao: TypeAlias = (
    Numero | String | Booleano | Identificador | Binaria | Unaria
)

# COMANDOS BÁSICOS

@dataclass
class Atribuicao:
    nome: Identificador
    valor: Expressao


@dataclass
class Imprimir:
    expressao: Expressao


@dataclass
class Servico:
    nome: str
    argumentos: list[Expressao]
    destino: Identificador | None = None


# ESTRUTURAS DE CONTROLE

@dataclass
class Condicional:
    condicao: Expressao
    entao: list[Comando]
    senao: list[Comando] | None = None


@dataclass
class Repeticao:
    quantidade: Expressao
    comandos: list[Comando]


# PARALELISMO 

@dataclass
class Paralelo:
    chamadas: list[Servico]


# TIPOS DE COMANDOS

Comando: TypeAlias = (
    Atribuicao | Imprimir | Servico |
    Condicional | Repeticao | Paralelo
)


# PROGRAMA COMPLETO

@dataclass
class Programa:
    comandos: list[Comando]

# TESTE DA ARVORE SINTATICA

if __name__ == "__main__":
    programa = Programa(
        comandos=[
            Atribuicao(Identificador("x"), Numero(10)),
            Atribuicao(Identificador("y"), Numero(20)),
            Imprimir(
                Binaria(
                    Identificador("x"),
                    "+",
                    Identificador("y")
                )
            )
        ]
    )

    print(programa)