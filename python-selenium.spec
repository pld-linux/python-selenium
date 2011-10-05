# TODO
# - better group

%define	no_install_post_chrpath	1

%define		_rc	%{nil}
%define 	module	selenium
Summary:	Python bindings for selenium.
Name:		python-%{module}
Version:	2.5.0
Release:	0.1
License:	BSD-like
Group:		Development/Languages/Python
Source0:	http://pypi.python.org/packages/source/s/%{module}/%{module}-%{version}%{_rc}.tar.gz
# Source0-md5:	5472b4a8e127ecb48230343599ad9e6c
URL:		http://pypi.python.org/pypi/selenium/
BuildRequires:	python-distribute
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}%{_rc}-root-%(id -u -n)

%description
Selenium Python Client Driver is a Python language binding for Selenium 
Remote Control (version 1.0 and 2.0).

Currently the remote protocol, Firefox and Chrome for Selenium 2.0 are 
supported, as well as the Selenium 1.0 bindings. As work will progresses 
we'll add more "native" drivers.
        
%package -n iceweasel-addon-%{module}
Summary:	Iceweasel add-on for python selenium.
Group:		Development

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

install -d $RPM_BUILD_ROOT%{_libdir}/iceweasel/extensions/fxdriver@googlecode.com
unzip $RPM_BUILD_DIR/%{module}-%{version}%{_rc}/py/selenium/webdriver/firefox/webdriver.xpi -d $RPM_BUILD_ROOT%{_libdir}/iceweasel/extensions/fxdriver@googlecode.com

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README* docs

%{py_sitescriptdir}/%{module}
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/%{module}-*.egg-info
%endif

%files -n iceweasel-addon-%{module}
%defattr(644,root,root,755)
%{_libdir}/iceweasel/extensions/fxdriver@googlecode.com/
