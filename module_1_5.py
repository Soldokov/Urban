immutable_var = ("data", 12, 4.576, True)
print(immutable_var)
mutable_list = ["data", 12, 4.576, True]
print(mutable_list)
try:
    immutable_var[0] = 99
except TypeError as e:
    print("Ошибка при попытке изменить кортеж:", e)
    explanation = (
        "Кортежи (tuple) являются неизменяемыми структурами данных. "
        "После создания кортежа невозможно изменить его элементы. Такое поведение обеспечивает "
        "большую надёжность данных, поскольку исключает возможность случайного изменения содержимого. "
        )
    print(explanation)
mutable_list[0] = 99
print(mutable_list)