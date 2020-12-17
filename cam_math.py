import math

def is_prime(num):
    base_primes = [1,2,3,5]
    if num in base_primes:
        return True
    elif num == 0 or num % 2 == 0 or num % 3 == 0 or num % 5 == 0:
        return False
    else:
        x = int(math.sqrt(num))
        for i in range(2,x):
            if x % i == 0:
                return False
        return True