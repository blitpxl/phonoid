from platform import system

IS_WINDOWS = system() == "Windows"
IS_MAC = system() == "Darwin"
IS_LINUX = system() == "Linux"
