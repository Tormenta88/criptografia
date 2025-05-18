p = 3
q = 5

eN= (p-1) * (q-1)

e = 'algo'
# no joder no quiero ser chinw




def mcd(n1, n2):
    n = 0
    divisores = []
    while True:
        n+=1
        if n1 % n == 0 and n2 % n == 0:
            divisores.append(n)
        if n == min(n1, n2):
            return divisores[-1]


if __name__ == '__main__':
    print(mcd(36, 60))