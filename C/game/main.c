#include <stdio.h>
#include <ncurses.h>
 
int main()
{
  initscr();
  cbreak();
  int derp = 4;
  printw("This is bog standard string output %d", derp);
  addch('a');
  move(12,13);

  mvprintw(15,20,"Movement");
  mvaddch(12,50,'@');

  getch();
  endwin();

  return 0;
}
