##LD_LIBRARY_PATH=$(LD_LIBRARY_PATH)
CXXFLAGS= -std=c++0x -fpermissive -pedantic -Wunused-variable -Werror=sign-compare -Wunused-but-set-variable -Werror=return-type -Werror=missing-braces -fPIC -O

ROOTLIB=$(ROOTSYS)/lib
ROOTINCLUDES=$(ROOTSYS)/include

target=main_fiducialXSTemplates

all: $(target)

$(target):
	$(CXX) $(CXXFLAGS) `$(ROOTSYS)/bin/root-config --ldflags` \
	-I $(ROOTINCLUDES) $(target).cpp -o $(target) -L. $(LIBFLAGS) -L $(ROOTLIB) \
	`$(ROOTSYS)/bin/root-config --libs --glibs`
