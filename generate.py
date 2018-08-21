import numpy as np

def setup():
    amir_text = open('data/amir.txt').read()
    jake_text = open('data/jake.txt').read()
    action_text = open('data/action.txt').read()

    amir_corpus = amir_text.split()
    jake_corpus = jake_text.split()
    action_corpus = action_text.split()

    word_dict_amir = get_word_dict(amir_corpus)
    word_dict_jake = get_word_dict(jake_corpus)
    word_dict_actions = get_word_dict(action_corpus)

    Amir = {"corpus": amir_corpus, "word_dict": word_dict_amir}
    Jake = {"corpus": jake_corpus, "word_dict": word_dict_jake}
    Actions = {"corpus": action_corpus, "word_dict": word_dict_actions}

    return Amir, Jake, Actions

def get_word_dict(corpus):
    def make_pairs(corpus):
        for i in range(len(corpus)-1):
            yield (corpus[i], corpus[i+1])

    pairs = make_pairs(corpus)

    word_dict = {}

    for word_1, word_2 in pairs:
        if word_1 in word_dict.keys():
            word_dict[word_1].append(word_2)
        else:
            word_dict[word_1] = [word_2]

    return word_dict

def generate_interleaving():
    length_allowed = np.random.randint(2,6)
    previous_character = np.random.randint(0,2) # 0-Jake, 1-Amir, 2-Actions
    interleaving = []
    for i in range(length_allowed):
        if previous_character == 0:
            next_character = np.random.randint(1,2)
        elif previous_character == 1:
            next_character = 2 if np.random.randint(0,1) == 1 else 0
        else:
            next_character = np.random.randint(0,2)
        interleaving.append(next_character)
        previous_character = next_character

    return interleaving

def generate_action(person_dict):
    corpus = person_dict["corpus"]
    word_dict = person_dict["word_dict"]
    terminate_chars = ["]"]

    first_word = np.random.choice(corpus)

    while not "[" in first_word:
        first_word = np.random.choice(corpus)

    chain = [first_word]

    n_words = np.floor(np.random.normal(10, 5))

    generate = True
    while generate:
        new_word = np.random.choice(word_dict[chain[-1]])
        while "[" in new_word:
            new_word = np.random.choice(word_dict[chain[-1]])
        if "]" in new_word:
            generate = False
        chain.append(new_word)

    return ' '.join(chain)


def generate_dialogue(person_dict):
    corpus = person_dict["corpus"]
    word_dict = person_dict["word_dict"]
    terminate_chars = [".", "?", "???", ". . . ?", "...", "--", "!"]
    open_punctuation = ["(", ")", "[", "]", "\""]

    first_word = np.random.choice(corpus)

    while first_word.islower():
        first_word = np.random.choice(corpus)

    chain = [first_word]

    # n_words = np.floor(np.random.normal(15, 10))
    n_words = np.random.randint(5, 20)
    generate = True
    count = 0
    while generate:
        new_word = np.random.choice(word_dict[chain[-1]])
        while any(word in new_word for word in open_punctuation):
            new_word = np.random.choice(word_dict[chain[-1]])

        count += 1
        if any(word in new_word for word in terminate_chars) and count > n_words:
            generate = False

        chain.append(new_word)


    return ' '.join(chain)


Amir, Jake, Actions = setup()
interleaving = generate_interleaving()
print(interleaving)

print("AMIR")
for i in range(0,10):
    print(generate_dialogue(Amir))
#
# print("JAKE")
# for i in range(0,10):
#     print(generate_dialogue(Jake))
#
# print("ACTION")
# for i in range(0,10):
#     print(generate_action(Actions))
