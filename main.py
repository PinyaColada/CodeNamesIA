import gensim
import nltk
from gensim.models import KeyedVectors
from itertools import combinations
import numpy as np
from nltk.stem import WordNetLemmatizer

# The download for the models are
# nltk.download('wordnet')
# glove_model = gensim.downloader.api.load("glove-wiki-gigaword-300")


class GloveWrapper:
    def __init__(self, model_path):
        self.model = KeyedVectors.load(model_path)
        self.stemmer = WordNetLemmatizer()

    def closer_to(self, word_list, prohibited_list=None):
        # Compute the average vector of the words in the list
        if prohibited_list is None:
            prohibited_list = []
        vecs = np.array([self.model[word] for word in word_list])
        average_vec = np.mean(vecs, axis=0)

        # Find words that are closest to the average vector
        similar_words = self.model.similar_by_vector(average_vec, topn=(len(word_list) + 10))
        for candidate, prob in similar_words:
            # Skip if the word is in the prohibited_list or if it is in the word_list
            candidate = self.stemmer.lemmatize(candidate)
            if candidate not in prohibited_list and candidate not in word_list:
                return candidate, prob

        # In case all similar words are prohibited or are in word_list
        return None, None

    def word_to_vec(self, word):
        # Convert a word to a vector
        return self.model[word]

    def compare_words(self, word_a, word_b):
        # Compute the similarity between two words
        return self.model.similarity(word_a, word_b)


class HeadmasterCodeName:
    def __init__(self, blue_words, red_words, neutral_words, spy, turn, glove_model_path):
        self.winner = None
        self.turn = turn
        self.blue_words = blue_words
        self.red_words = red_words
        self.neutral_words = neutral_words
        self.spy = spy
        self.glove_wrapper = GloveWrapper(glove_model_path)

    def remove_card(self, card_name):
        if card_name in self.blue_words:
            self.blue_words.remove(card_name)
        elif card_name in self.red_words:
            self.red_words.remove(card_name)
        elif card_name in self.neutral_words:
            self.neutral_words.remove(card_name)
        elif card_name == self.spy:
            self.spy = None
            self.winner = not self.turn

    def get_outcome(self, display=False):
        if self.winner is not None:  # If the spy has been flipped
            return self.winner
        if not self.blue_words:  # If there is no blue words the blue has won
            self.winner = True
            if display:
                print("The winner is the blue team!")
        if not self.red_words:  # If there is no red words the red won
            self.winner = False
            print("The winner is the red team!")
        return self.winner

    def start_loop(self, red_player_is_ia=True, blue_player_is_ia=True, display=False):
        while self.get_outcome(display=display) is None:
            hint, number = game.find_word(display=display)
            game.apply_action(hint, number, display=display)
            input("Press enter to show the next hint: ")

    def find_word(self, display=False):
        team_words = self.blue_words if self.turn else self.red_words
        all_words = self.blue_words + self.red_words + self.neutral_words + self.spy

        candidate_words = []
        for r in range(len(team_words), 0, -1):
            for combo in combinations(team_words, r):
                candidate_word, _ = self.glove_wrapper.closer_to(list(combo), prohibited_list=all_words)
                candidate_words.append(candidate_word)

        # Evaluate each candidate word
        max_reward = -float('inf')
        best_hint_length = 0
        best_word = None
        for candidate_word in candidate_words:
            reward, hint_length = self.reward_word(candidate_word)
            if reward > max_reward or (reward == max_reward and hint_length < best_hint_length):
                max_reward = reward
                best_hint_length = hint_length
                best_word = candidate_word

        if display:
            print(f"The hint is: {best_word}, {best_hint_length}")
        return best_word, best_hint_length

    def reward_word(self, word):
        all_words = self.blue_words + self.red_words + self.neutral_words + self.spy

        similarities = [(w, self.glove_wrapper.compare_words(word, w)) for w in all_words]

        sorted_similarities = sorted(similarities, key=lambda x: x[1], reverse=True)

        reward = 0
        hint_length = 0
        for w, _ in sorted_similarities:
            hint_length += 1

            if self.turn:
                if w in self.blue_words:
                    reward += 1
                elif w in self.red_words or w == self.spy or self.neutral_words:
                    break
            else:
                if w in self.red_words:
                    reward += 1
                elif w in self.blue_words or w == self.spy or self.neutral_words:
                    break

        return reward, hint_length - 1

    def apply_action(self, action, action_length, display=False):
        # Combine all words
        all_words = self.blue_words + self.red_words + self.neutral_words + self.spy

        # Calculate similarity scores
        similarities = [(w, self.glove_wrapper.compare_words(action, w)) for w in all_words]

        # Sort words based on similarity
        sorted_similarities = sorted(similarities, key=lambda x: x[1], reverse=True)

        # Flip cards according to hint_length
        for i in range(action_length):
            if i < len(sorted_similarities):
                card_to_flip = sorted_similarities[i][0]
                self.remove_card(card_to_flip)
                if display:
                    print(f"The card '{card_to_flip}' has been flipped.")

        # self.turn = not self.turn


# Example usage
# Example usage
if __name__ == "__main__":
    # Example words
    neutral_words = ["cabin", "iron", "snail", "port", "cat", "water", "day"]
    blue_words = ["area", "snow", "war", "pooper", "life", "frequency", "hollywood", "goal", "witch"]
    red_words = ["cliff", "death", "pound", "radius", "circle", "dog", "class", "atlantis"]
    spy = ["ambulance"]

    # Load GloVe model
    glove_model_path = 'models/glove_big_model.kv'

    # Create a HeadmasterCodeName game
    game = HeadmasterCodeName(blue_words, red_words, neutral_words, spy, True, glove_model_path)
    game.start_loop(display=True)


