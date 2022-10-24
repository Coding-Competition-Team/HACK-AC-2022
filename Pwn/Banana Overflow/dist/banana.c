# include <stdio.h>

int main() {
    int balance = 1;
    int donate;
    while (balance < 1000000000) {
        puts("Please enter in how much you want to donate (don't worry, money is free!)")
        scanf("%d", &donate);
        if (donate <= 0) {
            puts("Why you so stingy");
            return 0;
        }
        balance -= donate;
        printf("You currently have: $%d\n\n", balance);
    }
    system("cat flag.txt");
}
