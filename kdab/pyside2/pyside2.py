# -*- coding: utf-8 -*-

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["5.9", "5.11", "dev"]:
          self.svnTargets[ver] = f"git://code.qt.io/pyside/pyside-setup.git|{ver}"
          self.targetConfigurePath[ver] = "sources/pyside2"

        qtver = CraftVersion(CraftPackageObject.get("libs/qt5/qtbase").version)
        if qtver > "5.10.1":
            self.defaultTarget = "dev"
        elif qtver > "5.9":
            self.defaultTarget = "5.11"
        else:
            self.defaultTarget = "5.9"



    def setDependencies(self):
        self.runtimeDependencies["kdab/shiboken2"] = self.defaultTarget
        self.runtimeDependencies["libs/qt5"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.supportsNinja = False



    def configureOptions(self, defines=""):
        defines = super().configureOptions(defines)
        if ("Paths", "Python") in CraftCore.settings:
            python = os.path.join(CraftCore.settings.get("Paths", "Python"), f"python{CraftCore.compiler.executableSuffix}")
        if not os.path.exists(python):
            if CraftCore.compiler.isWindows:
                CraftCore.log.warning(f"Could not find {python} as provided by [Paths]Python, using {sys.executable} as a fallback")
            python = sys.executable
        defines += f" -DPYTHON_EXECUTABLE=\"{python}\""

        disabledModules = ["WebKit", "WebKitWidgets"]

        # Qt3d needs https://codereview.qt-project.org/#/c/219105/ so 5.10.2?
        if CraftVersion(CraftPackageObject.get("libs/qt5/qtbase").version) < CraftVersion("5.10.2"):
            disabledModules += ["3DCore", "3DRender", "3DInput", "3DLogic", "3DAnimation", "3DExtras"]

        for p in disabledModules:
            defines += f" -DCMAKE_DISABLE_FIND_PACKAGE_Qt5{p}=ON"

        return defines

