import numpy as np
import random

window_size = 2

def setup():
    amir_text = open('data/amir.txt').read()
    jake_text = open('data/jake.txt').read()
    action_text = open('data/action.txt').read()

    amir_corpus = amir_text.split()
    jake_corpus = jake_text.split()
    action_corpus = action_text.split()

    model_amir = get_model(amir_corpus)
    model_jake = get_model(jake_corpus)
    model_actions = get_model(action_corpus)

    Amir = {"corpus": amir_corpus, "model": model_amir}
    Jake = {"corpus": jake_corpus, "model": model_jake}
    Actions = {"corpus": action_corpus, "model": model_actions}

    return Amir, Jake, Actions

def get_model(corpus):
    model = {}

    for i in range(0, len(corpus)-window_size):
        window = tuple(corpus[i:i+window_size])
        if window in model:
            model[window].append(corpus[i+window_size])
        else:
            model[window] = [corpus[i+window_size]]

    return model

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
    model = person_dict["model"]
    terminate_chars = ["]"]

    first_word = np.random.choice(corpus)

    while not "[" in first_word:
        first_word = np.random.choice(corpus)

    chain = [first_word]

    n_words = np.floor(np.random.normal(10, 5))
    generate = True
    while generate:
        new_word = np.random.choice(model[chain[-1]])
        while "[" in new_word:
            new_word = np.random.choice(model[chain[-1]])
        if "]" in new_word:
            generate = False
        chain.append(new_word)

    return ' '.join(chain)


def generate_dialogue(person_dict):
    corpus = person_dict["corpus"]
    model = person_dict["model"]
    terminate_chars = [".", "?", "???", ". . . ?", "...", "--", "!"]
    open_punctuation = ["(", ")", "[", "]", "\""]

    # import pdb; pdb.set_trace()
    first_clump = random.choice(model.keys())
    while first_clump[0].islower():
        first_clump = random.choice(model.keys())

    chain = []
    for i in first_clump:
        chain.append(i)

    # n_words = np.floor(np.random.normal(15, 10))
    n_words = np.random.randint(5, 25)
    generate = True
    count = 0
    while generate:
        if not all(word in model[tuple(chain[0-window_size:])] for word in open_punctuation):
            new_clump = random.choice(model[tuple(chain[0-window_size:])])
            while any(word in new_clump for word in open_punctuation):
                new_clump = random.choice(model[tuple(chain[0-window_size:])])


        count += 1
        if any(word in new_clump for word in terminate_chars) and count > n_words:
            generate = False

        chain.append(new_clump)


    return ' '.join(chain)


Amir, Jake, Actions = setup()
interleaving = generate_interleaving()
print(interleaving)

print("AMIR")
for i in range(0,10):
    print(generate_dialogue(Amir))

print("JAKE")
for i in range(0,10):
    print(generate_dialogue(Jake))

# print("ACTION")
# for i in range(0,10):
#     print(generate_action(Actions))
