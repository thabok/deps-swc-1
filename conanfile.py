from os.path import join

from conan import ConanFile
from conan.tools.env import VirtualBuildEnv, VirtualRunEnv
from conan.tools.files import copy


class SWC1(ConanFile):
    name = "swc_1"
    version = "1.0.0"
    license = "MIT"
    url = "https://github.com/thabok/deps-swc-1"
    description = "Conan package for SWC1"
    requires = "shared_module_a/1.3.0"


    def generate(self):
        # disable generation of scripts in the build folder
        VirtualBuildEnv(self)
        VirtualRunEnv(self)

        # copy model files from dependencies root folder into
        # folders with the dep-name inside the build_folder
        for dep in self.dependencies.values():
            copy(self, "*.slx", dep.package_folder, join(self.build_folder, 'shared'))

