from minComunDivisor import mcd

p = 7
q = 3
n = p*q
eN= (p-1) * (q-1)

def comprobadorDeE(n):
    if type(n) == int:
        if n > 1 and n < eN:
            if mcd(n, eN) == 1:
                print(f'Número entero')
                print('Número dentro del intevalo')
                print(f'el numero es {num}')
                return True
    else:
        print('Número erroneo')
        return False


num = 0
while True:
    num += 1
    if comprobadorDeE(num):
        break

clave_publica = (n)