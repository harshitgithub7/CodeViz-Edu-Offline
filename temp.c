# Test Code
#include <stdio.h>
int main() {
    int n = 5, i, j, space;
    for(i = 0; i < n; i++) {
        for(space = 0; space < n - i - 1; space++) {
            printf("  ");
        }
        for(j = 0; j < 2 * i + 1; j++) {
            printf("* ");
        }
        printf("\n");
    }
    return 0;
}
