%global qt_version 5.15.9

Summary: Qt5 - Gamepad component
Name:    opt-qt5-qtgamepad
Version: 5.15.9
Release: 1%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License: LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:     http://www.qt.io
Source0: %{name}-%{version}.tar.bz2

%{?opt_qt5_default_filter}

BuildRequires: make
BuildRequires: opt-qt5-qtbase-devel >= %{qt_version}
BuildRequires: opt-qt5-qtbase-static >= %{qt_version}
BuildRequires: opt-qt5-qtbase-private-devel
%{?_opt_qt5:Requires: %{_opt_qt5}%{?_isa} = %{_opt_qt5_version}}
BuildRequires: opt-qt5-qtdeclarative-devel >= %{qt_version}
BuildRequires: pkgconfig(libudev)
BuildRequires: pkgconfig(sdl2)
Requires: opt-qt5-qtbase-gui >= %{qt_version}
Requires: opt-qt5-qtdeclarative >= %{qt_version}

%description
Qt Gamepad provides a way to display web content in a QML application without necessarily
including a full web browser stack by using native APIs where it makes sense.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: opt-qt5-qtbase-devel%{?_isa}
Requires: opt-qt5-qtdeclarative-devel%{?_isa}
%description devel
%{summary}.


%prep
%autosetup -n %{name}-%{version}/upstream


%build
export QTDIR=%{_opt_qt5_prefix}
touch .git
mkdir %{_target_platform}
pushd %{_target_platform}
%{opt_qmake_qt5} ..
popd

# have to restart build several times due to bug in sb2
%make_build -C %{_target_platform} -k || chmod -R ugo+r . || true
%make_build -C %{_target_platform}
chmod -R ugo+r .


%install
make install INSTALL_ROOT=%{buildroot} -C %{_target_platform}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE.GPL LICENSE.LGPLv3
%{_opt_qt5_libdir}/libQt5Gamepad.so.5*
%{_opt_qt5_qmldir}/QtGamepad/
%{_opt_qt5_plugindir}/gamepads/

%files devel
%{_opt_qt5_headerdir}/QtGamepad/
%{_opt_qt5_libdir}/libQt5Gamepad.so
%{_opt_qt5_libdir}/libQt5Gamepad.prl
%{_opt_qt5_libdir}/pkgconfig/Qt5Gamepad.pc
%{_opt_qt5_libdir}/cmake/Qt5Gamepad
%{_opt_qt5_archdatadir}/mkspecs/modules/*
%exclude %{_opt_qt5_libdir}/libQt5Gamepad.la
