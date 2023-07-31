/* toolchain */
#include <iostream>

/* third-party */
#include "yambs-sample/example/sample.h"
#include "yambs-sample2/example/sample.h"
#include "yambs2/sample.h"

/* internal */
#include "test.h"

int test2(int a, int b) { return a + b; }

int main(void) {
  std::cout << test2(1, 2) << std::endl;

  float a = 0.0f;
  for (int i = 0; i < 2000; i++) {
    a *= 2.0f;
    a /= 2.0f;
    std::cout << a << std::endl;
  }

  Example::method1();
  Example::method2();
  Example::method3();

  Example2::method1();
  Example2::method2();

  Example3::method1();
  Example3::method2();
  Example3::method3();

  Example4::method1();
  Example4::method2();

  return 0;
}
