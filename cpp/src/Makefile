# C++ compiler and flags to use
CXX = g++
CXXFLAGS = -std=c++11 -O3 -mtune=native 

main: main.o graph.o
	$(CXX) $(CXXFLAGS) -o main main.o graph.o

main.o: main.cpp graph.h

graph.o: graph.cpp graph.h

clean:
	rm -f *.o

distclean: clean
	rm -f main