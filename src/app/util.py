import glob
import re
import os


def get_files(path: str, filetypes: list):
    """
    Scan a directory for files with specific file types

    :param path: [str] path to directory that you want to scan
    :param filetypes: [list] the file types that you want to get from the specific directory
    :return: [list] list of path to the files
    """

    # remove the directory slashes (/) or (\) and let os.path.join decide what kind of slashes to use later.
    # this avoids the slash clash such as (dir/subdir\file.txt)
    path = re.split(r"[\\|/]", path)
    path[0] = path[0] + os.path.sep
    files = []
    for filetype in filetypes:
        files.extend(glob.glob(os.path.join(*path, f"*{filetype}")))
    return files
