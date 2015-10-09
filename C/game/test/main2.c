#include <ncurses.h>
#include <unistd.h>
#define DELAY 300000


int main(int argc, char *argv[]) {
  int x = 0, y = 0;
  int PLAYER = 5;
  

  initscr();
  noecho();
  curs_set(FALSE);
  while(1) {
    clear();             // Clear the screen of all previously-printed characters

    mvprintw(y, x, "%d", PLAYER); // Print our "ball" at the current xy position
    refresh();
    usleep(DELAY);       // Shorter delay between movements


    int dir = getch();
    switch(dir)
    {

        case KEY_UP:
            y--;
            break;
        case KEY_DOWN:
            y++;
            break;
        case KEY_LEFT:
            x--;
            break;
        case KEY_RIGHT:
            x++;
            break;
        default:
            break;


    }


  }
  endwin();
}
