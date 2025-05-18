def mcd(a, b): # Maximo Comun Divisor
  while b != 0:
    a = b
    b = a % b
  return a

def mcdExtend(a, b): # Maximo Comun Divisor extendido
  if a == 0:
    return (b, 0, 1)
  else:
    g, y, x = mcdExtend(b % a, a) # Aplicamos recursivamente
    return (g, x - (b // a) * y, y) # Creo que esto esta bien ¿?

def modInverso(a, m):
  g, x, y = mcdExtend(a, m)
  if g != 1:
    print('El inverso modular no existe : / (No sirve el resto)')
  else:
    return x % m

def generarClavesRSA(p, q, exponentePublico=65537):
    #Generamos el par de claves RSA con los primos p y q.
    # Vamos a asumir que p y q son primos | No importa
    n = p * q
    phi_n = (p - 1) * (q - 1)

    # Elegimos e
    e = exponentePublico
    # Calculamos d
    d = modInverso(e, phi_n)

    clavePublica = (n, e)
    clavePrivada = (n, d)

    return clavePublica, clavePrivada

def encriptar(clavePublica, intMensaje):
    #Ciframos usando la clave pública RSA.
    n, e = clavePublica
    if intMensaje >= n:
      print(f"El mensaje ({intMensaje}) es >= al módulo n ({n}). Por tanto puede que haya fallos descifrando : (")

    textoCifrado = pow(intMensaje, e, n) # C = M^e mod n, pow es función normal de python que viene perfecta para esto
    return textoCifrado

def decrypt(clavePrivada, intCifradoTexto):
    #Desciframos usando la clave privada
    n, d = clavePrivada
    intMensaje = pow(intCifradoTexto, d, n) # M = C^d mod n
    return intMensaje


def strToInt(s):
    #Convertimos la cadena de texto a numero
    bytesRepresentacion = s.encode('utf-8')
    intRepresentacion = int.from_bytes(bytesRepresentacion, byteorder='big') # Usamos big para que nos de un entero grande, valga la redundancia
    return intRepresentacion

def intToString(i):
    """Convierte un entero grande de vuelta a una cadena de texto."""
    # Calcula cuántos bytes se necesitan
    # (i.bit_length() + 7) // 8 calcula el número de bytes necesarios
    byte_length = (i.bit_length() + 7) // 8
    # Si el entero es 0, necesita 1 byte para representar el byte nulo
    if byte_length == 0:
      byte_length = 1
    # Convierte el entero a bytes
    bytesRepresentacion = i.to_bytes(byte_length, byteorder='big')
    # Decodifica los bytes a una cadena (usando utf-8)
    try:
      s = bytesRepresentacion.decode('utf-8')
      return s
    except UnicodeDecodeError:
      # Si la decodificación falla, podría ser que el número no representaba
      # una cadena utf-8 válida (posible error en cifrado/descifrado o padding)
      return f"<Error de decodificación: {bytesRepresentacion}>"



# 1 Parámetros de Alicia
p_a = 13
q_a = 131
print(f"\nAlicia: p={p_a}, q={q_a}")

# 2 Generación de Claves de Alicia
clavePublAli, clavePrivAli = generarClavesRSA(p_a, q_a)
n_a, e_a = clavePublAli
_, d_a = clavePrivAli
print(f"  Clave Pública de Alicia (n_a, e_a): ({n_a}, {e_a})")
print(f"  Clave Privada de Alicia (n_a, d_a): ({n_a}, {d_a})")

# 3 Parámetros de Benito
p_b = 59
q_b = 571
print(f"\nBenito: p={p_b}, q={q_b}")

# 4 Generación de Claves de Benito
clavePublBen, clavePrivBen = generarClavesRSA(p_b, q_b)
n_b, e_b = clavePublBen
_, d_b = clavePrivBen
print(f"  Clave Pública de Benito (n_b, e_b): ({n_b}, {e_b})")
print(f"  Clave Privada de Benito (n_b, d_b): ({n_b}, {d_b})")


# 5 Alicia envía mensaje cifrado a Benito

mensajeHex_Ali_Ben = "3BC"
# Convertir hexadecimal a entero
mensajeInt_a_b = int(mensajeHex_Ali_Ben, 16)
print(f"\n1. Alicia quiere enviar a Benito el mensaje: '{mensajeHex_Ali_Ben}' (hex) = {mensajeInt_a_b} (int)")

# Alicia cifra el mensaje usando la clave publica de Benito
print(f"   Alicia cifra {mensajeInt_a_b} usando la clave pública de Benito ({clavePublBen})...")
try:
    ciphertextAli_to_Ben = encriptar(clavePublBen, mensajeInt_a_b)
    print(f"   Texto cifrado enviado por Alicia: {ciphertextAli_to_Ben}")

    # 6 Benito descifra el mensaje de Alicia

    print(f"\n2 Benito recibe el texto cifrado: {ciphertextAli_to_Ben}")
    print(f"   Benito descifra usando su clave privada ({clavePrivBen})...")
    # Benito descifra usando su clave privada
    descifradoIntAli_to_Ben = decrypt(clavePrivBen, ciphertextAli_to_Ben)
    # Convertir el entero descifrado de nuevo a hexadecimal para verificar
    descifradoHexAli_to_Ben = hex(descifradoIntAli_to_Ben)

    print(f"   Mensaje descifrado por Benito (int): {descifradoIntAli_to_Ben}")
    print(f"   Mensaje descifrado por Benito (hex): {descifradoHexAli_to_Ben[2:].upper()}") # [2:] para quitar el 0x

    if descifradoHexAli_to_Ben[2:].upper() == mensajeHex_Ali_Ben:
        print("###################### Esta bien : D ######################")
    else:
        print("###################### Esta mal : ( ######################")

except Exception as e:
    print(f"   Error durante el cifrado/descifrado: {e}")


# 7 Benito envía mensaje cifrado a Alicia

mensajeStr_Ben_to_Ali = "TODO OK"
print(f"\n3. Benito quiere enviar a Alicia el mensaje: '{mensajeStr_Ben_to_Ali}'")

# Convertir string a entero
try:
    mensajeInt_Ben_to_Ali = strToInt(mensajeStr_Ben_to_Ali)
    print(f"   Mensaje convertido a entero: {mensajeInt_Ben_to_Ali}")

    # Comprobación importante: El tamaño del mensaje vs el módulo de Alicia
    if mensajeInt_Ben_to_Ali >= n_a:
         print(f"   El entero del mensaje ({mensajeInt_Ben_to_Ali}) es mayor o igual que el módulo 'n' de Alicia ({n_a}). Puede que haya fallos")

    # Benito cifra el mensaje usando la CLAVE PÚBLICA de Alicia
    print(f"   Benito cifra {mensajeInt_Ben_to_Ali} usando la clave pública de Alicia ({clavePublAli})...")
    cifradoBen_to_Ali = encriptar(clavePublAli, mensajeInt_Ben_to_Ali)
    print(f"   Texto cifrado enviado por Benito: {cifradoBen_to_Ali}")


    # 8 Alicia descifra el mensaje de Benito

    print(f"\n4. Alicia recibe el texto cifrado: {cifradoBen_to_Ali}")
    print(f"   Alicia descifra usando su clave privada ({clavePrivAli})...")
    # Alicia descifra usando su CLAVE PRIVADA
    descifradoInt_Ben_to_Ali = decrypt(clavePrivAli, cifradoBen_to_Ali)
    print(f"   Mensaje descifrado por Alicia (int): {descifradoInt_Ben_to_Ali}")

    # Convertir el entero descifrado de nuevo a string
    descifradoStr_Ben_to_Ali = intToString(descifradoInt_Ben_to_Ali)
    print(f"   Mensaje descifrado por Alicia (str): '{descifradoStr_Ben_to_Ali}'")

    # Verificación (considerando la advertencia anterior)
    if descifradoStr_Ben_to_Ali == mensajeStr_Ben_to_Ali:
        print("###################### Esta bien : D ######################")
    elif mensajeInt_Ben_to_Ali >= n_a:
       print("###################### Esta mal : ( ######################")
       print("No esta bien debido a que el resultado no coincide debido a que M >= n.")
    else:
       print("###################### Esta mal : ( ######################")

except Exception as e:
    print(f"   Error durante el cifrado/descifrado: {e}")
