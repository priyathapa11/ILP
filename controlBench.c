#include <stdio.h>

int main() {
    int x = 0;
    for (int i = 0; i < 100000; i++) {
        if (i % 2 == 0)
            x += i;
        else
            x -= i;
    }
    printf("Final: %d\n", x);
    return 0;
}
