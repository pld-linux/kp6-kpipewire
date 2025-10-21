#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	6.5.0
%define		qtver		5.15.2
%define		kpname		kpipewire
Summary:	a set of convenient classes to use PipeWire in Qt projects
Name:		kp6-%{kpname}
Version:	6.5.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	3382e784a5c6cc2fc5a4eb4e8b138f76
URL:		http://www.kde.org/
BuildRequires:	Qt6WaylandClient-devel
BuildRequires:	cmake >= 3.16.0
BuildRequires:	ffmpeg-devel
BuildRequires:	kf6-extra-cmake-modules
BuildRequires:	kp6-kwayland-devel
BuildRequires:	ninja
BuildRequires:	pipewire-devel
BuildRequires:	plasma-wayland-protocols-devel
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	kp5-%{kpname} < 6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
kpipewire offers a set of convenient classes to use PipeWire
(https://pipewire.org/) in Qt projects.

%package devel
Summary:	Header files for %{kpname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kpname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	cmake >= 3.16
Obsoletes:	kp5-%{kpname}-devel < 6

%description devel
Header files for %{kpname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kpname}.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir}
%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kpname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kpname}.lang
%defattr(644,root,root,755)
%doc README.md
%ghost %{_libdir}/libKPipeWire.so.6
%{_libdir}/libKPipeWire.so.*.*
%ghost %{_libdir}/libKPipeWireRecord.so.6
%{_libdir}/libKPipeWireRecord.so.*.*
%dir %{_libdir}/qt6/qml/org/kde/pipewire
%{_libdir}/qt6/qml/org/kde/pipewire/KPipeWire.qmltypes
%{_libdir}/qt6/qml/org/kde/pipewire/libKPipeWireplugin.so
%{_libdir}/qt6/qml/org/kde/pipewire/qmldir
%dir %{_libdir}/qt6/qml/org/kde/pipewire/monitor
%dir %{_libdir}/qt6/qml/org/kde/pipewire/record
%{_libdir}/qt6/qml/org/kde/pipewire/record/KPipeWireRecord.qmltypes
%{_libdir}/qt6/qml/org/kde/pipewire/record/libKPipeWireRecordplugin.so
%{_libdir}/qt6/qml/org/kde/pipewire/record/qmldir
%{_datadir}/qlogging-categories6/kpipewire.categories
%{_datadir}/qlogging-categories6/kpipewirerecord.categories
%ghost %{_libdir}/libKPipeWireDmaBuf.so.6
%{_libdir}/libKPipeWireDmaBuf.so.*.*
%{_libdir}/qt6/qml/org/kde/pipewire/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/pipewire/monitor/KPipeWireMonitorDeclarative.qmltypes
%{_libdir}/qt6/qml/org/kde/pipewire/monitor/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/pipewire/monitor/libKPipeWireMonitorDeclarative.so
%{_libdir}/qt6/qml/org/kde/pipewire/monitor/qmldir
%{_libdir}/qt6/qml/org/kde/pipewire/record/kde-qmlmodule.version

%files devel
%defattr(644,root,root,755)
%{_includedir}/KPipeWire
%{_libdir}/cmake/KPipeWire
%{_libdir}/libKPipeWire.so
%{_libdir}/libKPipeWireRecord.so
%{_libdir}/libKPipeWireDmaBuf.so
