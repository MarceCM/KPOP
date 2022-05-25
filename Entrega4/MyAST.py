import re
from Analisador import Lexer

RAK, CAK, PAK, DAESANG, BONSANG, COMEBACK, KAMSAMIDA, EOF, ANNYEONG, YG, JYP, SM,  HYBE, BIAS, OPPA, EONNI, NOONA, INKIGAYO, MCORE, MBANK, MCOUNTDOWN, MELON, KAKAO, MNET, DISBAND, SULJIBN, SULJIBT, SEMIKOLLON, BANJEOM, DUJEOM, BLACKPINK, BTS, LOONA, WJSN, LPAREN, RPAREN = (
"RAK", "CAK", "PAK", "DAESANG", "BONSANG", "COMEBACK", "KAMSAMIDA", "EOF", "ANNYEONG", "YG", "JYP", "SM", "HYBE", "BIAS","OPPA","EONNI","NOONA", "INKIGAYO", "MCORE", "MBANK", "MCOUNTDOWN", "MELON", "KAKAO", "MNET", "DISBAND", "SULJIBN", "SULJIBT", "SEMIKOLLON", "BANJEOM", "DUJEOM", "BLACKPINK", "BTS", "LOONA", "WJSN", "LPAREN", "RPAREN"
)


class Token(object):
  def __init__(self, type, value):
    self.type = type
    self.value = value

  #representação em string da classe
  def __str__(self):
    return "Token({type}, {value})".format(type = self.type, value = repr(self.value))

  def __repr__(self):
    return self.__str__()

class AST(object):
  pass

class BinOp(AST):
  def __init__(self, left, op, right):
    self.left = left
    self.token = self.op = op
    self.right = right

class Declrc(AST):
  def __init__(self, left, right):
    self.left = left
    self.right = right

class Atrbc(AST):
  def __init__(self, left, eq, right):
    self.left = left
    self.token = self.eq = eq
    self.right = right

class Num(AST):
  def __init__(self, token):
    self.token = token
    self.value = token.value

class Identifier(AST):
  def __init__(self, token):
    self.token = token
    self.value = token.value

class Var(AST):
  def __init__(self, token):
    self.token = token
    self.value = token.value

class Parser(object):
  def __init__(self, lexer):
    self.lexer = lexer
    # set current token to the first token taken from the input
    self.current_token = self.lexer.get_next_token()

  def error(self):
    raise Exception('Invalid syntax')

  def eat(self, token_type):
    if self.current_token.type == token_type:
      self.current_token = self.lexer.get_next_token()
    else:
      self.error()

  def sijag(self):
    "sijag: dec | atr | cont | estrCond | e "

    token = self.current_token
    if token.type in [YG,JYP,SM,HYBE]:
      node = self.dec()
    elif token.type == BIAS:
      node = self.atr()
    elif token.type in [OPPA,EONNI,NOONA]:
      node = self.cont()
    elif token.type in [RAK,CAK,PAK]:
      node = self.estrCond()
    elif token.type == 'e':
      node = self.e()

    return node
  
  def dec(self):
    """dec : tipo iden (BANJEOM iden)* (SULJIBN sijag)*"""
    node_left = self.tipo()
    node_right = self.iden()

    while self.current_token.type == BANJEOM:
      self.eat(BANJEOM)
      self.iden()

    while self.current_token.type == SULJIBN:
      self.eat(SULJIBN)
      self.sijag()

    node = Declrc(left=node_left, right=node_right)

    return node

  def tipo(self):
    """tipo : YG | JYP | SM | HYBE"""
    token = self.current_token
    if token.type == YG:
      self.eat(YG)
      return Var(token)
    elif token.type == JYP:
      self.eat(JYP)
      return Var(token)
    elif token.type == SM:
      self.eat(SM)
      return Var(token)
    elif token.type == HYBE:
      self.eat(HYBE)
      return Var(token)

  def iden(self):
    """iden: BIAS"""
    token = self.current_token
    if token.type == BIAS:
      self.eat(BIAS)
      return Identifier(token)

  def atr(self):
    "iden MELON value (SULJIBN sijag)*"
    node_left = self.iden()
    
    if self.current_token.type == MELON:
      token = self.current_token
      self.eat(MELON)
      node_right = self.value()
    else:
      raise(self.error)

    node = Atrbc(left=node_left, eq=token, right=node_right)

    return node 

  def value(self):
    """value : OPPA | EONNI | NOONA """
    token = self.current_token
    print(token)
    if token.type == OPPA:
      self.eat(OPPA)
      return Num(token)
    elif token.type == EONNI:
      self.eat(EONNI)
      return Num(token)
    elif token.type == NOONA:
      self.eat(NOONA)
      return Num(token)

  def cont(self):
    """cont : value (opr value)* (SULJIBN sijag)*"""
    node_left = self.value()

    while self.current_token.type in [INKIGAYO, MCORE, MBANK, MCOUNTDOWN]:
      token = self.current_token
      if token.type == INKIGAYO:
        self.eat(INKIGAYO)
      elif token.type == MCORE:
        self.eat(MCORE)
      elif token.type == MBANK:
        self.eat(MBANK)
      elif token.type == MCOUNTDOWN:
        self.eat(MCOUNTDOWN)

      node = BinOp(left=node_left, op=token, right=self.value())

      return node

  def opr(self):
    """opr: INKIGAYO | MCORE | MBANK | MCOUNTDOWN"""
    token = self.current_token
    if token.type == INKIGAYO:
      self.eat(INKIGAYO)
      return token
    elif token.type == MCORE:
      self.eat(MCORE)
      return token
    elif token.type == MBANK:
      self.eat(MBANK)
      return token
    elif token.type == MCOUNTDOWN:
      self.eat(MCOUNTDOWN)
      return token

  def estrCond(self):
    """estrCond:  condi (opcio)* DUJEOM SULJIBN SULJIBT bloco"""
    condicional = self.condi()

    if condicional != 'pak':
      self.opcio()
      self.bloco()
    else:
      self.bloco()

  def condi(self):
    """condi : RAK | CAK | PAK"""
    token = self.current_token
    if token.type == RAK:
      self.eat(RAK)
      return token.value
    elif token.type == CAK:
      self.eat(CAK)
      return token.value
    elif token.type == PAK:
      self.eat(PAK)
      return token.value

  def opcio (self):
    """opcio :  iden oprCond (iden | value)"""
    self.iden()
    self.oprcCond()

    if self.current_token.type == BIAS:
      self.iden()
    elif self.current_token.type in [OPPA, EONNI, NOONA]:
      self.value()

    return True

  def oprcCond(self):
    """oprCond: KAKAO | MNET | DISBAND | BLACKPINK | BTS | LOONA | WJSN"""
    token = self.current_token
    if token.type == KAKAO:
      self.eat(KAKAO)
      return token.value
    elif token.type == MNET:
      self.eat(MNET)
      return token.value
    elif token.type == DISBAND:
      self.eat(DISBAND)
      return token.value
    elif token.type == BLACKPINK:
      self.eat(BLACKPINK)
      return token.value
    elif token.type == BTS:
      self.eat(BTS)
      return token.value
    elif token.type == LOONA:
      self.eat(LOONA)
      return token.value
    elif token.type == WJSN:
      self.eat(WJSN)
      return token.value

  def bloco(self):
    self.sijag()

  def parse(self):
    return self.sijag()

class Interpreter(object):
  def __init__(self, parser):
    self.parser = parser

  def interpret(self):
    tree = self.parser.parse()
    return tree

def main():
  while True:
    try:
      #get the input
      text = input('MyCompiler> ')
    except EOFError:
      break
    if not text:
      continue

    text = re.split('([^a-zA-Z0-9])', text)
    text = [i for i in text if i != '']

    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    result = interpreter.interpret()
    print(result)
    print(result.left)
    print(result.right)

if __name__ == '__main__':
  main()