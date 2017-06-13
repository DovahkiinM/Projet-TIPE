#Fonctions d'évaluation

#Nombre de pions
def Eval1(board):
    score=len(board.whitelist)+len(board.whitequeen)-len(board.blacklist)-len(board.blackqueen)
    if board.turn==board.WHITE:
        return score
    else:
        return -score
#Position des pions
def Eval2(board):
    score1=0
    score2=0

    for pion in board.whitelist:
        if pion in board.whitequeen:
            score1+=10
        else:
            if pion[1]>3:
                score1 +=3
            else:
                score1 +=5

    for pion in board.blacklist:
        if pion in board.blackqueen:
            score2 +=10
        else:
            if pion[1]>3:
                score2 +=5
            else:
                score2 +=3
    if board.turn==board.WHITE:
        return score1-score2
    else:
        return score2-score1
