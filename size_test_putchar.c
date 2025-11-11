#include <stdio.h>
void putstr(const char *s, int len) {
    while (len--) putchar(*s++);
}
int main() {
    char *s = "Hello World";
    putstr(s, 11);
    putchar('\n');
    return 0;
}
