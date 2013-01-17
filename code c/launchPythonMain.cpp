#include <stdlib.h>
int main ()
{
    // Change the name of the file
    // Change the value main.py to the name of the file you want to launch
    // build and put the .exe in the folder next to the .py file
    // Then you can run command such as 'mpiexec -n 5 launchPythonMain.exe'
    system ("main.py");
    return 0;
}
