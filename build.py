#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from conans import tools
from cpt.packager import ConanMultiPackager


if __name__ == "__main__":

    if tools.os_info.is_linux:
        installer = tools.SystemPackageTool()
        installer.install("xterm")
        os.environ["TERM"] = "xterm"

    builder = ConanMultiPackager()
    builder.add_common_builds(pure_c=True)
    builder.update_build_if(lambda bool: True, new_options={"ncurses:with_cpp": False})
    builder.add_common_builds(pure_c=False)
    builder.run()
