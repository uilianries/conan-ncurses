#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <ncurses.h>

int main(int argc, char *argv[]) {
    initscr();
    start_color();

    init_pair(1, COLOR_BLACK, COLOR_CYAN);
    init_pair(2, COLOR_BLACK, COLOR_GREEN);

    attron(COLOR_PAIR(1));
    printw("Conan, the C / C++ Package Manager for Developers\n");

    attron(COLOR_PAIR(2));
    printw("This is the ncurses Conan package!\n");
    refresh();

    sleep(1);

    endwin();
}