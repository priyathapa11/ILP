#include <stdio.h>
#include <stdlib.h>

int main() {
    int size = 100000;
    int *arr = malloc(sizeof(int) * size);
    for (int i = 0; i < size; i++) arr[i] = i;
    long sum = 0;
    for (int i = 0; i < size; i++) sum += arr[i];
    printf("Sum: %ld\n", sum);
    free(arr);
    return 0;
}
