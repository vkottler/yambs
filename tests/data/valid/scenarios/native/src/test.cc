#include "test.h"

/* third-party */
#include "yambs-sample/example/sample.h"
#include "yambs-sample2/example/sample.h"
#include "yambs2/sample.h"
#include "yambs3/sample2.h"

namespace Example4 {

void method1(void) {
  Example::method1();
  Example::method2();
  Example::method3();

  Example2::method1();
  Example2::method2();

  Example3::method1();
  Example3::method2();
  Example3::method3();
}

void method2(void) {
  Example::method1();
  Example::method2();
  Example::method3();

  Example2::method1();
  Example2::method2();

  Example3::method1();
  Example3::method2();
  Example3::method3();

  Example5::method1();
  Example5::method2();
  Example5::method3();
}

} // namespace Example4
