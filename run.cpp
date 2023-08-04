#include <iostream>

using namespace std;
int main() {
   system("echo $(date) >> log.txt 2>&1");
   system("python3 master_verification.py >> log.txt 2>&1");
   return 0;
}