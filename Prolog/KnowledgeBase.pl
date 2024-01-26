%% etat de la porte
%% ENV=['METAL','COLOR1','COLOR2','COlOR3',NULL,NULL,NULL]
%% ['silver','blue','green','yellow']
%% ['silver','red','green','yellow', 'black']
%% ['silver','red','green','yellow', '', '', '']

color(red).
color(yellow).
color(blue).
color(black).
color(white).
color(green).

metal(silver).
metal(gold).
metal(bronze).


% Longueur de la liste de cristaux
longueur([], 0).
longueur([X|Qliste], NombreItems) :- 
    longueur(Qliste, NombreItemsQueue), color(X), NombreItems is NombreItemsQueue + 1.
longueur([X|Qliste], NombreItems) :- 
    longueur(Qliste, NombreItems), not(color(X)).

% Longueur de la liste de cristaux
longueur_couleur([],_,0).
longueur_couleur([X|Qliste], Couleur, NombreItems) :- 
    X == Couleur, longueur_couleur(Qliste, Couleur, NombreItemsQueue), NombreItems is NombreItemsQueue + 1.
longueur_couleur([X|Qliste], Couleur, NombreItems) :- X \== Couleur, longueur_couleur(Qliste, Couleur, NombreItems).

% Aller chercher le dernier cristal bleu
% dernier_bleu([], 0, Flag).
% dernier_bleu([X|Qliste], NombreItems, Flag) :- 
%     dernier_bleu(Qliste, NombreItemsQueue, Flag), Flag=:=0, NombreItems is NombreItemsQueue + 1, X == blue, Flag is + 1.
% dernier_bleu([X|Qliste], NombreItems, Flag) :- 
%     dernier_bleu(Qliste, NombreItemsQueue, Flag), Flag=:=0, NombreItems is NombreItemsQueue + 1, X \== blue.

dernier_bleu([], 0, Index).
dernier_bleu([X|Qliste], NombreItems, Index) :- 
    dernier_bleu(Qliste, NombreItemsQueue, Index), NombreItems is NombreItemsQueue + 1, X == blue, Index=NombreItems ,!.
% dernier_bleu([X|Qliste], NombreItems, Index) :- 
%     dernier_bleu(Qliste, NombreItemsQueue, Index), NombreItems is NombreItemsQueue + 1, X \== blue.


% dernier_bleu([], 0).
% dernier_bleu([X|Qliste], NombreItems) :- 
%     dernier_bleu(Qliste, NombreItemsQueue), NombreItems is NombreItemsQueue + 1, X \== blue.
% dernier_bleu([X|Qliste], NombreItems) :- 
%     dernier_bleu(Qliste, NombreItemsQueue), NombreItems is NombreItemsQueue + 1, X == blue, !.


% dernier_bleu([X|Qliste], NombreItems, DernierBleu) :- 
%     dernier_bleu(Qliste, NombreItemsQueue, DernierBleu), NombreItems is NombreItemsQueue + 1, X == blue, DernierBleu=NombreItemsQueue.

% dernier_bleu([X|Qliste], DernierBleu) :- 
%     X == blue, longueur_bleu(Qliste, NombreItemsQueue), NombreItemsQueue == 0, DernierBleu = X.
% dernier_bleu([X|Qliste], DernierBleu) :- 
%     dernier_bleu(Qliste, DernierBleu).

% Etat de la porte (3;4;5;6)
cristaux_etat([_|Env], NombreCristaux) :- longueur(Env, NombreItems), NombreItems =:= NombreCristaux.

% Dernier cristal
dernier_est_blanc([X, Y, Z, W|Env]) :- W = white.
dernier_est_jaune([X, Y, Z, W, A|Env]) :- A = yellow.
dernier_est_noir([X, Y, Z, W, A, B|Env]) :- B = black.

% si 3 cristaux(...
action(Env, Res) :-
    cristaux_etat(Env, 3),
    (not(member(red, Env)), Res=second, !;
    dernier_est_blanc(Env), Res=third,!; 
    % member(blue, Env), longueur_couleur(Env, blue, 2), Res=dernier blue,!;   
    Res=first,!).

% 4 cristaux
% action(Env, Res):-
%     cristaux_etat(Env, 4),
%     (member(red), plus un red, member(silver, Env), retirer dernier red;
%     member(yellow, Env), dernier_est_jaune(Env), not(member(red)), Res=first;                                     
%     member(blue, Env), longueur_couleur(Env, blue, 1), Res=first,!;                                               
%     member(yellow, Env), (longueur_couleur(Env, yellow, 2) ; longueur_couleur(Env, yellow, 3) ; longueur_couleur(Env, yellow, 4)), Res=fourth,!;                      
%     Res=second,!).                                                                                                

% 5 cristaux
% action(Env, Res):-
%     cristaux_etat(Env, 5),
%     (member(black, Env), dernier_est_noir(Env), member(gold, Env), Res=fourth;                                    
%     member(red, Env), longueur_couleur(Env, red, 1), member(yellow, Env), (longueur_couleur(Env, yellow, 2) ; longueur_couleur(Env, yellow, 3) ; longueur_couleur(Env, yellow, 4) ; longueur_couleur(Env, yellow, 5)), Res=first;
%     not(member(black, Env)), Res=second;                                                                          
%     Res=first,!).                                                                                                

% 6 cristaux
% action(Env, Res):-
%     cristaux_etat(Env, 5),
%     (not(member(yellow, Env)), member(bronze), Res=third;                                                         
%     member(yellow, Env), longueur_couleur(Env, yellow, 1), member(blanc, Env),(longueur_couleur(Env, white, 2) ; longueur_couleur(Env, white, 3) ; longueur_couleur(Env, white, 4) ; longueur_couleur(Env, white, 5) ; longueur_couleur(Env, white, 6)), Res=fourth;                           
%     not(member(red, Env)), Res=sixth;                                                                             
%     Res=fourth,!).                                                                                                