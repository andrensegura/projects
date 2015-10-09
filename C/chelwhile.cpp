#include <iostream>
#include <ctime>
#include <stdlib.h> 
using namespace std;
int main()
{
    srand(static_cast<unsigned int>(time(0)));

    char answer = 'Y';

    while (toupper(answer) == 'Y')
    {                               //#THINGS TO DO BEFORE EACH NEW GAME#
        int num = rand() % 10 + 1;  //#initialize number to guess       #
        int guess = 11;             //#you cant get a num above 10      #
        int count = 0;              //#set counter to zero              #

        while (guess != num)
        {
            count++;

            cout << "Guess a number between 1 and 10: ";
            cin >> guess;
        }

        cout << "It took " << count << " guesses to get the correct answer." << endl;
        cout << "Would you like to play again? (y/n): ";
        cin >> answer;    
    }

    return 0;
}
