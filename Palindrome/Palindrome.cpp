#include <iostream>
#include <algorithm>
#include <string>
using namespace std;

bool isPalindrome(string str) {
    transform(str.begin(), str.end(), str.begin(), ::tolower);
    str.erase(remove(str.begin(), str.end(), ' '), str.end());
    
    string rev = str;
    reverse(rev.begin(), rev.end());
    return str == rev;
}

int main() {
    cout << boolalpha;
    cout << isPalindrome("madam") << endl;    // true
    cout << isPalindrome("racecar") << endl;  // true
    cout << isPalindrome("hello") << endl;    // false
    return 0;
}
