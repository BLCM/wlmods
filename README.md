Wonderlands Mods
================
[![Support Discord](https://img.shields.io/static/v1?label=&message=Support%20Discord&logo=discord&color=424)](https://discord.gg/bXeqV8Ef9R)

This is the github home to a collection of Tiny Tina's Wonderlands Mods.  At the
moment, all the mods stored here are made using the hotfix injection
method of WL modding, which basically just adds custom hotfixes to the
ones sent to the game by Gearbox.

Running Mods
------------

There are two methods for running mods on Wonderlands.

### Open Hotfix Loader

As of writing (August 28, 2022), this has just recently been released and is
still in beta.  [Open Hotfix Loader](https://github.com/apple1417/OpenHotfixLoader/),
by apple1417, is a new method of injecting hotfixes which doesn't rely on doing
any "man in the middle" proxying like B3HM does.  Some links:

- [Main Github Site](https://github.com/apple1417/OpenHotfixLoader)
- [Video Install Guide](https://youtu.be/gHX3dtZIojY)
- [Releases](https://github.com/apple1417/OpenHotfixLoader/releases)

### B3HM

**NOTE:** As of writing (August 28, 2022), B3HM does **not** yet support Wonderlands!
Support for Wonderlands is forthcoming in version 1.0.2, which should be
out within a few weeks, but don't pester anyone for the exact release date.  :)

c0dycode's [B3HM (Borderlands 3 Hotfix Merger)](https://www.nexusmods.com/borderlands3/mods/244)
has long been the only public tool for BL3 hotfix mod injection.  It's B3HM is a
tool which merges in custom hotfixes for BL3 to pick up, when the game requests
hotfixes from Gearbox.  It's available either as a standalone EXE, or as a DLL
which you can inject in a variety of methods.  You can find B3HM in these locations:

- [B3HM at Nexusmods](https://www.nexusmods.com/borderlands3/mods/244)
- [B3HM at Github Releases](https://github.com/c0dycode/BL3HotfixWebUI/releases)

The B3HM project has [documentation right at its github page](https://github.com/c0dycode/BL3HotfixWebUI/wiki/B3HM-Wiki).

For the DLL version, it's recommended that you use
[FromDarkHell's BL3DX11Injection/PluginLoader](https://github.com/FromDarkHell/BL3DX11Injection/releases)
to inject the B3HM into the Borderlands 3 process.  For the EXE version, just
download the EXE and give it a run.

See the [B3HM documentation](https://github.com/c0dycode/BL3HotfixWebUI/wiki/B3HM-Wiki) for
further information about how to use the app!  There's also an [easy-to-follow
HOWTO about running PluginLoader + B3HM](https://docs.google.com/document/d/1gdJX7eje3v-S7INIX5ZzIvaLfzGaWjauB2rcPgPqslw),
and a [tutorial video, both by by FromDarkHell](https://www.youtube.com/watch?v=KYgUzKomXrk).

Other information (such as some info for Linux users) can be found at
[borderlandsmodding.com](http://borderlandsmodding.com/bl3-running-mods/).

Finding Mods
------------

Obviously you can just browse around this github repo to find mods that
you like, but since the mods are arranged by author, it might be difficult
to know exactly what's available.  Like for BL3 mods, we've created a
[Wonderlands ModCabinet Wiki](https://github.com/BLCM/wlmods/wiki)
which categorizes mods by what they do, and will probably be much easier
to work with.

Some mod authors might decide to store their WL mods somewhere other than
here, of course.  If any major hubs of WL mod distribution ever becomes
popular, we'll link it in here.

For Mod Authors
===============

See [README-authors.md](README-authors.md) for information on both
writing WL mods, and contributing to this github (and associated
wiki).

