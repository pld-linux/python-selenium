# TODO:
# Seems on 64bit selenium looks for wrong arch webdriver
# Seems to be fixed by ugly hack:
# [root@appserver4 /usr/share/python2.7/site-packages/selenium/webdriver/firefox]# ln -s ./amd64 x86

%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define	no_install_post_chrpath	1

%define		_rc	%{nil}
%define		module	selenium
Summary:	Python bindings for selenium
Name:		python-%{module}
Version:	3.11.0
Release:	3
License:	BSD-like
Group:		Development/Languages/Python
Source0:	https://pypi.debian.net/selenium/%{module}-%{version}%{_rc}.tar.gz
# Source0-md5:	c565de302e12ffaf7e59c1e47b45bbef
URL:		http://pypi.python.org/pypi/selenium/
%if %{with python2}
BuildRequires:	python-distribute
%endif
%if %{with python3}
BuildRequires:	python3-distribute
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
BuildRequires:	unzip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Selenium Python Client Driver is a Python language binding for
Selenium Remote Control (version 1.0 and 2.0).

Currently the remote protocol, Firefox and Chrome for Selenium 2.0 are
supported, as well as the Selenium 1.0 bindings. As work will
progresses we'll add more "native" drivers.

%package -n python3-%{module}
Summary:	Python bindings for selenium
Group:		Development/Languages/Python

%description -n python3-%{module}
Selenium Python Client Driver is a Python language binding for
Selenium Remote Control (version 1.0 and 2.0).

Currently the remote protocol, Firefox and Chrome for Selenium 2.0 are
supported, as well as the Selenium 1.0 bindings. As work will
progresses we'll add more "native" drivers.

%package -n firefox-addon-%{module}
Summary:	Firefox add-on for python selenium
Group:		X11/Applications/Networking
Requires:	firefox >= 24.0

%description -n firefox-addon-%{module}
Driver for python selenium.

%prep
%setup -q -n %{module}-%{version}%{_rc}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

install -d $RPM_BUILD_ROOT%{_datadir}/firefox/browser/extensions/fxdriver@googlecode.com
unzip $RPM_BUILD_DIR/%{module}-%{version}%{_rc}/selenium/webdriver/firefox/webdriver.xpi -d $RPM_BUILD_ROOT%{_datadir}/firefox/browser/extensions/fxdriver@googlecode.com

# remove binaries for incorrect arch
%ifnarch %{x8664}
%if %{with python2}
%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}/%{module}/webdriver/firefox/amd64
%endif
%if %{with python3}
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/webdriver/firefox/amd64
%endif
%endif

%ifnarch %{ix86}
%if %{with python2}
%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}/%{module}/webdriver/firefox/x86
%endif
%if %{with python3}
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/webdriver/firefox/x86
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%dir %{py_sitedir}/selenium
%dir %{py_sitedir}/selenium/webdriver
%{py_sitedir}/selenium/webdriver/remote
%ifarch %{x8664} %{ix86}
%dir %{py_sitedir}/selenium/webdriver/firefox
%dir %{py_sitedir}/selenium/webdriver/firefox/[ax]*
%attr(755,root,root) %{py_sitedir}/selenium/webdriver/firefox/*/x_ignore_nofocus.so
%endif
%{py_sitescriptdir}/%{module}
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/%{module}-*.egg-info
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%dir %{py3_sitedir}/selenium
%dir %{py3_sitedir}/selenium/webdriver
%{py3_sitedir}/selenium/webdriver/remote
%ifarch %{x8664} %{ix86}
%dir %{py3_sitedir}/selenium/webdriver/firefox
%dir %{py3_sitedir}/selenium/webdriver/firefox/[ax]*
%attr(755,root,root) %{py3_sitedir}/selenium/webdriver/firefox/*/x_ignore_nofocus.so
%endif
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%ifarch %{x8664} %{ix86}
%files -n firefox-addon-%{module}
%defattr(644,root,root,755)
%{_datadir}/firefox/browser/extensions/fxdriver@googlecode.com
%endif
