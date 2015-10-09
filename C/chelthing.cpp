#include <iostream>
#include <string>

using namespace std;

int main()
{
    string choose = "yes";

    while (choose == "yes")
    {

        string name, badName = "andre";

    cout << "what's your name? ";
    cin >> name;

        if (name == badName)
        {
            string choice;
            cout << "What a shit name, are you sure you don't just want to change it to shithead? " << endl;
            cin >> choice;

            if (choice == "no")
            {
                cout << "Well let's just try it! Hello shithead, doesn't that feel better?\nAlmost impowering. Amazing how a name can make so much of a change inside of yourself!\nIt really suits you, if you ask me." << endl;
            }
            else
            {
                cout << "That's too bad... I think I much preferred shithead. Hmm, oh well.\nSome people just have shit taste, huh?"
                    << endl;
            }
        }
        else
        {
            cout << name << " is such a lovely name!!! Much better than " << badName << ".\nCould you imagine? Ha ha. Man, what a shit name. Whew, teared up a little. I'm okay now." << endl;
        }

        cout << "Want to enter another name? ";
        cin >> choose;
    }

    return 0;
}
