#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
from conans import ConanFile, AutoToolsBuildEnvironment, tools


class ncursesConan(ConanFile):
    name = "ncurses"
    version = "6.1"    
    url = "https://github.com/conan-community/conan-ncurses"
    homepage = "https://www.gnu.org/software/ncurses"
    author = "Conan Community"
    license = "X11"
    description = "An API, allowing the programmer to write text-based user interfaces, TUIs, in a terminal-independent manner"
    topics = ("conan", "ncurses", "terminal", "screen", "tui")
    settings = "os", "compiler", "arch", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    exports = "LICENSE"
    _autotools = None
    _source_subfolder = "source_subfolder"
    
    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        folder_name = "ncurses-%s" % self.version
        sha256 = "aa057eeeb4a14d470101eff4597d5833dcef5965331be3528c08d99cebaa0d17"
        url = "https://invisible-mirror.net/archives/ncurses/%s.tar.gz" % folder_name
        tools.get(url=url, sha256=sha256)
        os.rename(folder_name, self._source_subfolder)

    def _configure_autotools(self):
        if not self._autotools:
            args = [
                '--enable-overwrite',
                '--without-manpages',
                '--without-tests',
                '--without-debug'
                '--with-%s' % ("shared" if self.options.shared else "normal")
                ]
            self._autotools = AutoToolsBuildEnvironment(self)
            self._autotools.configure(args=args)
        return self._autotools

    def build(self):
        with tools.chdir(self._source_subfolder):
            autotools = self._configure_autotools()
            autotools.make()

    def package(self):
        self.copy("COPYING", dst="licenses", src=self._source_subfolder)
        with tools.chdir(self._source_subfolder):
            autotools = self._configure_autotools()
            autotools.install()


    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
