def get_matrix(n, m, value):
    return [[value for i in range(m)] for i in range(n)]


print("Первая матрица: ", get_matrix(2,2,10))
print("Вторая матрица: ", get_matrix(3,5,42))
print("Третья матрица: ", get_matrix(4,2,13))