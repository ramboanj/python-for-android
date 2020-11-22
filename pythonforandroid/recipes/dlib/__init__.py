from pythonforandroid.recipe import CppCompiledComponentsPythonRecipe
import sh
from os.path import join
from multiprocessing import cpu_count
from pythonforandroid.logger import shprint
from pythonforandroid.util import current_directory

from pythonforandroid.logger import (logger, info, warning, debug, shprint, info_main)


class DlibRecipe(CppCompiledComponentsPythonRecipe):
    site_packages_name = 'dlib'
    version = '19.17'
    url = 'http://dlib.net/files/dlib-{version}.zip'
    depends = ['python3','cmake','setuptools','numpy','clang']
    setup_extra_args = []

    
    def get_lib_dir(self, arch):
        return join(self.get_build_dir(arch.arch), 'build', 'lib', arch.arch)

    def get_recipe_env(self, arch):
        env = super(DlibRecipe, self).get_recipe_env(arch)
        env['ANDROID_NDK'] = self.ctx.ndk_dir
        env['ANDROID_SDK'] = self.ctx.sdk_dir
        
        return env

    def prebuild_arch(self, arch):
        print("Build dlib with")
        print(self.get_recipe_env(arch))
    def build_arch(self, arch):

        env = self.get_recipe_env(arch)
        python_major = self.ctx.python_recipe.version[0]
        python_include_root = self.ctx.python_recipe.include_root(arch.arch)
        python_site_packages = self.ctx.get_site_packages_dir()
        python_link_root = self.ctx.python_recipe.link_root(arch.arch)
        python_link_version = self.ctx.python_recipe.major_minor_version_string
        if 'python3' in self.ctx.python_recipe.name:
            python_link_version += 'm'
        python_library = join(python_link_root,
                              'libpython{}.so'.format(python_link_version))
        python_include_numpy = join(python_site_packages,
                                'numpy', 'core', 'include')
        python_include_opencv = join(python_site_packages,
                                    'opencv', 'core', 'include')
        newArgs=[
                "--set ANDROID_ABI={}".format(arch.arch),
                 "--set ANDROID_STANDALONE_TOOLCHAIN={}".format(self.ctx.ndk_dir),
                 "--set ANDROID_NATIVE_API_LEVEL={}".format(self.ctx.ndk_api),
                 "--set ANDROID_EXECUTABLE={}/tools/android".format(env["ANDROID_SDK"]),
                 "--set CMAKE_TOOLCHAIN_FILE={}".format(
                     join(self.ctx.ndk_dir, "build", "cmake",
                          "android.toolchain.cmake")),
                 # Make the linkage with our python library, otherwise we
                 # will get dlopen error when trying to import dlib"s module.
                 "--set CMAKE_SHARED_LINKER_FLAGS=-L{path} -lpython{version}".format(
                     path=python_link_root,
                     version=python_link_version),
                 
                 "--set BUILD_WITH_STANDALONE_TOOLCHAIN=ON",
                 # Force to build as shared libraries the dlib"s dependant
                 # libs or we will not be able to link with our python
                 "--set BUILD_SHARED_LIBS=OFF",
                 "--set BUILD_STATIC_LIBS=ON",
#        "--set Python_USE_STATIC_LIBS=TRUE"
                 
                 # Disable some dlib"s features
                 "--set BUILD_dlib_java=OFF",
                 "--set BUILD_dlib_java_bindings_generator=OFF",
                  "--set BUILD_dlib_highgui=OFF",
                  "--set BUILD_dlib_imgproc=OFF",
                  "--set BUILD_dlib_flann=OFF",
                 "--set BUILD_TESTS=OFF",
                 "--set BUILD_PERF_TESTS=OFF",
                 "--set ENABLE_TESTING=OFF",
                 "--set BUILD_EXAMPLES=OFF",
                 "--set BUILD_ANDROID_EXAMPLES=OFF",
                 "--set BUILD_ANDROID_EXAMPLES=OFF",

                 # Force to install the `dlib.so` library directly into
                 # python"s site packages (otherwise the dlib"s loader fails
                 # on finding the dlib.so library)
                 "--set DLIB_SKIP_PYTHON_LOADER=OFF",
                 "--set DLIB_PYTHON_INSTALL_PATH={site_packages}".format(
                      site_packages=python_site_packages),

                 # Define python"s paths for: exe, lib, includes, numpy...
                 "--set PYTHON_DEFAULT_EXECUTABLE={}".format(self.ctx.hostpython),
                 "--set PYTHON_EXECUTABLE={host_python}".format(
                      host_python=self.ctx.hostpython),
                 "--set PYTHON_INCLUDE_DIRS={include_path}".format(
                      include_path=python_include_root),
                "--set PYTHON_LIBRARY={python_lib}".format(
                     python_lib=python_library),
                "--set PYTHON_NUMPY_INCLUDE_DIRS={numpy_include}".format(
                     numpy_include=python_include_numpy),
                 "--set PYTHON_PACKAGES_PATH={site_packages}".format(

                      site_packages=python_site_packages)]
        for arg in newArgs:
            info(arg)
            setArg=arg.split(" ")[1]
            self.setup_extra_args.append("--set")
            self.setup_extra_args.append(setArg)

            
        super().build_arch(arch)


recipe = DlibRecipe()
