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
longueur([_|Qliste], NombreItems) :- 
    longueur(Qliste, NombreItemsQueue), NombreItems is NombreItemsQueue + 1.

% Longueur de la liste de cristaux bleus
longueur_bleu([], 0).
longueur_bleu([X|Qliste], NombreItems) :- 
    X == blue, longueur_bleu(Qliste, NombreItemsQueue), NombreItems is NombreItemsQueue + 1.
longueur_bleu([X|Qliste], NombreItems) :- X \== blue, longueur_bleu(Qliste, NombreItems).

% Etat de la porte
cristaux_etat([_|Env], NombreCristaux) :- longueur(Env, NombreItems), NombreItems =:= NombreCristaux.

% Dernier cristal est blanc
dernier_est_blanc([X, Y, Z, W|Env]) :- W = white.

% action(Env, cristal(Res)) :-
    % cristaux_etat(Env, 3),
    % (member(red, Env), cristal(second)).
    % member(blanc,Env), si blanc dernier , print('third');
    % member(blue,Env), plus un blue, retirer dernier blue;
    % print('first')).


% si 3 cristaux(...
action(Env) :-
    cristaux_etat(Env, 3),
    (not(member(red, Env)), print('second');
    dernier_est_blanc(Env), print('third')).

    % member(blue,Env), plus un blue, retirer dernier blue;
    % print('first')).

% 4 cristaux
% action(Env, four()):-
%      member(red), plus un red, member(silver,Env), retirer dernier red;
%      member(yellow,Env), dernier yellow, member(not(red)), print('first');
%      member(blue,Env), un seul blue, print('first');
%      member(yellow,Env), plus un yellow, print('fourth');
%      print('second').

% 5 cristaux
% action(Env, five()):-
%     member(black,Env), dernier black, member(gold,Env), print('fourth');
%     member(red,Env), un seul red, member(yellow,Env), plus un yellow, print('first');
%     member(not(black),Env), print('second');
%     print('first').

% 6 cristaux
% action(Env, six()):-
%     member(not(yellow),Env), member(bronze), print('third');
%     member(yellow,Env), un seul yellow, member(blanc,Env), plus un blanc, print('fourth');
%     member(not(red),Env), print('sixth');
%     print('fourth').
