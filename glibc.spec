Summary:	GNU libc
Summary(de):	GNU libc
Summary(fr):	GNU libc
Summary(pl):	GNU libc
Summary(tr):	GNU libc
name:		glibc
Version:	2.2
Release:	3
License:	LGPL
Group:		Libraries
Group(de):	Libraries
Group(fr):	Librairies
Group(pl):	Biblioteki
Source0:	ftp://sources.redhat.com/pub/glibc/releases/%{name}-%{version}.tar.bz2
Source1:	ftp://sources.redhat.com/pub/glibc/releases/%{name}-linuxthreads-%{version}.tar.bz2
Source2:	nscd.init
Source3:	nscd.sysconfig
Source4:	nscd.logrotate
Source5:	ldconfig.8
Patch0:		%{name}-info.patch
Patch1:		%{name}-versions.awk_fix.patch
Patch2:		%{name}-pld.patch
Patch3:		%{name}-crypt-blowfish.patch
Patch4:		%{name}-string2-pointer-arith.patch
Patch5:		%{name}-linuxthreads-lock.patch
Patch6:		%{name}-pthread_create-manpage.patch
Patch7:		%{name}-sparc-linux-chown.patch
Patch8:		%{name}-ldconfig.patch
Patch9:		%{name}-getxxxxinfo.patch
URL:		http://www.gnu.org/software/libc/
BuildRequires:	perl
BuildRequires:	gd-devel
BuildRequires:	texinfo
Provides:	ld.so.2
Provides:	ldconfig
Provides:	/sbin/ldconfig
Obsoletes:	%{name}-profile
Obsoletes:	%{name}-debug
Obsoletes:	ldconfig
Autoreq:	false
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Contains the standard libraries that are used by multiple programs on
the system. In order to save disk space and memory, as well as to ease
upgrades, common system code is kept in one place and shared between
programs. This package contains the most important sets of shared
libraries, the standard C library and the standard math library.
Without these, a Linux system will not function. It also contains
national language (locale) support and timezone databases.

%description -l de
Enthält die Standard-Libraries, die von verschiedenen Programmen im
System benutzt werden. Um Festplatten- und Arbeitsspeicher zu sparen
und zur Vereinfachung von Upgrades ist der gemeinsame Systemcode an
einer einzigen Stelle gespeichert und wird von den Programmen
gemeinsam genutzt. Dieses Paket enthält die wichtigsten Sets der
shared Libraries, die Standard-C-Library und die
Standard-Math-Library, ohne die das Linux-System nicht funktioniert.
Ferner enthält es den Support für die verschiedenen Sprachgregionen
(locale) und die Zeitzonen-Datenbank.

%description -l fr
Contient les bibliothèques standards utilisées par de nombreux
programmes du système. Afin d'économiser l'espace disque et mémoire,
et de faciliter les mises à jour, le code commun au système est mis à
un endroit et partagé entre les programmes. Ce paquetage contient les
bibliothèques partagées les plus importantes, la bibliothèque standard
du C et la bibliothèque mathématique standard. Sans celles-ci, un
système Linux ne peut fonctionner. Il contient aussi la gestion des
langues nationales (locales) et les bases de données des zones
horaires.

%description -l pl
W pakiecie znajduj± siê podstawowe biblioteki, u¿ywane przez ró¿ne
programy w Twoim systemie. U¿ywanie przez programy bibliotek z tego
pakietu oszczêdza miejsce na dysku i pamiêæ. Wiekszo¶æ kodu
systemowego jest usytuowane w jednym miejscu i dzielone miêdzy wieloma
programami. Pakiet ten zawiera bardzo wa¿ny zbiór bibliotek
standardowych wspó³dzielonych (dynamicznych) bibliotek C i
matematycznych. Bez glibc system Linux nie jest w stanie funkcjonowaæ.
Znajduj± siê tutaj równie¿ definicje ró¿nych informacji dla wielu
jêzyków (locale) oraz definicje stref czasowych.

%description -l tr
Bu paket, birçok programýn kullandýðý standart kitaplýklarý içerir.
Disk alaný ve bellek kullanýmýný azaltmak ve ayný zamanda güncelleme
iþlemlerini kolaylaþtýrmak için ortak sistem kodlarý tek bir yerde
tutulup programlar arasýnda paylaþtýrýlýr. Bu paket en önemli ortak
kitaplýklarý, standart C kitaplýðýný ve standart matematik kitaplýðýný
içerir. Bu kitaplýklar olmadan Linux sistemi çalýþmayacaktýr. Yerel
dil desteði ve zaman dilimi veri tabaný da bu pakette yer alýr.

%package devel
Summary:	Additional libraries required to compile
Summary(de):	Weitere Libraries zum Kompilieren
Summary(fr):	Librairies supplémentaires nécessaires à la compilation.
Summary(pl):	Dodatkowe biblioteki wymagane podczas kompilacji
Summary(tr):	Geliþtirme için gerekli diðer kitaplýklar
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description devel
To develop programs which use the standard C libraries (which nearly
all programs do), the system needs to have these standard header files
and object files available for creating the executables.

%description -l de devel
Bei der Entwicklung von Programmen, die die Standard-C-Libraries
verwenden (also fast alle), benötigt das System diese Standard-Header-
und Objektdateien zum Erstellen der ausführbaren Programme.

%description -l fr devel
Pour développer des programmes utilisant les bibliothèques standard du
C (ce que presque tous les programmes font), le système doit posséder
ces fichiers en-têtes et objets standards pour créer les exécutables.

%description -l pl devel
Pakiet ten jest niezbêdny przy tworzeniu w³asnych programów
korzystaj±cych ze standardowej biblioteki C. Znajduj± siê tutaj pliki
nag³ówkowe oraz pliki objektowe, niezbêdne do kompilacji programów
wykonywalnych i innych bibliotek.

%description -l tr devel
C kitaplýðýný kullanan (ki hemen hemen hepsi kullanýyor) programlar
geliþtirmek için gereken standart baþlýk dosyalarý ve statik
kitaplýklar.

%package -n nscd
Summary:	Name Service Caching Daemon
Summary(pl):	Name Service Caching Daemon
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Prereq:		/sbin/chkconfig
Requires:	rc-scripts >= 0.2.0

%description -n nscd
nscd caches name service lookups; it can dramatically improve
performance with NIS+, and may help with DNS as well. You cannot use
nscd with 2.0 kernels, due to bugs in the kernel-side thread support.
nscd happens to hit these bugs particularly hard.

%description -n nscd -l pl
nscd zapmiêtuje zapytania i odpowiedzi NIS oraz DNS. Pozwala
drastycznie poprawiæ szybko¶æ dzia³ania NIS+. Nie jest mo¿liwe
u¿ywanie nscd z j±drami serii 2.0.x z powodu b³adów po stronie j±dra w
ods³udze w±tków.

%package -n localedb-src
Summary:	Souce code locale database
Summary(pl):	Kod ¬ród³owy bazy locale
Group:		Daemons
Group(de):	Server
Group(pl):	Serwery

%description -n localedb-src
This add-on package contains the data needed to build the locale data
files to use the internationalization features of the GNU libc. Glibc
package contains standard set of locale binary database and You need
this package if want build some non standard locale database.

%description -l pl -n localedb-src
Pakiet ten kod ¼ród³owy baz locale który jest potrzebny do zbudowania
binarnej wersji baz locale potrzebnej do poprawnego wspierania ró¿nych
jêzyków przez glibc. Pakiet glibc zawira binarn± wersjê standardowych
baz locale i ten pakiet jest potrzebny tylko w sytuacji kiedy potrzeba
wygenerowaæ jak±¶ niestandardow± bazê.

%package -n iconv
Summary:	Convert encoding of given files from one encoding to another
Summary(pl):	Program do konwersji plików tekstowych z jednego enkodingu w inny
Group:		Daemons
Group(de):	Server
Group(pl):	Serwery

%description -n iconv
Convert encoding of given files from one encoding to another. You need
this package if You want to convert some documet from one encoding to
another or if You have installed some programs which use Generic
Character Set Conversion Interface.

%description -l pl -n iconv
Program do konwersji plików tekstowych z jednego enkodingu w inny.
Potrzebujesz mieæ zainstalowany ten pakiet je¿eli wykonujesz konwersjê
dokumentów z jednego enkodingu w inny lub je¿eli masz zainstalowane
jakie¶ programy które korzystaj± z Generic Character Set Conversion
Interface w glibc, czyli z zestawu funkcji z tej biblioteki, które
umo¿liwiaj± konwersjê enkodingu danych z poziomu dowolnego programu.

%package static
Summary:	Static libraries
Summary(pl):	Biblioteki statyczne
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-devel = %{version}

%description static
GNU libc static libraries.

%description -l pl static
Biblioteki statyczne GNU libc.

%package profile
Summary:	glibc with profiling support
Summary(de):	glibc mit Profil-Unterstützung
Summary(fr):	glibc avec support pour profiling
Summary(tr):	Ölçüm desteði olan glibc
Group:		Development/Libraries/Libc
Group(de):	Entwicklung/Libraries/Libc
Group(pl):	Programowanie/Biblioteki/Libc
Obsoletes:	libc-profile
Requires:	%{name}-devel = %{version}

%description profile
When programs are being profiled used gprof, they must use these
libraries instead of the standard C libraries for gprof to be able to
profile them correctly.

%description -l de profile
Damit Programmprofile mit gprof richtig erstellt werden, müssen diese
Libraries anstelle der üblichen C-Libraries verwendet werden.

%description -l tr profile
gprof kullanýlarak ölçülen programlar standart C kitaplýðý yerine bu
kitaplýðý kullanmak zorundadýrlar.

%package pic
Summary:	glibc PIC archive 
Group:		Development/Libraries/Libc
Group(de):	Entwicklung/Libraries/Libc
Group(pl):	Programowanie/Biblioteki/Libc
Requires:	%{name}-devel = %{version}

%description pic
GNU C Library PIC archive contains an archive library (ar file)
composed of individual shared objects. This is used for creating a
library which is a smaller subset of the standard libc shared library.

%package -n nss_compat
Summary:	Old style NYS NSS glibc module
Group:		Base
Group(de):	Gründsätzlich
Group(pl):	Podstawowe
Requires:	%{name} = %{version}

%description -n nss_compat
Old style NYS NSS glibc module

%package -n nss_dns
Summary:	BIND NSS glibc module
Group:		Base
Group(de):	Gründsätzlich
Group(pl):	Podstawowe
Requires:	%{name} = %{version}

%description -n nss_dns
BIND NSS glibc module.

%package -n nss_files
Summary:	Traditional files databases NSS glibc module
Group:		Base
Group(de):	Gründsätzlich
Group(pl):	Podstawowe
Requires:	%{name} = %{version}

%description -n nss_files
Traditional files databases NSS glibc module.

%package -n nss_hesiod
Summary:	Hesiod NSS glibc module
Group:		Base
Group(de):	Gründsätzlich
Group(pl):	Podstawowe
Requires:	%{name} = %{version}

%description -n nss_hesiod
Glibc NSS (Name Service Switch) module for databases acces.

%package -n nss_nis
Summary:	NIS(YP) NSS glibc module
Group:		Base
Group(de):	Gründsätzlich
Group(pl):	Podstawowe
Requires:	%{name} = %{version}

%description -n nss_nis
Glibc NSS (Name Service Switch) module for NIS(YP) databases acces.

%package -n nss_nisplus
Summary:	NIS+ NSS module
Group:		Base
Group(de):	Gründsätzlich
Group(pl):	Podstawowe
Requires:	%{name} = %{version}

%description -n nss_nisplus
Glibc NSS (Name Service Switch) module for NIS+ databases acces.

%package memusage
Summary:	A toy.
Group:		Toys
######		Unknown group!
Requires:	%{name} = %{version}
Requires:	gd

%description memusage
A toy.

%prep
%setup  -q -a 1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p0
%patch9 -p1

%build
%configure \
	--enable-add-ons=linuxthreads \
	--enable-kernel="%{?kernel:%{kernel}}%{!?kernel:2.2.0} \
	--enable-profile \
	--disable-omitfp

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{etc/{rc.d/init.d,sysconfig,logrotate.d},%{_mandir}/man{3,8},var/log}

env LANGUAGE=C LC_ALL=C  \
%{__make} install \
	install_root=$RPM_BUILD_ROOT \
	infodir=%{_infodir} \
	mandir=%{_mandir}

env LANGUAGE=C LC_ALL=C  \
%{__make} install-locales -C localedata \
	install_root=$RPM_BUILD_ROOT

PICFILES="libc_pic.a libc.map 
          math/libm_pic.a libm.map 
          resolv/libresolv_pic.a"

install $PICFILES $RPM_BUILD_ROOT/%{_libdir}
install elf/soinit.os $RPM_BUILD_ROOT/%{_libdir}/soinit.o
install elf/sofini.os $RPM_BUILD_ROOT/%{_libdir}/sofini.o

mv -f $RPM_BUILD_ROOT/lib/libmemusage.so $RPM_BUILD_ROOT%{_libdir}
mv -f $RPM_BUILD_ROOT/lib/libpcprofile.so $RPM_BUILD_ROOT%{_libdir}

%{__make} -C linuxthreads/man
install linuxthreads/man/*.3thr $RPM_BUILD_ROOT%{_mandir}/man3

rm -rf $RPM_BUILD_ROOT%{_datadir}/zoneinfo/{localtime,posixtime,posixrules}

ln -sf ../../..%{_sysconfdir}/localtime $RPM_BUILD_ROOT%{_datadir}/zoneinfo/localtime
ln -sf localtime $RPM_BUILD_ROOT%{_datadir}/zoneinfo/posixtime
ln -sf localtime $RPM_BUILD_ROOT%{_datadir}/zoneinfo/posixrules
ln -sf ../..%{_libdir}/libbsd-compat.a $RPM_BUILD_ROOT%{_libdir}/libbsd.a

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/localtime

install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/nscd
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/nscd
install %{SOURCE4} $RPM_BUILD_ROOT/etc/logrotate.d/nscd
install nscd/nscd.conf $RPM_BUILD_ROOT%{_sysconfdir}
install nss/nsswitch.conf $RPM_BUILD_ROOT%{_sysconfdir}


install %{SOURCE5} $RPM_BUILD_ROOT%{_mandir}/man8/
touch	$RPM_BUILD_ROOT%{_sysconfdir}/ld.so.{cache,conf}

:> $RPM_BUILD_ROOT/var/log/nscd

rm -rf documentation
install -d documentation

cp linuxthreads/ChangeLog  documentation/ChangeLog.threads
cp linuxthreads/Changes documentation/Changes.threads
cp linuxthreads/README documentation/README.threads
cp crypt/README.ufc-crypt documentation/

cp ChangeLog ChangeLog.8 documentation

gzip -9nf README NEWS FAQ BUGS NOTES PROJECTS documentation/*

# Collect locale files and mark them with %%lang()
rm -f glibc.lang
for i in $RPM_BUILD_ROOT%{_datadir}/locale/* $RPM_BUILD_ROOT%{_libdir}/locale/* ; do
	if [ -d $i ]; then
		lang=`echo $i | sed -e 's/.*locale\///' -e 's/\/.*//'`
		dir=`echo $i | sed "s#$RPM_BUILD_ROOT##"`
		echo "%lang($lang) $dir" >>glibc.lang
	fi

done

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%post -n nscd
/sbin/chkconfig --add nscd
touch /var/log/nscd && (chown root.root /var/log/nscd ; chmod 640 /var/log/nscd)
if [ -f /var/lock/subsys/nscd ]; then
	/etc/rc.d/init.d/nscd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/nscd start\" to start nscd daemon." 1>&2
fi

%preun -n nscd
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/nscd ]; then
		/etc/rc.d/init.d/nscd stop 1>&2
	fi
	/sbin/chkconfig --del nscd
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files -f glibc.lang
%defattr(644,root,root,755)
%doc {README,NEWS,FAQ,BUGS}.gz

%config(noreplace) %verify(not mtime md5 size) %{_sysconfdir}/nsswitch.conf
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/ld.so.conf
%config %{_sysconfdir}/rpc
%ghost %{_sysconfdir}/ld.so.cache

%attr(755,root,root) /sbin/*
%attr(755,root,root) %{_bindir}/catchsegv
%attr(755,root,root) %{_bindir}/getent
%attr(755,root,root) %{_bindir}/glibcbug
%attr(755,root,root) %{_bindir}/ldd
%attr(755,root,root) %{_bindir}/lddlibc4
%attr(755,root,root) %{_bindir}/locale
%attr(755,root,root) %{_bindir}/rpcgen
%attr(755,root,root) %{_bindir}/tzselect

%attr(755,root,root) %{_sbindir}/rpcinfo
%attr(755,root,root) %{_sbindir}/zdump
%attr(755,root,root) %{_sbindir}/zic

%attr(755,root,root) /lib/ld-*
%attr(755,root,root) /lib/libdl*
%attr(755,root,root) /lib/libnsl*
%attr(755,root,root) /lib/lib[BScmprtu]*

%dir %{_datadir}/locale
%{_datadir}/locale/locale.alias
%{_datadir}/zoneinfo

%dir %{_libdir}/locale

%{_mandir}/man8/ldconfig*

#%files -n nss_dns
%defattr(644,root,root,755)
%attr(755,root,root) /lib/libnss_dns*.so*

#%files -n nss_files
%defattr(644,root,root,755)
%attr(755,root,root) /lib/libnss_files*.so*

%files -n nss_compat
%defattr(644,root,root,755)
%attr(755,root,root) /lib/libnss_compat*.so*

%files -n nss_hesiod
%defattr(644,root,root,755)
%attr(755,root,root) /lib/libnss_hesiod*.so*

%files -n nss_nis
%defattr(644,root,root,755)
%attr(755,root,root) /lib/libnss_nis.so.*
%attr(755,root,root) /lib/libnss_nis-*.so

%files -n nss_nisplus
%defattr(644,root,root,755)
%attr(755,root,root) /lib/libnss_nisplus*.so*

%files memusage
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/memusage*

%files devel
%defattr(644,root,root,755)
%doc documentation/* {NOTES,PROJECTS}.gz
%attr(755,root,root) %{_bindir}/gencat
%attr(755,root,root) %{_bindir}/getconf
%attr(755,root,root) %{_bindir}/*prof*
%attr(755,root,root) %{_bindir}/*trace

%{_includedir}/*.h
%{_includedir}/arpa
%{_includedir}/bits
%{_includedir}/gnu
%{_includedir}/net
%{_includedir}/netash
%{_includedir}/netatalk
%{_includedir}/netax25
%{_includedir}/neteconet
%{_includedir}/netinet
%{_includedir}/netipx
%{_includedir}/netpacket
%{_includedir}/netrom
%{_includedir}/netrose
%{_includedir}/nfs
%{_includedir}/protocols
%{_includedir}/rpc
%{_includedir}/rpcsvc
%{_includedir}/scsi
%{_includedir}/sys

%{_infodir}/libc.inf*.gz

%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_libdir}/*crt*.o
%{_libdir}/libc_nonshared.a

%{_mandir}/man3/*

%files -n nscd
%defattr(644,root,root,755)
%attr(640,root,root) %config %verify(not size mtime md5) /etc/sysconfig/nscd
%attr(640,root,root) %config(noreplace) %verify(not mtime md5 size) %{_sysconfdir}/nscd.*
%attr(754,root,root) /etc/rc.d/init.d/nscd
%attr(755,root,root) %{_sbindir}/nscd*
%attr(640,root,root) /etc/logrotate.d/nscd
%attr(640,root,root) %ghost /var/log/nscd

%files -n localedb-src
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/localedef
%{_datadir}/i18n

%files -n iconv
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/iconv
%dir %{_libdir}/gconv
%{_libdir}/gconv/gconv-modules
%attr(755,root,root) %{_libdir}/gconv/*.so

%files static
%defattr(644,root,root,755)
%{_libdir}/libBrokenLocale.a
%{_libdir}/libbsd-compat.a
%{_libdir}/libbsd.a
%{_libdir}/libc.a
%{_libdir}/libcrypt.a
%{_libdir}/libdl.a
%{_libdir}/libg.a
%{_libdir}/libieee.a
%{_libdir}/libm.a
%{_libdir}/libmcheck.a
%{_libdir}/libnsl.a
%{_libdir}/libpthread.a
%{_libdir}/libresolv.a
%{_libdir}/librpcsvc.a
%{_libdir}/librt.a
%{_libdir}/libutil.a

%files profile
%defattr(644,root,root,755)
%{_libdir}/lib*_p.a

%files pic
%defattr(644,root,root,755)
%{_libdir}/lib*_pic.a
%{_libdir}/lib*.map
%{_libdir}/soinit.o
%{_libdir}/sofini.o
