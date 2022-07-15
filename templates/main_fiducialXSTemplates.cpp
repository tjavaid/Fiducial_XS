#include "fiducialXSTemplates.C"
#include <iostream>

using namespace std;


int main(int argc, char* argv[])
{

    cout<<"argc "<<argc<<" argv[11] "<<argv[11]<<endl;

    if (argc != 10 && argc != 11 && argc != 12 && argc != 13 && argc != 14 && argc != 15 && argc != 16 && argc != 17  && argc != 18)
    {
        cout << "Exit programs: As it does not have expected number of arguments" << endl;
        return 1;
    }

    if(argc == 10)
        fiducialXSTemplates(argv[1], argv[2], argv[3], argv[4], argv[5], argv[6], argv[7], argv[8], argv[9]);

    if(argc == 11)
        fiducialXSTemplates(argv[1], argv[2], argv[3], argv[4], argv[5], argv[6], argv[7], argv[8], argv[9], argv[10]);

    if(argc == 12){
        cout << "Has 12 arguments..." << endl;
        fiducialXSTemplates(argv[1], argv[2], argv[3], argv[4], argv[5], argv[6], argv[7], argv[8], argv[9], argv[10], argv[11]);
    }

    if(argc == 13){
        fiducialXSTemplates(argv[1], argv[2], argv[3], argv[4], argv[5], argv[6], argv[7], argv[8], argv[9], argv[10], argv[11], std::stoi(argv[12]));
    }

    if(argc == 14){
        fiducialXSTemplates(argv[1], argv[2], argv[3], argv[4], argv[5], argv[6], argv[7], argv[8], argv[9], argv[10], argv[11], std::stoi(argv[12]), (argv[13]));
    }

    if (argc == 15)
        fiducialXSTemplates(argv[1], argv[2], argv[3], argv[4], argv[5], argv[6], argv[7], argv[8], argv[9], argv[10], argv[11], std::stoi(argv[12]), argv[13], argv[14]);

    if (argc == 16)
        fiducialXSTemplates(argv[1], argv[2], argv[3], argv[4], argv[5], argv[6], argv[7], argv[8], argv[9], argv[10], argv[11], std::stoi(argv[12]), argv[13], argv[14], argv[15]);

    if (argc == 17)
        fiducialXSTemplates(argv[1], argv[2], argv[3], argv[4], argv[5], argv[6], argv[7], argv[8], argv[9], argv[10], argv[11], std::stoi(argv[12]), argv[13], argv[14], argv[15], std::stoi(argv[16]));

    if (argc == 18)
        fiducialXSTemplates(argv[1], argv[2], argv[3], argv[4], argv[5], argv[6], argv[7], argv[8], argv[9], argv[10], argv[11], std::stoi(argv[12]), argv[13], argv[14], argv[15],  std::stoi(argv[16]), argv[17]);

    return 0;
}
