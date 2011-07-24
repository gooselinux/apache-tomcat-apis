Name:		apache-tomcat-apis
Version:	0.1
Release:	1%{?dist}
Summary:	Tomcat Servlet and JSP APIs

Group:		System/Libraries
License:	ASL 2.0
URL:		http://tomcat.apache.org/
Source0:	%{name}-%{version}.tar.bz2
# These MANIFESTs come from the Eclipse Orbit project
# http://eclipse.org/orbit
Source1:	%{name}-servlet2.4-OSGi-MANIFEST.MF
Source2:	%{name}-jsp2.0-OSGi-MANIFEST.MF
Source3:	%{name}-servlet2.5-OSGi-MANIFEST.MF
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch:	noarch
BuildRequires:	ant
# For %%{_javadir} definition
Requires:       jpackage-utils

%description
Apache Tomcat's Servlet 2.4/JSP 2.0 and Servlet 2.5/JSP 2.1 APIs.

%prep
%setup -q

%build
pushd servlet2.4jsp2.0
cd jsr154
ant jar
pushd dist/lib
# inject OSGi manifest
unzip -q servlet-api.jar
cp -p %{SOURCE1} META-INF/MANIFEST.MF
zip -qr servlet-api.jar javax META-INF
popd

cd ../jsr152
ant jar
pushd dist/lib
# inject OSGi manifest
unzip -q jsp-api.jar
cp -p %{SOURCE2} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -qr jsp-api.jar javax META-INF
popd
popd

pushd servlet2.5jsp2.1
ant
cd output
# inject OSGi manifest
unzip -q servlet-api.jar
cp -p %{SOURCE3} META-INF/MANIFEST.MF
zip -qr servlet-api.jar javax META-INF
popd

%install
rm -rf %{buildroot}
install -m 755 -d %{buildroot}/%{_javadir}/%{name}
install -m 644 \
  servlet2.4jsp2.0/jsr154/dist/lib/servlet-api.jar \
  %{buildroot}/%{_javadir}/%{name}/tomcat-servlet2.4-api.jar
install -m 644 \
  servlet2.4jsp2.0/jsr152/dist/lib/jsp-api.jar \
  %{buildroot}/%{_javadir}/%{name}/tomcat-jsp2.0-api.jar
install -m 644 \
  servlet2.5jsp2.1/output/servlet-api.jar \
  %{buildroot}/%{_javadir}/%{name}/tomcat-servlet2.5-api.jar
install -m 644 \
  servlet2.5jsp2.1/output/jsp-api.jar \
  %{buildroot}/%{_javadir}/%{name}/tomcat-jsp2.1-api.jar

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc servlet2.4jsp2.0/jsr152/dist/LICENSE
%{_javadir}/%{name}/tomcat-servlet2.4-api.jar
%{_javadir}/%{name}/tomcat-jsp2.0-api.jar
%{_javadir}/%{name}/tomcat-servlet2.5-api.jar
%{_javadir}/%{name}/tomcat-jsp2.1-api.jar

%changelog
* Tue Feb 02 2010 Andrew Overholt <overholt@redhat.com> 0.1-1
- Initial package
