Summary:	Fancybox - Fancy lightbox alternative
Name:		jquery-fancybox
Version:	1.3.1
Release:	0.1
License:	MIT / GPL
Group:		Applications/WWW
Source0:	http://fancybox.googlecode.com/files/jquery.fancybox-%{version}.zip
# Source0-md5:	d72d950a798ffaa83750dfd6e4a0e382
URL:		http://www.fancybox.net/
BuildRequires:	rpmbuild(macros) > 1.268
Requires:	jquery >= 1.3
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir		%{_datadir}/jquery

%description
FancyBox is a tool for displaying images, html content and multi-media
in a Mac-style "lightbox" that floats overtop of web page.

- Can display images, HTML elements, SWF movies, Iframes and also Ajax
  requests
- Customizable through settings and CSS
- Groups related items and adds navigation.
- If the mouse wheel plugin is included in the page then FancyBox will
  respond to mouse wheel events as well
- Support fancy transitions by using easing plugin
- Adds a nice drop shadow under the zoomed item

%package demo
Summary:	Demo for jQuery.fancybox
Summary(pl.UTF-8):	Pliki demonstracyjne dla pakietu jQuery.fancybox
Group:		Development
Requires:	%{name} = %{version}-%{release}

%description demo
Demonstrations and samples for jQuery.fancybox.

%prep
%setup -qn jquery.fancybox-%{version}

find '(' -name '*.js' -o -name '*.html' -o -name '*.txt' ')' -print0 | xargs -0 %{__sed} -i -e 's,\r$,,'

mv fancybox/jquery.fancybox{-%{version},}.css
mv fancybox/jquery.fancybox{-%{version}.pack,}.js
mv fancybox/jquery.mousewheel{-3.0.2.pack,}.js
mv fancybox/jquery.easing{-1.3.pack,}.js
rm fancybox/jquery.fancybox-%{version}.js

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_examplesdir}/%{name}-%{version}}
cp -a fancybox $RPM_BUILD_ROOT%{_appdir}
cp -a example ajax.txt index.html style.css $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_appdir}/fancybox

%files demo
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
