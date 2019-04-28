#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <tuple>
#include <vector>

using namespace std;

int main(int argc, char *argv[]) {
    ifstream f;
    string line;
    int n_combat_posts, n_possible_teleports;
    f.open(argv[1]);

    getline(f, line);
    istringstream iss(line);
    iss >> n_combat_posts >> n_possible_teleports;

    vector< vector<int> > possible_teleports(n_possible_teleports, vector<int>(2));
    vector< vector<int> > combat_posts_state(n_combat_posts, vector<int>(2));

    int m=0, n=0;

    while (getline(f, line) and m < n_possible_teleports) {
      int a, b;
      istringstream iss(line);
      if (!(iss >> a >> b)) { 
        cout << "Error parsing input file.";
      }
      possible_teleports[m][0] = a;
      possible_teleports[m][1] = b;
      cout << possible_teleports[m][0] << " " << possible_teleports[m][1] << "\n";
      m++;
    }
    f.close();

    return 0;
}