/* toolchain */
#include <iostream>

/* third-party */
#include "yambs-sample/example/sample.h"

int test1(int a, int b) { return a + b; }

int main(void) {
  std::cout << test1(1, 2) << std::endl;

  float a = 0.0f;
  for (int i = 0; i < 1000; i++) {
    a *= 2.0f;
    a /= 2.0f;
    std::cout << a << std::endl;
  }

  Example::method1();
  Example::method2();
  Example::method3();

  return 0;
}
