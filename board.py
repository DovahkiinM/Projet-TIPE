#Classe du damier
from copy import deepcopy

class board(object):
    BLACK = 1
    WHITE = 0
    NOTDONE = -1
    started = False
    case = 60

    def __init__(self, height, width, firstPlayer):
        #On construit le damier 8x8
        self.width=8
        self.height=8
        # On crée une liste contenant tous les pions noirs, et une liste vide pour stocker éventuellement les dames
        self.blacklist = [(0, 1), (1, 0), (2, 1), (3, 0), (4, 1), (5, 0), (6, 1), (7, 0), (1, 2), (3, 2), (5, 2),(7, 2)]
        self.blackqueen = []
        #De même pour les pions blancs
        self.whitelist = [(0, 7), (1, 6), (2, 7), (3, 6), (4, 7), (5, 6), (6, 7), (7, 6), (0, 5), (2, 5), (4, 5),(6, 5)]
        self.whitequeen = []

        self.canjump=False
        #On enregistre le score ( pions sautés )
        self.whitescore=0
        self.blackscore=0
        
        # L'état du damier : le joueur qui peut jouer ainsi que la profondeur maximale des algorithmes.
        self.turn = firstPlayer
        self.maxDepth = 6

    # On vérifie si la partie est finie, et on retourne le gagnant.
    def end(self):

        if len(self.iterBlackMoves()) == 0:
            return board.WHITE
        elif len(self.iterWhiteMoves()) == 0:
            return board.BLACK

    #On génère les mouvements permis des deux joueurs
    def iterMoves(self,player):
        if player==self.BLACK:
            moves=self.iterBlackMoves()
        else:
           moves=self.iterWhiteMoves()
        #Règle de la prise obligatoire
        canjump=False
        for move in moves:
            if len(move)==3:
                canjump=True
        #On enlève les mouvements non permis s'il y'a prise
        if canjump:
            temp=deepcopy(moves)
            for move in temp:
                if len(move) != 3:
                    moves.pop(moves.index(move))

        return moves



    # On génère les mouvements possibles du joueur blanc
    def iterWhiteMoves(self):

        moves = []
        for piece in self.whitelist:
            for move in self.iterWhitePiece(piece):
                moves += [move]
        return moves

    def iterBlackMoves(self):
        moves = []
        for piece in self.blacklist:
            for move in self.iterBlackPiece(piece):
                moves += [move]
        return moves

    #On génère les mouvements possibles d'un pion blanc
    def iterWhitePiece(self, piece):

        if piece in self.whitequeen:

            return self.iterBoth(piece, ((-1, -1), (1, -1), (-1, 1), (1, 1)))
        else:

            return self.iterBoth(piece, ((-1, -1), (1, -1)))

    # On génère les mouvements possibles d'un pion blanc
    def iterBlackPiece(self, piece):

        if piece in self.blackqueen:

            return self.iterBoth(piece, ((-1, -1), (1, -1), (-1, 1), (1, 1)))
        else:
            return self.iterBoth(piece, ((-1, 1), (1, 1)))

    def iterBoth(self, piece, moves):

        action = []
        for move in moves:
            # Déplacement normal

            targetx = piece[0] + move[0]
            targety = piece[1] + move[1]
            # Si la cible est en dehors du damier, on ne compte pas le déplacement
            if targetx < 0 or targetx >= self.width or targety < 0 or targety >= self.height:
                continue
            target = (targetx, targety)
            # On vérifie si la case ciblée est vide
            black = target in self.blacklist
            white = target in self.whitelist
            if not black and not white:
                action += [(piece, target)]

            else:
                #On vérifie si on peut effectuer une prise
                if self.turn == self.BLACK and black:
                    continue
                elif self.turn == self.WHITE and white:
                    continue

                jumpx = target[0] + move[0]
                jumpy = target[1] + move[1]
                # Si le saut est hors damier, on l'ignore
                if jumpx < 0 or jumpx >= self.width or jumpy < 0 or jumpy >= self.height:
                    continue
                jump = (jumpx, jumpy)
                # On vérifie que la case de saut est vide
                black2 = jump in self.blacklist
                white2 = jump in self.whitelist
                if not black2 and not white2:
                    action += [(piece, jump, target)]
        return action

    # Mouvement des pièces noires
    def moveBlack(self, moveFrom, moveTo,  jumped=None):

        self.canjump=False#Vérifie qu'il y'a prise

        if self.turn == self.BLACK:
            if moveTo[0] < 0 or moveTo[0] >= self.width or moveTo[1] < 0 or moveTo[1] >= self.height:
                raise Exception("Le déplacement est hors damier")

            black = moveTo in self.blacklist
            white = moveTo in self.whitelist
            if not (black or white): #On vérifie que la case est vide
                if jumped != None: #Si il y'a un saut
                    self.whitelist.pop(self.whitelist.index(jumped))#On enlève le pion pris
                    self.blackscore+=1
                    if jumped in self.whitequeen:#De même si c'est une dame
                        self.whitequeen.pop(self.whitequeen.index(jumped))

                    self.blacklist[self.blacklist.index(moveFrom)] = moveTo #On déplace le pion

                    if moveFrom in self.blackqueen:#Si c'est une dame
                        self.blackqueen[self.blackqueen.index(moveFrom)] = moveTo

                    #Double prise
                    if self.can_jump(moveTo):
                        self.turn=self.BLACK #Le tour est toujours le notre, on a double prise
                        self.canjump=True
                    else:
                        self.turn=self.WHITE #On cède le tour s'il n'y a pas de double prise

                    if moveTo[1] == 7: #Il y'a eu promotion, on passe le tour
                        self.blackqueen.append(moveTo)
                        self.turn = self.WHITE



                else:
                    for piece in self.blacklist:
                        if self.can_jump(piece):
                            self.canjump=True
                    if not self.canjump: #Prise obligatoire s'il y'a possibilité
                        self.turn = self.WHITE
                        self.blacklist[self.blacklist.index(moveFrom)] = moveTo
                        if moveFrom in self.blackqueen:
                            self.blackqueen[self.blackqueen.index(moveFrom)] = moveTo
                        if moveTo[1] == 7:
                            self.blackqueen.append(moveTo)



        else:
            raise Exception
    #Mouvement d'une pièce blanche, identique à une pièce noire.
    def moveWhite(self, moveFrom, moveTo,  jumped=None):
       
        self.canjump=False
        if moveTo[0] < 0 or moveTo[0] >= self.width or moveTo[1] < 0 or moveTo[1] >= self.height:
            raise Exception("Le déplacement est hors damier")
        black = moveTo in self.blacklist
        white = moveTo in self.whitelist

        if not (black or white):

            if jumped != None:
                self.whitescore+=1
                
                self.blacklist.pop(self.blacklist.index(jumped))
                
                if jumped in self.blackqueen:
                    self.blackqueen.pop(self.blackqueen.index(jumped))

                self.whitelist[self.whitelist.index(moveFrom)] = moveTo
                if moveFrom in self.whitequeen:
                    self.whitequeen[self.whitequeen.index(moveFrom)] = moveTo

               
                if self.can_jump(moveTo):
                    self.turn=self.WHITE
                else:
                    self.turn=self.BLACK

                if moveTo[1] == 0:
                    self.whitequeen.append(moveTo)
                    self.turn = self.BLACK

            else:
               
                for piece in self.whitelist:
                    if self.can_jump(piece):
                        self.canjump = True
                
                if not self.canjump:
                    self.turn=self.BLACK 
                    self.whitelist[self.whitelist.index(moveFrom)] = moveTo #On modifie sa position
                    if moveFrom in self.whitequeen:
                        self.whitequeen[self.whitequeen.index(moveFrom)] = moveTo #On suit le déplacment de la dame
                    if moveTo[1] == 0:
                        self.whitequeen.append(moveTo) #Promotion du pion
                   

        else:
            raise Exception
        
    #On déplace une pièce quelconque
    def movePiece(self,player,moveFrom,moveTo,jumped=None):
        if player==self.BLACK:
            self.moveBlack(moveFrom,moveTo,jumped)
        else:
            self.moveWhite(moveFrom,moveTo,jumped)

    def can_jump(self, piece):
        if piece in self.blacklist:
            for move in self.iterBlackPiece(piece):
                if len(move) == 3:
                    return True
        else:
            for move in self.iterWhitePiece(piece):
                if len(move) == 3:
                    return True
        return False

    #On génère le damier : Couleur verte pour une case à pion, et marron pour une case vide.
    def damier(self, can1):
        for i in range(8):
            for j in range(8):
                if (i % 2) == 0:
                    if (j % 2) == 1:
                        can1.create_rectangle(j * self.case, i * self.case, (j * self.case) + self.case,
                                              (i * self.case) + self.case,
                                              fill='dark green')
                    else:
                        can1.create_rectangle(j * self.case, i * self.case, (j * self.case) + self.case,
                                              (i * self.case) + self.case, fill='tan')
                else:
                    if (j % 2) == 1:
                        can1.create_rectangle(j * self.case, i * self.case, (j * self.case) + self.case,
                                              (i * self.case) + self.case, fill='tan')
                    else:
                        can1.create_rectangle(j * self.case, i * self.case, (j * self.case) + self.case,
                                              (i * self.case) + self.case,
                                              fill='dark green')

    def drawBoard(self, chaine, can1):
        "On place les pions"
        if self.started:

            if self.turn == self.BLACK:
                chaine.configure(text="Les NOIRS jouent...", fg='black')
            else:
                chaine.configure(text="Les BLANCS jouent...", fg='black')
        #On commence par les pions blancs
        i = 0
        while i < len(self.whitelist):
            if self.whitelist[i] != -1:
                y = (self.whitelist[i][1] * self.case) + self.case // 2
                x = (self.whitelist[i][0] * self.case) + self.case // 2
                # Le centre du cercle est calculé, on le dessine.
                if self.whitelist[i] in self.whitequeen:
                    can1.create_rectangle(x - 12, y - 12, x + 12, y + 12, fill='white')
                else:
                    can1.create_oval(x - 20, y - 20, x + 20, y + 20, fill='white')
            i += 1
        #De même pour les pions noirs
        i = 0
        while i < len(self.blacklist):
            if self.blacklist[i] != ():
                y = (self.blacklist[i][1] * self.case) + self.case // 2
                x = (self.blacklist[i][0] * self.case) + self.case // 2

                if self.blacklist[i] in self.blackqueen:
                    can1.create_rectangle(x - 12, y - 12, x + 12, y + 12, fill='black')
                else:
                    can1.create_oval(x - 20, y - 20, x + 20, y + 20, fill='black')
            i += 1
