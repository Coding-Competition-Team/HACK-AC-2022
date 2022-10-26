#include <stdio.h>
#include <string.h>

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void win() {
    system("cat flag.txt");
}

int main() {
    char demo[256] = "";
    setup();

    puts("Let's leak the PIE offset first.");
    gets(demo);
    printf(demo);
    puts("");

    puts("How about the canary?");
    gets(demo);
    printf(demo);
    puts("");

    puts("Now you've got everything you need!");
    gets(demo);
    printf(demo);
    puts("");

    puts("Goodbye!");
    return 0;
}
