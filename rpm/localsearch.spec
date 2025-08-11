Name:       localsearch
Summary:    Tracker miners and metadata extractors
Version:    3.9.0
Release:    1
License:    LGPLv2+ and GPLv2+
URL:        https://gnome.pages.gitlab.gnome.org/localsearch/
Source0:    %{name}-%{version}.tar.bz2
Source1:    10-rtf.rule
Source2:    10-csv.rule
Source3:    tracker-reset.sh
Patch1:     0001-Tracker-config-overrides.patch
Patch2:     0002-Fix-systemd-unit-files.patch
Patch3:     0003-Prevent-tracker-extract-failing-when-seccomp-loading.patch
Patch4:     0004-Fix-database-corruption-caused-by-the-miner-being-re.patch
Patch5:     0005-Allow-D-Bus-activation-only-through-systemd.patch

BuildRequires:  meson >= 0.50
BuildRequires:  gettext
BuildRequires:  pkgconfig(tinysparql-3.0)
BuildRequires:  pkgconfig(blkid)
BuildRequires:  pkgconfig(dbus-glib-1) >= 0.60
BuildRequires:  pkgconfig(exempi-2.0) >= 2.1.0
BuildRequires:  pkgconfig(glib-2.0) >= 2.40.0
BuildRequires:  pkgconfig(gio-2.0) >= 2.40.0
BuildRequires:  pkgconfig(gio-unix-2.0) >= 2.40.0
BuildRequires:  pkgconfig(gmodule-2.0) >= 2.40.0
BuildRequires:  pkgconfig(gobject-2.0) >= 2.40.0
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gudev-1.0)
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
BuildRequires:  oneshot

Requires:   systemd-user-session-targets
Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig
%{_oneshot_requires_post}

Obsoletes:      tracker-miners < 3.8
Provides:       tracker-miners = %{version}-%{release}

%description
Tinysparql is a powerful desktop-neutral first class object database,
tag/metadata database and search tool.

This package contains various miners and metadata extractors for tinysparql.

%prep
%autosetup -p1 -n %{name}-%{version}/upstream

%build
%meson -Dman=false -Dfunctional_tests=false \
       -Dbattery_detection=none \
       -Dfanotify=disabled \
       -Dguarantee_metadata=true \
       -Dwriteback=false \
       -Draw=disabled -Dcue=disabled -Dxps=disabled -Diso=disabled \
       -Dlibav=enabled \
       -Dlandlock=disabled \
       -Dsystemd_user_services_dir=%{_userunitdir} \
       -Ddefault_index_recursive_dirs=\&DESKTOP,\&DOCUMENTS,\&DOWNLOAD,\&MUSIC,\&PICTURES,\&VIDEOS,\$HOME/android_storage/DCIM,\$HOME/android_storage/Download,\$HOME/android_storage/Pictures,\$HOME/android_storage/Podcasts,\$HOME/android_storage/Music \
       -Ddefault_index_single_dirs=[]

%meson_build

%install
%meson_install

mkdir -p %{buildroot}%{_userunitdir}/post-user-session.target.wants
ln -s ../localsearch-3.service %{buildroot}%{_userunitdir}/post-user-session.target.wants/

cp -a %{SOURCE1} %{buildroot}%{_datadir}/localsearch3/extract-rules/
cp -a %{SOURCE2} %{buildroot}%{_datadir}/localsearch3/extract-rules/

install -D -m 755 %{SOURCE3} %{buildroot}/%{_oneshotdir}/tracker-reset.sh

%find_lang localsearch3

%post
/sbin/ldconfig
glib-compile-schemas   /usr/share/glib-2.0/schemas/
add-oneshot --now --new-users --all-users tracker-reset.sh || :
if [ "$1" -ge 1 ]; then
systemctl-user daemon-reload || :
systemctl-user try-restart localsearch-3.service || :
fi

%postun
/sbin/ldconfig
glib-compile-schemas   /usr/share/glib-2.0/schemas/
if [ "$1" -eq 0 ]; then
systemctl-user stop localsearch-3.service || :
systemctl-user daemon-reload || :
fi

%files -f localsearch3.lang
%license COPYING COPYING.GPL COPYING.LGPL
%exclude %{_sysconfdir}/xdg/autostart/localsearch-3.desktop
%{_bindir}/localsearch
%{_libdir}/localsearch-3.0/
%{_libexecdir}/localsearch-3
%{_libexecdir}/localsearch-control-3
%{_libexecdir}/localsearch-extractor-3
%{_datadir}/dbus-1/interfaces/org.freedesktop.Tracker3.Miner.Files.Index.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.Tracker3.Miner.xml
%{_datadir}/dbus-1/services/org.freedesktop.Tracker*.service
%{_datadir}/dbus-1/services/org.freedesktop.LocalSearch*
%{_datadir}/glib-2.0/schemas/org.freedesktop.Tracker*.xml
%{_datadir}/localsearch3/
%{_userunitdir}/localsearch*.service
%{_userunitdir}/post-user-session.target.wants/localsearch-3.service
%attr(0755, -, -) %{_oneshotdir}/tracker-reset.sh
