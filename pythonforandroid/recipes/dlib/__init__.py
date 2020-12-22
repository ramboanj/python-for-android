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
    depends = ['python3','numpy','boost','cmake']

    built_libraries = {"*.so" : "build/lib.dlib"}


    

    def get_recipe_env(self, arch):
        env = super(DlibRecipe, self).get_recipe_env(arch)
        
        env['ANDROID_NDK'] = self.ctx.ndk_dir
        env['ANDROID_SDK'] = self.ctx.sdk_dir
        #     import os
        #     for ls in os.environ:
        #         self.env[ls] = os.environ[ls]
        #     pyConfig=sh.Command("python3-config")
        #     #Make true python binding
        #     ldflags= pyConfig("--ldflags")
        #     cflags= pyConfig("--cflags")
        #     include= pyConfig("--includes")
        #     self.env['LDFLAGS'] += str(ldflags)
        #     self.env['CFLAGS'] += str(cflags)
        #     self.env['PYTHON_INCLUDE_DIRS'] = str(include)
        #     info("Iniitiate environnement")
        return env

    def prebuild_arch(self, arch):
        info("Try to add env")
        info(str(self.get_recipe_env(arch)));
        info(str(self.ctx.python_recipe))

    def build_arch(self, arch):
        build_dir = join(self.get_build_dir(arch.arch), 'build')
        shprint(sh.mkdir, '-p', build_dir)
        with current_directory(build_dir):
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
                #Create a libçdir to put building 
            lib_dir = join(build_dir,"lib.dlib")

            info("Create "+lib_dir)                                                   
            shprint(sh.mkdir, '-p', lib_dir)
            
            
            
            newArgs=[                                                                    
 #                    "-D P4A=ON" ,                                                        
#                     "-D ANDROID_ABI={}".format(arch.arch),                               
#                     "-D ANDROID_STANDALONE_TOOLCHAIN={}".format(self.ctx.ndk_dir),       
#                     "-D ANDROID_NATIVE_API_LEVEL={}".format(self.ctx.ndk_api),           
#                     "-D ANDROID_EXECUTABLE={}/tools/android".format(env["ANDROID_SDK"]), 
#                      "-D CMAKE_TOOLCHAIN_FILE={}".format(                                 
#                         join(self.ctx.ndk_dir, "build", "cmake",                         
#                              "android.toolchain.cmake")),                                
 #                    # Make the linkage with our python library, otherwise we             
 #                    # will get dlopen error when trying to import dlib"s module.         
#                      "-D CMAKE_SHARED_LINKER_FLAGS=-L{path} -lpython{version}".format(   
#                          path=python_link_root,                                          
#                          version=python_link_version),                                   
                                                                                         
#                     "-D BUILD_WITH_STANDALONE_TOOLCHAIN=ON",                             
 #                    # Force to build as shared libraries the dlib"s dependant            
 #                    # libs or we will not be able to link with our python                
                      "-D BUILD_SHARED_LIBS=ON",                                           
                      "-D BUILD_STATIC_LIBS=OFF",                                          
 #                    "-D LLVM_LIBDIR_SUFFIX=64",
 #                    # Disable some dlib"s features                                       
 #                    "-D BUILD_dlib_java=OFF",                                            
 #                    "-D BUILD_dlib_java_bindings_generator=OFF",                         
 #                    # "-D BUILD_dlib_highgui=OFF",                                       
 #                    # "-D BUILD_dlib_imgproc=OFF",                                       
 #                    # "-D BUILD_dlib_flann=OFF",                                         
                      "-D BUILD_TESTS=OFF",                                                
 #                    "-D BUILD_PERF_TESTS=OFF",                                           
 #                    "-D ENABLE_TESTING=OFF",                                             
 #                    "-D BUILD_EXAMPLES=OFF",                                             
 #                    "-D BUILD_ANDROID_EXAMPLES=OFF",                                     
 #                    "-D BUILD_ANDROID_EXAMPLES=OFF",                                     
 #                    # Create sub-directory into build to ouput it                        
                      "-D CMAKE_LIBRARY_OUTPUT_DIRECTORY={output}".format(output=lib_dir),
            #         "-D CMAKE_LIBRARY_OUTPUT_NAME=libdlib",
 #                    # Force to only build our version of python                          
 #                    "-D BUILD_DLIB_PYTHON=ON".format(major=python_major),                
 #                    "-D BUILD_DLIB_PYTHON=OFF".format(                                   
 #                        major="2" if python_major == "3" else "3"),                      
                                                                                         
 #                    # Force to install the `dlib.so` library directly into               
 #                    # python"s site packages (otherwise the dlib"s loader fails          
 #                    # on finding the dlib.so library)                                    
 #                    "-D DLIB_SKIP_PYTHON_LOADER=OFF",                                    
                     "-D DLIB_PYTHON_INSTALL_PATH={site_packages}".format(                
                          site_packages=python_site_packages),                            
                                                                                         
                    # Define python"s paths for: exe, lib, includes, numpy...            
                    "-D PYTHON_DEFAULT_EXECUTABLE={}".format(self.ctx.hostpython),       
                    "-D PYTHON_EXECUTABLE={host_python}".format(                         
                         host_python=self.ctx.hostpython),                               
                    "-D PYTHON_INCLUDE_DIRS={include_path}".format(                      
                         include_path=python_include_root),                              
                    "-D PYTHON_LIBRARIES={python_lib}".format(                             
                         python_lib=python_library),                                     
                    "-D PYTHON_NUMPY_INCLUDE_DIRS={numpy_include}".format(               
                         numpy_include=python_include_numpy),                            
                    "-D PYTHON_PACKAGES_PATH={site_packages}".format(                    
                         site_packages=python_site_packages)]                            


#            buildTemp="--build-temp={output}".format(output=lib_dir)
            
#            self.setup_extra_args.append(buildTemp)                                                                                 
            for arg in newArgs:                                                          
                info(arg)                                                                
                setArg=arg.split(" ")[1]                                                 
                self.setup_extra_args.append("--set")                                    
                self.setup_extra_args.append(setArg)                                     
                                                                                         

            super().build_arch(arch)
            sh.cp('-a', sh.glob('{}/*.so'.format(lib_dir))  ,self.ctx.get_libs_dir(arch.arch))     
            self.setup_extra_args.clear()#After finished compiled ,remove all setup
            
recipe = DlibRecipe()
