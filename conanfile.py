#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import glob
from conans import ConanFile, AutoToolsBuildEnvironment, tools, VisualStudioBuildEnvironment
from conans.errors import ConanInvalidConfiguration


class ncursesConan(ConanFile):
    name = "ncurses"
    version = "6.1"
    url = "https://github.com/conan-community/conan-ncurses"
    homepage = "https://www.gnu.org/software/ncurses"
    author = "Conan Community"
    license = "X11"
    description = "An API, allowing the programmer to write text-based user interfaces, TUIs, " \
                  "in a terminal-independent manner"
    topics = ("conan", "ncurses", "terminal", "screen", "tui")
    settings = "os", "compiler", "arch", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False], "with_cpp": [True, False],
               "allow_msvc": [True, False], "allow_mingw": [True, False]}
    default_options = {"shared": False, "fPIC": True, "with_cpp": True,
                       "allow_msvc": True, "allow_mingw": True}
    exports = "LICENSE"
    # NOTE: "compile" was patched: .cc files are properly handled with MinGW-style path conversion
    exports_sources = ["ncurses.patch", "compile", "ar-lib"]
    _autotools = None
    _source_subfolder = "source_subfolder"

    @property
    def _is_msvc(self):
        return self.settings.compiler == "Visual Studio"

    @property
    def _is_mingw_windows(self):
        return self.settings.os == "Windows" and self.settings.compiler == "gcc" and os.name == "nt"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def requirements(self):
        if self._is_msvc:
            self.requires("getopt/1.0@bincrafters/stable")
            self.requires("dirent-win32/1.23.2@bincrafters/stable")

    def configure(self):
        # FIXME (uilian): Fix Windows support
        if self.settings.os == "Windows" and self.settings.compiler == "gcc" and not self.options.allow_mingw:
            raise ConanInvalidConfiguration("Oops! ncurses is not supported on MinGW yet")
        if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio" and not self.options.allow_msvc:
            raise ConanInvalidConfiguration("Oops! ncurses is not supported for Visual Studio yet")
        if not self.options.with_cpp:
            del self.settings.compiler.libcxx

    def source(self):
        folder_name = "ncurses-%s" % self.version
        sha256 = "aa057eeeb4a14d470101eff4597d5833dcef5965331be3528c08d99cebaa0d17"
        url = "https://invisible-mirror.net/archives/ncurses/%s.tar.gz" % folder_name
        tools.get(url=url, sha256=sha256)
        os.rename(folder_name, self._source_subfolder)

        os.makedirs(os.path.join(self._source_subfolder, 'build-aux'))
        shutil.move('compile', os.path.join(self._source_subfolder, 'build-aux', 'compile'))
        shutil.move('ar-lib', os.path.join(self._source_subfolder, 'build-aux', 'ar-lib'))

    def build_requirements(self):
        if self._is_msvc or self._is_mingw_windows:
            self.build_requires("msys2_installer/latest@bincrafters/stable")

    def _configure_autotools(self):
        if not self._autotools:
            args = [
                '--enable-overwrite',
                '--without-manpages',
                '--without-tests',
                '--enable-term-driver',
                '--disable-echo',
                '--with-{}'.format("shared" if self.options.shared else "normal"),
                '--without-{}'.format("normal" if self.options.shared else "shared")
                ]

            if self._is_msvc:
                prefix = tools.unix_path(self.package_folder)
                runtime = str(self.settings.compiler.runtime)
                args.extend(['--prefix=%s' % prefix,
                             '--disable-stripping',  # disable, as /bin/install cannot find strip
                             '--disable-db-install',  # disable, as run_tic.sh (/bin/tic.exe) segfaults
                             '--disable-database',  # TODO : figure out how to work with fallback entries or
                             # without database in general?
                             'ac_cv_func_setvbuf_reversed=no',  # asserts during configure in debug builds
                             'CC=$PWD/build-aux/compile cl -nologo',
                             'CXX=$PWD/build-aux/compile cl -nologo',
                             'CFLAGS=-FS -%s' % runtime,
                             'CXXFLAGS=-FS -%s' % runtime,
                             # TODO: move FILENO to patch
                             'CPPFLAGS=-DSTDIN_FILENO=0 -DSTDOUT_FILENO=1 -DSTDERR_FILENO=2 -D_WIN32_WINNT=0x0600 -I%s/include' % prefix,
                             'LD=link',
                             'LDFLAGS=user32.lib -L%s/lib' % prefix,
                             'NM=dumpbin -symbols',
                             'STRIP=:',
                             'AR=$PWD/build-aux/ar-lib lib',
                             'RANLIB=:'])

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
            if self._is_msvc:
                with tools.vcvars(self.settings):
                    env_build = VisualStudioBuildEnvironment(self)
                    with tools.environment_append(env_build.vars):
                        autotools = self._configure_autotools()
                        autotools.make()
            else:
                autotools = self._configure_autotools()
                autotools.make()

    def package(self):
        self.copy("COPYING", dst="licenses", src=self._source_subfolder)
        with tools.chdir(self._source_subfolder):
            if self._is_msvc:
                with tools.vcvars(self.settings):
                    env_build = VisualStudioBuildEnvironment(self)
                    with tools.environment_append(env_build.vars):
                        autotools = self._configure_autotools()
                        autotools.install()
                with tools.chdir(os.path.join(self.package_folder, "lib")):
                    libs = glob.glob("lib*.a")
                    for lib in libs:
                        vslib = lib[3:-2] + ".lib"
                        self.output.info('renaming %s into %s' % (lib, vslib))
                        shutil.move(lib, vslib)
            else:
                autotools = self._configure_autotools()
                autotools.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
