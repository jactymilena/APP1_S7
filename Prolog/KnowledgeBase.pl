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

% Longueur de la liste de cristaux bleus
longueur_bleu([], 0).
longueur_bleu([X|Qliste], NombreItems) :- 
    X == blue, longueur_bleu(Qliste, NombreItemsQueue), NombreItems is NombreItemsQueue + 1.
longueur_bleu([X|Qliste], NombreItems) :- X \== blue, longueur_bleu(Qliste, NombreItems).

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

% Etat de la porte
cristaux_etat([_|Env], NombreCristaux) :- longueur(Env, NombreItems), NombreItems =:= NombreCristaux.

% Dernier cristal est blanc
dernier_est_blanc([X, Y, Z, W|Env]) :- W = white.

% si 3 cristaux(...
action(Env, Res) :-
    cristaux_etat(Env, 3),
    (not(member(red, Env)), Res=second, !;
    dernier_est_blanc(Env), Res=third). 

    % member(blue,Env), plus un blue, retirer dernier blue;
    % print('first')).

% 4 cristaux
% action(Env, Res):-
%      member(red), plus un red, member(silver, Env), retirer dernier red;
%      member(yellow, Env), dernier yellow, not(member(red)), Res=first;
%      member(blue, Env), un seul blue, Res=first;
%      member(yellow, Env), plus un yellow, Res=fourth;
%      Res=second.

% 5 cristaux
% action(Env, five()):-
%     member(black, Env), dernier black, member(gold, Env), Res=fourth;
%     member(red, Env), un seul red, member(yellow, Env), plus un yellow, Res=first;
%     not(member(black, Env)), Res=second;
%     Res=first.

% 6 cristaux
% action(Env, six()):-
%     not(member(yellow, Env)), member(bronze), Res=third;
%     member(yellow, Env), un seul yellow, member(blanc, Env), plus un blanc, Res=fourth;
%     not(member(red, Env)), Res=sixth;
%     Res=fourth.