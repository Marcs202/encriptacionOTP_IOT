def scrambled(P, S):
        return ((P << (S & 0b11111)) | (P >> (64 - (S & 0b11111)))) & 0xFFFFFFFFFFFFFFFF
    #(S & 0b11111) obtiene los bit menos significativos
def generative(P0, Q):
    return (P0 & Q) & 0xFFFFFFFFFFFFFFFF
#solo se usa un and y se corta a 64 bits
def mutative(S, Q):
    return (S | Q) & 0xFFFFFFFFFFFFFFFF
class GeneracionLlaves:
   
    #or bit a bit 
    def generate_keys(p, q, s, n):
        keys = []
        s0 = s
        for i in range(1,n+1):
            if i % 2 == 0:
                q0 = scrambled(q, s0)
                k = generative(q0, p0) # k = generative(q0, p0)
                s0 = mutative(s0, p0)  #  s0 = mutative(s0, p0)
            else: #!la primera iteracion empieza aca, ya que el for fue configurado para empezar en 1
                p0 = scrambled(p, s)
                k = generative(p0, q)
                s0 = mutative(s, q)
            keys.append(k)
            p, q = q, p0  # Swap p and q for the next iteration
        return keys