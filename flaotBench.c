#include <stdio.h>
#include <math.h>

int main() {
    double result = 0.0;
    for (int i = 1; i < 100000; i++) {
        result += sqrt(i) * sin(i) - log(i);
    }
    printf("Result: %f\n", result);
    return 0;
}

