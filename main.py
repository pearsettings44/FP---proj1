############################################################
#             Projeto 1 de FP                              #
#             Nome: José Augusto Alves Pereira             #
#             Número: ist1103252                           #
#             Email: jose.a.pereira@tecnico.ulisboa.pt     #
#             Data: 27/10/2021                             #
############################################################


def corrigir_palavra(expressao):
    """
    Recebe uma cadeia de caracteres (palavra) (potencialmente modificada por um surto de letras)
    e devolve a cadeia de caracteres que corresponde á aplicação da sequência de reduções.
    str ---> str
    """
    i = 0
    expressao = list(expressao)
    while i < len(expressao) - 1:
        # Caso duas letras seguidas sejam iguais mas não ambas maiusculas ou minusculas, elimina-se ambas da string.
        if expressao[i].upper() == expressao[i + 1].upper() and expressao[i] != expressao[i + 1]:
            del expressao[i:i + 2]
            i = 0
        else:
            i += 1
    return ''.join(expressao)


def eh_anagrama(palavra1, palavra2):
    """
    Recebe duas cadeias de caracteres (palavras) e devolve True se uma é anagrama da outra,
    em caso contrário devolve False.
    str, str ---> bool
    """
    if sorted(palavra1.lower()) == sorted(palavra2.lower()):
        return True
    else:
        return False


def corrigir_doc(texto):
    """
    Recebe uma cadeira de caracteres (texto com erros da BDB) e devolve a cadeia
    de caracteres filtrada com as palavras corrigidas e os anagramas retirados.
    str ---> str
    """
    # Verificar a validade do argumento, levantando ValueError caso o argumento não seja válido.
    if type(texto) != str or len(texto) == 0:
        raise ValueError("corrigir_doc: argumento invalido")
    j = 0
    while j <= len(texto) - 1:
        # Levantar ValueError caso existam dois espaços seguidos, ou caso um caractere do texto não seja uma letra.
        if texto[j] == " " and texto[j + 1] == " " or (texto[j] != " " and not texto[j].isalpha()):
            raise ValueError("corrigir_doc: argumento invalido")
        j += 1
    texto = corrigir_palavra(texto)
    texto_list = list(texto.split())
    # Caso duas palavras sejam anagramas, retira-se a segunda, com exceção de serem palavras iguais.
    for palavra1 in texto_list:
        for palavra2 in texto_list:
            if eh_anagrama(palavra1, palavra2) and palavra1.lower() != palavra2.lower():
                texto_list.remove(palavra2)
    return ' '.join(texto_list)


def obter_posicao(direcao, posicao_atual):
    """
    Recebe um caracter (direção de um movimento) e um inteiro (posição atual),
    e devolve o inteiro correspondente à nova posição após o movimento.
    str, int ---> int
    """
    # Representação de cada dígito no painel como um ponto num espaço cartesiano, sendo a origem o ponto 5 (0,0).
    posicoes = {7: [-1, -1], 8: [0, -1], 9: [1, -1], 4: [-1, 0], 5: [0, 0], 6: [1, 0], 1: [-1, 1], 2: [0, 1], 3: [1, 1]}
    posicao = list(posicoes.get(posicao_atual))
    if direcao == "C":
        return movimentar(posicao, posicoes, 1, 1)
    if direcao == "B":
        return movimentar(posicao, posicoes, -1, 1)
    if direcao == "E":
        return movimentar(posicao, posicoes, -1, 0)
    if direcao == "D":
        return movimentar(posicao, posicoes, 1, 0)


def movimentar(posicao, posicoes, incremento, index):
    """
    Função auxiliar à função obter_posicao: realiza o movimento da posição.
    list, dict, int, int ---> int
    """
    posicao[index] = posicao[index] + incremento
    # Caso o movimento originar um ponto que não está no dicionario posicoes, não acontece nenhum movimento.
    if posicao not in posicoes.values():
        posicao[index] = posicao[index] - incremento
    for key, value in posicoes.items():
        if value == posicao:
            return key


def obter_digito(seq, p_inicial):
    """
    Recebe uma cadeira de caracteres (sequencia de movimentos) e a
    posiçáo incial, devolvendo a posição final após os movimentos.
    str, int ---> int
    """
    i = 0
    posicao = p_inicial
    while i < len(seq):
        posicao = obter_posicao(seq[i], posicao)
        i += 1
    return posicao


def obter_pin(sequencias):
    """
    Esta função recebe sequências de movimentos e devolve
    o pin codificado de acordo com os movimentos.
    tuple ---> tuple
    """
    # Verificar a validade do argumento, levantando ValueError caso o argumento não seja válido.
    if type(sequencias) != tuple or (len(sequencias) < 4 or len(sequencias) > 10):
        raise ValueError("obter_pin: argumento invalido")
    for seq in sequencias:
        if len(seq) == 0:
            raise ValueError("obter_pin: argumento invalido")
        for c in seq:
            if c not in ["E", "D", "C", "B"]:
                raise ValueError("obter_pin: argumento invalido")
    posicao_incial = 5
    pin = ()
    # Loop para obter todos os dígitos do pin
    for mov in sequencias:
        pin = pin + (obter_digito(mov, posicao_incial),)
        posicao_incial = pin[-1]
    return pin


def validar_a_cifra(cifra):
    """
    Função auxiliar à função eh_entrada: verifica a validade da cifra.
    str ---> bool
    """
    # Verificar a validade do argumento, retornando False caso o argumento não seja válido.
    if type(cifra) != str or len(cifra) == 0:
        return False
    # O argumento só tem letras minusculas e '-', caso só tenha uma letra, não tem '-'.
    for c in cifra:
        if not c.isalpha() and c != "-" or (len(cifra) == 1 and c == "-") or (c.lower() != c):
            return False
    # O argumento não tem dois '-' de seguida.
    i = 0
    while i < len(cifra) - 1:
        if cifra[i] == "-" and cifra[i] == cifra[i + 1]:
            return False
        i += 1
    # O argumento não começa nem acaba com '-'.
    if cifra[-1] == "-" or cifra[0] == "-":
        return False
    return True


def validar_checksum(checksum):
    """
    Função auxiliar à função eh_entrada: verifica a validade do checksum.
    str ---> bool
    """
    if type(checksum) != str or len(checksum) != 7:
        return False
    # O argumento começa e acaba com parênteses retos.
    if checksum[0] != "[" or checksum[6] != "]":
        return False
    # O argumento tem 5 letras minusculas entre os parênteses retos.
    for c in checksum[1:6]:
        if not c.isalpha() or c != c.lower():
            return False
    return True


def validar_numeros_seguranca(nums):
    """
    Função auxiliar à função eh_entrada: verifica a validade dos numeros de segurança.
    tuple ---> bool
    """
    if type(nums) != tuple or len(nums) < 2:
        return False
    # Os elementos do tuple são todos inteiros positivos.
    for num in nums:
        if type(num) != int:
            return False
        if num < 1:
            return False
    return True


def eh_entrada(entrada_bdb):
    """
    Devolve True, se e só se o argumento corresponde a uma entrada da BDB.
    universal ---> bool
    """
    if type(entrada_bdb) != tuple or len(entrada_bdb) != 3:
        return False
    if not validar_a_cifra(entrada_bdb[0]):
        return False
    if not validar_checksum(entrada_bdb[1]):
        return False
    if not validar_numeros_seguranca(entrada_bdb[2]):
        return False
    return True


def validar_cifra(cifra, checksum):
    """
    Esta função recebe uma cifra e uma sequência de controlo, e devolve True
    se e só se a sequência de controlo é coerente com a cifra conforme descrito.
    str, str ---> bool
    """
    # counters: conta o número de ocorrências na cifra de cada letra na sequência de controlo.
    counters = [0, 0, 0, 0, 0]
    i = 0
    letters = list(checksum[1:6])
    # Sempre que uma das letras da sequencia de controlo estiver na cifra, aumenta uma unidade no seu slot em counters
    for letter in letters:
        if letter not in cifra:
            return False
        for c in cifra:
            if c == letter:
                counters[i] += 1
        i += 1
    # Verificar se as letras mais frequentes na cifra estão de facto no checksum
    cifra_lista = sorted(list("".join(cifra.split("-"))))
    cifra_ordenada = sorted(cifra_lista, key=cifra_lista.count, reverse=True)
    letras_em_cifra_ordenada = []
    [letras_em_cifra_ordenada.append(x) for x in cifra_ordenada if x not in letras_em_cifra_ordenada]
    for letra in letras_em_cifra_ordenada[:5]:
        if letra not in letters:
            return False
    # Verificar se a sequência de controlo está em ordem inversa de ocorrências.
    if counters != sorted(counters, reverse=True):
        return False
    j = 0
    # Caso exista o mesmo número de ocorrências de letras diferentes, decidir o empate por ordem alfabética.
    while j < len(counters) - 1:
        if counters[j] == counters[j + 1] and letters[j] > letters[j + 1]:
            return False
        j += 1
    return True


def filtrar_bdb(entradas):
    """
    Esta função recebe uma ou mais entradas BDB e devolve uma lista com as entradas
    em que a cifra não é coerente com o checksum correspondente.
    list ---> list
    """
    if type(entradas) != list or len(entradas) == 0:
        raise ValueError("filtrar_bdb: argumento invalido")
    entradas_incorretas = []
    for entrada in entradas:
        if not eh_entrada(entrada):
            raise ValueError("filtrar_bdb: argumento invalido")
        if not validar_cifra(entrada[0], entrada[1]):
            entradas_incorretas.append(entrada)
    return entradas_incorretas


def obter_num_seguranca(numeros):
    """
    Esta função recebe um tuplo de números inteiros positivos e devolve o
    número de segurança (menor diferença positiva entre qualquer par de números).
    tuple ---> int
    """
    diferencas = []
    numeros = sorted(numeros)
    i = 0
    # Calcular as diferencas absolutas entres os números no tuplo (números já organizado por ordem crescente)
    while i < len(numeros) - 1:
        diferencas.append(abs(numeros[i] - numeros[i + 1]))
        i += 1
    # O número de segurança é o menor valor em diferencas.
    num_de_seguranca = min(diferencas)
    return num_de_seguranca


def decifrar_texto(cifra, num_seguranca):
    """
    Esta função descodifica a cifra de acordo com o número de segurança.
    str, int ---> str
    """
    # Retirar os "-" da cifra e substituir por espaços.
    cifra_sem_tracinho = " ".join(cifra.split("-"))
    cifra_descodificada = ""
    letras_pares, letras_impares = [], []
    # Analisar todos os caracteres em posições pares da cifra.
    for caracter in cifra_sem_tracinho[0::2]:
        # Desde que o caractere não seja um espaço, somar o número de segurança  mais 1 ao seu valor decimal.
        if caracter != " ":
            new_ord = ord(caracter) + num_seguranca + 1
            # Importante notar que os valores decimais de a-z estão entre 97 (a) e 122 (z), sendo que enquanto o valor
            # que está na variavel new_ord for superior a 122, retiramos 26 unidades (122-97 +1 = 26).
            while new_ord > 122:
                new_ord -= 26
            letras_pares += chr(new_ord)
        else:
            letras_pares += " "
    # Efetuar o mesmo raciocinio para as posições pares, mas desta vez para as impares, onde a principal diferença é
    # em vez de somar mais 1, subtraimos 1 unidade ao valor de new_ord.
    for caracter in cifra_sem_tracinho[1::2]:
        if caracter != " ":
            new_ord = ord(caracter) + num_seguranca - 1
            while new_ord > 122:
                new_ord -= 26
            letras_impares += chr(new_ord)
        else:
            letras_impares += " "
    i = 0
    # Adicionar alternamente as caracteres em posições pares e impares, obtendo assim a cifra descodificada.
    # Caso exista um número impar de caracteres, ao adicionar duas a duas sobra sempre uma.
    if (len(letras_pares) + len(letras_impares)) % 2 == 0:
        while i < len(letras_pares):
            cifra_descodificada += letras_pares[i] + letras_impares[i]
            i += 1
        return cifra_descodificada
    else:
        while i < len(letras_impares):
            cifra_descodificada += letras_pares[i] + letras_impares[i]
            i += 1
        # Adicionar o caractere que falta.
        cifra_descodificada += letras_pares[-1]
        return cifra_descodificada


def decifrar_bdb(entradas):
    """
    Esta função recebe uma ou mais entradas da BDB
    e devolve o texto das entradas decifradas.
    list ---> list
    """
    texto = []
    if type(entradas) != list or len(entradas) == 0:
        raise ValueError("decifrar_bdb: argumento invalido")
    for entrada in entradas:
        if not eh_entrada(entrada):
            raise ValueError("decifrar_bdb: argumento invalido")
    for entrada in entradas:
        num_seguranca = obter_num_seguranca(entrada[2])
        texto.append(decifrar_texto(entrada[0], num_seguranca))
    return texto


def eh_utilizador(dicionario):
    """
    Esta função recebe um argumento de qualquer tipo e retorna True se e so se esse argumento
    corresponder a um dicionario contendo informação de utilizador relevante da BDB
    universal ---> bool
    """
    argumentos, argumentos2 = ["name", "pass", "rule"], ["vals", "char"]
    if type(dicionario) != dict:
        return False
    if type(dicionario["rule"]) != dict:
        return False
    if len(dicionario) != 3 or len(dicionario["rule"]) != 2:
        return False
    # Verificar se todos os argumentos necessários estão no dicionário.
    for argumento in argumentos:
        if argumento not in dicionario.keys():
            return False
    # Verificar se todos os argumentos necessários estão no dicionário associado a "rule".
    for argumento2 in argumentos2:
        if argumento2 not in dicionario["rule"].keys():
            return False
    if type(dicionario["name"]) != str or type(dicionario["pass"]) != str:
        return False
    if len(dicionario["name"]) < 1 or len(dicionario["pass"]) < 1:
        return False
    if type(dicionario["rule"]["vals"]) != tuple or len(dicionario["rule"]["vals"]) != 2:
        return False
    if dicionario["rule"]["vals"][0] > dicionario["rule"]["vals"][1]:
        return False
    for inteiro in dicionario["rule"]["vals"]:
        if type(inteiro) != int or inteiro < 1:
            return False
    if type(dicionario["rule"]["char"]) != str or len(dicionario["rule"]["char"]) != 1:
        return False
    # verificar se o valor de "char" é um letra minúscula.
    if not dicionario["rule"]["char"].isalpha() or dicionario["rule"]["char"].lower() != dicionario["rule"]["char"]:
        return False
    return True


def eh_senha_valida(senha, regra):
    """
    Esta função recebe uma senha e as regras individuais correspondentes,
    e devolve True se e só se a senha respeita essas regras e as regras gerais.
    str, tuple ---> bool
    """
    vogais = "aeiou"
    counter_vogal = 0
    counter_repeticao = 0
    counter_regra = 0
    # Contar o número de vogais na senha,
    # Caso a letra seja o valor de "char", contar o número das suas ocorrências.
    for letra in senha:
        if letra in vogais:
            counter_vogal += 1
        if letra == regra["char"]:
            counter_regra += 1
    if counter_vogal < 3:
        return False
    if counter_regra < regra["vals"][0] or counter_regra > regra["vals"][1]:
        return False
    i = 0
    # Verificar se existem  duas letras consecutivas iguais
    while i < len(senha) - 1:
        if senha[i] == senha[i+1]:
            counter_repeticao += 1
        i += 1
    if counter_repeticao == 0:
        return False
    return True


def filtrar_senhas(dicionarios):
    """
    Esta função recebe uma lista de um ou mais dicionários correspondentes a entradas BDB, e
    devolve a lista ordenada alfabeticamente com os nomes dos utilizador com senhas erradas.
    list ---> list
    """
    users = []
    if type(dicionarios) != list or len(dicionarios) < 1:
        raise ValueError("filtrar_senhas: argumento invalido")
    for entrada in dicionarios:
        if not eh_utilizador(entrada):
            raise ValueError("filtrar_senhas: argumento invalido")
        if not eh_senha_valida(entrada["pass"], entrada["rule"]):
            users.append(entrada["name"])
    return sorted(users)
