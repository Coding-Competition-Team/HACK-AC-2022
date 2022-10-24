# include <stdio.h>

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int main() {
    int balance = 1;
    int donate;
    setup();
    while (balance < 1000000000) {
        puts("Please enter in how much you want to donate (what happens if you donate a large sum of money?)");
        scanf("%d", &donate);
        if (donate < 0) {
            puts("Why you so stingy, you can't donate less than 0");
            return 0;
        }
        balance -= donate;
        printf("You currently have: $%d\n\n", balance);
    }
    puts("Well done! An integer is -2^31 < x < 2^31 - 1, or -2147483638 < x < 2147483637, if you overflow that, it'll go back from the other end of the range!");
    system("cat flag.txt");
}
