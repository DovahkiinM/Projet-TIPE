# Marrakchi Benazzouz Mouad
# Sujet TIPE : Résolution du jeu de dames

from board import *
from alpha_beta import *
from evaluation import *
from minimax import *
from tkinter.messagebox import showinfo,askyesno
from tkinter.simpledialog import *

temps_blanc=[]
temps_noir=[]

# Paramètre de jeu
width = 8
height = 8
firstPlayer = 0
human=False



#

#





def restart(): #Nouvelle partie
    global j1,j2,selected,b,txt1,txt2,human
    if askyesno('Lancer la partie', 'Voulez-vous lancer la partie robot contre robot ?'):
       human=False
       j1="Robot"
       fenetre.after(0, bot)
    else:
        human=True
        j1 = askstring("Nouvelle Partie...", "Joueur 1:")

    b = board(width, height, firstPlayer) #On ré-initialise le damier
    txt1.configure(text=j1 + ' (Blanc) :'+ str(b.whitescore) ) #On écrit les scores des joueurs
    txt2.configure(text='Robot (Noir) :' + str(b.blackscore) )

    b.started=True #Commencement de la partie
    selected=-1 #stock la position cliquée précedemment sur le canevas
    b.damier(can1)#On dessine le damier
    b.drawBoard(chaine,can1)#On place les pions

def interface():
    
    global fenetre, can1, bt1, bt2, chaine, txt1, txt2
    fenetre = Tk() #On initialise le fenêtre

    w=480 #largeur du programme
    h=600 #hauteur du programme
    ws = fenetre.winfo_screenwidth()  # largeur de l'écran
    hs = fenetre.winfo_screenheight()  # hauteur de l'écran
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    fenetre.geometry('%dx%d+%d+%d' % (w, h, x, y)) #on centre le programme dans l'écran

    fenetre.title("Jeu de dames")
    can1 = Canvas(fenetre, width=480, height=480, bg='dark grey') #Enregistrement des cliques
    can1.bind("<Button-1>", select)
    can1.pack(side=TOP)

    chaine = Label(fenetre)
    chaine.configure(text="", fg='red')
    chaine.pack()

    txt1 = Label(fenetre, text='')
    txt2 = Label(fenetre, text='')
    txt1.pack()
    txt2.pack()
    bt1 = Button(fenetre, text='Quitter', command=fenetre.destroy)
    bt1.pack(side=LEFT)
    bt2 = Button(fenetre, text='Nouvelle Partie', command=restart)
    bt2.pack(side=RIGHT)
    bt3 = Button(fenetre, text='Sauvegarder', command=save)
    bt3.pack(side=LEFT)
    b.damier(can1)



def select(event):
    global selected, poss, b, tempb, moves,txt1,txt2
    # On traite les cliques si le joueur est humain
    if b.started and human:
        # On détermine la case cliquée
        ligne = event.y // b.case
        colonne = event.x // b.case
        coord_case = (colonne,ligne)
        
        if selected == -1: #Pas de cliques précedemment
            y = ligne * b.case + b.case // 2
            x = colonne * b.case + b.case // 2

            if coord_case in b.whitelist and b.turn == 0:
                if coord_case in b.whitequeen:
                    can1.create_rectangle(x - 12, y - 12, x + 12, y + 12, fill='red')
                else:

                    can1.create_oval(x - 20, y - 20, x + 20, y + 20, fill='red')
                selected = coord_case
                poss=list(b.iterWhitePiece(coord_case))
                moves=[]
                #On dessine les mouvements possibles
                for move in poss:

                    moves+=[move[1]]

                    x=move[1][0]* b.case + b.case // 2
                    y=move[1][1]* b.case + b.case // 2
                    if coord_case in b.whitequeen:
                        can1.create_rectangle(x - 12, y - 12, x + 12, y + 12, fill='yellow')
                    else:

                        can1.create_oval(x - 20, y - 20, x + 20, y + 20, fill='yellow')

        else:
            # Déplacement ou déselection de la case
            if selected == coord_case:
                selected = -1
                #On redessine le damier
                b.damier(can1)
                b.drawBoard(chaine,can1)

            else:
                #Mouvement possible
                if coord_case in moves:
                    #On effectue le mouvement
                    b.moveWhite(*poss[moves.index(coord_case)])
                    #Règle de la prise obligatoire
                    if b.canjump:
                        showinfo("Erreur","Si vous pouvez capturer un pion, vous devez le faire !")
                    selected = -1 #Déplacement effectué, on n'a plus besoin de mémoriser la case initiale
                    b.damier(can1)
                    b.drawBoard(chaine, can1) #Actualise le damier
                    #Fin du jeu
                    if b.end() == b.WHITE:
                        showinfo("Victoire !", "Le joueur blanc a gagné la partie")
                        b.started=False
                    elif b.end() == b.BLACK:
                        showinfo("Victoire !", "Le joueur noir a gagné la partie")
                        b.started=False
                    #Tant que le tour est au robot, il joue son tour.
                    while b.turn==b.BLACK:
                        #best_move=minimax(b,b.turn,0)
                        best_move = alphabeta(b, b.turn, 0)[0]
                        b.movePiece(b.turn, *best_move)

                        b.damier(can1)
                        b.drawBoard(chaine, can1)


                else:
                    selected = -1
                    # on redessine le damier
                    b.damier(can1)
                    b.drawBoard(chaine, can1)
        #Mise à jour des scores
        txt1.configure(text=j1 + ' (Blanc) :' + str(b.whitescore))
        txt2.configure(text='Robot (Noir) :' + str(b.blackscore))

        if b.end() == b.WHITE:
            showinfo("Victoire !", "Le joueur blanc a gagné la partie")

        elif b.end() == b.BLACK:
            showinfo("Victoire !", "Le joueur noir a gagné la partie")

#Sauvegarde des statistiques:
def save(gagnant="None"):

    with open('E:/TIPE PYTHON/stats-white.txt', 'a') as f:
        somme=0
        for temps in temps_blanc:

            somme+=temps

        moyenne=somme/len(temps_blanc)
        f.write("Profondeur :" + str(b.maxDepth) + "\n")
        f.write("Moyenne : " + str(moyenne)+ "\n")
        f.write("Gagnant :" + gagnant+"\n \n")

    with open('E:/TIPE PYTHON/stats-black.txt', 'a') as f:
        somme=0
        maxi=0
        for temps in temps_noir:
            somme+=temps

        moyenne=somme/len(temps_noir)
        f.write("Profondeur :" + str(b.maxDepth) + "\n")
        f.write("Moyenne : " + str(moyenne)+ "\n")
        f.write("Gagnant :" + gagnant+"\n \n")

#Robot contre robot
def bot():
    global b,selected,j1
    if not human and b.started:
        txt1.configure(text=j1 + ' (Blanc) :' + str(b.whitescore))
        txt2.configure(text='Robot (Noir) :' + str(b.blackscore))
        fenetre.update()
        if b.turn == b.WHITE:
            best_move,temps=alphabeta(b,b.turn,0,Eval1)
            temps_blanc.append(temps)
            b.movePiece(b.turn, *best_move)

        else:
            best_move,temps=alphabeta(b,b.turn,0,Eval2)
            temps_noir.append(temps)
            b.movePiece(b.turn, *best_move)



        b.damier(can1)
        b.drawBoard(chaine, can1)

        if b.end() == b.WHITE:
            b.started = False
            showinfo("Victoire !", "Le joueur blanc a gagné la partie")
            save("Blanc")
        elif b.end() == b.BLACK:
            b.started = False
            showinfo("Victoire !", "Le joueur noir a gagné la partie")
            save("Noir")
        fenetre.after(0, bot)

    #Si l'utilisateur décide de jouer.
    if human:
        b = board(width, height, firstPlayer)
        txt1.configure(text=j1 + ' (Blanc) :' + str(b.whitescore))
        txt2.configure(text='Robot (Noir) :' + str(b.blackscore))

        b.started = True
        selected = -1
        b.damier(can1)
        b.drawBoard(chaine, can1)



#PROGRAMME PRINCIPAL

b = board(width, height, firstPlayer)
selected=-1

interface()
restart()
fenetre.update()
fenetre.after(0,bot) #Il n'y a pas d'événements (cliques du joueur) on doit donc imposer l'appel de la fonction dans la boucle de la GUI
fenetre.mainloop()#Commence la boucle






