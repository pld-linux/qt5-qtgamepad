#
# Conditional build:
%bcond_without	doc	# Documentation

%define		orgname		qtgamepad
%define		qtbase_ver		%{version}
%define		qtdeclarative_ver	%{version}
%define		qttools_ver		%{version}
Summary:	The Qt5 Gamepad library
Summary(pl.UTF-8):	Biblioteka Qt5 Gamepad
Name:		qt5-%{orgname}
Version:	5.15.2
Release:	3
License:	LGPL v3 or GPL v2+ or commercial
Group:		Libraries
Source0:	http://download.qt.io/official_releases/qt/5.15/%{version}/submodules/%{orgname}-everywhere-src-%{version}.tar.xz
# Source0-md5:	f2225019450f0a0b59536aed9f6f0c27
URL:		https://www.qt.io/
BuildRequires:	Qt5Core-devel >= %{qtbase_ver}
BuildRequires:	Qt5DeviceDiscoverySupport-devel >= %{qtbase_ver}
BuildRequires:	Qt5Gui-devel >= %{qtbase_ver}
BuildRequires:	Qt5Qml-devel >= %{qtdeclarative_ver}
BuildRequires:	Qt5Quick-devel >= %{qtdeclarative_ver}
BuildRequires:	SDL2-devel
%if %{with doc}
BuildRequires:	qt5-assistant >= %{qttools_ver}
%endif
BuildRequires:	qt5-build >= %{qtbase_ver}
BuildRequires:	qt5-qmake >= %{qtbase_ver}
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing
%define		qt5dir		%{_libdir}/qt5

%description
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.

This package contains Qt5 Gamepad library.

%description -l pl.UTF-8
Qt to wieloplatformowy szkielet aplikacji i interfejsów użytkownika.
Przy użyciu Qt można pisać aplikacje powiązane z WWW i wdrażać je w
systemach biurkowych, przenośnych i wbudowanych bez przepisywania kodu
źródłowego.

Ten pakiet zawiera bibliotekę Qt5 Gamepad.

%package -n Qt5Gamepad
Summary:	The Qt5 Gamepad library
Summary(pl.UTF-8):	Biblioteka Qt5 Gamepad
Group:		Libraries
Requires:	Qt5Core >= %{qtbase_ver}
Requires:	Qt5Gui >= %{qtbase_ver}
Requires:	Qt5Qml-devel >= %{qtdeclarative_ver}
Requires:	Qt5Quick-devel >= %{qtdeclarative_ver}

%description -n Qt5Gamepad
Qt Gamepad is an add-on library that enables Qt applications to
support the use of gamepad hardware and in some cases remote control
equipment.

%description -n Qt5Gamepad -l pl.UTF-8
Biblioteka Qt5 Gamepad ułatwia użycie kontrolerów w apikacjach Qt.

%package -n Qt5Gamepad-devel
Summary:	Qt5 Gamepad library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 Gamepad - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt5Core-devel >= %{qtbase_ver}
Requires:	Qt5Gui-devel >= %{qtbase_ver}
Requires:	Qt5Gamepad = %{version}-%{release}

%description -n Qt5Gamepad-devel
Qt5 Gamepad library - development files.

%description -n Qt5Gamepad-devel -l pl.UTF-8
Biblioteka Qt5 Gamepad - pliki programistyczne.

%package -n Qt5Gamepad-SDL2
Summary:	The Qt5 Gamepad library plugin for SDL2
Summary(pl.UTF-8):	Biblioteka Qt5 Gamepad - plugin do SDL2
Group:		Libraries
Requires:	Qt5Gamepad = %{version}-%{release}

%description -n Qt5Gamepad-SDL2
The Qt5 Gamepad library plugin for SDL2.

%description -n Qt5Gamepad-SDL2 -l pl.UTF-8
Biblioteka Qt5 Gamepad - plugin do SDL2.

%package doc
Summary:	Qt5 Gamepad documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 Gamepad w formacie HTML
License:	FDL v1.3
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
%{?noarchpackage}

%description doc
Qt5 Gamepad documentation in HTML format.

%description doc -l pl.UTF-8
Dokumentacja do biblioteki Qt5 Gamepad w formacie HTML.

%package doc-qch
Summary:	Qt5 Gamepad documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 Gamepad w formacie QCH
License:	FDL v1.3
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
%{?noarchpackage}

%description doc-qch
Qt5 Gamepad documentation in QCH format.

%description doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt5 Gamepad w formacie QCH.

%package examples
Summary:	Qt5 Gamepad examples
Summary(pl.UTF-8):	Przykłady do biblioteki Qt5 Gamepad
License:	BSD or commercial
Group:		Development/Libraries
%{?noarchpackage}

%description examples
Qt5 Gamepad examples.

%description examples -l pl.UTF-8
Przykłady do biblioteki Qt5 Gamepad.

%prep
%setup -q -n %{orgname}-everywhere-src-%{version}

%build
qmake-qt5
%{__make}
%{?with_doc:%{__make} docs}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%if %{with doc}
%{__make} install_docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

# useless symlinks
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.so.5.??
# actually drop *.la, follow policy of not packaging them when *.pc exist
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.la

# Prepare some files list
ifecho() {
	r="$RPM_BUILD_ROOT$2"
	if [ -d "$r" ]; then
		echo "%%dir $2" >> $1.files
	elif [ -x "$r" ] ; then
		echo "%%attr(755,root,root) $2" >> $1.files
	elif [ -f "$r" ]; then
		echo "$2" >> $1.files
	else
		echo "Error generation $1 files list!"
		echo "$r: no such file or directory!"
		return 1
	fi
}
ifecho_tree() {
	ifecho $1 $2
	for f in `find $RPM_BUILD_ROOT$2 -printf "%%P "`; do
		ifecho $1 $2/$f
	done
}

echo "%defattr(644,root,root,755)" > examples.files
ifecho_tree examples %{_examplesdir}/qt5/gamepad

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n Qt5Gamepad -p /sbin/ldconfig
%postun	-n Qt5Gamepad -p /sbin/ldconfig

%files -n Qt5Gamepad
%defattr(644,root,root,755)
%doc README.md dist/changes-*
# R: Qt5Core Qt5Gui
%attr(755,root,root) %{_libdir}/libQt5Gamepad.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Gamepad.so.5
%dir %{qt5dir}/qml/QtGamepad
# R: Qt5Core Qt5Gamepad Qt5Gui Qt5Qml Qt5Quick
%attr(755,root,root) %{qt5dir}/qml/QtGamepad/libdeclarative_gamepad.so
%{qt5dir}/qml/QtGamepad/plugins.qmltypes
%{qt5dir}/qml/QtGamepad/qmldir
%dir %{qt5dir}/plugins/gamepads
# R: Qt5Core Qt5Gamepad udev-libs
%attr(755,root,root) %{qt5dir}/plugins/gamepads/libevdevgamepad.so
%dir %{_libdir}/cmake/Qt5Gamepad

%files -n Qt5Gamepad-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5Gamepad.so
%{_libdir}/libQt5Gamepad.prl
%{_includedir}/qt5/QtGamepad
%{_pkgconfigdir}/Qt5Gamepad.pc
%{_libdir}/cmake/Qt5Gamepad/Qt5GamepadConfig*.cmake
%{_libdir}/cmake/Qt5Gamepad/Qt5Gamepad_QEvdevGamepadBackendPlugin.cmake
%{qt5dir}/mkspecs/modules/qt_lib_gamepad.pri
%{qt5dir}/mkspecs/modules/qt_lib_gamepad_private.pri

%files -n Qt5Gamepad-SDL2
%defattr(644,root,root,755)
# R: Qt5Core Qt5Gamepad SDL2
%attr(755,root,root) %{qt5dir}/plugins/gamepads/libsdl2gamepad.so
%{_libdir}/cmake/Qt5Gamepad/Qt5Gamepad_QSdl2GamepadBackendPlugin.cmake

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtgamepad

%files doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtgamepad.qch
%endif

%files examples -f examples.files
%defattr(644,root,root,755)
# XXX: dir shared with qt5-qtbase-examples
%dir %{_examplesdir}/qt5
