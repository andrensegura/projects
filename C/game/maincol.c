#include <ncurses.h>

int main()
{
    initscr();
    cbreak();
    start_color();
    init_pair(1,COLOR_RED, COLOR_BLUE);
    attron(COLOR_PAIR(1));
    printw("ahh my eyes");
    attroff(COLOR_PAIR(1));

    getch();
    endwin();
    return 0;
}
