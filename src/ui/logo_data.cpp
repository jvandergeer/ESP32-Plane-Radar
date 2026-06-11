#include "ui/logo_data.h"

extern "C" {
extern const uint8_t _binary_data_logo_png_start[] asm(
    "_binary_data_data_logo_png_start");
extern const uint8_t _binary_data_logo_png_end[] asm(
    "_binary_data_data_logo_png_end");
}

const uint8_t* logoPngData() {
  return _binary_data_logo_png_start;
}

size_t logoPngDataLen() {
  return static_cast<size_t>(_binary_data_logo_png_end -
                              _binary_data_logo_png_start);
}
