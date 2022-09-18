import hangman_helper

UNDER_LINE = "_"
MAX_LOWER = 123
MIN_LOWER = 96


def update_word_pattern(word, pattern, letter):
    new_pattern = list(pattern)
    word_by_letter = list(word)
    for i in range(len(new_pattern)):
        if word_by_letter[i] == letter:
            new_pattern[i] = letter
    return "".join(new_pattern)


def run_single_game(word_list, scor):
    word = hangman_helper.get_random_word(word_list)
    wrong_list = []
    new_word = UNDER_LINE * len(word)
    msg = "Welcome to Hell"

    while scor > 0 and UNDER_LINE in new_word:
        # show the current stat
        hangman_helper.display_state(new_word, wrong_list, scor, msg)
        output = hangman_helper.get_input()
        if output[0] == 1:
            if len(output[1]) > 1 or (len(output[1]) == 1 and not (MAX_LOWER > ord(output[1]) > MIN_LOWER)):
                msg = "Incorrect feed"

            elif output[1] in wrong_list or output[1] in new_word:
                msg = "You've tried it before"

            else:
                scor = scor - 1
                if output[1] in word:
                    new_word = update_word_pattern(word, new_word, output[1])
                    n = new_word.count(output[1])
                    scor = scor + int((n * (n + 1)) / 2)
                else:
                    wrong_list.append(output[1])

        elif output[0] == 2:
            if output[1] == word:
                n = new_word.count(UNDER_LINE)
                scor = scor + int((n * (n + 1)) / 2) - 1
                new_word = word
            else:
                scor = scor - 1

        elif output[0] == 3:
            scor = scor - 1
            if scor > 0:
                hint = filter_word_list(word_list, new_word, word_list)
                if len(hint) > hangman_helper.HINT_LENGTH:
                    new_hint_list = []
                    for i in range(hangman_helper.HINT_LENGTH):
                        new_hint_list.append((hint[int(i * len(hint) / hangman_helper.HINT_LENGTH)]))
                    hangman_helper.show_suggestions(new_hint_list)
                else:
                    hangman_helper.show_suggestions(hint)
    if scor == 0:
        hangman_helper.display_state(new_word, wrong_list, scor, "you lose. the was: " + word)
    else:
        hangman_helper.display_state(new_word, wrong_list, scor, "you won")

    return scor


def filter_word_list(words, pattern, wrong_guess_lst):
    new_word = []
    i = 0
    for word in words:
        if len(word) == len(pattern):

            for i in range(0, len(word)):
                if word[i] in wrong_guess_lst:
                    break
                if pattern[i] == UNDER_LINE:
                    continue
                if pattern[i] != word[i]:
                    break
            if i == (len(pattern) - 1):
                new_word.append(word)
    return new_word


def main():
    nam_game = 1
    word_list = hangman_helper.load_words()
    scor = run_single_game(word_list, hangman_helper.POINTS_INITIAL)

    if scor == 0:
        msg = " Number of games you have played " + str(nam_game)
    else:
        msg = "You gained points " + str(scor) + " Number of games you have played " + str(nam_game)

    while hangman_helper.play_again(msg):
        if scor > 0:
            scor = run_single_game(word_list, scor)
            nam_game += 1
            msg = "You gained points " + str(scor) + " Number of games you have played " + str(nam_game)
        else:

            scor = run_single_game(word_list, hangman_helper.POINTS_INITIAL)
            nam_game = 1
            msg = " Number of games you have played " + str(nam_game)


if __name__ == '__main__':
    main()
