#
# Conditional build:
%bcond_without	license_agreement	# generates package

%define		base_name	adobe-air
%define		rel 1
Summary:	Adobe Integrated Runtime
%if %{with license_agreement}
Name:		%{base_name}
%else
Name:		%{base_name}-installer
%endif
Version:	2.6.0.19140
Release:	%{rel}%{?with_license_agreement:wla}
License:	Commercial, non-distributable
Group:		X11/Applications/Multimedia
%if %{with license_agreement}
Source0:	http://airdownload.adobe.com/air/lin/download/latest/AdobeAIRInstaller.bin
# NoSource0-md5:	9a751473ff4386a72f65dc7decc56fb9
NoSource:	0
%endif
Source2:	http://svn.pld-linux.org/svn/license-installer/license-installer.sh
# Source2-md5:	329c25f457fea66ec502b7ef70cb9ede
URL:		http://www.adobe.com/products/air/
%if %{with license_agreement}
BuildRequires:	perl-base
Requires:	adobe-certs
Suggests:	gnome-keyring
Suggests:	kdeutils-kwalletmanager
Obsoletes:	adobeair
%else
Requires:	rpm-build-tools >= 4.4.37
Requires:	rpmbuild(macros) >= 1.544
%endif
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# No debuginfo to be stored
%define		_enable_debug_packages	0
# fail on file names containing spaces
%define		no_install_post_strip			1

%description
Adobe Integrated Runtime.

%package -n adobe-certs
Summary:	Adobe Certificates
Group:		Libraries

%description -n adobe-certs
Certificates distributed by Adobe Systems.

%prep
%if %{with license_agreement}
%setup -q -T -c
perl -ne 'if($lzma_start) {print} elsif(/(]\000\000\200\000.*)/) {print "$1\n"; $lzma_start=1}' %{SOURCE0} | lzma -d > %{name}-%{version}.tar || :
tar xvf %{name}-%{version}.tar
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{without license_agreement}
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{base_name}}

sed -e '
	s/@BASE_NAME@/%{base_name}/g
	s/@TARGET_CPU@/%{_target_cpu}/g
	s-@VERSION@-%{version}-g
	s-@RELEASE@-%{release}-g
	s,@SPECFILE@,%{_datadir}/%{base_name}/%{base_name}.spec,g
	s,@DATADIR@,%{_datadir}/%{base_name},g
' %{SOURCE2} > $RPM_BUILD_ROOT%{_bindir}/%{base_name}.install

install %{_specdir}/%{base_name}.spec $RPM_BUILD_ROOT%{_datadir}/%{base_name}

%else

install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_bindir},%{_libdir},%{_datadir}/mime/packages,%{_desktopdir},%{_iconsdir}/hicolor,{%{_var},}/opt}

cp -a build/etc/opt $RPM_BUILD_ROOT%{_sysconfdir}
cp -a build/opt/Adobe\ AIR $RPM_BUILD_ROOT/opt
cp -a build/var/opt/Adobe\ AIR $RPM_BUILD_ROOT%{_var}/opt

%{__mv} $RPM_BUILD_ROOT{/opt/Adobe\ AIR/Versions/1.0/Resources/aucm,%{_bindir}}
%{__mv} $RPM_BUILD_ROOT{/opt/Adobe\ AIR/Versions/1.0/Resources/libadobecertstore.so,%{_libdir}}
%{__mv} $RPM_BUILD_ROOT{/opt/Adobe\ AIR/Versions/1.0/Resources/support/icons/*,%{_iconsdir}/hicolor}
%{__mv} $RPM_BUILD_ROOT{/opt/Adobe\ AIR/Versions/1.0/Resources/support/AdobeAIR.desktop,%{_desktopdir}}
%{__mv} $RPM_BUILD_ROOT{/opt/Adobe\ AIR/Versions/1.0/Resources/support/AdobeAIR.xml,%{_datadir}/mime/packages}
%{__rm} -r $RPM_BUILD_ROOT/opt/Adobe\ AIR/Versions/1.0/Resources/{appinstall,control,xdg-utils,{appinstall,control}.spec,application.d{esktop,irectory},pkcon_air,setup.deb}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%if %{without license_agreement}
%{_bindir}/%{base_name}.install
%else
[ ! -x /usr/bin/update-desktop-database ] || %update_desktop_database
%postun
[ ! -x /usr/bin/update-desktop-database ] || %update_desktop_database
%endif

%files
%defattr(644,root,root,755)
%if %{without license_agreement}
%attr(755,root,root) %{_bindir}/%{base_name}.install
%{_datadir}/%{base_name}
%else
%dir "/opt/Adobe AIR"
%dir "/opt/Adobe AIR/Versions"
%dir "/opt/Adobe AIR/Versions/1.0/"
"/opt/Adobe AIR/Versions/1.0/Adobe AIR Application Installer.swf"
%attr(755,root,root) "/opt/Adobe AIR/Versions/1.0/Adobe AIR Application Installer"
%attr(755,root,root) "/opt/Adobe AIR/Versions/1.0/libCore.so"
%dir "/opt/Adobe AIR/Versions/1.0/Resources"
%lang(cs) "/opt/Adobe AIR/Versions/1.0/Resources/cs.lproj"
%lang(de) "/opt/Adobe AIR/Versions/1.0/Resources/de.lproj"
%lang(en) "/opt/Adobe AIR/Versions/1.0/Resources/en.lproj"
%lang(es) "/opt/Adobe AIR/Versions/1.0/Resources/es.lproj"
%lang(fr) "/opt/Adobe AIR/Versions/1.0/Resources/fr.lproj"
%lang(it) "/opt/Adobe AIR/Versions/1.0/Resources/it.lproj"
%lang(ja) "/opt/Adobe AIR/Versions/1.0/Resources/ja.lproj"
%lang(ko) "/opt/Adobe AIR/Versions/1.0/Resources/ko.lproj"
%lang(nl) "/opt/Adobe AIR/Versions/1.0/Resources/nl.lproj"
%lang(pl) "/opt/Adobe AIR/Versions/1.0/Resources/pl.lproj"
%lang(pt) "/opt/Adobe AIR/Versions/1.0/Resources/pt.lproj"
%lang(ru) "/opt/Adobe AIR/Versions/1.0/Resources/ru.lproj"
%lang(sv) "/opt/Adobe AIR/Versions/1.0/Resources/sv.lproj"
%lang(tr) "/opt/Adobe AIR/Versions/1.0/Resources/tr.lproj"
%lang(zh_CN) "/opt/Adobe AIR/Versions/1.0/Resources/zh_Hans.lproj"
%lang(zh_TW) "/opt/Adobe AIR/Versions/1.0/Resources/zh_Hant.lproj"
%attr(755,root,root) "/opt/Adobe AIR/Versions/1.0/Resources/Adobe AIR Updater"
%attr(755,root,root) "/opt/Adobe AIR/Versions/1.0/Resources/airappinstaller"
%attr(755,root,root) "/opt/Adobe AIR/Versions/1.0/Resources/appentry"
%attr(755,root,root) "/opt/Adobe AIR/Versions/1.0/Resources/installCertificate"
%attr(755,root,root) "/opt/Adobe AIR/Versions/1.0/Resources/lib*.so
%attr(755,root,root) "/opt/Adobe AIR/Versions/1.0/Resources/rpmbuilder"
"/opt/Adobe AIR/Versions/1.0/Resources/AdobeAIR.png"
"/opt/Adobe AIR/Versions/1.0/Resources/curl-ca-bundle.crt"
"/opt/Adobe AIR/Versions/1.0/Resources/digest.s"
"/opt/Adobe AIR/Versions/1.0/Resources/nss3"
/opt/Adobe*AIR/Versions/1.0/Resources/*.cer
/opt/Adobe*AIR/Versions/1.0/Resources/*.swf
/opt/Adobe*AIR/Versions/1.0/Resources/*.vch
%{_datadir}/mime/packages/AdobeAIR.xml
%{_desktopdir}/AdobeAIR.desktop
%{_iconsdir}/hicolor/12x12/*.png
%{_iconsdir}/hicolor/16x16/*.png
%{_iconsdir}/hicolor/20x20/*.png
%{_iconsdir}/hicolor/22x22/*.png
%{_iconsdir}/hicolor/24x24/*.png
%{_iconsdir}/hicolor/32x32/*.png
%{_iconsdir}/hicolor/36x36/*.png
%{_iconsdir}/hicolor/48x48/*.png
%{_iconsdir}/hicolor/64x64/*.png
%{_iconsdir}/hicolor/96x96/*.png
%{_iconsdir}/hicolor/128x128/*.png
%{_iconsdir}/hicolor/192x192/*.png
%attr(1777,root,root) "%{_var}/opt/Adobe AIR"

%files -n adobe-certs
%defattr(644,root,root,755)
%{_sysconfdir}/opt/Adobe
%attr(755,root,root) %{_bindir}/aucm
%attr(755,root,root) %{_libdir}/libadobecertstore.so
%endif
