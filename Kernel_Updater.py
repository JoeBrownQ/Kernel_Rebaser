# Module Imports
import os

# Variables - Changable
KERNEL_VERSION = "4.19" # Set Kernel Version (4.4/4.14/4.19)
KERNEL_TAG = "LA.UM.10.2.1.r1-03400-sdm660.0" # Set CAF Tag / Upstream Version (LA.UM.10.2.1.r1-0300-sdm660.0/v4.19.157)
REPO_LINK = "https://github.com/iamimmanuelraj/android_kernel_xiaomi_jasmine_sprout.git" # Repo link to pull/fetch/push Kernel
BASE_BRANCH = "LA.UM.10.2.1.r1-03700-sdm660.0" # Base branch to pick the old/device base changes from

# Variables - Non_Changable
QCACLD_LINK = "https://git.codelinaro.org/clo/la/platform/vendor/qcom-opensource/wlan/qcacld-3.0" # Qcacld repo link
FW_API_LINK = "https://git.codelinaro.org/clo/la/platform/vendor/qcom-opensource/wlan/fw-api" # Firmware Api repo link
QCA_WIFI_HOST_CM_LINK = "https://git.codelinaro.org/clo/la/platform/vendor/qcom-opensource/wlan/qca-wifi-host-cmn" # Qualcom Wifi host repo link
AUDIO_TECHPACK_LINK = "https://git.codelinaro.org/clo/la/platform/vendor/opensource/audio-kernel" # Audio Techpack repo link
EXFAT_LINK = "https://github.com/arter97/exfat-linux.git" # Exfat repo link

# Clone the kernel
os.system("git clone https://git.codelinaro.org/clo/la/kernel/msm-%s.git -b %s %s"%(KERNEL_VERSION,KERNEL_TAG,KERNEL_TAG))

# Go into the folder
os.chdir("%s"%(KERNEL_TAG))

# Checkout to a TEMP branch
os.system("git checkout -b TEMP")

# Add QCACLD
os.system("git subtree add --prefix=drivers/staging/qcacld-3.0 %s %s --squash"%(QCACLD_LINK,KERNEL_TAG))

# Add Firmware Api
os.system("git subtree add --prefix=drivers/staging/fw-api %s %s --squash"%(FW_API_LINK,KERNEL_TAG))

# Add Qualcom Wifi host
os.system("git subtree add --prefix=drivers/staging/qca-wifi-host-cmn %s %s --squash"%(QCA_WIFI_HOST_CM_LINK,KERNEL_TAG))

# Add Audio Techpack
os.system("git subtree add --prefix=techpack/audio %s %s --squash"%(AUDIO_TECHPACK_LINK,KERNEL_TAG))

# Add Exfat
os.system("git subtree add --prefix=fs/exfat %s master --squash"%(EXFAT_LINK))

# Fetch the changes from old kernel and cherry pick em
os.system("git fetch %s %s"%(REPO_LINK,BASE_BRANCH))
os.system("git cherry-pick c46747559bcc8abab8f1674aca4f5a6ddbc71aad^..58743c137cccac80b7ca4a104467d615a72c1f2f")

# Change Localversion in defconfig (Add defconfig paths for your devices)
DEFCONFIG = open("arch/arm64/configs/vendor/jasmine_sprout_defconfig", "r")
NUMBER_OF_LINES = DEFCONFIG.readlines()
NUMBER_OF_LINES[0] = '''CONFIG_LOCALVERSION="-%s"\n'''%KERNEL_TAG
DEFCONFIG = open("arch/arm64/configs/vendor/jasmine_sprout_defconfig", "w")
DEFCONFIG.writelines(NUMBER_OF_LINES)
DEFCONFIG.close()
DEFCONFIG = open("arch/arm64/configs/vendor/jasmine_sprout-debug_defconfig", "r")
NUMBER_OF_LINES = DEFCONFIG.readlines()
NUMBER_OF_LINES[0] = '''CONFIG_LOCALVERSION="-%s"\n'''%KERNEL_TAG
DEFCONFIG = open("arch/arm64/configs/vendor/jasmine_sprout-debug_defconfig", "w")
DEFCONFIG.writelines(NUMBER_OF_LINES)
DEFCONFIG.close()
DEFCONFIG = open("arch/arm64/configs/vendor/wayne_defconfig", "r")
NUMBER_OF_LINES = DEFCONFIG.readlines()
NUMBER_OF_LINES[0] = '''CONFIG_LOCALVERSION="-%s"\n'''%KERNEL_TAG
DEFCONFIG = open("arch/arm64/configs/vendor/wayne_defconfig", "w")
DEFCONFIG.writelines(NUMBER_OF_LINES)
DEFCONFIG.close()
DEFCONFIG = open("arch/arm64/configs/vendor/wayne-debug_defconfig", "r")
NUMBER_OF_LINES = DEFCONFIG.readlines()
NUMBER_OF_LINES[0] = '''CONFIG_LOCALVERSION="-%s"\n'''%KERNEL_TAG
DEFCONFIG = open("arch/arm64/configs/vendor/wayne-debug_defconfig", "w")
DEFCONFIG.writelines(NUMBER_OF_LINES)
DEFCONFIG.close()

# Commit Localversion Changes
os.system("git add . && git commit -m 'config: defconfig: update LOCALVERSION to latest caf tag/version' -m 'Rebased over Latest tag so lets update this too'")

# Push Changes to Repo
os.system("git remote add upstream  %s"%(REPO_LINK))
os.system("git push upstream HEAD:refs/heads/%s -f"%(KERNEL_TAG))
