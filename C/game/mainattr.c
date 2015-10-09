#include <ncurses.h>

int main()
{
  initscr();
  cbreak();
  attron(A_STANDOUT | A_UNDERLINE);
  mvprintw(12,40, "READ THIS NOW");
  attroff(A_STANDOUT | A_UNDERLINE);




  getch();
  endwin();



  return 0;
}
