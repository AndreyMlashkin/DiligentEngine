#include <iostream>
#include <vulkan/vulkan.h>
#include <glslang/SPIRV/GlslangToSpv.h>
#include <spirv-tools/optimizer.hpp>

int main(int argc, char *argv[])
{
  std::vector<unsigned int> spirv;
  spv::SpvBuildLogger logger;
  std::cout << "messages count: " << logger.getAllMessages() << std::endl;

  return 0;
}
