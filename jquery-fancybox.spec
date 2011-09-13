# TODO
# - pkg for optional mousewheel?
%define		plugin	fancybox
Summary:	Fancybox - Fancy lightbox alternative
Name:		jquery-%{plugin}
Version:	1.3.4
Release:	2
License:	MIT / GPL v2
Group:		Applications/WWW
Source0:	http://fancybox.googlecode.com/files/jquery.fancybox-%{version}.zip
# Source0-md5:	f964f34f37237a33f62188cebbbb927a
URL:		http://www.fancybox.net/
Patch0:		no-pngfix.patch
BuildRequires:	js
BuildRequires:	rpmbuild(macros) >= 1.565
BuildRequires:	unzip
BuildRequires:	yuicompressor
Requires:	jquery >= 1.3
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir	%{_datadir}/jquery/%{plugin}

%description
FancyBox is a tool for displaying images, html content and multi-media
in a Mac-style "lightbox" that floats overtop of web page.

Features include:
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

%undos -f js,css,html,txt

mv fancybox/jquery.fancybox{-%{version},}.css
mv fancybox/jquery.fancybox{-%{version}.pack,}.js

%patch0 -p0

# source
install -d demo src
mv fancybox/jquery.fancybox-%{version}.js src/jquery.fancybox.js

# deps - rename for now
mv fancybox/jquery.easing{-1.3.pack,}.js # ? not used?
mv fancybox/jquery.mousewheel{-3.0.4.pack,}.js
# otherwise yuicompressor won't pack
sed -i -e 's,^/\*!,/*,' fancybox/jquery.mousewheel.js

# adjust demos to work offline
mv index.html style.css ajax.txt example demo
ln -s %{_datadir}/jquery demo

sed -i -e '
	s,./fancybox/jquery.fancybox-%{version}.pack.js,jquery/fancybox/fancybox.js,
	s,./fancybox/jquery.fancybox-%{version}.css,jquery/fancybox/fancybox.css,

	s,http://ajax.googleapis.com/ajax/libs/jquery/1.4/jquery.min.js,jquery/jquery.js,
	s,jquery-1.4.3.min.js,jquery/jquery.js,

	s,./fancybox/jquery.mousewheel-3.0.4.pack.js,jquery/fancybox/mousewheel.js,

	s,./example/,example/,g
' demo/index.html

%build
install -d build

# compress .js
for js in fancybox/*.js; do
	out=build/${js#*/jquery.}
%if 0%{!?debug:1}
	yuicompressor --charset UTF-8 $js -o $out
	js -C -f $out
%else
	cp -a $js $out
%endif
done

# pack .css
for css in fancybox/*.css; do
	out=build/${css#*/jquery.}
%if 0%{!?debug:1}
	yuicompressor --charset UTF-8 $css -o $out
%else
	cp -a $css $out
%endif
done

cp -a fancybox/*.png build
cp -a fancybox/*.gif build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_examplesdir}/%{name}-%{version}}
cp -a build/* $RPM_BUILD_ROOT%{_appdir}
cp -a demo/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_appdir}

%files demo
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
