#include <stdio.h>

int main() {
    int a = 0;
    for (int i = 0; i < 100000; i++) {
        a += i * 2 - i / 3;
    }
    printf("Result: %d\n", a);
    return 0;
}

