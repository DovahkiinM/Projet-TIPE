from copy import deepcopy
from evaluation import *
from time import *

#On vérifie si la partie est finie
def is_won(board):
    if len(board.iterBlackMoves()) == 0 or len(board.iterWhiteMoves())==0:
        return True
    return False

#Algorithme minimax
def minimax(board,player,depth):

  moves = board.iterMoves(player) #On génère les mouvements possibles
  temps=time() #Enregistre le temps de chaque coup
  best_move = moves[0]
  best_score = float('-inf') #Score maximal
  for move in moves:

    clone =deepcopy(board) #On duplique le damier pour ne pas modifier le cours de la partie
    clone.movePiece(clone.turn,*move) #On effectue un mouvement possible
    if clone.canjump:
        continue
    if clone.turn != player: #C'est à l'adversaire de jouer, on minimise.
        score = min_play(clone,clone.turn,depth+1)
    else:
        score=max_play(clone,clone.turn,depth+1) #On maximise
    if score > best_score: #Mouvement optimal
      best_move = move
      best_score = score
  return best_move,time()-temps

#Fonction min
def min_play(board,player,depth):


  if is_won(board) or depth > board.maxDepth: # Si on dépasse la profondeur maximale, ou que la partie est finie, on retourne l'évaluation du damier
    return Eval1(board)
  moves = board.iterMoves(player) #Génération des mouvements
  best_score = float('inf')
  for move in moves: #On essaie tous les mouvements, et on effectue les déplacements
    clone=deepcopy(board)
    clone.movePiece(player,*move)

    if clone.canjump:
        continue
    if clone.turn!=player: #On maximise car c'est notre tour
        score = max_play(clone,clone.turn,depth+1)
    else:
        score=min_play(clone,clone.turn,depth+1) #C'est le tour de l'adversaire

    best_score=min(score,best_score) #On prend la valeur minimale
  return best_score


def max_play(board,player,depth):

  if is_won(board) or depth > board.maxDepth: #La recherche est terminée
    return Eval1(board)

  moves = board.iterMoves(player) #On génère tous les déplacements possibles

  best_score = float('-inf')

  for move in moves:

    clone=deepcopy(board) #On duplique le damier
    clone.movePiece(player,*move) #On effectue le déplacement

    if clone.turn!=player:
        score = min_play(clone,clone.turn,depth+1) #C'est à l'adversaire de jouer, on minimise.
    else:
        score=max_play(clone,clone.turn,depth+1) #On maximise car c'est notre tour

    best_score=max(best_score,score) #On prend la valeur maximale
  return best_score


