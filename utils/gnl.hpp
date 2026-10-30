#ifndef GNL_HPP
# define GNL_HPP
# include "leaks.hpp"
# include "report.hpp"

//Don't do that at home
#define TEST(x) { \
    int status = 0; \
    int test = fork(); \
    if (test == 0) { \
        x showLeaks(); \
        cout << FG_DEFAULT; \
        exit(EXIT_SUCCESS); \
    } else if (test < 0) { \
        report_check('E'); \
    } else { \
        int nb_sleep = 0; \
        const int usleep_time = TIMEOUT_US / 100; \
        int waited; \
        while ((waited = waitpid(test, &status, WNOHANG)) == 0 && nb_sleep * usleep_time <= TIMEOUT_US) { \
            usleep(usleep_time); \
            nb_sleep++; \
        } \
        if (waited == 0) { \
            kill(test, 9); \
            waitpid(test, &status, 0); \
            cout << FG_RED << "TIMEOUT" << FG_DEFAULT; \
            report_check('E'); \
        } else if (waited < 0 || !WIFEXITED(status) || WEXITSTATUS(status) != 0) { \
            report_check('E'); \
        } \
    } \
}

void gnl(int fd, char const * s);

#endif