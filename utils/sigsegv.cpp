#include "sigsegv.hpp"
#include "color.hpp"
#include <unistd.h>

extern int iTest;

void sigsegv(int signal)
{
	(void)signal;
	cout << FG_LYELLOW << iTest++ << ".SIGSEGV" << ENDL;
	_exit(128 + signal);
}
