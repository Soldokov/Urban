def print_params(a = 1, b = 'строка', c = True):
    print(a,b,c)
value_list = [False, 'bingo', 8]
value_list_2 = [433, 'bologan',]
values_dict = {'a':'fish', 'b':True, 'c':76}
print_params()
print_params(a=4)
print_params(a = 4, b = 90)
print_params(a = 4, b = 90, c = "asfw")
print_params(b = 25)
print_params(c = [1,2,3])
print_params(*value_list)
print_params(**values_dict)
print_params(*value_list_2, 42)