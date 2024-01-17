% print un sur deux 
un_sur_deux([]).
un_sur_deux([X, Y|Qliste]) :- un_sur_deux(Qliste), print(Y). 
un_sur_deux([X|Qliste]) :- un_sur_deux(Qliste).
