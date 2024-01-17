horsoeuvre(salade).
points(salade, 1).

horsoeuvre(pate).
points(pate, 6).

poisson(sole).
points(sole, 2).

poisson(thon).
points(thon, 4).

viande(porc).
points(porc, 7).

viande(boeuf).
points(boeuf, 3).

dessert(glace).
points(glace, 5).

dessert(fruit).
points(fruit, 1).

menu(H, P, D) :- horsoeuvre(H), poisson(P), dessert(D).
menupoints(H, P, D) :- points(H, PH), points(P, PP), points(D, PD), PH + PP + PD < 10.

repasleger(H, P, D) :- menu(H, P, D), menupoints(H, P, D).
