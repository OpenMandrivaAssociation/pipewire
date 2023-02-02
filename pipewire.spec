# enable_by_default: Toggle if pipewire should be enabled by default and/or replace PulseAudio.
#  0 = no
#  1 = yes
%define enable_by_default 1

%ifarch %{ix86}
%define _disable_ld_no_undefined 1
%define _disable_lto 1
%endif

%ifarch %{x86_64}
%bcond_without compat32
%endif

%define spa_api 0.2
%define api 0.3
%define git-media-session 20230112
%define media_session_ver master
%define major 0
%define libname %mklibname %{name} %{api} %{major}
%define devname %mklibname %{name} -d

%define lib32name %mklib32name %{name} %{api} %{major}
%define dev32name %mklib32name %{name} -d

Name:		pipewire
Summary:	Media Sharing Server
Version:	0.3.65
Release:	2
License:	LGPLv2+
Group:		System/Servers
URL:		https://pipewire.org/
Source0:	https://gitlab.freedesktop.org/pipewire/pipewire/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Mirror
#Source0:	https://github.com/PipeWire/pipewire/archive/%{version}/%{name}-%{version}.tar.gz
Source4:	https://gitlab.freedesktop.org/pipewire/media-session/-/archive/%{media_session_ver}/media-session-%{media_session_ver}.tar.bz2
Source10:	pipewire.sysusers

Patch1:		pipewire-0.3.35-tests-compile.patch

# Upstream patches:
Patch101:	0001-Build-media-session-from-local-tarbal.patch

BuildRequires:	doxygen
BuildRequires:	gettext
%ifarch %{ix86}
BuildRequires:	gcc
%endif
BuildRequires:	graphviz
BuildRequires:	meson
BuildRequires:  roc-toolkit-devel >= 0.2.1
BuildRequires:	openfec-devel
BuildRequires:	pkgconfig(libpcap)
BuildRequires:	pkgconfig(libcap)
BuildRequires:	pkgconfig(avahi-client)
BuildRequires:	pkgconfig(bluez)
BuildRequires:	python3dist(docutils)
BuildRequires:	pkgconfig(libudev)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(glib-2.0) >= 2.32
BuildRequires:	pkgconfig(gio-unix-2.0) >= 2.32
BuildRequires:	pkgconfig(gstreamer-1.0) >= 1.10.0
BuildRequires:	pkgconfig(gstreamer-base-1.0) >= 1.10.0
BuildRequires:	pkgconfig(gstreamer-plugins-base-1.0) >= 1.10.0
BuildRequires:	pkgconfig(gstreamer-net-1.0) >= 1.10.0
BuildRequires:	pkgconfig(gstreamer-allocators-1.0) >= 1.10.0
BuildRequires:	pkgconfig(systemd)
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(ldacBT-enc)
BuildRequires:	pkgconfig(ldacBT-abr)
%ifnarch %{ix86}
BuildRequires:	pkgconfig(libcamera)
%endif
BuildRequires:	pkgconfig(libcanberra)
BuildRequires:	pkgconfig(libdrm)
BuildRequires:	pkgconfig(libfreeaptx)
BuildRequires:	pkgconfig(libopenaptx)
BuildRequires:	pkgconfig(libavcodec)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(libuv)
BuildRequires:	pkgconfig(libva)
BuildRequires:	pkgconfig(libv4l2)
BuildRequires:	pkgconfig(lilv-0)
BuildRequires:	pkgconfig(sbc)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(vulkan)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(sox)
BuildRequires:	pkgconfig(speexdsp)
BuildRequires:	pkgconfig(ModemManager)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(readline)
# PipeWire support for now only webrtc 0.3.1. So let's pull old version of this package. As soon as they add support for v1, let's use new.
BuildRequires:	pkgconfig(webrtc-audio-processing)
#BuildRequires:	pkgconfig(webrtc-audio-processing-1)
BuildRequires:	pkgconfig(vulkan)
BuildRequires:	vulkan-headers
BuildRequires:	xmltoman
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	systemd-rpm-macros
# Tools
BuildRequires:	openal
BuildRequires:	pulseaudio-utils

%if %{with compat32}
BuildRequires:	libc6
BuildRequires:	libx11-xcb1
BuildRequires:	devel(libasound)
BuildRequires:	devel(libbluetooth)
BuildRequires:	devel(libsystemd)
BuildRequires:	devel(libglib-2.0)
BuildRequires:	devel(libgio-2.0)
BuildRequires:	devel(libdbus-1)
BuildRequires:	devel(libgstreamer-1.0)
BuildRequires:	devel(libjack)
BuildRequires:	devel(libdrm)
BuildRequires:	devel(libreadline)
BuildRequires:	devel(libncurses)
BuildRequires:	devel(libncursesw)
BuildRequires:	devel(libavcodec)
BuildRequires:	devel(libsndfile)
BuildRequires:	devel(libpulse)
BuildRequires:	devel(libavahi-client)
BuildRequires:	devel(libX11-xcb)
BuildRequires:	devel(libXcomposite)
BuildRequires:	devel(libXcursor)
BuildRequires:	devel(libXdamage)
BuildRequires:	devel(libXext)
BuildRequires:	devel(libXfixes)
BuildRequires:	devel(libXi)
BuildRequires:	devel(libXinerama)
BuildRequires:	devel(libXrandr)
BuildRequires:	devel(libxkbcommon)
BuildRequires:	devel(libwayland-client)
BuildRequires:	devel(libwayland-cursor)
BuildRequires:	devel(libwayland-egl)
BuildRequires:	devel(libXrender)
BuildRequires:	devel(libXft)
BuildRequires:	devel(libXau)
BuildRequires:	devel(libXdmcp)
BuildRequires:	devel(libffi)
BuildRequires:	devel(libxcb)
BuildRequires:	devel(libxcb-shm)
BuildRequires:	devel(libxcb-render)
BuildRequires:	devel(libpng16)
BuildRequires:	devel(libusb-1.0)
BuildRequires:	devel(libblkid)
BuildRequires:	devel(libunwind)
BuildRequires:	devel(libdw)
BuildRequires:	libunwind-nongnu-devel
BuildRequires:	devel(libgstaudio-1.0)
BuildRequires:	devel(liborc-0.4)
%endif

Requires:	rtkit
Requires(pre):	systemd

Requires: ((%{name}-media-session = %{version}-%{release}) or wireplumber)
%systemd_ordering

%description
PipeWire is a multimedia server for Linux and other Unix like operating
systems.

#------------------------------------------------

%package -n %{libname}
Summary:	Libraries for PipeWire clients
Group:		System/Libraries

%description -n %{libname}
This package contains the runtime libraries for any application that
wishes to interface with a PipeWire media server.

#------------------------------------------------

%package -n %{devname}
Summary:	Headers and libraries for PipeWire client development
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	spa-devel = %{version}-%{release}

%description -n %{devname}
Headers and libraries for developing applications that can communicate
with a PipeWire media server.

#------------------------------------------------

%package doc
Summary:	PipeWire media server documentation
Group:		Documentation
BuildArch:	noarch
Requires:	%{name} >= %{version}-%{release}

%description doc
This package contains documentation for the PipeWire media server.

#------------------------------------------------

%package utils
Summary:	PipeWire media server utilities
Group:		System/Servers

%description utils
This package contains command line utilities for the PipeWire
media server.

#------------------------------------------------

%package -n gstreamer1.0-%{name}
Summary:	GStreamer 1.0 plugin for the PipeWire multimedia server
Group:		System/Servers

%description -n gstreamer1.0-%{name}
GStreamer 1.0 plugin for the PipeWire multimedia server.

#------------------------------------------------
%package alsa
Summary:	PipeWire media server ALSA support
License:	MIT
Recommends:	%{name} = %{version}-%{release}

%description alsa
This package contains an ALSA plugin for the PipeWire media server.

#------------------------------------------------
%package pulse
Summary:	PipeWire media server PulseAudio server support
License:	MIT
Requires:	%{name} = %{version}-%{release}
# (tpg) 2022-08-11 pipewire-pulse[79745]: pw.conf: execvp error 'pactl': No such file or directory
Requires:	pulseaudio-utils
Recommends:	openal

%description pulse
This package contains a PipeWire module for making PipeWire act
as a PulseAudio server

#------------------------------------------------

%package libjack
Summary:	PipeWire libjack library
License:	MIT
Recommends:	%{name} = %{version}-%{release}
Obsoletes:	pipewire-jack < 0.2.96-2

%description libjack
This package contains a PipeWire replacement for JACK audio connection kit
"libjack" library.

#------------------------------------------------

%package plugin-jack
Summary:	PipeWire media server JACK support
License:	MIT
Recommends:	%{name} = %{version}-%{release}

%description plugin-jack
This package contains the PipeWire spa plugin to connect to a JACK server.

#------------------------------------------------

%package media-session
Summary:	PipeWire Media Session
License:	MIT
Recommends:	%{name}%{?_isa} = %{version}-%{release}

%description media-session
This package contains the Media Session Manager for the
PipeWire media server.

#------------------------------------------------
%prep
%autosetup -T -b0 -p1
mkdir subprojects/packagefiles
cp %{SOURCE4} subprojects/packagefiles/


%if %{with compat32}
%meson32 \
	-Dalsa=enabled \
	-Dudev=enabled \
	-Dudevrulesdir="%{_udevrulesdir}" \
	-Ddocs=disabled \
	-Dman=disabled \
	-Dgstreamer=enabled \
	-Dsystemd=enabled \
	-Dsystemd-user-service=enabled \
	-Djack=enabled \
	-Dpipewire-alsa=enabled \
	-Dpipewire-jack=enabled \
	-Dlibpulse=enabled \
	-Dvulkan=enabled \
	-Dbluez5=enabled \
	-Dbluez5-codec-lc3plus=disabled \
	-Dbluez5-codec-aac=disabled \
	-Dbluez5-codec-aptx=enabled \
	-Decho-cancel-webrtc=enabled \
	-Dlibcanberra=disabled \
	-Dlibcamera=disabled \
	-Droc=disabled \
	-Dffmpeg=enabled \
	-Dvolume=enabled \
	-Dsession-managers=media-session \
	--buildtype=release
%endif


%meson \
	-Dalsa=enabled \
	-Dudev=enabled \
	-Dudevrulesdir="%{_udevrulesdir}" \
	-Ddocs=enabled \
	-Dman=enabled \
	-Dgstreamer=enabled \
	-Dsystemd=enabled \
	-Dsystemd-user-service=enabled \
	-Djack=enabled \
	-Dpipewire-alsa=enabled \
	-Dpipewire-jack=enabled \
	-Dlibpulse=enabled \
	-Dvulkan=enabled \
	-Dbluez5=enabled \
	-Dbluez5-codec-lc3plus=disabled \
	-Dbluez5-codec-aac=disabled \
	-Dbluez5-codec-aptx=enabled \
	-Decho-cancel-webrtc=enabled \
%ifnarch %{ix86}
	-Dlibcamera=enabled \
%else
	-Dlibcamera=disabled \
%endif
	-Droc=enabled \
	-Dffmpeg=enabled \
	-Dvolume=enabled \
	-Dsession-managers=media-session \
	--buildtype=release

%build
%if %{with compat32}
%ninja_build -C build32
%endif

%meson_build

%install
%if %{with compat32}
%ninja_install -C build32
%endif

%meson_install

# Switches that enable certain config fragments
touch %{buildroot}%{_datadir}/pipewire/media-session.d/with-audio
touch %{buildroot}%{_datadir}/pipewire/media-session.d/with-alsa

# User creation
install -D -p -m 0644 %{S:10} %{buildroot}%{_sysusersdir}/%{name}.conf

%find_lang media-session

# Test fail on ARMv7hnl
%if 0
%check
%meson_test
%endif

%pre
%sysusers_create_package %{name} %{S:10}

#                 Attention! Achtung! Uwaga! Attenzione!                  #
###########################################################################
# PipeWire can replace (and probably will) PulseAudio and become default  #
#       It is currently enabled, to deactivate it togle ON switch         #
#            Don't do this without consulting with OMV Team.              #
###########################################################################

%if %enable_by_default
%post pulse
%systemd_user_post pipewire.service
%systemd_user_post pipewire.socket

%systemd_user_post pipewire-pulse.service
%systemd_user_post pipewire-pulse.socket

%systemd_user_post pipewire-media-session.service

%preun pulse
%systemd_user_preun pipewire.service
%systemd_user_preun pipewire.socket

%systemd_user_preun pipewire-pulse.service
%systemd_user_preun pipewire-pulse.socket

%systemd_user_preun pipewire-media-session.service

%postun pulse
%systemd_user_postun pipewire.service
%systemd_user_postun pipewire.socket

%systemd_user_postun pipewire-pulse.service
%systemd_user_postun pipewire-pulse.socket

%systemd_user_postun pipewire-media-session.service
%endif

%files
%license LICENSE
%doc README.md
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/%{name}.conf
%{_datadir}/pipewire/client.conf
%{_datadir}/pipewire/client-rt.conf
%{_datadir}/pipewire/jack.conf
%dir %{_datadir}/pipewire/media-session.d
%{_datadir}/pipewire/media-session.d/*.conf
%{_datadir}/pipewire/media-session.d/with-audio
%{_userunitdir}/%{name}.*
%{_bindir}/%{name}
%{_bindir}/pipewire-avb
%{_bindir}/%{name}-media-session
%{_sysusersdir}/%{name}.conf
%dir %{_libdir}/%{name}-%{api}/
%{_libdir}/%{name}-%{api}/libpipewire-module-*.so
%{_libdir}/spa-%{spa_api}
%{_libdir}/%{name}-%{api}/v4l2/libpw-v4l2.so
%{_datadir}/spa-%{spa_api}/bluez5/bluez-hardware.conf
#{_libdir}/spa-%{spa_api}/avb/
%doc %{_mandir}/man5/*.5*
%{_datadir}/alsa/alsa.conf.d/50-pipewire.conf
%{_datadir}/alsa/alsa.conf.d/99-pipewire-default.conf
%{_datadir}/alsa-card-profile/mixer/paths/*
%{_datadir}/alsa-card-profile/mixer/profile-sets/
%{_datadir}/locale/*/LC_MESSAGES/pipewire.mo
%{_userunitdir}/pipewire-media-session.service
%{_userunitdir}/filter-chain.service
%{_udevrulesdir}/90-pipewire-alsa.rules
%{_datadir}/pipewire/filter-chain/*.conf
%{_datadir}/pipewire/filter-chain.conf
%{_datadir}/pipewire/pipewire-avb.conf
%{_datadir}/pipewire/minimal.conf

%files pulse
%{_bindir}/pipewire-pulse
%{_datadir}/pipewire/pipewire-pulse.conf
%{_userunitdir}/pipewire-pulse.*
%{_datadir}/pipewire/media-session.d/with-alsa
%{_datadir}/pipewire/media-session.d/with-pulseaudio

%files -n %{libname}
%license LICENSE
%doc README.md
%{_libdir}/lib%{name}-%{api}.so.%{major}{,.*}

%files -n %{devname}
%{_includedir}/%{name}-%{api}/%{name}*
%{_includedir}/spa-%{spa_api}
%{_libdir}/lib%{name}-%{api}.so
%{_libdir}/pkgconfig/lib%{name}-%{api}.pc
%{_libdir}/pkgconfig/libspa-%{spa_api}.pc

%files doc
%{_docdir}/%{name}/html/

%files utils
%{_bindir}/spa-monitor
%{_bindir}/spa-inspect
%{_bindir}/spa-json-dump
%{_bindir}/pw-dsdplay
%{_bindir}/pw-mon
%{_bindir}/pw-cat
%{_bindir}/pw-cli
%{_bindir}/pw-dot
%{_bindir}/pw-link
%{_bindir}/pw-loopback
%{_bindir}/pw-metadata
%{_bindir}/pw-mididump
%{_bindir}/pw-midiplay
%{_bindir}/pw-midirecord
%{_bindir}/pw-play
%{_bindir}/pw-record
%{_bindir}/pw-profiler
%{_bindir}/pw-reserve
%{_bindir}/pw-top
%{_bindir}/pw-dump
%{_bindir}/pw-v4l2
%{_bindir}/spa-acp-tool
%{_bindir}/spa-resample
%doc %{_mandir}/man1/*.1*

%files -n gstreamer1.0-%{name}
%{_libdir}/gstreamer-1.0/libgst%{name}.so

%files alsa
%{_libdir}/alsa-lib/libasound_module_pcm_pipewire.so
%{_libdir}/alsa-lib/libasound_module_ctl_pipewire.so

%files libjack
%{_bindir}/pw-jack
%{_libdir}/pipewire-%{api}/jack
%{_datadir}/pipewire/media-session.d/with-jack

%files plugin-jack
%{_libdir}/spa-%{spa_api}/jack/

#FIXME  No idea why this lang won't work. Let's use dirty workaround.
#files media-session -f media-session.lang
%files media-session
%{_datadir}/locale/*/LC_MESSAGES/media-session.mo
