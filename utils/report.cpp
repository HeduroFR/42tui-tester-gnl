#include "report.hpp"
#include <cstdlib>
#include <fcntl.h>
#include <unistd.h>

void report_check(char result)
{
    const char *path = getenv("GNL_REPORT_EVENTS");
    if (!path) return;
    int fd = open(path, O_WRONLY | O_APPEND);
    if (fd < 0) _exit(120);
    if (write(fd, &result, 1) != 1) _exit(120);
    close(fd);
}
