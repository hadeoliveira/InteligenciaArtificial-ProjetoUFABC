#!/usr/bin/env python
# marioAstar.py
# Author: Fabrício Olivetti de França
#
# A* algorithm for Super Mario World
# using RLE

import sys
import os
import pickle
import retro
import copy
import time
from rominfo import *
from utils import *

sys.setrecursionlimit(10000)

# quais movimentos estarão disponíveis
moves = {'direita':128, 'corre':130, 'pula':131, 'spin':386, 'esquerda':64}
# raio de visão (quadriculado raio x raio em torno do Mario)
raio = 6

# Classe da árvore de jogos para o Super Mario World
class Tree:
    def __init__(self, estado, filhos=None, pai=None, g=0, h=0, terminal=False, obj=False):
        self.estado   = estado
        self.filhos   = filhos # lista de filhos desse nó
        
        self.g = g
        self.h = h
        
        self.eh_terminal = terminal
        self.eh_obj      = obj
        
        self.pai = pai # apontador para o pai, útil para fazer o backtracking

    def __str__(self):
        return self.estado
  
def melhor_filho(tree):
    '''
    Encontra o melhor filho do nós representado por tree.
    
    Entrada: tree, o nó atual da árvore
    Saída:   a tupla (t, f) com t sendo o melhor filho de tree e f a heurística g+h
             retorna None caso o nó seja terminal
    ''' 
    print(f'entrei aqui com {tree.g}')

    # Implemente as tarefas abaixo e remove a instrução pass.
    
    # 1) Se o nó é terminal, retorna None
    if tree.eh_terminal: 
        return None
    
    # 2) Se o nó não tem filhos, retorna ele mesmo e seu f
    if tree.filhos == None:
        return tree, (tree.h)
    
    # 3) Para cada filho de tree, procura por qual tem melhor heuristica
    melhorfilho = sorted([(i,j) for i,j in tree.filhos.items()],key=lambda i: i[1].h)[0]
    
    

    # 4) Se todos os filhos resultarem em terminal, marca tree como terminal e retorna None
    if all(filho.eh_terminal for filho in tree.filhos.values()):
        tree.eh_terminal = True
        return None
    # 5) Caso contrário retorna aquele com o menor f
    else:
        # Implementar lógica para ordenar lista com menor f dos filhos
        return melhorfilho[1],melhorfilho[1].h # retorna uma tupla (no, f)
    
# Nossa heurística é a quantidade
# de passos mínimos estimados para
# chegar ao final da fase
def heuristica(estado, x):
#    return (4800 - x)/8
    estNum = np.reshape(list(map(int, estado.split(','))), (2*raio+1,2*raio+1))
    dist = np.abs(estNum[:raio+1,raio+2:raio+7]).sum()
    return ((4800 - x)/8) + 0.3*dist
 
# Verifica se chegamos ao final    
def checaObj(estado, x):
    if(x > 4800):
        print('CHEGAMOS NO OBJETIVO FINAL')
    return x>4800

# Verifica se um nó é uma folha 
def folha(tree):
    """ Verifica se tree é um nó folha. """
    # Um nó folha é aquele que não tem filhos.
    pass

# Joga uma partida usando uma
# sequência de ações
def emula(acoes, env, mostrar):
    env.reset()

    while len(acoes)>0 and (not env.data.is_done()):
        a = acoes.pop(0)
        estado, xn, y = getState(getRam(env), raio)
        performAction(a, env)
        if mostrar:
            env.render()

    estado, x, y = getState(getRam(env), raio)
    
    return estado, x, env.data.is_done()
def atingiuObj(nos):
    
    return False
def expande(nos,acao,env,mostrar):
    print(f'estou em expande com o no: {nos.g} e acao = {acao}')
    acoes = []

    raiz = nos
    while raiz.pai != None:
        print(nos.g)
        print(nos.pai.g)
        input('wait')
    # 2) Atribua raiz a uma variável neto
        neto = raiz
    # 3) faça raiz = seu próprio 
        raiz = raiz.pai
    # 4) verifique qual a ação de raiz leva ao nó neto
        for acao, filho in nos.filhos.items():
            if filho == neto:
    # 5) faça um append dessa ação na lista acoes
                acoes.append(acao)
        
        # inverte a lista de ações e imprime para debug
    acoes.reverse()
    print('ACOES:  (  ', len(acoes), ' ): ',  acoes)
    estado, x, over = emula(acoes, env, mostrar)
    maxX            = max(x, 0)
    obj = False
    obj             = obj or checaObj(estado, x)
    nos.filhos = {}
    nos.filhos[acao]              = Tree(estado, g=nos.g + 1, h=heuristica(estado,x),
                            pai=nos, terminal=over, obj=obj)
    return nos.filhos[acao]
# Expande a árvore utilizando a heurística
def argmin(nos):
    
    print(f'min de nos = {nos}')
    input('wait')
    return 

def buscaGulosa(nos,env,mostrar):
    if len(nos) == 1:
        no = nos[0]
    else:
        no = argmin(nos)
    sl = {}
    for a in moves.keys():
        sl[a] = expande(no,a,env,mostrar) 
    if any(atingiuObj(s) for s in sl):
        return filter(atingiuObj,sl)[0]
    print(no.g)
    print(no.filhos)
    if len(nos) == 0:
        return None
    return buscaGulosa(sl,env,mostrar)

# Gera a árvore utilizando A*
def startfunc():
    
    # Se devemos mostrar a tela do jogo (+ lento) ou não (+ rápido)
    mostrar = True
 
    # Gera a árvore com o estado inicial do jogo 
    env = retro.make(game='SuperMarioWorld-Snes', state='YoshiIsland1', players=1)    
    env.reset()
    estado, x, y = getState(getRam(env), raio)  
    tree         = Tree(estado, g=0, h=heuristica(estado,x))

    # Se já existe alguma árvore, carrega
    if os.path.exists('AstarTree.pkl'):
        tree = pickle.load(open('AstarTree.pkl', 'rb'))
    # Repete enquanto não atingir objetivo    
    tree = buscaGulosa([tree],env,mostrar)
        
    # obj, acoes = atingiuObj(tree)
    # mostrar    = True
    # emula(acoes, mostrar)

    return tree
  

def main():  
  tree = startfunc()
    
if __name__ == "__main__":
  main()
