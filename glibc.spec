%define		min_kernel	2.2.0
Summary:	GNU libc
Summary(de):	GNU libc
Summary(fr):	GNU libc
Summary(pl):	GNU libc
Summary(tr):	GNU libc
Name:		glibc
Version:	2.2.4
Release:	6
License:	LGPL
Group:		Libraries
Group(de):	Libraries
Group(es):	Bibliotecas
Group(fr):	Librairies
Group(pl):	Biblioteki
Group(pt_BR):	Bibliotecas
Group(ru):	âÉÂÌÉÏÔÅËÉ
Group(uk):	â¦ÂÌ¦ÏÔÅËÉ
Source0:	ftp://sources.redhat.com/pub/glibc/releases/%{name}-%{version}.tar.gz
Source1:	ftp://sources.redhat.com/pub/glibc/releases/%{name}-linuxthreads-%{version}.tar.gz
Source2:	nscd.init
Source3:	nscd.sysconfig
Source4:	nscd.logrotate
Source5:	%{name}-man-pages.tar.bz2
Source6:	%{name}-non-english-man-pages.tar.bz2
Patch0:		%{name}-info.patch
Patch1:		%{name}-versions.awk_fix.patch
Patch2:		%{name}-pld.patch
Patch3:		%{name}-crypt-blowfish.patch
Patch4:		%{name}-string2-pointer-arith.patch
Patch5:		%{name}-linuxthreads-lock.patch
Patch6:		%{name}-pthread_create-manpage.patch
Patch7:		%{name}-sparc-linux-chown.patch
Patch8:		%{name}-ldconfig-bklinks.patch
Patch9:		%{name}-paths.patch
Patch10:	%{name}-vaargs.patch
Patch11:	%{name}-malloc.patch
URL:		http://www.gnu.org/software/libc/
BuildRequires:	gd-devel >= 2.0.1
BuildRequires:	gettext-devel >= 0.10.36
BuildRequires:	libpng-devel
BuildRequires:	perl
BuildRequires:	rpm-build >= 4.0-11
BuildRequires:	texinfo
Provides:	ld.so.2
Provides:	ldconfig
Provides:	/sbin/ldconfig
Obsoletes:	%{name}-common
Obsoletes:	%{name}-debug
Obsoletes:	ldconfig
Autoreq:	false
Prereq:		basesystem
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Conflicts:	kernel < %{min_kernel}
Conflicts:	man-pages < 1.43
Conflicts:	ld.so < 1.9.9-9

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
standardowych, wspó³dzielonych (dynamicznych) bibliotek C i
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
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	òÁÚÒÁÂÏÔËÁ/âÉÂÌÉÏÔÅËÉ
Group(uk):	òÏÚÒÏÂËÁ/â¦ÂÌ¦ÏÔÅËÉ
Requires:	%{name} = %{version}

%description devel
To develop programs which use the standard C libraries (which nearly
all programs do), the system needs to have these standard header files
and object files available for creating the executables.

%description devel -l de
Bei der Entwicklung von Programmen, die die Standard-C-Libraries
verwenden (also fast alle), benötigt das System diese Standard-Header-
und Objektdateien zum Erstellen der ausführbaren Programme.

%description devel -l fr
Pour développer des programmes utilisant les bibliothèques standard du
C (ce que presque tous les programmes font), le système doit posséder
ces fichiers en-têtes et objets standards pour créer les exécutables.

%description devel -l pl
Pakiet ten jest niezbêdny przy tworzeniu w³asnych programów
korzystaj±cych ze standardowej biblioteki C. Znajduj± siê tutaj pliki
nag³ówkowe oraz pliki objektowe, niezbêdne do kompilacji programów
wykonywalnych i innych bibliotek.

%description devel -l tr
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
Prereq:		rc-scripts >= 0.2.0
Requires:	%{name} = %{version}

%description -n nscd
nscd caches name service lookups; it can dramatically improve
performance with NIS+, and may help with DNS as well. You cannot use
nscd with 2.0 kernels, due to bugs in the kernel-side thread support.
nscd happens to hit these bugs particularly hard.

%description -n nscd -l pl
nscd zapmiêtuje zapytania i odpowiedzi NIS oraz DNS. Pozwala
drastycznie poprawiæ szybko¶æ dzia³ania NIS+. Nie jest mo¿liwe
u¿ywanie nscd z j±drami serii 2.0.x z powodu b³êdów po stronie j±dra w
ods³udze w±tków.

%package -n localedb-src
Summary:	Souce code locale database
Summary(pl):	Kod ¼ród³owy bazy locale
Group:		Daemons
Group(de):	Server
Group(pl):	Serwery
Requires:	%{name} = %{version}

%description -n localedb-src
This add-on package contains the data needed to build the locale data
files to use the internationalization features of the GNU libc. glibc
package contains standard set of locale binary database and You need
this package if want build some non standard locale database.

%description -n localedb-src -l pl
Pakiet ten kod ¼ród³owy baz locale który jest potrzebny do zbudowania
binarnej wersji baz locale potrzebnej do poprawnego wspierania ró¿nych
jêzyków przez glibc. Pakiet glibc zawira binarn± wersjê standardowych
baz locale i ten pakiet jest potrzebny tylko w sytuacji kiedy potrzeba
wygenerowaæ jak±¶ niestandardow± bazê.

%package -n iconv
Summary:	Convert encoding of given files from one encoding to another
Summary(pl):	Program do konwersji plików tekstowych z jednego kodowania do innego
Group:		Daemons
Group(de):	Server
Group(pl):	Serwery
Requires:	%{name} = %{version}

%description -n iconv
Convert encoding of given files from one encoding to another. You need
this package if You want to convert some documet from one encoding to
another or if You have installed some programs which use Generic
Character Set Conversion Interface.

%description -n iconv -l pl
Program do konwersji plików tekstowych z jednego kodowania do innego.
Musisz mieæ zainstalowany ten pakiet je¿eli wykonujesz konwersjê
dokumentów z jednego kodowania do innego lub je¿eli masz zainstalowane
jakie¶ programy, które korzystaj± z Generic Character Set Conversion
Interface w glibc, czyli z zestawu funkcji z tej biblioteki, które
umo¿liwiaj± konwersjê kodowania danych z poziomu dowolnego programu.

%package static
Summary:	Static libraries
Summary(pl):	Biblioteki statyczne
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	òÁÚÒÁÂÏÔËÁ/âÉÂÌÉÏÔÅËÉ
Group(uk):	òÏÚÒÏÂËÁ/â¦ÂÌ¦ÏÔÅËÉ
Requires:	%{name}-devel = %{version}

%description static
GNU libc static libraries.

%description static -l pl
Biblioteki statyczne GNU libc.

%package profile
Summary:	glibc with profiling support
Summary(de):	glibc mit Profil-Unterstützung
Summary(fr):	glibc avec support pour profiling
Summary(pl):	glibc ze wsparciem dla profilowania
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

%description profile -l de
Damit Programmprofile mit gprof richtig erstellt werden, müssen diese
Libraries anstelle der üblichen C-Libraries verwendet werden.

%description profile -l pl
Programy profilowane za pomoc± gprof musz± u¿ywaæ tych bibliotek
zamiast standardowych bibliotek C, aby gprof móg³ odpowiednio je
wyprofilowaæ.

%description profile -l tr
gprof kullanýlarak ölçülen programlar standart C kitaplýðý yerine bu
kitaplýðý kullanmak zorundadýrlar.

%package pic
Summary:	glibc PIC archive
Summary(pl):	archiwum PIC glibc
Group:		Development/Libraries/Libc
Group(de):	Entwicklung/Libraries/Libc
Group(pl):	Programowanie/Biblioteki/Libc
Requires:	%{name}-devel = %{version}

%description pic
GNU C Library PIC archive contains an archive library (ar file)
composed of individual shared objects. This is used for creating a
library which is a smaller subset of the standard libc shared library.

%description pic -l pl
Archiwum PIC biblioteki GNU C zawiera archiwaln± bibliotekê (plik ar)
z³o¿on± z pojedyñczych obiektów wspó³dzielonych. U¿ywana jest do
tworzenia biblioteki bêd±cej mniejszym podzestawem standardowej
biblioteki wspó³dzielonej libc.

%package -n nss_compat
Summary:	Old style NYS NSS glibc module
Summary(pl):	Stary modu³ NYS NSS glibc
Group:		Base
Group(de):	Gründsätzlich
Group(es):	Base
Group(pl):	Podstawowe
Group(pt_BR):	Base
Requires:	%{name} = %{version}

%description -n nss_compat
Old style NYS NSS glibc module.

%description -n nss_compat -l pl
Stary modu³ NYS NSS glibc.

%package -n nss_dns
Summary:	BIND NSS glibc module
Summary(pl):	Modu³ BIND NSS glibc
Group:		Base
Group(de):	Gründsätzlich
Group(es):	Base
Group(pl):	Podstawowe
Group(pt_BR):	Base
Requires:	%{name} = %{version}

%description -n nss_dns
BIND NSS glibc module.

%description -n nss_dns -l pl
Modu³ BIND NSS glibc.

%package -n nss_files
Summary:	Traditional files databases NSS glibc module
Summary(pl):	Modu³ tradycyjnych plikowych baz danych NSS glibc
Group:		Base
Group(de):	Gründsätzlich
Group(es):	Base
Group(pl):	Podstawowe
Group(pt_BR):	Base
Requires:	%{name} = %{version}

%description -n nss_files
Traditional files databases NSS glibc module.

%description -n nss_files -l pl
Modu³ tradycyjnych plikowych baz danych NSS glibc.

%package -n nss_hesiod
Summary:	Hesiod NSS glibc module
Summary(pl):	Modu³ hesiod NSS glibc
Group:		Base
Group(de):	Gründsätzlich
Group(es):	Base
Group(pl):	Podstawowe
Group(pt_BR):	Base
Requires:	%{name} = %{version}

%description -n nss_hesiod
glibc NSS (Name Service Switch) module for databases access.

%description -n nss_hesiod -l pl
Modu³ glibc NSS (Name Service Switch) dostêpu do baz danych.

%package -n nss_nis
Summary:	NIS(YP) NSS glibc module
Summary(pl):	Modu³ NIS(YP) NSS glibc
Group:		Base
Group(de):	Gründsätzlich
Group(es):	Base
Group(pl):	Podstawowe
Group(pt_BR):	Base
Requires:	%{name} = %{version}

%description -n nss_nis
glibc NSS (Name Service Switch) module for NIS(YP) databases access.

%description -n nss_nis -l pl
Modu³ glibc NSS (Name Service Switch) dostêpu do baz danych NIS(YP).

%package -n nss_nisplus
Summary:	NIS+ NSS module
Summary(pl):	Modu³ NIS+ NSS
Group:		Base
Group(de):	Gründsätzlich
Group(es):	Base
Group(pl):	Podstawowe
Group(pt_BR):	Base
Requires:	%{name} = %{version}

%description -n nss_nisplus
glibc NSS (Name Service Switch) module for NIS+ databases accesa.

%description -n nss_nisplus -l pl
Modu³ glibc NSS (Name Service Switch) dostêpu do baz danych NIS+.

%package memusage
Summary:	A toy
Summary(pl):	Zabawka
Group:		Applications
Group(de):	Applikationen
Group(pl):	Aplikacje
Requires:	%{name} = %{version}
Requires:	gd

%description memusage
A toy.

%description memusage -l pl
Zabawka.

%prep
%setup -q -a 1
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
%patch10 -p1
%patch11 -p1

%build
LDFLAGS=" " ; export LDFLAGS
%configure2_13 \
	--enable-add-ons=linuxthreads \
	--enable-kernel="%{?kernel:%{kernel}}%{!?kernel:%{min_kernel}}" \
	--enable-profile \
	--disable-omitfp

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{logrotate.d,rc.d/init.d,sysconfig},%{_mandir}/man{3,8},/var/log}

env LANGUAGE=C LC_ALL=C \
%{__make} install \
	install_root=$RPM_BUILD_ROOT \
	infodir=%{_infodir} \
	mandir=%{_mandir}

env LANGUAGE=C LC_ALL=C \
%{__make} install-locales -C localedata \
	install_root=$RPM_BUILD_ROOT

PICFILES="libc_pic.a libc.map
	math/libm_pic.a libm.map
	resolv/libresolv_pic.a"

install $PICFILES				$RPM_BUILD_ROOT%{_libdir}
install elf/soinit.os				$RPM_BUILD_ROOT%{_libdir}/soinit.o
install elf/sofini.os				$RPM_BUILD_ROOT%{_libdir}/sofini.o

mv -f $RPM_BUILD_ROOT/lib/libmemusage.so	$RPM_BUILD_ROOT%{_libdir}
mv -f $RPM_BUILD_ROOT/lib/libpcprofile.so	$RPM_BUILD_ROOT%{_libdir}

%{__make} -C linuxthreads/man
install linuxthreads/man/*.3thr			$RPM_BUILD_ROOT%{_mandir}/man3

rm -rf $RPM_BUILD_ROOT%{_datadir}/zoneinfo/{localtime,posixtime,posixrules}

ln -sf ../../..%{_sysconfdir}/localtime		$RPM_BUILD_ROOT%{_datadir}/zoneinfo/localtime
ln -sf localtime				$RPM_BUILD_ROOT%{_datadir}/zoneinfo/posixtime
ln -sf localtime				$RPM_BUILD_ROOT%{_datadir}/zoneinfo/posixrules
ln -sf ../..%{_libdir}/libbsd-compat.a		$RPM_BUILD_ROOT%{_libdir}/libbsd.a

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/localtime

install %{SOURCE2}		$RPM_BUILD_ROOT/etc/rc.d/init.d/nscd
install %{SOURCE3}		$RPM_BUILD_ROOT/etc/sysconfig/nscd
install %{SOURCE4}		$RPM_BUILD_ROOT/etc/logrotate.d/nscd
install nscd/nscd.conf		$RPM_BUILD_ROOT%{_sysconfdir}
install nss/nsswitch.conf	$RPM_BUILD_ROOT%{_sysconfdir}

bzip2 -dc %{SOURCE5} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}
bzip2 -dc %{SOURCE6} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}
touch	$RPM_BUILD_ROOT%{_sysconfdir}/ld.so.{cache,conf}

:> $RPM_BUILD_ROOT/var/log/nscd

rm -rf documentation
install -d documentation

cp -f linuxthreads/ChangeLog documentation/ChangeLog.threads
cp -f linuxthreads/Changes documentation/Changes.threads
cp -f linuxthreads/README documentation/README.threads
cp -f crypt/README.ufc-crypt documentation/

cp -f ChangeLog documentation

gzip -9nf README NEWS FAQ BUGS NOTES PROJECTS documentation/*

# strip ld.so with --strip-debug only (other ELFs are stripped by rpm):
%{!?debug:strip -g -R .comment -R .note $RPM_BUILD_ROOT/lib/ld-%{version}.so}

# Collect locale files and mark them with %%lang()
rm -f glibc.lang
for i in $RPM_BUILD_ROOT%{_datadir}/locale/* $RPM_BUILD_ROOT%{_libdir}/locale/* ; do
	if [ -d $i ]; then
		lang=`echo $i | sed -e 's/.*locale\///' -e 's/\/.*//'`
		dir=`echo $i | sed "s#$RPM_BUILD_ROOT##"`
		echo "%lang($lang) $dir" >> glibc.lang
	fi
done

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post	memusage -p /sbin/ldconfig
%postun memusage -p /sbin/ldconfig

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

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc {README,NEWS,FAQ,BUGS}.gz

%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/ld.so.conf
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/nsswitch.conf
%config %{_sysconfdir}/rpc
%ghost %{_sysconfdir}/ld.so.cache

%attr(755,root,root) /sbin/*
%attr(755,root,root) %{_bindir}/catchsegv
%attr(755,root,root) %{_bindir}/getent
%attr(755,root,root) %{_bindir}/glibcbug
%attr(755,root,root) %{_bindir}/iconv
%attr(755,root,root) %{_bindir}/ldd
%ifnarch alpha
%attr(755,root,root) %{_bindir}/lddlibc4
%endif
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

%{_mandir}/man1/[^ls]*
%{_mandir}/man1/locale.1*
%{_mandir}/man1/ldd.1*
%{_mandir}/man5/???[^d]*
%{_mandir}/man7/*
%{_mandir}/man8/[^n]*
%lang(cs) %{_mandir}/cs/man[578]/*
%lang(de) %{_mandir}/de/man[578]/*
%lang(es) %{_mandir}/es/man[578]/*
%lang(fi) %{_mandir}/fi/man1/ldd.1*
%lang(fr) %{_mandir}/fr/man1/ldd.1*
%lang(fr) %{_mandir}/fr/man[578]/*
%lang(hu) %{_mandir}/hu/man1/ldd.1*
%lang(hu) %{_mandir}/hu/man[578]/*
%lang(it) %{_mandir}/it/man[578]/*
%lang(ja) %{_mandir}/ja/man1/[^ls]*
%lang(ja) %{_mandir}/ja/man1/ldd.1*
%lang(ja) %{_mandir}/ja/man5/???[^d]*
%lang(ja) %{_mandir}/ja/man7/*
%lang(ja) %{_mandir}/ja/man8/[^n]*
%lang(ko) %{_mandir}/ko/man[578]/*
# %lang(nl) %{_mandir}/nl/man[578]/*
%lang(pl) %{_mandir}/pl/man1/ldd.1*
%lang(pl) %{_mandir}/pl/man[578]/*
%lang(pt) %{_mandir}/pt/man5/???[^d]*
%lang(pt) %{_mandir}/pt/man7/*
%lang(pt) %{_mandir}/pt/man8/[^n]*
%lang(pt_BR) %{_mandir}/pt_BR/man5/???[^d]*
%lang(pt_BR) %{_mandir}/pt_BR/man7/*
%lang(pt_BR) %{_mandir}/pt_BR/man8/[^n]*
%lang(ru) %{_mandir}/ru/man[578]/*

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
%attr(755,root,root) %{_libdir}/libmemusage*

%files devel
%defattr(644,root,root,755)
%doc documentation/* {NOTES,PROJECTS}.gz
%attr(755,root,root) %{_bindir}/gencat
%attr(755,root,root) %{_bindir}/getconf
%attr(755,root,root) %{_bindir}/*prof*
%attr(755,root,root) %{_bindir}/*trace

%{_includedir}/*

%{_infodir}/libc.info*

%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_libdir}/*crt*.o
%{_libdir}/libc_nonshared.a

%{_mandir}/man1/sprof*
%{_mandir}/man3/*
%lang(cs) %{_mandir}/cs/man3/*
%lang(de) %{_mandir}/de/man3/*
%lang(es) %{_mandir}/es/man3/*
%lang(fr) %{_mandir}/fr/man3/*
%lang(hu) %{_mandir}/hu/man3/*
# %lang(it) %{_mandir}/it/man3/*
%lang(ja) %{_mandir}/ja/man3/*
%lang(ko) %{_mandir}/ko/man3/*
%lang(nl) %{_mandir}/nl/man3/*
%lang(pl) %{_mandir}/pl/man3/*
%lang(pt) %{_mandir}/pt/man3/*
%lang(pt_BR) %{_mandir}/pt_BR/man3/*
%lang(ru) %{_mandir}/ru/man3/*

%files -n nscd
%defattr(644,root,root,755)
%attr(640,root,root) %config %verify(not md5 size mtime) /etc/sysconfig/nscd
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/nscd.*
%attr(754,root,root) /etc/rc.d/init.d/nscd
%attr(755,root,root) %{_sbindir}/nscd*
%attr(640,root,root) /etc/logrotate.d/nscd
%attr(640,root,root) %ghost /var/log/nscd
%{_mandir}/man5/nscd.conf*
%{_mandir}/man8/nscd*
%lang(ja) %{_mandir}/ja/man5/nscd.conf*
%lang(ja) %{_mandir}/ja/man8/nscd*
%lang(pt) %{_mandir}/pt/man5/nscd.conf*
%lang(pt) %{_mandir}/pt/man8/nscd*
%lang(pt_BR) %{_mandir}/pt_BR/man5/nscd.conf*
%lang(pt_BR) %{_mandir}/pt_BR/man8/nscd*

%files -n localedb-src
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/localedef
%{_datadir}/i18n
%{_mandir}/man1/localedef*

%files -n iconv
%defattr(644,root,root,755)
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
