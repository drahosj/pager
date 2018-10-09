# pager.py
Send POCSAG pages using SDR with GNURadio.

# STAY LEGAL - STAY SAFE
Transmit legally. If operating on Amateur Radio frequencies, make sure
to be licensed and identify with your callsign (and follow
all other applicable rules)! If operating on other
frequencies, you'd better have a special license from the FCC.

There are a few tweaks you have to make to the code to make sure
you're legal.

# Usage
`python page.py <capcode> <message>`

This transmits a POCSAG message. Any pagers set to receive the given
capcode will beep and display it. Pretty simple.

Technical details (all tweakable):
- Baud rate: 512 (POCSAG512)
- Alphanumeric
- +- 4.5kHz shift (wideband)
- Frequency/callsign: Read and edit the code.

# Setup
A bit harder than the usage. This is just an overview.

The first part (setting up GNURadio + hardware support) can be
skipped, but you'll still need to install mixalot.

## Setup SDR environment
### Install hardware support
For this step, install the libs for whatever SDR you're using.
These are actually pretty likely to be in the repos, so just install with
apt/yum/dnf/zypper/pacman.

Also make sure to install the development versions of the library, or you'll
have missing headers issues.

- BladeRF - bladeRF/libbladeRF1
- HackRF - hackrf/libhackrf0
- RTL-SDR (RX only, but hey, you might want support anyway) - librtlsdr
- LimeRF - liblimesdr

It's pretty self-explanatory. But you want to do this step first.
If the relevant library isn't in the repos, you'll have to compile it
from source. These are all pretty easy - the only typical dependency
is libusb.

### Install GNURadio
Clone down GNURadio, check out a recent tag (master is usually pretty stable).
Configure with cmake and then build and install. GNURadio has a ton
of dependencies, so you might want to try to install this from repos
or using PyBombs or something. Alternatively you could use a better
guide than this on installing GNURadio.

### Install GR-OsmoSDR
Even if this is available in the repos, you might want to recompile it
yourself, ESPECIALLY if you had to install one of
the hardware support libraries by hand.

```
git clone https://github.com/osmocom/gr-osmosdr
cd gr-osmosdr
# Optionally, check out a recent tag now
mkdir build
cd build
cmake ..
make
sudo make install
```

### Summary
Install hardware libraries first, then GNURadio, then gr-osmosdr. Make sure
to check CMake's summaries and that all of the expected modules will be
available. Alternatively, skip this whole step if using Kali because
gnuradio and gr-osmosdr are preinstalled.

## Install Mixalot
Installing mixalot is fairly straightforward, for a gnuradio block. Download
the sources, cmake, make, make install. Dependencies are minimal, but
expect numpy and of course GNURadio. This will be necessary even
if you are on Kali because mixalot isn't in repos for anything.

```
git clone https://github.com/unsynchronized/gr-mixalot
cd gr-mixalot
mkdir build
cd build
cmake ..
make
sudo make install
```

At this point, hope for magic and everything will have worked!
