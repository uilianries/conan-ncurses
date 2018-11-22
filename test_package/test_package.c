#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <ncurses.h>

#define TRACE() printf("%s:%d\n", __func__, __LINE__)

int main(int argc, char *argv[]) {
    WINDOW* window = NULL;

    printf("ncurses version: %s\n", curses_version());

    TRACE();
    window = initscr();
    TRACE();

    if (window != NULL) {
        TRACE();
        if (start_color() != ERR) {
            TRACE();
            init_pair(1, COLOR_BLACK, COLOR_CYAN);
            init_pair(2, COLOR_BLACK, COLOR_GREEN);
            TRACE();

            attron(COLOR_PAIR(1));
            printw("Conan, the C / C++ Package Manager for Developers\n");
            TRACE();

            attron(COLOR_PAIR(2));
        }
        printw("This is the ncurses Conan package!\n");
        TRACE();
        refresh();
        TRACE();

        sleep(1);

        endwin();
        TRACE();
    }
    return EXIT_SUCCESS;
}