Summary:	GNU libc
Summary(de):	GNU libc
Summary(fr):	GNU libc
Summary(pl):	GNU libc
Summary(tr):	GNU libc
name:		glibc
Version:	2.1.3
Release:	20
License:	LGPL
Group:		Libraries
Group(fr):	Librairies
Group(pl):	Biblioteki
Source0:	ftp://sourceware.cygnus.com/pub/glibc/%{name}-%{version}.tar.bz2
Source1:	ftp://sourceware.cygnus.com/pub/glibc/%{name}-linuxthreads-%{version}.tar.gz
Source2:	http://www.ozemail.com.au/~geoffk/glibc-crypt/%{name}-crypt-2.1.1.tar.gz
Source3:	utmpd.init
Source4:	nscd.init
Source5:	utmpd.sysconfig
Source6:	nscd.sysconfig
Source7:	nscd.logrotate
Source10:	ftp://ftp.yggdrasil.com/private/hjl/ldconfig-980708.tar.gz
Source11:	ldconfig.8
Patch0:		glibc-2.1-CVS-20000905.patch.bz2
Patch1:		glibc-info.patch
Patch2:		glibc-versions.awk_fix.patch
Patch3:		glibc-pld.patch
Patch4:		glibc-crypt-blowfish.patch
Patch5:		glibc-string2-pointer-arith.patch
Patch6:		glibc-db2-alpha-mutex.patch
Patch7:		glibc-linuxthreads-lock.patch
Patch8:		glibc-pthread_create-manpage.patch
Patch9:		glibc-sparc-linux-chown.patch
Patch10:	ldconfig-glibc.patch
Patch11:	ldconfig-bklinks.patch
Patch12:	glibc-cvs-20000824-md5-align-clean.patch.gz
URL:		http://www.gnu.org/software/libc/
BuildRequires:	perl
Provides:	ld.so.2
Provides:	ldconfig
Provides:	/sbin/ldconfig
Obsoletes:	%{name}-profile
Obsoletes:	%{name}-debug
Obsoletes:	ldconfig
Prereq:		basesystem
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

%package -n nss_compat
Summary:	Old style NYS NSS glibc module
Group:		Base
Requires:	%{name} = %{version}

%description -n nss_compat
Old style NYS NSS glibc module

%package -n nss_db
Summary:	Berkeley DB NSS glibc module
Group:		Base
Requires:	%{name} = %{version}

%description -n nss_db
Berkeley DB NSS glibc module.

%package -n nss_dns
Summary:	BIND NSS glibc module
Group:		Base
Requires:	%{name} = %{version}

%description -n nss_dns
BIND NSS glibc module.

%package -n nss_files
Summary:	Traditional files databases NSS glibc module
Group:		Base
Requires:	%{name} = %{version}

%description -n nss_files
Traditional files databases NSS glibc module.

%package -n nss_hesiod
Summary:	Hesiod NSS glibc module
Group:		Base
Requires:	%{name} = %{version}

%description -n nss_hesiod
Glibc NSS (Name Service Switch) module for databases acces.

%package -n nss_nis
Summary:	NIS(YP) NSS glibc module
Group:		Base
Requires:	%{name} = %{version}

%description -n nss_nis
Glibc NSS (Name Service Switch) module for NIS(YP) databases acces.

%package -n nss_nisplus
Summary:	NIS+ NSS module
Group:		Base
Requires:	%{name} = %{version}

%description -n nss_nisplus
Glibc NSS (Name Service Switch) module for NIS+ databases acces.

%package -n nscd
Summary:	Name Service Caching Daemon
Summary(pl):	Name Service Caching Daemon
Group:		Networking/Daemons
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

%package -n utmpd
Summary:	utmp and utmpx synchronizer for libc5 applications.
Summary(pl):	Synchrnnizuje zapis do plików utmp i utmpx.
Group:		Daemons
Group(pl):	Serwery
Prereq:		/sbin/chkconfig
Requires:	rc-scripts >= 0.2.0

%description -n utmpd
utmpd is a utmp and utmpx synchronizer. Is only needed for libc5 based
program with utmp access.

%description -n utmpd -l pl
utmpd stara siê utrzymaæ tak± sam± zawarto¶æ plików /var/run/utmp i
/var/run/utmpx. Potrzebny jest tylko w przypadku korzystania ze
starszych programów (bazuj±cych na libc5).

%package -n localedb-src
Summary:	Souce code locale database
Summary(pl):	Kod ¬ród³owy bazy locale
Group:		Daemons
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
Summary:        glibc PIC archive 
Group:          Development/Libraries/Libc
Group(pl):      Programowanie/Biblioteki/Libc
Requires:       %{name}-devel = %{version}

%description pic
GNU C Library PIC archive contains an archive library (ar file) composed
of individual shared objects. This is used for creating a library which
is a smaller subset of the standard libc shared library.

%package db1
Summary:	BSD database library for C
Group:		Libraries
PreReq:		/sbin/ldconfig
Provides:	db1

%description db1
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
It should be installed if compatibility is needed with databases created with
db1. This library used to be part of the glibc package.

%package db1-devel
Summary:	Development libraries and header files for Berkeley database library
Group:		Development/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-db1 = %{version}
Provides:	db1-devel

%description db1-devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB includes B tree, Hashing, Fixed and Variable-length record access
methods.

This package contains the header files, libraries, and documentation
for building programs which use Berkeley DB.

%package db1-static
Summary:	Static libraries for Berkeley database library
Group:		Development/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-db1-devel = %{version}
Provides:	db1-static

%description db1-static
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB includes B tree, Hashing, Fixed and Variable-length record access
methods.

This package contains the static libraries for building programs which use
Berkeley DB.

%package db2
Summary:	BSD database library for C
Group:		Libraries
PreReq:		/sbin/ldconfig
Provides:	db2

%description db2
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
This library used to be part of the glibc package.

%package db2-devel
Summary:	Development libraries and header files for Berkeley database library
Group:		Development/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-db2 = %{version}
Provides:	db2-devel

%description db2-devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB includes B tree, Hashing, Fixed and Variable-length record access
methods.

This package contains the header files, libraries, and documentation
for building programs which use Berkeley DB.

%package db2-static
Summary:	Static libraries for Berkeley database library
Group:		Development/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-db2-devel = %{version}
Provides:	db2-static

%description db2-static
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB includes B tree, Hashing, Fixed and Variable-length record access
methods.

This package contains the static libraries for building programs which use
Berkeley DB.

%prep
%setup -q -a 1 -a 2 -a 10
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch12 -p1
cd ldconfig-980708
%patch10 -p1
%patch11 -p1

%build
%configure \
	--enable-add-ons=crypt,linuxthreads \
	--enable-profile \
	--disable-omitfp

%{__make}

cd ldconfig-980708
rm -f ldconfig
gcc -c $RPM_OPT_FLAGS -D_LIBC ldconfig.c -o ldconfig.o

%ifarch alpha
gcc -nostdlib -nostartfiles -static -o ldconfig ../csu/crt1.o \
	../csu/crti.o ../csu/crtbegin.o ldconfig.o \
	../libc.a -lgcc ../libc.a ../csu/crtend.o \
	../csu/crtn.o
%else
gcc -nostdlib -nostartfiles -static -o ldconfig ../csu/crt1.o \
	../csu/crti.o `gcc --print-file-name=crtbegin.o` ldconfig.o \
	../libc.a -lgcc ../libc.a `gcc --print-file-name=crtend.o` \
	../csu/crtn.o
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{etc/{rc.d/init.d,sysconfig,logrotate.d},%{_mandir}/man{3,8},var/{db,log}}

%{__make} install \
	install_root=$RPM_BUILD_ROOT \
	infodir=%{_infodir} \
	mandir=%{_mandir}

%{__make} install-locales -C localedata \
	install_root=$RPM_BUILD_ROOT

PICFILES="libc_pic.a libc.map 
          math/libm_pic.a libm.map 
          resolv/libresolv_pic.a"

install $PICFILES $RPM_BUILD_ROOT/%{_libdir}
install elf/soinit.os $RPM_BUILD_ROOT/%{_libdir}/soinit.o
install elf/sofini.os $RPM_BUILD_ROOT/%{_libdir}/sofini.o

%{__make} -C linuxthreads/man
install linuxthreads/man/*.3thr $RPM_BUILD_ROOT%{_mandir}/man3

rm -rf $RPM_BUILD_ROOT%{_datadir}/zoneinfo/{localtime,posixtime,posixrules}

ln -sf ../../..%{_sysconfdir}/localtime $RPM_BUILD_ROOT%{_datadir}/zoneinfo/localtime
ln -sf localtime $RPM_BUILD_ROOT%{_datadir}/zoneinfo/posixtime
ln -sf localtime $RPM_BUILD_ROOT%{_datadir}/zoneinfo/posixrules
ln -sf libbsd-compat.a $RPM_BUILD_ROOT%{_libdir}/libbsd.a
ln -sf libdb.a $RPM_BUILD_ROOT%{_libdir}/libdb2.a
ln -sf ../../lib/libdb.so.3 $RPM_BUILD_ROOT%{_libdir}/libdb2.so
ln -sf libdb.so.3 $RPM_BUILD_ROOT/lib/libdb2.so.3

%ifarch alpha
ln -sf libdb.so.2.1 $RPM_BUILD_ROOT/lib/libdb.so.2
%endif

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/localtime

install %{SOURCE4} $RPM_BUILD_ROOT/etc/rc.d/init.d/nscd
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/utmpd
install %{SOURCE6} $RPM_BUILD_ROOT/etc/sysconfig/nscd
install %{SOURCE5} $RPM_BUILD_ROOT/etc/sysconfig/utmpd
install %{SOURCE7} $RPM_BUILD_ROOT/etc/logrotate.d/nscd
install nscd/nscd.conf $RPM_BUILD_ROOT%{_sysconfdir}
install nss/nsswitch.conf $RPM_BUILD_ROOT%{_sysconfdir}

install -s ldconfig-980708/ldconfig $RPM_BUILD_ROOT/sbin/ldconfig

install %{SOURCE11} $RPM_BUILD_ROOT%{_mandir}/man8
touch	$RPM_BUILD_ROOT%{_sysconfdir}/ld.so.{cache,conf}

install nss/db-Makefile $RPM_BUILD_ROOT/var/db/Makefile
:> $RPM_BUILD_ROOT/var/log/nscd

cat << EOF > $RPM_BUILD_ROOT%{_bindir}/create-db
#!/bin/sh
/usr/bin/make -sC /var/db/
EOF

ln -sf create-db $RPM_BUILD_ROOT%{_bindir}/update-db

rm -rf documentation
install -d documentation

cp linuxthreads/ChangeLog  documentation/ChangeLog.threads
cp linuxthreads/Changes documentation/Changes.threads
cp linuxthreads/README documentation/README.threads
cp crypt/README documentation/README.crypt
cp ldconfig-980708/README ldconfig-980708/README.ldconfig

cp ChangeLog ChangeLog.8 documentation

gzip -9nf README NEWS FAQ BUGS NOTES PROJECTS \
	$RPM_BUILD_ROOT{%{_mandir}/man*/*,%{_infodir}/libc*} \
	documentation/* login/README.utmpd ldconfig-980708/README.ldconfig

strip $RPM_BUILD_ROOT/{sbin/*,usr/{sbin/*,bin/*}} ||:
strip --strip-unneeded $RPM_BUILD_ROOT/lib/lib*.so.* \
	$RPM_BUILD_ROOT%{_libdir}/gconv/*.so

# Collect locale files and mark them with %%lang()
rm -f glibc.lang
for i in $RPM_BUILD_ROOT%{_datadir}/locale/* ; do
	if [ -d $i ]; then
		lang=`echo $i | sed -e 's/.*locale\///' -e 's/^\(..\).*/\1/'`
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

%post -n utmpd
/sbin/chkconfig --add utmpd
if [ -f /var/lock/subsys/utmpd ]; then
	/etc/rc.d/init.d/utmpd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/utmpd start\" to start utmpd daemon." 1>&2
fi

%preun -n utmpd
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/utmpd ]; then
		/etc/rc.d/init.d/utmpd stop 1>&2
	fi
	/sbin/chkconfig --del utmpd
fi

%post db1  -p /sbin/ldconfig
%postun db1 -p /sbin/ldconfig

%post db2  -p /sbin/ldconfig
%postun db2 -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files -f glibc.lang
%defattr(644,root,root,755)
%doc {README,NEWS,FAQ,BUGS,ldconfig-980708/README.ldconfig}.gz

%config(noreplace) %verify(not mtime md5 size) %{_sysconfdir}/nsswitch.conf
%config %{_sysconfdir}/rpc

%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/ld.so.conf
%ghost %{_sysconfdir}/ld.so.cache

%attr(755,root,root) /sbin/*
%attr(755,root,root) %{_bindir}/catchsegv
%attr(755,root,root) %{_bindir}/create-db
%attr(755,root,root) %{_bindir}/getent
%attr(755,root,root) %{_bindir}/glibcbug
%attr(755,root,root) %{_bindir}/ldd
%ifnarch alpha
%attr(755,root,root) %{_bindir}/lddlibc4
%endif
%attr(755,root,root) %{_bindir}/locale
%attr(755,root,root) %{_bindir}/makedb
%attr(755,root,root) %{_bindir}/rpcgen
%attr(755,root,root) %{_bindir}/tzselect
%attr(755,root,root) %{_bindir}/update-db

%attr(755,root,root) %{_sbindir}/rpcinfo
%attr(755,root,root) %{_sbindir}/zdump
%attr(755,root,root) %{_sbindir}/zic

%attr(755,root,root) /lib/ld-*
%attr(755,root,root) /lib/libdl*
%attr(755,root,root) /lib/libnsl*
%attr(755,root,root) /lib/lib[BScmprtu]*

%{_mandir}/man8/*

%dir %{_datadir}/locale
%{_datadir}/locale/locale.alias
%{_datadir}/zoneinfo

#%files -n nss_db
%defattr(644,root,root,755)
%attr(755,root,root) /lib/libnss_db*.so*
%config /var/db/Makefile

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

%files devel
%defattr(644,root,root,755)
%doc documentation/* {NOTES,PROJECTS}.gz
%attr(755,root,root) %{_bindir}/gencat
%attr(755,root,root) %{_bindir}/getconf
%attr(755,root,root) %{_bindir}/mtrace
%attr(755,root,root) %{_bindir}/sprof

%{_includedir}/*.h
%ifarch alpha
%{_includedir}/alpha
%endif
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

%attr(755,root,root) %{_libdir}/lib[A-Z]*.so
%attr(755,root,root) %{_libdir}/libc*.so
%attr(755,root,root) %{_libdir}/libdl*.so
%attr(755,root,root) %{_libdir}/libm*.so
%attr(755,root,root) %{_libdir}/libns*.so
%attr(755,root,root) %{_libdir}/lib[p-z]*.so
%attr(755,root,root) %{_libdir}/*crt*.o
%{_libdir}/libc_nonshared.a

%{_mandir}/man3/*

%files -n nscd
%defattr(644,root,root,755)
%attr(640,root,root) %config %verify(not size mtime md5) /etc/sysconfig/nscd
%attr(640,root,root) %config(noreplace) %verify(not mtime md5 size) %{_sysconfdir}/nscd.*
%attr(754,root,root) /etc/rc.d/init.d/nscd
%attr(755,root,root) %{_sbindir}/nscd
%attr(640,root,root) /etc/logrotate.d/nscd
%attr(640,root,root) %ghost /var/log/nscd

%files -n utmpd
%defattr(644,root,root,755)
%doc login/README.utmpd.gz
%attr(640,root,root) %config %verify(not size mtime md5) /etc/sysconfig/utmpd
%attr(754,root,root) /etc/rc.d/init.d/utmpd
%attr(755,root,root) %{_sbindir}/utmpd

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
%{_libdir}/libposix.a
%{_libdir}/libpthread.a
%{_libdir}/libresolv.a
%{_libdir}/librpcsvc.a
%{_libdir}/librt.a
%{_libdir}/libutil.a

%files profile
%defattr(644,root,root,755)
%{_libdir}/libBrokenLocale_p.a
%{_libdir}/libc_p.a
%{_libdir}/libcrypt_p.a
%{_libdir}/libdl_p.a
%{_libdir}/libm_p.a
%{_libdir}/libnsl_p.a
%{_libdir}/libpthread_p.a
%{_libdir}/libresolv_p.a
%{_libdir}/librpcsvc_p.a
%{_libdir}/librt_p.a
%{_libdir}/libutil_p.a

%files pic
%defattr(644,root,root,755)
%{_libdir}/lib*_pic.a
%{_libdir}/lib*.map
%{_libdir}/soinit.o
%{_libdir}/sofini.o

%files db1
%defattr(644,root,root,755)
%attr(755,root,root) /lib/libdb1*
%attr(755,root,root) /lib/libdb.so.2
%ifarch alpha
%attr(755,root,root) /lib/libdb.so.2.1
%endif

%files db1-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/db_dump185
%attr(755,root,root) %{_libdir}/libdb1.so
%{_includedir}/db1

%files db1-static
%defattr(644,root,root,755)
%{_libdir}/libdb1.a

%files db2
%defattr(644,root,root,755)
%attr(755,root,root) /lib/libdb-*
%attr(755,root,root) /lib/libdb.so.3
%attr(755,root,root) /lib/libdb2.so.3

%files db2-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/db_archive
%attr(755,root,root) %{_bindir}/db_checkpoint
%attr(755,root,root) %{_bindir}/db_deadlock
%attr(755,root,root) %{_bindir}/db_dump
%attr(755,root,root) %{_bindir}/db_load
%attr(755,root,root) %{_bindir}/db_printlog
%attr(755,root,root) %{_bindir}/db_recover
%attr(755,root,root) %{_bindir}/db_stat
%attr(755,root,root) %{_libdir}/libdb.so
%attr(755,root,root) %{_libdir}/libdb2.so
%attr(755,root,root) %{_libdir}/libndbm.so
%{_includedir}/db*.h

%files db2-static
%defattr(644,root,root,755)
%{_libdir}/libdb.a
%{_libdir}/libdb2.a
%{_libdir}/libndbm.a
