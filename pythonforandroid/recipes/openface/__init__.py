from pythonforandroid.recipe import CppCompiledComponentsPythonRecipe
import sh
from os.path import join
from multiprocessing import cpu_count
from pythonforandroid.logger import shprint
from pythonforandroid.util import current_directory

from pythonforandroid.logger import (logger, info, warning, debug, shprint, info_main)




class OpenFaceRecipe(CppCompiledComponentsPythonRecipe):
    site_packages_name = 'dlib'
    version = '0.21'
    url = 'https://github.com/cmusatyalab/openface/archive/{version}.zip'
    depends = ['python2','opencv2','dlib','numpy', 'pandas', 'scipy', 'scikit-learn','scikit-image']

    def get_recipe_env(self, arch):
        env = super(OpenFaceRecipe, self).get_recipe_env(arch)
        
        env['ANDROID_NDK'] = self.ctx.ndk_dir
        env['ANDROID_SDK'] = self.ctx.sdk_dir
        return env

    def build_arch(self, arch):
        super().build_arch(arch)                                                      
recipe = DlibRecipe()
