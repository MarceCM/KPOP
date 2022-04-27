RAK, CAK, PAK, DAESANG, BONSANG, COMEBACK, KAMSAMIDA, EOF, ANNYEONG, YG, JYP, SM, HYBE,BIAS,OPPA,EONNI,NOONA,INKIGAYO,MCORE,MBANK,MCOUNTDOWN,MELON,KAKAO,MNET,DISBAND, SULJIBN, SULJIBT, SEMIKOLLON, BANJEOM, DUJEOM, BLACKPINK, BTS, LOONA, WJSN, LPAREN, RPAREN = (
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


class Lexer(object):
  def __init__(self, text):
    #string do usuario
    self.text = text
    #indice que marca a posicao do texto (o caractere corrente sendo processado no texto)
    self.pos = 0
    #guarda o caractere que está sendo analisado de fato
    self.current_char = self.text[self.pos]

  #para retorno de erro
  def error(self):
    raise Exception("Invalid character!")

  #funcao que avanca caractere a caractere no texto
  #vai avancar o indice "pos" e modificar o conteudo da variavle "current_char"
  def advance(self):
    self.pos += 1
    #verifica se a leitura chegou ao fim da sentença
    if self.pos > len(self.text) - 1:
      self.current_char = None
    else:
      self.current_char = self.text[self.pos]

  #funcao que pula um espaco em branco e avanca para o proximo caractere
  def skip_whitespace(self):
    while self.current_char is not None and self.current_char.isspace():
      self.advance()

  #funcao que verifica se um lexema lido eh um inteiro
  def integer(self):
    #variavel para concatecar numeros
    result = ""
    while self.current_char is not None and self.current_char.isdigit():
      result += self.current_char
      self.advance()
    return int(result)
  
  #funcao que verifica se um lexema lido eh uma string
  def string(self):
    #variavel para verificar se o char eh aspas
    is_aspas = False

    #variavel que vai guardar os digitos da string
    result = ''

    while self.current_char is not None:
      if self.current_char == "'" or self.current_char == '"':
        is_aspas = True
      else:
        result += self.current_char
        is_aspas = False

      self.advance()

    if is_aspas and len(result) != 0:
      return str(result)

  def defineFloat(self):
    #variavel para concatecar numeros
    result = ""
    while self.current_char is not None:
      if self.current_char.isdigit():
        result += self.current_char
      elif self.current_char == '.':
        result += self.current_char
      self.advance()
    return float(result)

  #arrumar para validar a palavra inteira  
  def boolean(self):
    result = ''
    estado = 0

    while estado != 'fim':
      if estado == 0:
        if self.current_char in ['C', 'G']:
          result += self.current_char
          estado = 1
        else:
          break
      elif estado == 1:
        if self.current_char == 'h' or self.current_char == 'e':
          result += self.current_char
          estado = 2
        else:
          break
      elif estado == 2:
        if self.current_char == 'a' or self.current_char == 'o':
          result += self.current_char
          estado = 3
        else:
          break
      elif estado == 3:
        if self.current_char == 'm':
          result += self.current_char
          estado = 'fim'
        elif self.current_char == 'j':
          result += self.current_char
          estado = 4
        else:
          break
      elif estado == 4:
        if self.current_char == 'i':
          result += self.current_char
          estado = 5
        else:
          break
      elif estado == 5:
        if self.current_char == 's':
          result += self.current_char
          estado = 'fim'
        else:
          break
      self.advance()

    return result if result in ['Cham', 'Geojis'] else None


  #funcao que implementa o "core/nucleo" do analisador lexico
  #vai quebrar a sentença/arquivo de texto em vários tokens, um por vez
  def get_next_token(self):
    #executa enquanto o caractere corrente não for None
    while self.current_char is not None:
      #verifica se o caractere corrente eh um espaco em branco
      if self.current_char.isspace():
        self.skip_whitespace()
        continue

      #verifica se o caractere atual eh um digito
      if self.current_char.isdigit() and '.' not in self.text:
        #retorno um Token do tipo YG, com valor referente ao lexema sendo processado caractere a caractere
        return Token(OPPA, self.integer())

      #verificando se o primeiro char é C (booleano)
      if self.text[0] == 'C' or self.text[0] == 'G':
        return Token(EONNI, self.boolean())

      #verifica se o caractere atual eh aspas
      if self.current_char == '"' or self.current_char == "'":
        #retorno um Token do tipo HYBE, com valor referente ao lexema sendo processado caractere a caractere
        return Token(NOONA, self.string())

      #verifica se o text contem . para ser considerado um float
      if '.' in self.text and '"' not in self.text and "'" not in self.text:
        return Token(OPPA, self.defineFloat())

      #verifica se o lexema encontrado é um operador
      if self.current_char == "+":
        self.advance()
        return Token(INKIGAYO, "+")

      if self.current_char == "-":
        self.advance()
        return Token(MCORE, "-")

      if self.current_char == "*":
        self.advance()
        return Token(MBANK, "*")

      if self.current_char == "/":
        self.advance()
        return Token(MCOUNTDOWN, "/")

      #verifica se o lexema encontrado é um parenteses (abrindo ou fechando)
      if self.current_char == "(":
        self.advance()
        return Token(LPAREN, "(")

      if self.current_char == ")":
        self.advance()
        return Token(RPAREN, ")")

      #tratamento de erros para não strings
      if '"' not in self.text and "'" not in self.text:
        for char in self.text:
          if not char.isdigit:
            self.error()

      #se nenhum dos lexemas acima foi encontrado, gera um erro
      self.error()

    #no fim, retorna o Token de fim de linha
    return Token(EOF, None)

class Interpreter(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    



def main():
    while True:
        try:
            #get the input
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()