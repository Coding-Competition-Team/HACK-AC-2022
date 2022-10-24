#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>

typedef struct choices {
  char choice[9];
} choices;

void sigalrm(int signum) {
  puts("Sorry I gtg, catch up another time!");
  exit(0);
}

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int check(int bot, int user) {
  int state = (15 + bot - user) % 15;
  if (state == 0) {
    return 0;
  } else if (state <= 7) {
    return -1;
  } else if (state > 7) {
    return 1;
  }
}

void win() {
  system("cat flag.txt");
}

int main() {
    setup();
restart: ;
    choices choices[15];
    memcpy(choices[0].choice, "Rock", 9);
    memcpy(choices[1].choice, "Gun", 9);
    memcpy(choices[2].choice, "Lightnig", 9);
    memcpy(choices[3].choice, "Devil", 9);
    memcpy(choices[4].choice, "Dragon", 9);
    memcpy(choices[5].choice, "Water", 9);
    memcpy(choices[6].choice, "Air", 9);
    memcpy(choices[7].choice, "Paper", 9);
    memcpy(choices[8].choice, "Sponge", 9);
    memcpy(choices[9].choice, "Wolf", 9);
    memcpy(choices[10].choice, "Tree", 9);
    memcpy(choices[11].choice, "Human", 9);
    memcpy(choices[12].choice, "Snake", 9);
    memcpy(choices[13].choice, "Scissors", 9);
    memcpy(choices[14].choice, "Fire", 9);

    char inp[8];
    int score = 0;
    int user;
    int bot;
    srand(time(NULL));

    puts("Welcome to RGLDDWAPSWTHSSF!");
    puts("---");
    puts("The design is very human! For example, Sponge beats Gun. \n(refer to the chart you've been given for more details)\n");
    puts("Now that you understand how to play, let's give it a try!");
    puts("Try to beat me!");
    puts("---");
    for (int i = 0; i < 15; i++) {
      printf("%d. %s\n", i+1, choices[i].choice);
    }
    bot = rand() % 15;
    printf("\nI choose %s\n", choices[bot].choice);
    printf("Make a choice: ");
    gets(inp);
    user = atoi(inp) - 1;
    printf("You chose %s\n", choices[user].choice);
    
    if ((user < 0) || (user > 14)) {
      puts("What are you doing? let's try this again.");
      goto restart;
    } 

    switch (check(bot, user)) {
      case 0:
        puts("Tie... let's try this again.");
        goto restart;
        break;
      case -1:
        puts("You lost... let's try this again.");
        goto restart;
        break;
      case 1:
        puts("Well done!");
        break;
      default:
        puts("???");
        break;
    }

    // don't allow slow ppl to win
    signal(SIGALRM, sigalrm);
    alarm(50);

    puts("---");
    puts("Now, let's go for a real match! First to 5!");
    for (int i = 0; i < 5; i++) {
      bot = rand() % 15;
      printf("I choose %s\n", choices[bot].choice);
      gets(inp);
      user = atoi(inp) - 1;
      printf("You chose %s\n", choices[user].choice);
      
      if ((user < 0) || (user > 14)) {
        puts("What are you doing? I don't want to play with you anymore.");
        exit(0);
      } 

      switch (check(bot, user)) {
        case 0:
          puts("Tie");
          break;
        case -1:
          puts("You lost heheheha");
          break;
        case 1:
          puts("Well played!");
          score += 1;
          break;
        default:
          puts("???");
          break;
      }

      puts("---");
    }

    printf("Your score: %d\n", score);
    if (score < 5) {
      puts("You didn't get a score of 5... restarting.");
      alarm(0);
      goto restart;
    } else {
      puts("ggwp");
    }
    return 0;
}
