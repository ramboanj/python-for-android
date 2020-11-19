from pythonforandroid.recipe import CppCompiledComponentsPythonRecipe
import sh
from os.path import join
from multiprocessing import cpu_count
from pythonforandroid.logger import shprint
from pythonforandroid.util import current_directory


class DlibRecipe(CppCompiledComponentsPythonRecipe):
    site_packages_name = 'dlib'
    version = '19.17'
    url = 'http://dlib.net/files/dlib-{version}.zip'
    depends = ['python3','numpy','cmake','virtualenv']
    setup_extra_args = []

    
    def get_lib_dir(self, arch):
        return join(self.get_build_dir(arch.arch), 'build', 'lib', arch.arch)

    def get_recipe_env(self, arch):
        env = super(DlibRecipe, self).get_recipe_env(arch)
        env['ANDROID_NDK'] = self.ctx.ndk_dir
        env['ANDROID_SDK'] = self.ctx.sdk_dir
        return env

    def build_arch(self, arch):

        super().build_arch(arch)


recipe = DlibRecipe()
