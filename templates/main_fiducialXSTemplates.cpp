#include "fiducialXSTemplates.C"
#include <iostream>

using namespace std;


int main(int argc, char* argv[])
{

    cout<<"argc "<<argc<<" argv[11] "<<argv[11]<<endl;

    if (argc != 10 && argc != 11 && argc != 12 && argc != 15)
        return 1;

    if(argc == 10)
        fiducialXSTemplates(argv[1], argv[2], argv[3], argv[4], argv[5], argv[6], argv[7], argv[8], argv[9]);

    if(argc == 11)
        fiducialXSTemplates(argv[1], argv[2], argv[3], argv[4], argv[5], argv[6], argv[7], argv[8], argv[9], argv[10]);

    if(argc == 12)
        fiducialXSTemplates(argv[1], argv[2], argv[3], argv[4], argv[5], argv[6], argv[7], argv[8], argv[9], argv[10], argv[11]);

    if (argc == 15)
        fiducialXSTemplates(argv[1], argv[2], argv[3], argv[4], argv[5], argv[6], argv[7], argv[8], argv[9], argv[10], argv[11], argv[12], argv[13], argv[14]);

    return 0;
}
