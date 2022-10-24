/* frozen.c */
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>

#define buffer 0x18

void arendelle() {
    printf("The crew reaches the castle gates just in time.\n");
    printf("\"When we're together, I'll forever feel at home,\"\n");
    printf("\"And when we're together, we'll be safe and warm;\"\n");
    printf("We all need warm hugs sometimes\n");
    system("/bin/sh");
}

void timeout(int signum) {
    printf("Standing, frozen, in the choice you've chosen,\n");
    printf("Kristoff, cradling, Anna, fading");
    exit(-1);
}

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    signal(SIGALRM, timeout);
    alarm(60);
}

int main() {
    //initialisation
    setup();
    //begin
    char path[buffer];
    printf("Kristoff arrives at a signpost that points in different directions.\n");
    printf("[ Straight ahead | %p ]\n", (main+151));
    printf("[ Arendelle | %p ]\n", (arendelle));
    printf("Many paths lie ahead, but which path will be the Return to Arendelle?\n");
    gets(path);
    printf("Returning home... %p\n", *((long*)(path + buffer + 16)));
    return 0;
}
