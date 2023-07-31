#include "sample1.h"

void sample1_method(void) {
  int a = 0;
  (void)a;

  for (int i = 0; i < 1000; i++) {
    a *= 2;
  }
}
