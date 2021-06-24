from conans import ConanFile, CMake, tools
from conans.model.version import Version
import os, getpass

class DiligentCoreConan(ConanFile):
    name = "diligent-engine"
    version="2.5"
    exports_sources = "*"

    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "cmake_find_package", "cmake"
    
    topics = ("conan", "gpu", "gui")
    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

    def _patch_sources(self):
        for patch in self.conan_data["patches"][self.version]:
            tools.patch(**patch)

    def requirements(self):
        #self.requires("spirv-tools/2019.2")
        #self.requires("spirv-cross/20200403")
        #self.requires("glslang/8.13.3559")
        
        self.requires("vulkan-memory-allocator/2.3.0")
        self.requires("vulkan-loader/1.2.172")
        self.requires("vulkan-headers/1.2.172")
        
        self.requires("glew/2.2.0")
        self.requires("stb/20200203")
        self.requires("volk/1.2.170")

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.definitions["DILIGENT_BUILD_SAMPLES"] = False
        self._cmake.definitions["DILIGENT_NO_FORMAT_VALIDATION"] = True
        return self._cmake

    def build(self):
        #self._patch_sources()
        cmake = self._configure_cmake()
        cmake.configure(build_folder=self._build_subfolder)
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        self.copy("License.txt", dst="licenses", src=self._source_subfolder)

    def package_info(self):
        self.cpp_info.libs.append("DiligentCore")

