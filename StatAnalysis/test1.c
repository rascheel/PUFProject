#include "gdef.h"
#include "swrite.h"
#include "bbattery.h"

int main (void)
{
    swrite_Basic = FALSE;
    bbattery_RabbitFile ("/home/rascheel/git/PUFProject/OutputGenerated/Strat1/resp1Bin", 3500);
    return 0;
}
