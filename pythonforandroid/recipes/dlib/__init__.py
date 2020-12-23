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
    depends = ['python3','numpy','scipy','opencv']

#    built_libraries = {"*.so" : "build/lib.dlib"}


    

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
            lib_dir = join(build_dir,"lib")

            info("Create "+lib_dir)                                                   
            shprint(sh.mkdir, '-p', lib_dir)
            info("Code = cmake {python} -B {output}".format(output=lib_dir,python=join(self.get_build_dir(arch.arch), 'tools/python')))
            shprint(sh.cmake,                        
                   # execute CMake in Tools/Python to build

                    '{python}'.format(python=join(self.get_build_dir(arch.arch), 'tools/python')),
                    #install on tmp
                    '-B{output}'.format(output=lib_dir),
                    
                    '-DP4A=ON' ,                                                                   
                    '-DANDROID_ABI={}'.format(arch.arch),                                          
                    '-DANDROID_STANDALONE_TOOLCHAIN={}'.format(self.ctx.ndk_dir),                  
                    '-DANDROID_NATIVE_API_LEVEL={}'.format(self.ctx.ndk_api),                      
                    '-DANDROID_EXECUTABLE={}/tools/android'.format(env['ANDROID_SDK']),            
                    '-DCMAKE_TOOLCHAIN_FILE={}'.format(                                            
                        join(self.ctx.ndk_dir, 'build', 'cmake',                                   
                             'android.toolchain.cmake')),                                          
                    # Make the linkage with our python library, otherwise we                       
                    # will get dlopen error when trying to import dlib's module.                   
                    '-DCMAKE_SHARED_LINKER_FLAGS=-L{path} -lpython{version}'.format(               
                        path=python_link_root,                                                     
                        version=python_link_version),                                              
                                                                                                   
                    '-DBUILD_WITH_STANDALONE_TOOLCHAIN=ON',                                        
                    # Force to build as shared libraries the dlib's dependant                      
                    # libs or we will not be able to link with our python                          
                    '-DBUILD_SHARED_LIBS=ON',                                                      
                    '-DBUILD_STATIC_LIBS=OFF',                                                     
                                                                                                   
                    # Disable some dlib's features                                                 
                    '-DBUILD_dlib_java=OFF',                                                       
                    '-DBUILD_dlib_java_bindings_generator=OFF',                                    
                    # '-DBUILD_dlib_highgui=OFF',                                                  
                    # '-DBUILD_dlib_imgproc=OFF',                                                  
                    # '-DBUILD_dlib_flann=OFF',                                                    
                    '-DBUILD_TESTS=OFF',                                                           
                    '-DBUILD_PERF_TESTS=OFF',                                                      
                    '-DENABLE_TESTING=OFF',                                                        
                    '-DBUILD_EXAMPLES=OFF',                                                        
                    '-DBUILD_ANDROID_EXAMPLES=OFF',                                                
                    '-DBUILD_ANDROID_EXAMPLES=OFF',                                                
                    # Create sub-directory into build to ouput it                                  
                    '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={output}'.format(output=lib_dir),            
                    # Force to only build our version of python                                    
                    '-DBUILD_DLIB_PYTHON{major}=ON'.format(major=python_major),                    
                    '-DBUILD_DLIB_PYTHON{major}=OFF'.format(                                       
                        major='2' if python_major == '3' else '3'),                                
                                                                                                   
                    # Force to install the `dlib.so` library directly into                         
                    # python's site packages (otherwise the dlib's loader fails                    
                    # on finding the dlib.so library)                                              
                    '-DDLIB_SKIP_PYTHON_LOADER=OFF',                                               
                    '-DDLIB_PYTHON{major}_INSTALL_PATH={site_packages}'.format(                    
                        major=python_major, site_packages=python_site_packages),                   
                                                                                                   
                    # Define python's paths for: exe, lib, includes, numpy...                      
                    '-DPYTHON_DEFAULT_EXECUTABLE={}'.format(self.ctx.hostpython),                  
                    '-DPYTHON{major}_EXECUTABLE={host_python}'.format(                             
                        major=python_major, host_python=self.ctx.hostpython),                      
                    '-DPYTHON{major}_INCLUDE_PATH={include_path}'.format(                          
                        major=python_major, include_path=python_include_root),                     
                    '-DPYTHON{major}_LIBRARIES={python_lib}'.format(                               
                        major=python_major, python_lib=python_library),                            
                    '-DPYTHON{major}_NUMPY_INCLUDE_DIRS={numpy_include}'.format(                   
                        major=python_major, numpy_include=python_include_numpy),                   
                    '-DPYTHON{major}_PACKAGES_PATH={site_packages}'.format(                        
                        major=python_major, site_packages=python_site_packages),                   
                    self.get_build_dir(arch.arch),                                                 
                    _env=env),                                                                     
            #Install python bindings (dlib.so)

            shprint(sh.cmake,'--build', '{output}'.format(output=lib_dir)  , '--config','RELEASE','--')                     
            sh.cp('-a', sh.glob('{}/*.so'.format(lib_dir))  ,self.ctx.get_libs_dir(arch.arch))     
            
recipe = DlibRecipe()
