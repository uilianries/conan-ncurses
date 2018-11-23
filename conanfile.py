#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, AutoToolsBuildEnvironment, tools
from conans.errors import ConanInvalidConfiguration


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
    options = {"shared": [True, False], "fPIC": [True, False], "with_cpp": [True, False]}
    default_options = {"shared": False, "fPIC": True, "with_cpp": True}
    exports = "LICENSE"
    exports_sources = "ncurses.patch"
    _autotools = None
    _source_subfolder = "source_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.settings.compiler == "Visual Studio":
            raise ConanInvalidConfiguration("ncurse is not supported for Visual Studio")
        if not self.options.with_cpp:
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
                '--with-{}'.format("shared" if self.options.shared else "normal"),
                '--without-{}'.format("normal" if self.options.shared else "shared")
                ]
            if self.options.with_cpp:
                args.append('--with-{}'.format("cxx-shared" if self.options.shared else "cxx"))
            else:
                args.extend(['--without-cxx-shared', "--without-cxx"])
            self._autotools = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
            self._autotools.configure(args=args)
        return self._autotools

    def build(self):
        tools.patch(patch_file="ncurses.patch", base_path=self._source_subfolder)
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
