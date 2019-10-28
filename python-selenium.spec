%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		_rc	%{nil}
%define		module	selenium
Summary:	Python bindings for selenium
Name:		python-%{module}
Version:	3.11.0
Release:	8
License:	BSD-like
Group:		Development/Languages/Python
Source0:	https://pypi.debian.net/selenium/%{module}-%{version}%{_rc}.tar.gz
# Source0-md5:	c565de302e12ffaf7e59c1e47b45bbef
Patch0:		x-ignore-nofocus-path.patch
Patch1:		xpi-path.patch
Patch2:		0002-Pick-debian-location-of-chromedriver-from-chromium-d.patch
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
BuildArch:	noarch
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

%prep
%setup -q -n %{module}-%{version}%{_rc}
%patch0 -p1
%patch1 -p1
%patch2 -p1

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

# driver is in selenium-firefoxdriver.spec
%if %{with python2}
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/%{module}/webdriver/remote/*.js
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/%{module}/webdriver/firefox/amd64
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/%{module}/webdriver/firefox/x86
%endif

%if %{with python3}
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/webdriver/remote/*.js
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/%{module}/webdriver/firefox/amd64
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/%{module}/webdriver/firefox/x86
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%{py_sitescriptdir}/%{module}
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/%{module}-*.egg-info
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif
