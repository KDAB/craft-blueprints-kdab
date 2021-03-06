import shutil

import info
from Package.BinaryPackageBase import *

from CraftCore import CraftCore
from Utils.CraftManifest import *

class subinfo(info.infoclass):
    vlc_ver = None

    def setTargets(self):
        repo = "http://downloads.kdab.com/ci/cache/gammaray/binaries"
        manifest = CraftManifest.fromJson(CraftCore.cache.cacheJsonFromUrl(f"{repo}/manifest.json"))

        self.targets["master"] = []
        self.targetDigests["master"] = ([], CraftHash.HashAlgorithm.SHA256)
        for abi in manifest.packages.keys():
            # use the probe only builds
            if abi == str(CraftCore.compiler):
                continue
            if not "qt-apps/gammaray" in manifest.packages[abi]:
                continue
            latest = manifest.packages[abi]["qt-apps/gammaray"].latest
            if latest.fileName.endswith(".exe"):
                continue
            self.targets["master"].append(f"{repo}/{latest.fileName}")
            self.targetDigests["master"][0].append(latest.checksum)

        self.description = "Multiple probes for GammaRay"

        self.defaultTarget = "master"

    def setDependencies(self):
        self.buildDependencies["virtual/bin-base"] = "default"
        self.buildDependencies["craft/craft-blueprints-kdab"] = "default"


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
