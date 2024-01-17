homme(louis).
homme(charles).
homme(georges).
homme(luc).
homme(lucien).

femme(isabelle).
femme(louise).
femme(catherine).
femme(claire).

pere(georges, louis).
pere(georges, isabelle).
pere(georges, charles).
pere(luc, catherine).
pere(luc, louise).
pere(lucien, georges).
pere(lucien, luc).

mere(claire, isabelle).
mere(claire, louis).
mere(claire, charles).

enfant(E, P) :- pere(P, E); mere(P, E).

parent(P, E) :- pere(P, E); mere(P, E).

grandparent(X, Z) :- parent(X, Y), parent(Y,Z).

fils(E, P):- homme(E), parent(P, E).

fraternel(E1, E2) :- parent(P, E1), parent(P, E2), E1\=E2.

soeur(E1, E2) :- fraternel(E1, E2), femme(E1).
frere(E1, E2) :- fraternel(E1, E2), homme(E1).

oncle(O, E) :- frere(O, P), parent(P, E).
tante(T, E) :- soeur(T, P), parent(P, E).












