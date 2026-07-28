// Copyright 2015 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#include <cassert>
#include <cstddef>
#include <cstdint>

#include <functional>
#include <limits>
#include <string>

#include "libxml/parser.h"
#include "libxml/xmlsave.h"

void ignore (void* ctx, const char* msg, ...) {
  // Error handler to avoid spam of error messages from libxml parser.
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size) {
  xmlSetGenericErrorFunc(NULL, &ignore);

  // Test default empty options value and one random combination of flags.
  const std::string data_string(reinterpret_cast<const char*>(data), size);
  const std::size_t data_hash = std::hash<std::string>()(data_string);
  const int max_option_value = std::numeric_limits<int>::max();
  // Disable XML_PARSE_HUGE to avoid stack overflow.  http://crbug.com/738947.
  const int random_option = data_hash & max_option_value & ~XML_PARSE_HUGE;
  const int options[] = {0, random_option};

  for (const auto option_value : options) {
    if (auto doc = xmlReadMemory(data_string.c_str(), data_string.length(),
                                 "noname.xml", NULL, option_value)) {
      auto buffer = xmlBufferCreate();
      assert(buffer);

      auto context = xmlSaveToBuffer(buffer, NULL, 0);
      xmlSaveDoc(context, doc);
      xmlSaveClose(context);
      xmlFreeDoc(doc);
      xmlBufferFree(buffer);
    }
  }

  return 0;
}

// ---------------------------------------------------------------------------
// Standalone driver (not part of the upstream fuzzer). Reads a single input
// file given on the command line and feeds it to LLVMFuzzerTestOneInput once,
// so the binary can run under AFL (@@), replay, and coverage measurement.
#include <cstdio>
#include <cstdlib>

int main(int argc, char** argv) {
  if (argc < 2) {
    fprintf(stderr, "Usage: %s <input_file>\n", argv[0]);
    return 1;
  }

  FILE* file = fopen(argv[1], "rb");
  if (!file) {
    perror("fopen");
    return 1;
  }

  fseek(file, 0, SEEK_END);
  size_t size = ftell(file);
  rewind(file);

  uint8_t* data = static_cast<uint8_t*>(malloc(size));
  if (!data) {
    perror("malloc");
    fclose(file);
    return 1;
  }

  if (fread(data, 1, size, file) != size) {
    perror("fread");
    fclose(file);
    free(data);
    return 1;
  }
  fclose(file);

  int result = LLVMFuzzerTestOneInput(data, size);
  free(data);
  return result;
}
