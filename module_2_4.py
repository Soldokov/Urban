numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
primes = []
not_primes = []
# Мне показалось это решение проще придумать, чем вложенные циклы перебрать и быстрее, на всякий оба варианта
'''def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5)+1):
        if num % i == 0:
            return False
    return True
    
for num in numbers:
    if num == 1:
        continue
    elif is_prime(num) and num != 1:
        primes.append(num)
    else:
        not_primes.append(num)
print("Простые числа: ", primes)
print("Непростые числа: ", not_primes)'''

for num in numbers:
    if num == 1:
        continue

    is_prime = True
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            is_prime = False
            break
    if is_prime:
        primes.append(num)
    else:
        not_primes.append(num)

print("Простые числа: ", primes)
print("Непростые числа: ", not_primes)