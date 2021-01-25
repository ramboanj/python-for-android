from pythonforandroid.recipe import CppCompiledComponentsPythonRecipe,PythonRecipe,CythonRecipe
import sh
from os.path import join,dirname
from multiprocessing import cpu_count
from pythonforandroid.logger import shprint
from pythonforandroid.util import current_directory

from pythonforandroid.logger import (logger, info, warning, debug, shprint, info_main) 




class DlibRecipe(CppCompiledComponentsPythonRecipe):
    site_packages_name = 'dlib'
    version = '19.8'
    url = 'https://github.com/davisking/dlib/archive/v{version}.zip'
#    url = 'http://dlib.net/files/dlib-{version}.zip'
    depends = ['numpy','scipy','setuptools']

#    built_libraries = {"libdlib.so" : "build/lib.dlib"}
#    patches = ["patchDlibCross.patch"]

    def get_recipe_env(self, arch):
        env = super(DlibRecipe, self).get_recipe_env(arch)
        
        env['ANDROID_NDK'] = self.ctx.ndk_dir
        env['ANDROID_SDK'] = self.ctx.sdk_dir
        #     import os
        #     for ls in os.environ:
        #         self.env[ls] = os.environ[ls]
        #     #Make true python binding
        #pyConfig=sh.Command(self.hostpython_location)
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
        info("major="+str(python_major))
        info("include_root="+str(python_include_root))
        info("site_packages="+str(python_site_packages))
        info("python_link_root="+str(python_link_root))
        info("link_version="+ str(python_link_version))        
        info("library="+ str(python_library))
        info("pythonLocate="+str(self.hostpython_location))

        
    def build_arch(self, arch):
        super().build_arch(arch);
            
recipe = DlibRecipe()
