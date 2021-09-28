Name:       tracker-miners
Summary:    Tracker miners and metadata extractors
Version:    3.2.0
Release:    1
License:    LGPLv2+ and GPLv2+
URL:        https://wiki.gnome.org/Projects/Tracker
Source0:    %{name}-%{version}.tar.bz2
Source1:    10-rtf.rule
Source2:    10-csv.rule
Patch1:     0001-Tracker-config-overrides.patch
Patch2:     0002-Fix-systemd-unit-files.patch
Patch3:     0003-Prevent-tracker-extract-failing-when-seccomp-loading.patch
Patch4:     0004-Add-also-fileSize-to-the-basic-set-of-file-info-on-a.patch
Patch5:     0005-Fix-database-corruption-caused-by-the-miner-being-re.patch
Patch6:     0006-Allow-D-Bus-activation-only-through-systemd.patch
Patch7:     0007-Update-nfo-fileLastModified-also-on-content-specific.patch

BuildRequires:  meson >= 0.50
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  oneshot
BuildRequires:  pkgconfig(tracker-sparql-3.0)
BuildRequires:  pkgconfig(dbus-glib-1) >= 0.60
BuildRequires:  pkgconfig(exempi-2.0) >= 2.1.0
BuildRequires:  pkgconfig(glib-2.0) >= 2.40.0
BuildRequires:  pkgconfig(gio-2.0) >= 2.40.0
BuildRequires:  pkgconfig(gio-unix-2.0) >= 2.40.0
BuildRequires:  pkgconfig(gmodule-2.0) >= 2.40.0
BuildRequires:  pkgconfig(gobject-2.0) >= 2.40.0
BuildRequires:  pkgconfig(icu-uc)
BuildRequires:  pkgconfig(icu-i18n)
BuildRequires:  pkgconfig(libexif) >= 0.6
BuildRequires:  pkgconfig(libgsf-1) >= 1.14.24
BuildRequires:  pkgconfig(libiptcdata)
BuildRequires:  pkgconfig(libpng) >= 0.89
BuildRequires:  pkgconfig(libxml-2.0) >= 2.6
BuildRequires:  pkgconfig(poppler-glib) >= 0.16.0
BuildRequires:  pkgconfig(totem-plparser)
BuildRequires:  pkgconfig(vorbis) >= 0.22
BuildRequires:  pkgconfig(flac) >= 1.2.1
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(libavcodec) >= 0.8.4
BuildRequires:  pkgconfig(libavformat) >= 0.8.4
BuildRequires:  pkgconfig(libavutil) >= 0.8.4
BuildRequires:  pkgconfig(libseccomp) >= 2.0
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libtiff-4) >= 3.8.2
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  giflib-devel

Requires:   systemd-user-session-targets
Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig
%{_oneshot_requires_post}

%description
Tracker is a powerful desktop-neutral first class object database,
tag/metadata database and search tool.

It consists of a common object database that allows entities to have an
almost infinite number of properties, metadata (both embedded/harvested as
well as user definable), a comprehensive database of keywords/tags and
links to other entities.

It provides additional features for file based objects including context
linking and audit trails for a file object.

This package contains various miners and metadata extractors for tracker.
It has the ability to index, store, harvest metadata. retrieve and search
all types of files and other first class objects.

%prep
%autosetup -p1 -n %{name}-%{version}/upstream

%build
%meson -Dman=false -Dfunctional_tests=false \
       -Dguarantee_metadata=true -Dminer_rss=false \
       -Dwriteback=false \
       -Draw=disabled -Dcue=disabled -Dxps=disabled -Diso=disabled \
       -Dgeneric_media_extractor=libav \
       -Dnetwork_manager=disabled \
       -Dsystemd_user_services_dir=%{_userunitdir} \
       -Ddefault_index_recursive_dirs=\&DESKTOP,\&DOCUMENTS,\&DOWNLOAD,\&MUSIC,\&PICTURES,\&VIDEOS,\$HOME/android_storage/DCIM,\$HOME/android_storage/Download,\$HOME/android_storage/Pictures,\$HOME/android_storage/Podcasts,\$HOME/android_storage/Music \
       -Ddefault_index_single_dirs=[]

%meson_build

%install
%meson_install

mkdir -p %{buildroot}%{_userunitdir}/post-user-session.target.wants
ln -s ../tracker-miner-fs-3.service %{buildroot}%{_userunitdir}/post-user-session.target.wants/

cp -a %{SOURCE1} %{buildroot}%{_datadir}/tracker3-miners/extract-rules/
cp -a %{SOURCE2} %{buildroot}%{_datadir}/tracker3-miners/extract-rules/

%find_lang tracker3-miners

%post
/sbin/ldconfig
glib-compile-schemas   /usr/share/glib-2.0/schemas/
if [ "$1" -ge 1 ]; then
systemctl-user daemon-reload || :
systemctl-user stop tracker-extract-3.service || :
systemctl-user try-restart tracker-miner-fs-3.service || :
fi

%postun
/sbin/ldconfig
glib-compile-schemas   /usr/share/glib-2.0/schemas/
if [ "$1" -eq 0 ]; then
systemctl-user stop tracker-miner-fs-3.service tracker-extract-3.service || :
systemctl-user daemon-reload || :
fi

%files -f tracker3-miners.lang
%defattr(-,root,root,-)
%license COPYING COPYING.GPL COPYING.LGPL
%exclude %{_sysconfdir}/xdg/autostart/tracker-miner-fs-3.desktop
%{_libdir}/tracker-miners-3.0/
%{_libexecdir}/tracker-extract-3
%{_libexecdir}/tracker-miner-fs-3
%{_libexecdir}/tracker-miner-fs-control-3
%{_libexecdir}/tracker3
%{_datadir}/dbus-1/interfaces/org.freedesktop.Tracker3.Miner.Files.Index.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.Tracker3.Miner.xml
%{_datadir}/dbus-1/services/org.freedesktop.Tracker*.service
%{_datadir}/glib-2.0/schemas/org.freedesktop.Tracker*.xml
%{_datadir}/tracker3-miners/
%{_userunitdir}/tracker-*.service
%{_userunitdir}/post-user-session.target.wants/tracker-miner-fs-3.service
