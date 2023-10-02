#pragma once

namespace Example5 {

void method1(void);
void method2(void);

inline void method3(void) {
  int b = 0;
  for (int i = 0; i < 1000; i++) {
    b *= 10;
  }
  (void)b;
}

} // namespace Example5
