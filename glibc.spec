Summary:	GNU libc
Summary(de):	GNU libc
Summary(fr):	GNU libc
Summary(pl):	GNU libc
Summary(tr):	GNU libc
name:		glibc
Version:	2.1
Release:	6
Copyright:	LGPL
Group:		Libraries
Group(pl):	Biblioteki
#######		ftp://sourceware.cygnus.com/pub/glibc/
Source0:	%{name}-%{version}.tar.gz
Source1:	%{name}-linuxthreads-%{version}.tar.gz
#######:	http://www.ozemail.com.au/~geoffk/glibc-crypt
Source2:	%{name}-crypt-%{version}.tar.gz
Source3:	utmpd.init
Source4:	nscd.init
Patch0:		glibc-info.patch
URL:		http://www.gnu.org/software/libc/
Provides:	ld.so.2
Obsoletes:	%{name}-profile
Obsoletes:	%{name}-debug
Autoreq:	false
BuildRoot:	/tmp/%{name}-%{version}-root

%description
Contains the standard libraries that are used by multiple programs on
the system. In order to save disk space and memory, as well as to
ease upgrades, common system code is kept in one place and shared between
programs. This package contains the most important sets of shared libraries,
the standard C library and the standard math library. Without these, a
Linux system will not function. It also contains national language (locale)
support and timezone databases.

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

%package	devel
Summary:	Additional libraries required to compile
Summary(de):	Weitere Libraries zum Kompilieren
Summary(fr):	Librairies supplémentaires nécessaires à la compilation.
Summary(pl):	Dodatkowe biblioteki wymagane podczas kompilacji
Summary(tr):	Geliþtirme için gerekli diðer kitaplýklar
Group:		Development/Libraries
Group(pl):	Programowanie/Biblioteki
Prereq:		/sbin/install-info
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

%prep 
%setup -q -a 1 -a 2
%patch -p1

%build
install -d sunrpc/cpp; ln -s /lib/cpp sunrpc/cpp/cpp 
CFLAGS="$RPM_OPT_FLAGS -pipe" \
./configure \
	--enable-add-ons=crypt,linuxthreads \
	--disable-profile \
	--prefix=/usr \
	--disable-omitfp
make  

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{etc/rc.d/init.d,usr/man/man3,var/db}

make install_root=$RPM_BUILD_ROOT install
make install_root=$RPM_BUILD_ROOT install-locales -C localedata

make -C linuxthreads/man
install linuxthreads/man/*.3thr $RPM_BUILD_ROOT/usr/man/man3

rm -rf $RPM_BUILD_ROOT/usr/share/zoneinfo/{localtime,posixtime,posixrules}

ln -sf ../../../etc/localtime $RPM_BUILD_ROOT/usr/share/zoneinfo/localtime
ln -sf localtime $RPM_BUILD_ROOT/usr/share/zoneinfo/posixtime
ln -sf localtime $RPM_BUILD_ROOT/usr/share/zoneinfo/posixrules
ln -sf ../../usr/lib/libbsd-compat.a $RPM_BUILD_ROOT/usr/lib/libbsd.a

rm -f $RPM_BUILD_ROOT/etc/localtime

install %{SOURCE3} $RPM_BUILD_ROOT/etc/nsswitch.conf

install %{SOURCE4} $RPM_BUILD_ROOT/etc/rc.d/init.d/nscd
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/utmpd

install nscd/nscd.conf		$RPM_BUILD_ROOT/etc
install nss/nsswitch.conf	$RPM_BUILD_ROOT/etc

install nss/db-Makefile $RPM_BUILD_ROOT/var/db

cat << EOF > $RPM_BUILD_ROOT/usr/bin/create-db
#!/bin/sh
/usr/bin/make -f /var/db/db-Makefile
EOF

ln -sf create-db $RPM_BUILD_ROOT/usr/bin/update-db 

rm -rf documentation
install -d documentation

cp linuxthreads/ChangeLog  documentation/ChangeLog.threads
cp linuxthreads/Changes documentation/Changes.threads
cp linuxthreads/README documentation/README.threads
cp login/README.utmpd documentation/
cp crypt/README documentation/README.crypt

cp ChangeLog ChangeLog.8 documentation

bzip2 -9 documentation/*

strip $RPM_BUILD_ROOT/{sbin/*,usr/{bin/*,sbin/*}} || :

bzip2 -9 README NEWS FAQ BUGS NOTES PROJECTS

gzip -9fn $RPM_BUILD_ROOT/usr/{man/man*/*,info/libc*}

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel
/sbin/install-info /usr/info/libc.info.gz /etc/info-dir

%preun devel
if [ "$1" = 0 ]; then
	/sbin/install-info --delete /usr/info/libc.info.gz /etc/info-dir
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {README,NEWS,FAQ,BUGS}.bz2

%attr(640,root,root) %config(noreplace) %verify(not mtime md5 size) /etc/nscd.*
%config(noreplace) %verify(not mtime md5 size) /etc/nsswitch.conf
%config /etc/rpc

%attr(750,root,root) /etc/rc.d/init.d/*

%attr(755,root,root) /sbin/*
%attr(755,root,root) /usr/bin/*
%attr(755,root,root) /usr/sbin/*

%attr(755,root,root) /lib/ld-*
%attr(755,root,root) /lib/lib*

%dir /usr/lib/gconv
/usr/lib/gconv/gconv-modules

/usr/share/i18n
/usr/share/locale
/usr/share/zoneinfo

%dir /var/db
%config /var/db/db-*

%files devel
%defattr(644,root,root,755)
%doc documentation/* {NOTES,PROJECTS}.bz2

/usr/include/*.h
/usr/include/arpa
/usr/include/bits
/usr/include/db1
/usr/include/gnu
/usr/include/net
/usr/include/netash
/usr/include/netatalk
/usr/include/netax25
/usr/include/neteconet
/usr/include/netinet
/usr/include/netipx
/usr/include/netpacket
/usr/include/netrom
/usr/include/netrose
/usr/include/nfs
/usr/include/protocols
/usr/include/rpc
/usr/include/rpcsvc
/usr/include/scsi
/usr/include/sys

/usr/info/libc.inf*.gz

%attr(755,root,root) /usr/lib/lib*.so
/usr/lib/*.o
/usr/lib/lib*.a

%attr(755,root,root) /usr/lib/gconv/*.so
/usr/man/man3/*

%changelog
* Sun Mar 14 1999 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [2.1-6]
- updated glibc-crypt to version-2.1

* Sat Mar 06 1999 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [2.1-5]
- removed striping of shared libraries -- no debug info in this libs,
- fixed /etc/rc.d/init.d/* -- Tomek, never again 754 on start scripts... 
- fixed permission of /var/db directory -- should be 755...

* Mon Feb 22 1999 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [2.1-4]
- removed man group from man pages,
- standarized {un}registering info pages (added libc-info.patch),
- changed base source url to ftp://sourceware.cygnus.com/pub/glibc/,
- changed URL,
- siplifications in %files devel,
- Group in devel changed to Development/Libraries,
- removed some %doc (INSTALL and outdated ChangeLog),
- removed %config and %verify rules fromn /etc/rc.d/init.d/* files,
- changed permission to 754 on /etc/rc.d/init.d/*,
- added striping shared libraries.

* Sun Feb 14 1999 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [2.1-3d]
- updated to stable version,
- fixed stripping ELF binaries,
- removed obsoletes /usr/include/{asm,linux}

* Fri Jan 29 1999 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [2.0.111-1d]
- updated to latest snapshoot,
- added utmpd.init, (don't run this piece of ... by default)
- added /var/db, (don't generate a data base by default)
- removed unused /usr/libexec/pt_ch*
- other changes.

* Sat Nov 07 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [2.0.100-1d]
- updated to latest snapshoot,
- added install-locales,
- minor changes.

* Tue Oct 13 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [2.0.99-1d]
- updated to 2.0.99,
- added Obsoletes: glibc-debug, glibc-profile

* Thu Aug 06 1998 Wojtek ¦lusarczyk <wojtek@SHADOW.EU.ORG>
  [2.0.96-1d]
- updated to 2.0.96,
- translation modified for pl, 
  (follow the suggestions Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>)
- major changes.
      (rewrote spec file -- follow the PLD policy)

* Wed Jul 16 1998 Wojtek ¦lusarczyk <wojtek@SHADOW.EU.ORG>
  [2.0.94-2d]
- added nscd.init and config
- fixed permision of pt_chown to 4711 
- added %defattr
- moved linux include links from kernel-headers to glibc-devel

* Tue Jun 2 1998 Wojtek ¦lusarczyk <wojtek@SHADOW.EU.ORG>
  [2.0.94-1d]
- updated to glibc 2.0.94

* Sun May 24 1998 Marcin Korzonek <mkorz@euler.mat.univ.szczecin.pl>
  [2.0.93-1d]
- updated for glibc 2.0.93
- build prepare for PLD-1.1 Tornado
- removed glibc-debug and glibc-profile packages generation (it took too
  long to compile the full featured version on my home linux box ;)
- compilation is now performed in compile directory as advised 
  in Glibc HOWTO,
- start at invalid RH spec file.  


  [2.1.1-1]
- based on RH spec,
- spec rewrited by PLD team,
  we start at GNU libc 2.0.92 one year ago ...
- pl translation by Wojtek ¦lusarczyk <wojtek@shadow.eu.org>.
