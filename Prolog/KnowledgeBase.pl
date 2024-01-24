%% etat de la porte
%% ENV=['METAL','COLOR1','COLOR2','COlOR3',NULL,NULL,NULL]
%% ['silver','blue','green','yellow', NULL, NULL, NULL]

color(red).
color(yellow).
color(blue).
color(black).
color(white).
color(green).

metal(silver).
metal(gold).
metal(bronze).


action([]).
action([X|Qliste]) :- color(X), print(X), action(Qliste).
action([X|Qliste]) :- action(Qliste).


% longueur([], 0).
% longueur([_|Qliste], NombreItems):- 
% 	longueur(Qliste, NombreItemsQueue), NombreItems is NombreItemsQueue + 1.
% longueur([X|Qliste], 0):- longueur(Qliste, 0).

longueur([], 0).
longueur([_|Qliste], NombreItems) :- 
    longueur(Qliste, NombreItemsQueue), NombreItems is NombreItemsQueue + 1.
longueur([X|Qliste], 0) :- longueur(Qliste, 0).

trois_cristaux([_|Env]) :- longueur(Env, NombreItems), NombreItems =:= 3.

%si 3 cristaux(...)

% action(Env, Res):-
%     % retirer second
%     longueur(Env, 0, 3),
%     member(not(red),Env), print('second');
%     % 
%     member(blanc,Env), si blanc dernier , retirer dernier;
%     member(blue,Env), plus un blue, retirer dernier blue;
%     retirer premier.

% %%4 cristaux
% action(Env, four()):-
%     member(red), plus un red, member(silver,Env), retirer dernier red;
%     member(yellow,Env), dernier yellow, member(not(red)), retirer premier;
%     member(blue,Env), un seul blue, retirer premier;
%     member(yellow,Env), plus un yellow, retirer dernier;
%     retirer le 2e cristal.

% %%5 cristaux
% action(Env, five()):-
%     member(black,Env), dernier black, member(gold,Env), retirer le 4e;
%     member(red,Env), un seul red, member(yellow,Env), plus un yellow, retirer premier;
%     member(not(black),Env), retirer le 2e;
%     retirer premier.

% %%6 cristaux
% action(Env, six()):-
%     member(not(yellow),Env), member(bronze), retirer 3e;
%     member(yellow,Env), un seul yellow, member(blanc,Env), plus un blanc, retirer 4e;
%     member(not(red),Env), retirer dernier;
%     retirer 4e.
