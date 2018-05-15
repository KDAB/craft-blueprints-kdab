# -*- coding: utf-8 -*-

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["5.9", "5.11", "dev"]:
          self.svnTargets[ver] = f"git://code.qt.io/pyside/pyside-setup.git|{ver}"
          self.targetConfigurePath[ver] = "sources/shiboken2"

        qtver = CraftVersion(CraftPackageObject.get("libs/qt5/qtbase").version)
        if qtver > "5.10.1":
            self.defaultTarget = "dev"
        elif qtver > "5.9":
            self.defaultTarget = "5.11"
        else:
            self.defaultTarget = "5.9"

    def setDependencies(self):
        self.runtimeDependencies["libs/libxml2"] = None
        self.runtimeDependencies["libs/libxslt"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtxmlpatterns"] = None
        self.runtimeDependencies["libs/llvm-meta/llvm"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        if ("Paths", "Python") in CraftCore.settings:
            python = os.path.join(CraftCore.settings.get("Paths", "Python"), f"python{CraftCore.compiler.executableSuffix}")
        if not os.path.exists(python):
            if CraftCore.compiler.isWindows:
                CraftCore.log.warning(f"Could not find {python} as provided by [Paths]Python, using {sys.executable} as a fallback")
            python = sys.executable
        self.subinfo.options.configure.args += f" -DPYTHON_EXECUTABLE=\"{python}\""
        self.subinfo.options.configure.args += f" -DLLVM_CONFIG=\"{os.path.join(CraftCore.standardDirs.craftRoot(), 'bin', 'llvm-config')}\""
