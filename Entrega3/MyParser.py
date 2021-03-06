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


class Interpreter(object):
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
      self.dec()
    elif token.type == BIAS:
      self.atr()
    elif token.type in [OPPA,EONNI,NOONA]:
      self.cont()
    elif token.type in [RAK,CAK,PAK]:
      self.estrCond()
    elif token.type == 'e':
      self.e()

    return True
  
  def dec(self):
    """dec : tipo iden (BANJEOM iden)* (SULJIBN sijag)*"""
    self.tipo()
    self.iden()

    while self.current_token.type == BANJEOM:
      self.eat(BANJEOM)
      self.iden()

    while self.current_token.type == SULJIBN:
      self.eat(SULJIBN)
      self.sijag()

    if self.current_token.type not in [YG, SM, HYBE, JYP, BIAS, BANJEOM, SULJIBN, EOF]:
      return False

    return True

  def tipo(self):
    """tipo : YG | JYP | SM | HYBE"""
    token = self.current_token
    if token.type == YG:
      self.eat(YG)
      return token.value
    elif token.type == JYP:
      self.eat(JYP)
      return token.value
    elif token.type == SM:
      self.eat(SM)
      return token.value
    elif token.type == HYBE:
      self.eat(HYBE)
      return token.value
  
  def iden(self):
    """iden: BIAS"""
    token = self.current_token
    if token.type == BIAS:
      self.eat(BIAS)
      return token.value

  
  def atr(self):
    "iden MELON value (SULJIBN sijag)*"
    self.iden()
    self.value()

    result = self.iden()
    
    while self.current_token == SULJIBN:
      self.eat(SULJIBN)
      result += self.sijag()

    return result 
    
  def value(self):
    """value : OPPA | EONNI | NOONA """
    token = self.current_token
    if token.type == OPPA:
      self.eat(OPPA)
      return token.value
    elif token.type == EONNI:
      self.eat(EONNI)
      return token.value
    elif token.type == NOONA:
      self.eat(NOONA)
      return token.value

  def cont(self):
    """cont : value (opr value)* (SULJIBN sijag)*"""
    return self.lexer.text

  def opr(self):
    """opr: INKIGAYO | MCORE | MBANK | MCOUNTDOWN"""
    token = self.current_token
    if token.type == INKIGAYO:
      self.eat(INKIGAYO)
      return token.value
    elif token.type == MCORE:
      self.eat(MCORE)
      return token.value
    elif token.type == MBANK:
      self.eat(MBANK)
      return token.value
    elif token.type == MCOUNTDOWN:
      self.eat(MCOUNTDOWN)
      return token.value

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


def main():
  while True:
    try:
      #get the input
      text = input('MyParser> ')
    except EOFError:
      break
    if not text:
      continue

    text = re.split('([^a-zA-Z0-9])', text)
    text = [i for i in text if i != '']

    lexer = Lexer(text)
    interpreter = Interpreter(lexer)
    result = interpreter.sijag()
    print(result)


if __name__ == '__main__':
  main()