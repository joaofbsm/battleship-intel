#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int main() {
    ifstream f;
    string line;

    f.open("tests/in/pdf1.in");
    while (getline(f, line)) {
      cout << line << "\n";
    }
    f.close();

    return 0;
}