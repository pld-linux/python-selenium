# TODO:
# Seems on 64bit selenium looks for wrong arch webdriver
# Seems to be fixed by ugly hack:
# [root@appserver4 /usr/share/python2.7/site-packages/selenium/webdriver/firefox]# ln -s ./amd64 x86  

%define	no_install_post_chrpath	1

%define		_rc	%{nil}
%define		module	selenium
Summary:	Python bindings for selenium
Name:		python-%{module}
Version:	2.39.0
Release:	2
License:	BSD-like
Group:		Development/Languages/Python
Source0:	http://pypi.python.org/packages/source/s/%{module}/%{module}-%{version}%{_rc}.tar.gz
# Source0-md5:	3f7aaad3eb52a218854bf0196c9daeda
URL:		http://pypi.python.org/pypi/selenium/
BuildRequires:	python-distribute
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRequires:	unzip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Selenium Python Client Driver is a Python language binding for
Selenium Remote Control (version 1.0 and 2.0).

Currently the remote protocol, Firefox and Chrome for Selenium 2.0 are
supported, as well as the Selenium 1.0 bindings. As work will
progresses we'll add more "native" drivers.

%package -n iceweasel-addon-%{module}
Summary:	Iceweasel add-on for python selenium
Group:		X11/Applications/Networking
Requires:	iceweasel >= 22.0

%description -n iceweasel-addon-%{module}
Driver for python selenium.

%prep
%setup -q -n %{module}-%{version}%{_rc}

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

install -d $RPM_BUILD_ROOT%{_datadir}/iceweasel/browser/extensions/fxdriver@googlecode.com
unzip $RPM_BUILD_DIR/%{module}-%{version}%{_rc}/py/selenium/webdriver/firefox/webdriver.xpi -d $RPM_BUILD_ROOT%{_datadir}/iceweasel/browser/extensions/fxdriver@googlecode.com

# remove windows binaries
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/iceweasel/browser/extensions/fxdriver@googlecode.com/platform/WINNT_x86-msvc
# remove binaries for incorrect arch
%ifnarch %{x8664}
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/iceweasel/browser/extensions/fxdriver@googlecode.com/platform/Linux_x86_64-gcc3
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/%{module}/webdriver/firefox/amd64
%endif
%ifnarch %{ix86}
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/iceweasel/browser/extensions/fxdriver@googlecode.com/platform/Linux_x86-gcc3
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/%{module}/webdriver/firefox/x86
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
#%%doc README*
%{py_sitescriptdir}/%{module}
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/%{module}-*.egg-info
%endif

%files -n iceweasel-addon-%{module}
%defattr(644,root,root,755)
%{_datadir}/iceweasel/browser/extensions/fxdriver@googlecode.com
