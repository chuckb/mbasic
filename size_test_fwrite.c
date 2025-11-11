#include <stdio.h>
int main() {
    char *s = "Hello World";
    fwrite(s, 1, 11, stdout);
    fputc('\n', stdout);
    return 0;
}
