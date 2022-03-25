#
# Conditional build:
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module	selenium
Summary:	Python bindings for Selenium
Summary(pl.UTF-8):	Wiązania Pythona do Selenium
Name:		python-%{module}
Version:	3.141.0
Release:	4
License:	Apache v2.0
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/selenium/
Source0:	https://files.pythonhosted.org/packages/source/s/selenium/%{module}-%{version}.tar.gz
# Source0-md5:	274693e383ff507df7ee190359828c84
Patch0:		xpi-path.patch
Patch1:		0002-Pick-debian-location-of-chromedriver-from-chromium-d.patch
URL:		https://pypi.org/project/selenium/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	unzip
Suggests:	chromedriver
Suggests:	selenium-firefoxdriver
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python language bindings for Selenium WebDriver.

The selenium package is used to automate web browser interaction from
Python.

%description -l pl.UTF-8
Wiązania Pythona do sterownika Selenium WebDriver.

Pakiet selenium służy automatyzacji interakcji z przeglądarką WWW z
poziomu Pythona.

%package -n python3-%{module}
Summary:	Python bindings for Selenium
Summary(pl.UTF-8):	Wiązania Pythona do Selenium
Group:		Development/Languages/Python
Suggests:	chromedriver
Suggests:	selenium-firefoxdriver

%description -n python3-%{module}
Python language bindings for Selenium WebDriver.

The selenium package is used to automate web browser interaction from
Python.

%description -n python3-%{module} -l pl.UTF-8
Wiązania Pythona do sterownika Selenium WebDriver.

Pakiet selenium służy automatyzacji interakcji z przeglądarką WWW z
poziomu Pythona.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1
%patch1 -p1

%build
%if %{with python2}
%py_build
%endif

%if %{with python3}
%py3_build
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
%{__rm} $RPM_BUILD_ROOT%{py_sitescriptdir}/%{module}/webdriver/firefox/webdriver.xpi
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/%{module}/webdriver/firefox/amd64
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/%{module}/webdriver/firefox/x86
%endif

%if %{with python3}
%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/%{module}/webdriver/firefox/webdriver.xpi
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/%{module}/webdriver/firefox/amd64
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/%{module}/webdriver/firefox/x86
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES README.rst
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif
