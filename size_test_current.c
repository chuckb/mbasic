#pragma output CLIB_MALLOC_HEAP_SIZE = 512

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Simulate current wasteful approach
char *mb25_to_c_string(const char *s, int len) {
    char *result = malloc(len + 1);
    if (result) {
        memcpy(result, s, len);
        result[len] = '\0';
    }
    return result;
}

int main() {
    char *s = "Hello World";
    char *temp = mb25_to_c_string(s, 11);
    printf("%s\n", temp);
    free(temp);
    return 0;
}
