[![Download](https://api.bintray.com/packages/conan-community/conan/ncurses%3Aconan/images/download.svg)](https://bintray.com/conan-community/conan/ncurses%3Aconan/_latestVersion)
[![Build status](https://ci.appveyor.com/api/projects/status/github/ConanCIintegration/conan-ncurses?svg=true)](https://ci.appveyor.com/project/ConanCIintegration/conan-ncurses)
[![Build Status](https://travis-ci.org/conan-community/conan-ncurses.svg)](https://travis-ci.org/conan-community/conan-ncurses)
# Conan ncurses

Conan package for ncurses library. https://www.gnu.org/software/ncurses/

The packages generated with this **conanfile** can be found in [Bintray](https://bintray.com/conan-community/conan/ncurses%3Aconan).

## Basic setup

    $ conan install ncurses/6.1@conan/stable

## Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    ncurses/6.1@conan/stable

    [options]
    ncurses:shared=true # false
    ncurses:fPIC=true # false (only available for Linux and Macos)

    [generators]
    cmake

## Issues

If you wish to report an issue for Conan Community related to this package or any other, please do so here:

[Conan Community Issues](https://github.com/conan-community/community/issues)

## Wish List

If you wish to make a request for Conan Community creating a new package, please do so here:

[Conan Wish List](https://github.com/conan-io/wishlist)


## License

[MIT](LICENSE)