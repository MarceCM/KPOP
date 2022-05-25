#Meu primeiro lexer

#Definir os tokens da minha linguagem

#EOF: token que representa o fim de um arquivo (end of file)

RAK, CAK, PAK, DAESANG, BONSANG, COMEBACK, KAMSAMIDA, EOF, ANNYEONG, YG, JYP, SM, HYBE,BIAS,OPPA,EONNI,NOONA,INKIGAYO,MCORE,MBANK,MCOUNTDOWN,MELON,KAKAO,MNET,DISBAND, SULJIBN, SULJIBT, SEMIKOLLON, BANJEOM, DUJEOM, BLACKPINK, BTS, LOONA, WJSN, LPAREN, RPAREN = (
"RAK", "CAK", "PAK", "DAESANG", "BONSANG", "COMEBACK", "KAMSAMIDA", "EOF", "ANNYEONG", "YG", "JYP", "SM", "HYBE", "BIAS","OPPA","EONNI","NOONA", "INKIGAYO", "MCORE", "MBANK", "MCOUNTDOWN", "MELON", "KAKAO", "MNET", "DISBAND", "SULJIBN", "SULJIBT", "SEMIKOLLON", "BANJEOM", "DUJEOM", "BLACKPINK", "BTS", "LOONA", "WJSN", "LPAREN", "RPAREN"
)

palavras_reservadas = [
  'yg', 'jyp', 'hybe', 'sm', 'rak',
  'pak', 'cak', 'daesang', 'bonsang',
  'comeback', 'kamsamida', 'annyeong',
  '"', "'", '+', '-', '*', '/', '=',
  '==', '&&', '||', '\n', '\t', ';',
  ',', ':,', '>', '<', '>=', '<=',
  '(', ')'
]

#classe Token, para representar os tokens durante a compilação
class Token(object):
  def __init__(self, type, value):
    self.type = type
    self.value = value

  #representação em string da classe
  def __str__(self):
    return "Token({type}, {value})".format(type = self.type, value = repr(self.value))

  def __repr__(self):
    return self.__str__()

#classe que implementa o analisador lexico
class Lexer(object):
  def __init__(self, text):
    self.list = text
    #string do usuario
    self.text = self.list[0] #"string"
    #indice que marca a posicao do texto (o caractere corrente sendo processado no texto)
    self.pos = 0
    #guarda o caractere que está sendo analisado de fato
    self.current_char = self.text[self.pos]#"

  def get_next_lexer(self):
    if ',' not in self.list[0] or self.text == ',':
      self.list.pop(0)
      if len(self.list) == 0:
        self.current_char = None
      else:
        self.text = self.list[0]
    else:
      self.text = self.text[1:]

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
    while self.current_char is not None and self.text.isspace():
      self.get_next_lexer()

  #funcao que verifica se um lexema lido eh um inteiro
  def integer(self):
    #variavel para concatecar numeros
    result = ""
    if self.current_char is not None and self.text.isdigit():
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

  def boolean(self):
    result = self.text
    self.current_char = None

    return result if result in ['Cham', 'Geojis'] else None

  #funcao que implementa o "core/nucleo" do analisador lexico
  #vai quebrar a sentença/arquivo de texto em vários tokens, um por vez
  def get_next_token(self):
    #executa enquanto o caractere corrente não for None
    while self.current_char is not None:
      #verifica se o caractere corrente eh um espaco em branco
      if self.text.isspace():
        self.skip_whitespace()
        continue

      #verifica se o caractere atual eh um digito
      if self.text.isdigit() and '.' not in self.text:
        valor = self.text
        self.get_next_lexer()
        #retorno um Token do tipo YG, com valor referente ao lexema sendo processado caractere a caractere
        return Token(OPPA, int(valor))

      #verificando se é booleano
      if self.text == 'Cham' or self.text == 'Geojis':
        bool = self.text
        self.get_next_lexer()
        return Token(EONNI, bool)

      #verifica se o caractere atual eh aspas
      if '"' in self.text or "'" in self.text:
        string = self.text
        self.get_next_lexer()
        #retorno um Token do tipo HYBE, com valor referente ao lexema sendo processado caractere a caractere
        return Token(NOONA, string)

      #verifica se o text contem . para ser considerado um float
      if self.text == '.' and self.list[self.list.index(self.text)-1].isdigit() and self.list[self.list.index(self.text)+1].isdigit():
        num1 = self.list[self.list.index(self.text)-1]
        num2 = self.list[self.list.index(self.text)+1]
        valor = float(f'{num1}.{num2}')
        self.get_next_lexer()
        return Token(OPPA, valor)

      #verifica se o text é um identifier
      if not self.text[0].isdigit() and self.text not in palavras_reservadas:
        token_value = self.text.replace(',', '')
        self.get_next_lexer()
        return Token(BIAS, token_value)

      #verifica se são palavras reservadas
      if self.text == "kamsamida":
        self.get_next_lexer()
        return Token(KAMSAMIDA, "kamsamida")

      if self.text == "daesang":
        self.get_next_lexer()
        return Token(DAESANG, "daesang")

      if self.text == "comeback":
        self.get_next_lexer()
        return Token(COMEBACK, "comeback")

      if self.text == "hybe":
        self.get_next_lexer()
        return Token(HYBE, "hybe")

      if self.text == "sm":
        self.get_next_lexer()
        return Token(SM, "sm")

      if self.text == 'yg':
        self.get_next_lexer()
        return Token(YG, 'yg')

      if self.text == "jyp":
        self.get_next_lexer()
        return Token(JYP, "jyp")

      if self.text == "annyeong":
        self.get_next_lexer()
        return Token(ANNYEONG, "annyeong")

      #verifica se são caracteres especiais
      if self.text == "\n":
        self.get_next_lexer()
        return Token(SULJIBN, "\n")

      if self.text == "\t":
        self.get_next_lexer()
        return Token(SULJIBT, "\t")

      if self.text == ",":
        self.get_next_lexer()
        return Token(BANJEOM, ",")

      if self.text == ":":
        self.get_next_lexer()
        return Token(DUJEOM, ":")

      if self.text == ";":
        self.get_next_lexer()
        return Token(SEMIKOLLON, ";")

      #verifica se o lexema encontrado é um operador
      if self.text == "+":
        self.get_next_lexer()
        return Token(INKIGAYO, "+")
    
      if self.text == "-":
        self.get_next_lexer()
        return Token(MCORE, "-")

      if self.text == "*":
        self.get_next_lexer()
        return Token(MBANK, "*")

      if self.text == "/":
        self.get_next_lexer()
        return Token(MCOUNTDOWN, "/")

      if self.text == "(":
        self.get_next_lexer()
        return Token(LPAREN, "(")

      if self.text == ")":
        self.get_next_lexer()
        return Token(RPAREN, ")")

      #verifica se o lexema encontrado é uma condicional
      if self.text == "=":
        self.get_next_lexer()
        return Token(MELON, "=")

      if self.text == "==":
        self.get_next_lexer()
        return Token(KAKAO, "==")

      if self.text == "<=":
        self.get_next_lexer()
        return Token(WJSN, "<=")
      
      if self.text == "rak":
        self.get_next_lexer()
        return Token(RAK, "rak")

      if self.text == "pak":
        self.get_next_lexer()
        return Token(PAK, "pak")

      if self.text == "cak":
        self.get_next_lexer()
        return Token(CAK, "cak")

      if self.text == "bonsang":
        self.get_next_lexer()
        return Token(BONSANG, "bonsang")

      if self.text == "<":
        self.get_next_lexer()
        return Token(BTS, "<")
      
      if self.text == ">=":
        self.get_next_lexer()
        return Token(LOONA, ">=")

      if self.text == "&&":
        self.get_next_lexer()
        return Token(MNET, "&&")

      if self.text == "||":
        self.get_next_lexer()
        return Token(DISBAND, "||")
      
      if self.text == ">":
        self.get_next_lexer()
        return Token(BLACKPINK, ">")
      
      #tratamento de erros para não strings
      if '"' not in self.text and "'" not in self.text:
        for char in self.text:
          if not char.isdigit:
            self.error()

      #se nenhum dos lexemas acima foi encontrado, gera um erro
      self.error()

    #no fim, retorna o Token de fim de linha
    return Token(EOF, None)

#programa principal que invoca o analisador lexico/Lexer
def main():
  #le o input de texto
  try:
    with open('testes.txt', 'r') as arquivo:
      lexemas = arquivo.readlines()[0].split(' ')
  except FileNotFoundError:
    print('Arquivo não encontrado, verifique.')

  for lexema in lexemas:
    #instancio o lexer
    lexer = Lexer(lexema)
    '''Imprime todos os tokens '''
    #reconheco o primeiro token do input
    token = lexer.get_next_token()
    #enquanto o token retornado for diferente de EOF, continua processando o texto
    while(token.type is not EOF):
      print(token)
      token = lexer.get_next_token()


if __name__ == "__main__":
  main()
