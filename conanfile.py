import os
from conans import ConanFile, tools, CMake


class DiligentCoreConan(ConanFile):
    name = "diligent-engine"
    url = "https://github.com/DiligentGraphics//"
    homepage = "https://github.com/DiligentGraphics/"
    description = "Diligent Engine is a modern cross-platfrom low-level graphics API."
    license = ("Apache 2.0")
    topics = ("graphics")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], 
    "fPIC":         [True, False],
    "with_glslang": [True, False],
    }
    default_options = {"shared": False, 
    "fPIC": True,
    "with_glslang" : True
    }
    generators = "cmake_find_package", "cmake"
    exports_sources = ["*", "!build/*", "!conanfile.py", "!doc/*", "!Tests/*", "!.github/*"]
    _cmake = None
    short_paths=True
    version="d72a87fa"

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    #def source(self):
    #    tools.get(**self.conan_data["sources"][self.version], strip_root=True, destination=self._source_subfolder)

    def package_id(self):
        if self.settings.compiler == "Visual Studio":
            if "MD" in self.settings.compiler.runtime:
                self.info.settings.compiler.runtime = "MD/MDd"
            else:
                self.info.settings.compiler.runtime = "MT/MTd"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

    def _patch_sources(self):
        pass
        #for patch in self.conan_data["patches"][self.version]:
        #    tools.patch(**patch)

    def requirements(self):
        self.requires("libjpeg/9d")
        self.requires("libtiff/4.3.0")
        self.requires("zlib/1.2.11")
        self.requires("libpng/1.6.37")

        if self.settings.os in ["Linux", "FreeBSD"]:
            self.requires("xorg/system")
            if not tools.cross_building(self, skip_x64_x86=True):
                self.requires("xkbcommon/1.3.0")        

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.definitions["DILIGENT_BUILD_SAMPLES"] = False
        self._cmake.definitions["DILIGENT_NO_FORMAT_VALIDATION"] = True
        self._cmake.definitions["DILIGENT_BUILD_TESTS"] = False
        self._cmake.definitions["DILIGENT_NO_GLSLANG"] = not self.options.with_glslang
        self._cmake.definitions["ENABLE_RTTI"] = True
        self._cmake.definitions["ENABLE_EXCEPTIONS"] = True
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
        
        #self.copy("*.h", src="ThirdParty/")
        self.copy("*.hpp", src="DiligentCore/ThirdParty/", dst="ThirdParty/")
        self.copy("*.h", src="DiligentCore/ThirdParty/",   dst="ThirdParty/")
        
        self.copy("HLSL2GLSLConverter*", src="DiligentTools/HLSL2GLSLConverter")

    def package_info(self):
        if self.settings.build_type == "Debug":
            self.cpp_info.libdirs.append("lib/DiligentCore/Debug")
            self.cpp_info.libdirs.append("lib/DiligentFX/Debug")
            self.cpp_info.libdirs.append("lib/DiligentTools/Debug")            
        if self.settings.build_type == "Release":
            self.cpp_info.libdirs.append("lib/DiligentCore/Release")
            self.cpp_info.libdirs.append("lib/DiligentFX/Release")
            self.cpp_info.libdirs.append("lib/DiligentTools/Release")
            
            #HLSL2GLSLConverter.exe

        self.cpp_info.includedirs.append('include')
        self.cpp_info.includedirs.append('DiligentCore/ThirdParty')
        self.cpp_info.includedirs.append('DiligentCore/ThirdParty/glslang')

        self.cpp_info.includedirs.append('DiligentCore/ThirdParty/SPIRV-Headers/include/')
        self.cpp_info.includedirs.append('DiligentCore/ThirdParty/SPIRV-Cross/')
        self.cpp_info.includedirs.append('DiligentCore/ThirdParty/SPIRV-Cross/include')
        self.cpp_info.includedirs.append('DiligentCore/ThirdParty/SPIRV-Tools/include')
        self.cpp_info.includedirs.append('DiligentCore/ThirdParty/Vulkan-Headers/include')
        
        self.cpp_info.libs = tools.collect_libs(self)

        self.cpp_info.defines.append("SPIRV_CROSS_NAMESPACE_OVERRIDE=diligent_spirv_cross")
        if self.settings.os in ["Macos", "Linux"]:
            self.cpp_info.system_libs = ["dl", "pthread"]
        if self.settings.os == 'Macos':
            self.cpp_info.frameworks = ["CoreFoundation", 'Cocoa']
