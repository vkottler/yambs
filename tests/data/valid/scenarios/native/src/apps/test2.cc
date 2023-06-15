/* toolchain */
#include <iostream>

int test2(int a, int b) { return a + b; }

int main(void) {
  std::cout << test2(1, 2) << std::endl;

  float a = 0.0f;
  for (int i = 0; i < 2000; i++) {
    a *= 2.0f;
    a /= 2.0f;
    std::cout << a << std::endl;
  }

  return 0;
}
