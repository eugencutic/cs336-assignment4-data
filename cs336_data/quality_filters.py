from nltk.tokenize import word_tokenize

class QualityFilters:
    @staticmethod
    def gopher_filter(text: str) -> bool:
        valid = True

        words = word_tokenize(text)
        lines = text.splitlines()
    
        valid = valid and 50 < len(words) < 100000

        mean_word_length = sum(len(word) for word in words) / len(words)
        valid = valid and 3 < mean_word_length < 10

        end_in_ellipsis_count = sum(1 for line in lines if line.endswith("..."))
        percentage_end_in_ellipsis = end_in_ellipsis_count / len(lines)
        valid = valid and percentage_end_in_ellipsis < 0.3

        has_alphabetic_character_word_count = sum(1 for word in words if any(char.isalpha() for char in word))
        percentage_has_alphabetic_character = has_alphabetic_character_word_count / len(words)
        valid = valid and percentage_has_alphabetic_character > 0.8

        return valid