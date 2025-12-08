import math
from typing import Tuple


def calculate_optimal_summary_length(text_word_count: int) -> Tuple[int, int, int]:
    COMPRESSION_RATIO = 0.08
    MIN_WORDS = 60
    MAX_WORDS = 180
    MIN_SENTENCES = 5
    MAX_SENTENCES = 12
    MIN_TOKENS = 700
    TOKEN_PER_WORD_RATIO = 1.3

    L_opt = int(text_word_count * COMPRESSION_RATIO)
    L_opt = max(MIN_WORDS, min(L_opt, MAX_WORDS))

    R_opt = math.ceil(L_opt / 15)
    R_opt = max(MIN_SENTENCES, min(R_opt, MAX_SENTENCES))

    T_opt = int(L_opt * TOKEN_PER_WORD_RATIO)
    T_opt = max(T_opt, MIN_TOKENS)

    return R_opt, L_opt, T_opt
