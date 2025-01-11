def single_root_words(root_word, *other_word):
    return [item for item in other_word if root_word.lower() in item.lower() or item.lower() in root_word.lower()]

print(single_root_words('rich', 'richiest', 'orichalcum', 'cheers', 'richies'))
print(single_root_words('Disablement', 'Able', 'Mable', 'Disable', 'Bagel'))


