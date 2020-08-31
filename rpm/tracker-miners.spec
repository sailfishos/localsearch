Name:       tracker-miners
Summary:    The Tracker indexer daemon (tracker-miner-fs) and tools to extract metadata from many different filetypes.
Version:    2.3.3
Release:    1
License:    GPLv2+ and LGPLv2+
URL:        https://gitlab.gnome.org/GNOME/%{name}/
Source0:    https://gitlab.gnome.org/GNOME/%{name}/-/archive/%{version}/%{name}-%{version}.tar.bz2
Source1:    10-rtf.rule
Patch1:     001-Tracker-config-overrides.patch
Patch2:     002-trackerlibav-get-metadata-from-audio-stream-instead-.patch
Patch3:     003-tracker-Fix-flac-tag-extraction-Fixes-JB35939.patch
Patch4:     004-fix-systemd-unit-files.patch
Patch5:     005-Use-date-instead-of-creationtime-for-ffmpeg-.patch
Patch6:     006-libav-Dont-count-audio-files-with-attached-pictures-.patch
Patch7:     007-trackerextractvorbis-add-null-protection-for-gobject.patch
Patch8:     008-seccomp-Prevent-trackerextract-failing-when-seccomp-.patch

Requires:   unzip
Requires:   systemd
Requires:   systemd-user-session-targets

Requires(post): /sbin/ldconfig
Requires(post):  oneshot
Requires(postun): /sbin/ldconfig
BuildRequires:  meson >= 0.50
BuildRequires:  ninja
BuildRequires:  pkgconfig(tracker-miner-2.0)
BuildRequires:  pkgconfig(tracker-sparql-2.0)
BuildRequires:  pkgconfig(dbus-glib-1) >= 0.60
BuildRequires:  pkgconfig(exempi-2.0)
BuildRequires:  pkgconfig(glib-2.0) >= 2.38.0
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(gmodule-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(icu-uc)
BuildRequires:  pkgconfig(id3tag)
BuildRequires:  pkgconfig(libexif)
BuildRequires:  pkgconfig(libgsf-1)
BuildRequires:  pkgconfig(libiptcdata)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(poppler-glib)
BuildRequires:  pkgconfig(totem-plparser)
BuildRequires:  pkgconfig(vorbis)
BuildRequires:  pkgconfig(flac)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libseccomp)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  gettext
BuildRequires:  giflib-devel
BuildRequires:  intltool
BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel >= 3.8.2
BuildRequires:  fdupes

%description
Tracker is a powerful desktop-neutral first class object database,
tag/metadata database, search tool and indexer.

It consists of a common object database that allows entities to have an
almost infinte number of properties, metadata (both embedded/harvested as
well as user definable), a comprehensive database of keywords/tags and
links to other entities.

It provides additional features for file based objects including context
linking and audit trails for a file object.

It has the ability to index, store, harvest metadata. retrieve and search
all types of files and other first class objects.

%prep
%autosetup -p1 -n %{name}-%{version}/upstream

%build
%meson -Dman=false -Ddocs=false -Dfunctional_tests=false \
       -Dguarantee_metadata=true -Dminer_rss=false \
       -Draw=disabled -Dcue=disabled -Dxps=disabled -Diso=disabled \
       -Dwriteback=false \
       -Dgeneric_media_extractor=libav \
       -Dsystemd_user_services=%{_userunitdir}

%install
rm -rf %{buildroot}

%meson_install
rm %{buildroot}/etc/xdg/autostart/tracker-*.desktop
mkdir -p %{buildroot}%{_userunitdir}/post-user-session.target.wants
ln -s ../tracker-miner-fs.service %{buildroot}%{_userunitdir}/post-user-session.target.wants/

cp -a %{SOURCE1} %{buildroot}%{_datadir}/tracker-miners/extract-rules/

%find_lang %{name}

%fdupes  %{buildroot}/%{_datadir}/

%post
/sbin/ldconfig
glib-compile-schemas   /usr/share/glib-2.0/schemas/
if [ "$1" -ge 1 ]; then
systemctl-user daemon-reload || :
systemctl-user stop tracker-extract.service || :
systemctl-user try-restart tracker-miner-fs.service || :
fi

%postun
/sbin/ldconfig
glib-compile-schemas   /usr/share/glib-2.0/schemas/
if [ "$1" -eq 0 ]; then
systemctl-user stop tracker-miner-fs.service tracker-extract.service || :
systemctl-user daemon-reload || :
fi

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_datadir}/dbus-1/services/org.freedesktop.Tracker1.*.service
%{_datadir}/tracker/miners/*
%dir %{_datadir}/tracker/miners
%dir %{_datadir}/tracker-miners/extract-rules
%{_datadir}/tracker-miners/extract-rules/*.rule
%dir %{_libdir}/tracker-miners-2.0/extract-modules
%{_datadir}/glib-2.0/schemas/org.freedesktop.Tracker*.xml
%{_libdir}/tracker-miners-2.0/libtracker-extract.so
%{_libdir}/tracker-miners-2.0/extract-modules/libextract-*.so
%{_libexecdir}/tracker-extract
%{_libexecdir}/tracker-miner-fs
%license COPYING COPYING.GPL COPYING.LGPL
%{_userunitdir}/tracker-miner-fs.service
%{_userunitdir}/tracker-extract.service
%{_userunitdir}/post-user-session.target.wants/tracker-miner-fs.service

