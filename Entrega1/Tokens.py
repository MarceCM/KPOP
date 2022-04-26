#### Compilador

### Integrantes
# Marcella Costa
# Mateus Queiroz
# Milena Teixeira
# Yasmin Vitorino

### Palavras-chave

##          | TOKEN      | EXPRESSÃO REGULAR 

# if        | RAK        | ^(rak)$
# elif      | CAK        | ^(cak)$
# else      | PAK        | ^(pak)$
# for       | DAESANG    | ^(daesang)$
# while     | BONSANG    | ^(bonsang)$
# functions | COMEBACK   | ^(comeback)$
# return    | KAMSAMIDA  | ^(kamsamida)$
# print     | ANNYEONG   | ^(annyeong)$
# int       | YG         | ^(yg)$
# float     | JYP        | ^(jyp)$
# bool      | SM         | ^(sm)$
# string    | HYBE       | ^(hybe)$
# identifier| BIAS       | ^([a-zA-Z])+(\w)*
# numeric   | OPPA       | ^(-|\+)?\d+$ | ^(-|\+)?\d+(.\d+)?$
# boolean   | EONNI      | ^(Cham | Geojis)$
# string    | NOONA      | ^¨[\s\S]*¨$


### Operadores

##      | TOKEN       | EXPRESSÃO REGULAR 

# +     | INKIGAYO    |       ^\+$
# -     | MCORE       |       ^\-$
# *     | MBANK       |       ^\*$
# /     | MCOUNTDOWN  |       ^\/$
# =     | MELON       |       ^=$
# ==    | KAKAO       |       ^(==)$
# &&    | MNET        |       ^(&&)$
# ||    | DISBAND     |       ^(||)$
# \n    | SULJIBN     |       ^\\n$
# \t    | SULJIBT     |       ^\\t$
# ;     | SEMIKOLLON  |       ^\;$
# ,     | BANJEOM     |       ^\,$
# :     | DUJEOM      |       ^\:$
# >     | BLACKPINK   |       ^\>$
# <     | BTS         |       ^\<$
# >=    | LOONA       |       ^\>=$
# <=    | WJSN        |       ^\<=$
# (     | LPAREN      |       ^\($
# )     | RPAREN      |       ^\)$

### Identificadores

## Boolean 

#^(Cham | Geojis)$

## Inteiro

#^(-|\+)?\d+$

## Float

#^(-|\+)?\d+(.\d+)?$

## String

# ^¨[\s\S]*¨$

## Identificador (Variável)

# ^([a-zA-Z])+(\w)*