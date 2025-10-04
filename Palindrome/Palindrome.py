def is_palindrome(s: str) -> bool:
    s = s.lower().replace(" ", "")  # normalize string
    return s == s[::-1]

# Example usage
print(is_palindrome("madam"))      # True
print(is_palindrome("racecar"))    # True
print(is_palindrome("hello"))      # False
