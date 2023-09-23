from typing import List

for i in range(100):
    print('hello world')


def longestPalindrome(s: str) -> list[str]:
    for i in range(0, len(s)):
        new_word = []
        for j in range(len(s)-1, 1, -1):
            if s[i] == s[j]:
                new_word.append(s[i:j])
                print(new_word)

print(longestPalindrome('bababdjc'))

