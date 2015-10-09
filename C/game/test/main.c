#include <stdlib.h>
#include <ncurses.h>
void drawPlayer(int** theMap);


#define HEIGHT  21
#define WIDTH  41


int main()
{

    unsigned int i, j;
    int** map;

    //dynamically allocate map space
    map = malloc(HEIGHT * sizeof(int*));
    for (i = 0; i < HEIGHT ; i++)
    {
        map[i] = malloc(WIDTH * sizeof(int));
    }

    initscr();
    cbreak();

    //while (1){

    //draw map
    for (i = 0; i < HEIGHT; i++)
    {
        for (j = 0 ; j < WIDTH ; j++)
        {
            mvprintw(i, j, "%d", map[i][j]);
        }
    }




    drawPlayer(map);







    //} // end main loop

    //free map memory
    for (i = 0; i < HEIGHT; i++)
    {
        free(map[i]);
    }
    free(map);




    getch();
    endwin();
    return 0;
}



void drawPlayer(int** theMap)
{

    theMap[HEIGHT / 2][WIDTH / 2] = 5;

}
