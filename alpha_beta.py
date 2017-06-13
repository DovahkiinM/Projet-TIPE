from copy import deepcopy
from time import *
from evaluation import *

#On vérifie si la partie est finie
def is_won(board):
    if len(board.iterBlackMoves()) == 0 or len(board.iterWhiteMoves())==0:
        return True
    return False
#Algorithme alpha-beta

#Beta est la plus grande valeur pour le joueur minimisant
#Alpha est la plus petite valeur pour le joueur maximisant

def alphabeta(board,player,depth,eva=Eval2):
  global fct  
  fct=eva # On utilise la fonction d'évaluation appelée pour pouvoir les comparer 
  moves = board.iterMoves(player)#On génère les mouvements possibles  
  temps=time() #Enregistrer le temps de chaque coup
  best_move = moves[0]
  alpha = float('-inf')
  beta=float('inf')
  for move in moves:

    clone =deepcopy(board)#On duplique le damier pour ne pas modifier la partie
    clone.movePiece(clone.turn,*move)#On effectue un mouvement possible

    if clone.turn != player: #Il n'y a pas de double prise, on minimise.
        score = min_play(clone,clone.turn,depth+1,alpha,beta)
    else:#Double prise, on maximise
        score=max_play(clone,clone.turn,depth+1,alpha,beta)

    if score > alpha: #C'est le mouvement le plus optimal
      best_move = move
      alpha=score

  return best_move,time()-temps


def min_play(board,player,depth,alpha,beta):

  if is_won(board) or depth > board.maxDepth: #La recherche est terminée
    return fct(board)
  moves = board.iterMoves(player) #On génère les mouvements possibles

  for move in moves:
    clone=deepcopy(board) #On duplique le damier
    clone.movePiece(player,*move) #On effectue notre mouvement


    if clone.turn!=player:
        score = max_play(clone,clone.turn,depth+1,alpha,beta) #C'est notre tour, on maximise
    else:
        score=min_play(clone,clone.turn,depth+1,alpha,beta) #C'est le tour de l'adversaire, on minimise

    beta=min(beta,score) #Beta est la valeur minimisante

    if alpha >= beta: #Si la valeur Beta est inférieure à Alpha, alors comme Alpha est la plus petite valeur possible
      return alpha    #pour le joueur, il est inutile de continuer la recherche du tableau

  return beta


def max_play(board,player,depth,alpha,beta):

  if is_won(board) or depth > board.maxDepth: #La partie est terminée
    return fct(board)

  moves = board.iterMoves(player) #On génère les mouvements possibles

  for move in moves: #On parcourt les déplacements possibles
    clone=deepcopy(board) #Duplication du damier
    clone.movePiece(player,*move) #On effectue le mouvement

    if clone.turn!=player:
        score = min_play(clone,clone.turn,depth+1,alpha,beta) #C'est le tour adverse, on minimise
    else:
        score=max_play(clone,clone.turn,depth+1,alpha,beta) #On maximise

    alpha=max(alpha,score) #Alpha est la valeur maximisante

    if alpha >= beta: #On est dans l'étape maximisante, si Beta est inférieure à Alpha, comme Beta est la plus grande valeur
      return beta     #pour le joueur minimisant, on retourne beta

  return alpha

