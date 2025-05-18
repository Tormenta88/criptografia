import random

# Funciones necesarias para RSA
# ------------------------------------------

# Verificamos si son números primos
def es_primo(num):
    """
    Verifica si un número es primo.
    """
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

# Encuentra dos números primos distintos por fuerza bruta en un rango, como dice el enunciado:
def encontrar_primos_en_rango(min_val, max_val):

    primos_encontrados = []
    numeros = list(range(min_val, max_val + 1))
    random.shuffle(numeros)

    for num in numeros:
        if es_primo(num):
            primos_encontrados.append(num)
            if len(primos_encontrados) == 2:
                break
    if len(primos_encontrados) < 2:
        raise ValueError("No se pudieron encontrar dos primos distintos en el rango especificado.")
    return primos_encontrados[0], primos_encontrados[1]


# Funciones de cálculo del MCD usando el algoritmo de Euclides y el inverso modular
def mcd(a, b):

    while b:
        a, b = b, a % b
    return a

def inverso_modular(e, phi_n):
    
    if mcd(e, phi_n) != 1:
        return None 

    m0, x0, x1 = phi_n, 0, 1
    temp_phi_n = phi_n
    
    while e > 1:
        q = e // temp_phi_n
        t = temp_phi_n
        temp_phi_n = e % temp_phi_n
        e = t
        t = x0
        x0 = x1 - q * x0
        x1 = t
    
    if x1 < 0:
        x1 += m0
        
    return x1

# Generación de claves RSA [cite: 24, 25, 26]
def generar_claves_rsa(min_primo=501, max_primo=1499):

    # 1. Se escogen 2 números primos: p y q.
    p, q = encontrar_primos_en_rango(min_primo, max_primo)
    while p == q: # Asegurarse de que p y q sean distintos
        p, q = encontrar_primos_en_rango(min_primo, max_primo)

    # 2. Se calcula n = p * q.
    n = p * q

    # 3. Se calcula phi(n) = (p-1)(q-1)
    phi_n = (p - 1) * (q - 1)

    # 4. Se debe elegir un número e tal que 1 < e < phi(n) y mcd(e, phi_n) = 1.
    # Comúnmente se usa e = 65537, pero aquí lo buscamos.
    e = random.randrange(2, phi_n)
    while mcd(e, phi_n) != 1:
        e = random.randrange(2, phi_n)
        
    # 5. Se debe calcular el número d que debe ser el inverso del número e en módulo phi(n)
    # d * e = 1 (mod phi_n)
    d = inverso_modular(e, phi_n)
    if d is None:
        raise Exception("No se pudo calcular d. Revisar la elección de e o la implementación del inverso modular.")
    return ((e, n), (d, n), p, q, phi_n)

# Funciones de encriptación y desencriptación RSA
# ------------------------------------------------

# Encriptar y desencriptar un mensaje usando RSA
def encriptar_rsa(clave_publica, mensaje_plano_numero):

    e, n = clave_publica
    if mensaje_plano_numero >= n:
        raise ValueError("El mensaje (como número) debe ser menor que n.")
    
    # Usar pow(base, exp, mod) para exponenciación modular eficiente
    texto_cifrado = pow(mensaje_plano_numero, e, n)
    return texto_cifrado


# Desencriptar un mensaje usando RSA
def desencriptar_rsa(clave_privada, texto_cifrado_numero):

    d, n = clave_privada
    mensaje_plano = pow(texto_cifrado_numero, d, n)
    return mensaje_plano

# Ejemplo de uso del RSA implementado:
# ------------------------------------------------

# Generar claves RSA
print("--- Ejemplo de RSA Implementado (sin librerías) ---")
try:
    clave_publica_rsa, clave_privada_rsa, p, q, phi_n = generar_claves_rsa()
    print(f"P (primo encontrado): {p}")
    print(f"Q (primo encontrado): {q}")
    print(f"N (p*q): {clave_publica_rsa[1]}")
    print(f"Phi(N) ((p-1)*(q-1)): {phi_n}")
    print(f"Clave Pública (e, N): {clave_publica_rsa}")
    print(f"Clave Privada (d, N): {clave_privada_rsa}")

    mensaje_original_numero = 123 # Ejemplo de mensaje como número
    if mensaje_original_numero >= clave_publica_rsa[1]:
        print(f"El mensaje de ejemplo {mensaje_original_numero} es demasiado grande para N={clave_publica_rsa[1]}. Usando un mensaje más pequeño.")
        mensaje_original_numero = random.randint(1, clave_publica_rsa[1]-1)


    print(f"\nMensaje original (número): {mensaje_original_numero}")

    texto_cifrado = encriptar_rsa(clave_publica_rsa, mensaje_original_numero)
    print(f"Texto cifrado: {texto_cifrado}")

    mensaje_desencriptado = desencriptar_rsa(clave_privada_rsa, texto_cifrado)
    print(f"Mensaje desencriptado: {mensaje_desencriptado}")

    if mensaje_original_numero == mensaje_desencriptado:
        print("\n¡Éxito! El mensaje original y el desencriptado coinciden.")
    else:
        print("\nError: El mensaje original y el desencriptado NO coinciden.")

except ValueError as e:
    print(f"Error durante la generación de RSA: {e}")
except Exception as e:
    print(f"Ocurrió un error: {e}")