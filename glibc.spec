Summary:	GNU libc
Summary(de):	GNU libc
Summary(fr):	GNU libc
Summary(pl):	GNU libc
Summary(tr):	GNU libc
name:		glibc
Version:	2.1.2
Release:	10
Copyright:	LGPL
Group:		Libraries
Group(pl):	Biblioteki
Source0:	ftp://sourceware.cygnus.com/pub/glibc/%{name}-%{version}.tar.bz2
Source1:	ftp://sourceware.cygnus.com/pub/glibc/%{name}-linuxthreads-%{version}.tar.bz2
Source2:	http://www.ozemail.com.au/~geoffk/glibc-crypt/%{name}-crypt-2.1.1.tar.gz
Source3:	utmpd.init
Source4:	nscd.init
Source5:	utmpd.sysconfig
Source6:	nscd.sysconfig
Source7:	nscd.logrotate
Patch0:		glibc-info.patch
Patch1:		glibc-paths.patch
Patch2:		glibc-versions.awk_fix.patch
Patch3:		glibc-pld.patch
Patch4:		glibc-getaddrinfo.patch
URL:		http://www.gnu.org/software/libc/
BuildRequires:	perl
Provides:	ld.so.2
Obsoletes:	%{name}-profile
Obsoletes:	%{name}-debug
Autoreq:	false
BuildRoot:	/tmp/%{name}-%{version}-root

%description
Contains the standard libraries that are used by multiple programs on the
system. In order to save disk space and memory, as well as to ease upgrades,
common system code is kept in one place and shared between programs. This
package contains the most important sets of shared libraries, the standard C
library and the standard math library. Without these, a Linux system will
not function. It also contains national language (locale) support and
timezone databases.

%description -l de
Enthält die Standard-Libraries, die von verschiedenen Programmen im System
benutzt werden. Um Festplatten- und Arbeitsspeicher zu sparen und zur
Vereinfachung von Upgrades ist der gemeinsame Systemcode an einer einzigen
Stelle gespeichert und wird von den Programmen gemeinsam genutzt. Dieses
Paket enthält die wichtigsten Sets der shared Libraries, die
Standard-C-Library und die Standard-Math-Library, ohne die das Linux-System
nicht funktioniert. Ferner enthält es den Support für die verschiedenen
Sprachgregionen (locale) und die Zeitzonen-Datenbank.

%description -l fr
Contient les bibliothèques standards utilisées par de nombreux programmes
du système. Afin d'économiser l'espace disque et mémoire, et de faciliter
les mises à jour, le code commun au système est mis à un endroit et partagé
entre les programmes. Ce paquetage contient les bibliothèques partagées les
plus importantes, la bibliothèque standard du C et la bibliothèque
mathématique standard. Sans celles-ci, un système Linux ne peut fonctionner.
Il contient aussi la gestion des langues nationales (locales) et les bases
de données des zones horaires.

%description -l pl
W pakiecie znajduj± siê podstawowe biblioteki, u¿ywane przez ró¿ne programy
w Twoim systemie. U¿ywanie przez programy bibliotek z tego pakietu oszczêdza
miejsce na dysku i pamiêæ. Wiekszo¶æ kodu systemowego jest usytuowane w
jednym miejscu i dzielone miêdzy wieloma programami. Pakiet ten zawiera
bardzo wa¿ny zbiór bibliotek standardowych wspó³dzielonych (dynamicznych)
bibliotek C i matematycznych. Bez glibc system Linux nie jest w stanie
funkcjonowaæ. Znajduj± siê tutaj równie¿ definicje ró¿nych informacji dla
wielu jêzyków (locale) oraz definicje stref czasowych.

%description -l tr
Bu paket, birçok programýn kullandýðý standart kitaplýklarý içerir. Disk
alaný ve bellek kullanýmýný azaltmak ve ayný zamanda güncelleme iþlemlerini
kolaylaþtýrmak için ortak sistem kodlarý tek bir yerde tutulup programlar
arasýnda paylaþtýrýlýr. Bu paket en önemli ortak kitaplýklarý, standart
C kitaplýðýný ve standart matematik kitaplýðýný içerir. Bu kitaplýklar olmadan
Linux sistemi çalýþmayacaktýr. Yerel dil desteði ve zaman dilimi veri tabaný
da bu pakette yer alýr.

%package devel
Summary:	Additional libraries required to compile
Summary(de):	Weitere Libraries zum Kompilieren
Summary(fr):	Librairies supplémentaires nécessaires à la compilation.
Summary(pl):	Dodatkowe biblioteki wymagane podczas kompilacji
Summary(tr):	Geliþtirme için gerekli diðer kitaplýklar
Group:		Development/Libraries
Group(pl):	Programowanie/Biblioteki
Prereq:		/usr/sbin/fix-info-dir
Requires:	%{name} = %{version}

%description devel
To develop programs which use the standard C libraries (which nearly all
programs do), the system needs to have these standard header files and object
files available for creating the executables.

%description -l de devel
Bei der Entwicklung von Programmen, die die Standard-C-Libraries verwenden
(also fast alle), benötigt das System diese Standard-Header- und Objektdateien
zum Erstellen der ausführbaren Programme.

%description -l fr devel
Pour développer des programmes utilisant les bibliothèques standard du C
(ce que presque tous les programmes font), le système doit posséder ces
fichiers en-têtes et objets standards pour créer les exécutables.

%description -l pl devel
Pakiet ten jest niezbêdny przy tworzeniu w³asnych programów korzystaj±cych
ze standardowej biblioteki C. Znajduj± siê tutaj pliki nag³ówkowe oraz pliki 
objektowe, niezbêdne do kompilacji programów wykonywalnych i innych bibliotek.

%description -l tr devel
C kitaplýðýný kullanan (ki hemen hemen hepsi kullanýyor) programlar
geliþtirmek için gereken standart baþlýk dosyalarý ve statik kitaplýklar.

%package -n nscd
Summary:	Name Service Caching Daemon
Summary(pl):	Name Service Caching Daemon
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Prereq:		/sbin/chkconfig
Requires:	rc-scripts

%description -n nscd
nscd caches name service lookups; it can dramatically improve performance
with NIS+, and may help with DNS as well.

You cannot use nscd with 2.0 kernels, due to bugs in the kernel-side thread
support. nscd happens to hit these bugs particularly hard.

%description -n nscd -l pl
nscd zapmiêtuje zapytania i odpowiedzi NIS oraz DNS. Pozwala drastycznie 
poprawiæ szybko¶æ dzia³ania NIS+.

Nie jest mo¿liwe u¿ywanie nscd z j±drami serii 2.0.x z powodu b³adów
po stronie j±dra w ods³udze w±tków.

%package -n utmpd
Summary:	utmp and utmpx synchronizer for libc5 applications.
Summary(pl):	Synchrnnizuje zapis do plików utmp i utmpx.
Group:		Daemons
Group(pl):	Serwery
Prereq:         /sbin/chkconfig
Requires:	rc-scripts

%description -n utmpd
utmpd is a utmp and utmpx synchronizer. Is only needed for libc5 based 
program with utmp access.

%description -n utmpd -l pl
utmpd stara siê utrzymaæ tak± sam± zawarto¶æ plików 
/var/run/utmp i /var/run/utmpx. Potrzebny jest tylko w przypadku korzystania
ze starszych programów (bazuj±cych na libc5).

%package -n localedb-src
Summary:	Souce code locale database
Summary(pl):	Kod ¬ród³owy bazy locale
Group:		Daemons
Group(pl):	Serwery

%description -n localedb-src
This add-on package contains the data needed to build the locale data files
to use the internationalization features of the GNU libc. Glibc package
contains standard set of locale binary database and You need this package if
want build some non standard locale database.

%description -l pl -n localedb-src
Pakiet ten kod ¼ród³owy baz locale który jest potrzebny do zbudowania
binarnej wersji baz locale potrzebnej do poprawnego wspierania ró¿nych
jêzyków przez glibc. Pakiet glibc zawira binarn± wersjê standardowych baz
locale i ten pakiet jest potrzebny tylko w sytuacji kiedy potrzeba
wygenerowaæ jak±¶ niestandardow± bazê.

%package -n iconv
Summary:	Convert encoding of given files from one encoding to another
Summary(pl):	Program do konwersji plików tekstowych z jednego enkodingu w inny
Group:		Daemons
Group(pl):	Serwery

%description -n iconv
Convert encoding of given files from one encoding to another.
You neet this package if You want to convert some documet from one encoding
to another or if Yoo have installed some programs which use Generic
Character Set Conversion Interface.

%description -l pl -n iconv
Program do konwersji plików tekstowych z jednego enkodingu w inny.
Potrzebujesz mieæ zainstalowany ten pakiet je¿eli wykonujesz konwersjê
dokumentów z jednego enkodingu w inny lub je¿eli masz zainstalowane jakie¶
programy które korzystaj± Generic Character Set Conversion Interface w glibc
czyli zestawu funkcji z tej biblioteki które umo¿liwiaj± kowersje enkodingu
danych z poziomu dowolnego programu.

%package static
Summary:	Static libraries
Summary(pl):	Biblioteki statyczne 
Group:		Development/Libraries
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
Obsoletes:	libc-profile
Requires:	%{name}-devel = %{version}

%description profile
When programs are being profiled used gprof, they must use these libraries
instrad of the standard C libraries for gprof to be able to profile them
correctly.

%description -l de profile
Damit Programmprofile mit gprof richtig erstellt werden, müssen diese
Libraries anstelle der üblichen C-Libraries verwendet werden.

%description -l tr profile
gprof kullanýlarak ölçülen programlar standart C kitaplýðý yerine bu
kitaplýðý kullanmak zorundadýrlar.

%prep 
%setup  -q -a 1 -a 2
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%configure \
	--enable-add-ons=crypt,linuxthreads \
	--enable-profile \
	--disable-omitfp
make   

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{etc/{rc.d/init.d,sysconfig,logrotate.d},%{_mandir}/man3,var/{db,log}}

make install \
	install_root=$RPM_BUILD_ROOT \
	infodir=%{_infodir} \
	mandir=%{_mandir}

make install-locales -C localedata \
	install_root=$RPM_BUILD_ROOT

make -C linuxthreads/man
install linuxthreads/man/*.3thr $RPM_BUILD_ROOT%{_mandir}/man3

rm -rf $RPM_BUILD_ROOT%{_datadir}/zoneinfo/{localtime,posixtime,posixrules}

ln -sf ../../../etc/localtime $RPM_BUILD_ROOT%{_datadir}/zoneinfo/localtime
ln -sf localtime $RPM_BUILD_ROOT%{_datadir}/zoneinfo/posixtime
ln -sf localtime $RPM_BUILD_ROOT%{_datadir}/zoneinfo/posixrules
ln -sf ../../usr/lib/libbsd-compat.a $RPM_BUILD_ROOT%{_libdir}/libbsd.a

rm -f $RPM_BUILD_ROOT/etc/localtime

install %{SOURCE4}		$RPM_BUILD_ROOT/etc/rc.d/init.d/nscd
install %{SOURCE3}		$RPM_BUILD_ROOT/etc/rc.d/init.d/utmpd
install %{SOURCE6}		$RPM_BUILD_ROOT/etc/sysconfig/nscd
install %{SOURCE5}		$RPM_BUILD_ROOT/etc/sysconfig/utmpd
install %{SOURCE7}		$RPM_BUILD_ROOT/etc/logrotate.d/nscd
install nscd/nscd.conf		$RPM_BUILD_ROOT/etc
install nss/nsswitch.conf	$RPM_BUILD_ROOT/etc

install nss/db-Makefile $RPM_BUILD_ROOT/var/db/Makefile
:> $RPM_BUILD_ROOT/var/log/nscd

cat << EOF > $RPM_BUILD_ROOT/usr/bin/create-db
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

cp ChangeLog ChangeLog.8 documentation

gzip -9fn README NEWS FAQ BUGS NOTES PROJECTS \
	$RPM_BUILD_ROOT{%{_mandir}/man*/*,%{_infodir}/libc*} \
	documentation/* login/README.utmpd

strip $RPM_BUILD_ROOT/{sbin/*,usr/{sbin/*,bin/*}} ||:
strip --strip-unneeded $RPM_BUILD_ROOT/lib/lib*.so.* \
	$RPM_BUILD_ROOT/usr/lib/gconv/*.so

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel
/usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun devel
/usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

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
	/sbin/chkconfig --del nscd
	/etc/rc.d/init.d/nscd stop 1>&2
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
	/sbin/chkconfig --del utmpd
	/etc/rc.d/init.d/utmpd stop 1>&2
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {README,NEWS,FAQ,BUGS}.gz

%config(noreplace) %verify(not mtime md5 size) /etc/nsswitch.conf
%config /etc/rpc

%attr(755,root,root) /sbin/*
%attr(755,root,root) %{_bindir}/catchsegv
%attr(755,root,root) %{_bindir}/create-db
%attr(755,root,root) %{_bindir}/db_archive
%attr(755,root,root) %{_bindir}/db_checkpoint
%attr(755,root,root) %{_bindir}/db_deadlock
%attr(755,root,root) %{_bindir}/db_dump
%attr(755,root,root) %{_bindir}/db_dump185
%attr(755,root,root) %{_bindir}/db_load
%attr(755,root,root) %{_bindir}/db_printlog
%attr(755,root,root) %{_bindir}/db_recover
%attr(755,root,root) %{_bindir}/db_stat
%attr(755,root,root) %{_bindir}/getent
%attr(755,root,root) %{_bindir}/glibcbug
%attr(755,root,root) %{_bindir}/ldd
%attr(755,root,root) %{_bindir}/lddlibc4
%attr(755,root,root) %{_bindir}/locale
%attr(755,root,root) %{_bindir}/makedb
%attr(755,root,root) %{_bindir}/rpcgen
%attr(755,root,root) %{_bindir}/tzselect
%attr(755,root,root) %{_bindir}/update-db

%attr(755,root,root) %{_sbindir}/rpcinfo
%attr(755,root,root) %{_sbindir}/zdump
%attr(755,root,root) %{_sbindir}/zic

%attr(755,root,root) /lib/ld-*
%attr(755,root,root) /lib/lib*

%{_datadir}/locale
%{_datadir}/zoneinfo

%config /var/db/Makefile

%files devel
%defattr(644,root,root,755)
%doc documentation/* {NOTES,PROJECTS}.gz
%attr(755,root,root) %{_bindir}/gencat
%attr(755,root,root) %{_bindir}/getconf
%attr(755,root,root) %{_bindir}/mtrace
%attr(755,root,root) %{_bindir}/sprof

%{_includedir}/*.h
%{_includedir}/arpa
%{_includedir}/bits
%{_includedir}/db1
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
%attr(755,root,root) %{_libdir}/*.o
%{_libdir}/libc_nonshared.a

%{_mandir}/man3/*

%files -n nscd
%defattr(644,root,root,755)
%attr(640,root,root) %config %verify(not size mtime md5) /etc/sysconfig/nscd
%attr(640,root,root) %config(noreplace) %verify(not mtime md5 size) /etc/nscd.*
%attr(755,root,root) /etc/rc.d/init.d/nscd
%attr(755,root,root) %{_sbindir}/nscd
%attr(640,root,root) /etc/logrotate.d/nscd
%attr(640,root,root) %ghost /var/log/nscd

%files -n utmpd
%defattr(644,root,root,755)
%doc login/README.utmpd.gz
%attr(640,root,root) %config %verify(not size mtime md5) /etc/sysconfig/utmpd
%attr(755,root,root) /etc/rc.d/init.d/utmpd
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
%{_libdir}/libdb.a
%{_libdir}/libdb1.a
%{_libdir}/libdl.a
%{_libdir}/libg.a
%{_libdir}/libieee.a
%{_libdir}/libm.a
%{_libdir}/libmcheck.a
%{_libdir}/libndbm.a
%{_libdir}/libnsl.a
%{_libdir}/libposix.a
%{_libdir}/libpthread.a
%{_libdir}/libresolv.a
%{_libdir}/librpcsvc.a
%{_libdir}/librt.a
%{_libdir}/libutil.a

%files profile
%defattr(644,root,root,755)
%{_libdir}/lib*_p.a
