function isPalindrome(str) {
    str = str.toLowerCase().replace(/\s+/g, "");
    return str === str.split("").reverse().join("");
}

// Example usage
console.log(isPalindrome("madam"));    // true
console.log(isPalindrome("racecar"));  // true
console.log(isPalindrome("hello"));    // false
