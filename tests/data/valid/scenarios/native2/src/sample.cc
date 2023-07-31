#include "sample.h"

/* third-party */
#include "yambs-sample/example/sample.h"
#include "yambs-sample2/example/sample.h"

namespace Example3 {

static void method4(void) {
  int a = 0;
  for (int i = 0; i < 1000; i++) {
    a *= 2;
  }

  (void)a;
}

void method1(void) {
  int a = 0;
  for (int i = 0; i < 1000; i++) {
    a *= 2;
  }
  method4();
  (void)a;

  Example::method1();
  Example2::method1();

  Example::method3();
}

void method2(void) {
  int a = 0;
  for (int i = 0; i < 1000; i++) {
    a *= 2;
  }
  method4();
  (void)a;

  Example::method2();
  Example2::method2();

  Example::method3();
}

} // namespace Example3
