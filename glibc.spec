Summary:	GNU libc
Summary(de):	GNU libc
Summary(fr):	GNU libc
Summary(pl):	GNU libc
Summary(tr):	GNU libc
name:		glibc
Version:	2.1
Release:	3d 
Copyright:	LGPL
Group:		Libraries
Group(pl):	Biblioteki
Source0:	ftp://alpha.gnu.org/pub/gnu/%{name}-2.0.112.tar.gz
URL:		ftp://sourceware.cygnus.com/pub/glibc
Source1:	%{name}-linuxthreads-2.1.tar.gz
Source2:	%{name}-crypt-2.0.111.tar.gz
Source3:	utmpd.init
Source4:	nscd.init
Patch:		%{name}-2.0.112-2.1.diff.gz
BuildRoot:	/tmp/%{name}-%{version}-root
Provides:	ld.so.2
Obsoletes:	%{name}-profile
Obsoletes:	%{name}-debug
Autoreq:	false

%description
Contains the standard libraries that are used by multiple programs on
the system. In order to save disk space and memory, as well as to
ease upgrades, common system code is kept in one place and shared between
programs. This package contains the most important sets of shared libraries,
the standard C library and the standard math library. Without these, a
Linux system will not function. It also contains national language (locale)
support and timezone databases.

%package	devel
Summary:	Additional libraries required to compile
Summary(de):	Weitere Libraries zum Kompilieren
Summary(fr):	Librairies supplémentaires nécessaires à la compilation.
Summary(pl):	Dodatkowe biblioteki wymagane podczas kompilacji
Summary(tr):	Geliþtirme için gerekli diðer kitaplýklar
Group:		Libraries
Group(pl):	Biblioteki
Prereq:		/sbin/install-info
Requires:	%{name} = %{version}

%description devel
To develop programs which use the standard C libraries (which nearly all
programs do), the system needs to have these standard header files and object
files available for creating the executables.

%description -l de
Enthält die Standard-Libraries, die von verschiedenen Programmen im 
System benutzt werden. Um Festplatten- und Arbeitsspeicher zu sparen 
und zur Vereinfachung von Upgrades ist der gemeinsame Systemcode an 
einer einzigen Stelle gespeichert und wird von den Programmen 
gemeinsam genutzt. Dieses Paket enthält die wichtigsten Sets der 
shared Libraries, die Standard-C-Library und die Standard-Math-Library, 
ohne die das Linux-System nicht funktioniert. Ferner enthält es den Support 
für die verschiedenen Sprachgregionen (locale) und die Zeitzonen-Datenbank.

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
miejsce na dysku i pamiêæ. Wiekszo¶æ kodu systemowego jest usytuowane w jednym
miejscu i dzielone miêdzy wieloma programami. Pakiet ten zawiera bardzo wa¿ny 
zbiór bibliotek wspó³dzielonych (dynamicznych), standardowych bibliotek C i
standardowych bibliotek matematycznych. Bez glibc system Linux nie jest w
stanie funkcjonowaæ. Znajduj± siê tutaj równie¿ definicje ró¿nych informacji
dla wielu jêzyków (locale) oraz definicje stref czasowych.

%description -l tr
Bu paket, birçok programýn kullandýðý standart kitaplýklarý içerir. Disk
alaný ve bellek kullanýmýný azaltmak ve ayný zamanda güncelleme iþlemlerini
kolaylaþtýrmak için ortak sistem kodlarý tek bir yerde tutulup programlar
arasýnda paylaþtýrýlýr. Bu paket en önemli ortak kitaplýklarý, standart
C kitaplýðýný ve standart matematik kitaplýðýný içerir. Bu kitaplýklar olmadan
Linux sistemi çalýþmayacaktýr. Yerel dil desteði ve zaman dilimi veri tabaný
da bu pakette yer alýr.

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
%setup -q -a 1 -a 2 -n %{name}-2.0.112
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
install -d $RPM_BUILD_ROOT

make install_root=$RPM_BUILD_ROOT install
make install_root=$RPM_BUILD_ROOT install-locales -C localedata

install -d $RPM_BUILD_ROOT/usr/man/man3

make -C linuxthreads/man
install linuxthreads/man/*.3thr $RPM_BUILD_ROOT/usr/man/man3

gzip -9nvf $RPM_BUILD_ROOT/usr/info/libc*

rm -rf $RPM_BUILD_ROOT/usr/share/zoneinfo/{localtime,posixtime,posixrules}

ln -sf ../src/linux/include/linux $RPM_BUILD_ROOT/usr/include/linux
ln -sf ../src/linux/include/asm $RPM_BUILD_ROOT/usr/include/asm

ln -sf ../../../etc/localtime $RPM_BUILD_ROOT/usr/share/zoneinfo/localtime
ln -sf localtime $RPM_BUILD_ROOT/usr/share/zoneinfo/posixtime
ln -sf localtime $RPM_BUILD_ROOT/usr/share/zoneinfo/posixrules
ln -sf ../../usr/lib/libbsd-compat.a $RPM_BUILD_ROOT/usr/lib/libbsd.a

rm -f $RPM_BUILD_ROOT/etc/localtime

install %{SOURCE3} $RPM_BUILD_ROOT/etc/nsswitch.conf

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

install %{SOURCE4} $RPM_BUILD_ROOT/etc/rc.d/init.d/nscd
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/utmpd

install nscd/nscd.conf		$RPM_BUILD_ROOT/etc
install nss/nsswitch.conf	$RPM_BUILD_ROOT/etc

install -d $RPM_BUILD_ROOT/var/db
install nss/db-Makefile $RPM_BUILD_ROOT/var/db

cat << EOF > $RPM_BUILD_ROOT/usr/bin/create-db
#!/bin/bash

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

cp ChangeLog* documentation

bzip2 -9 documentation/*

strip $RPM_BUILD_ROOT/{sbin/*,usr/{bin/*,sbin/*}} || :

bzip2 -9  README NEWS FAQ BUGS NOTES PROJECTS INSTALL

gzip -9fn $RPM_BUILD_ROOT/usr/man/man3/*

%post -p /sbin/ldconfig
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
%doc README.bz2 NEWS.bz2 FAQ.bz2 BUGS.bz2 
%doc documentation/* NOTES.bz2 PROJECTS.bz2 INSTALL.bz2

%attr(640,root,root) %config(noreplace) %verify(not mtime md5 size) /etc/nscd.*
%config(noreplace) %verify(not mtime md5 size) /etc/nsswitch.conf
%attr(750,root,root) %config %verify(not mtime md5 size) /etc/rc.d/init.d/*
%attr(644,root,root) %config /etc/rpc

%attr(755,root,root) /sbin/*
%attr(755,root,root) /usr/bin/*
%attr(755,root,root) /usr/sbin/*

%attr(755,root,root) /lib/ld-*
%attr(755,root,root) /lib/lib*

%dir /usr/lib/gconv
/usr/lib/gconv/gconv-modules

%dir /usr/share/i18n
%attr(-,root,root) /usr/share/i18n/*

%dir /usr/share/locale
%attr(-,root,root) /usr/share/locale/*

%dir /usr/share/zoneinfo
%attr(-,root,root) /usr/share/zoneinfo/*

%attr(750,root,root) %dir /var/db
%config /var/db/db-*

%files devel
%defattr(644,root,root,755)

/usr/include/*.h

%dir /usr/include/arpa
/usr/include/arpa/*.h

#%attr(755,root,root) /usr/include/asm
#%attr(755,root,root) /usr/include/linux

%dir /usr/include/scsi
/usr/include/scsi/*.h

%dir /usr/include/bits
/usr/include/bits/*.h

%dir /usr/include/db1
/usr/include/db1/*.h

%dir /usr/include/gnu
/usr/include/gnu/*.h

%dir /usr/include/net
/usr/include/net/*.h

%dir /usr/include/netash
/usr/include/netash/*.h

%dir /usr/include/netatalk
/usr/include/netatalk/*.h

%dir /usr/include/netax25
/usr/include/netax25/*.h

%dir /usr/include/neteconet
/usr/include/neteconet/*.h

%dir /usr/include/netinet
/usr/include/netinet/*.h

%dir /usr/include/netipx
/usr/include/netipx/*.h

%dir /usr/include/netpacket
/usr/include/netpacket/*.h

%dir /usr/include/netrom
/usr/include/netrom/*.h

%dir /usr/include/netrose
/usr/include/netrose/*.h

%dir /usr/include/nfs
/usr/include/nfs/*.h

%dir /usr/include/protocols
/usr/include/protocols/*.h

%dir /usr/include/rpc
/usr/include/rpc/*

%dir /usr/include/rpcsvc
/usr/include/rpcsvc/*

%dir /usr/include/sys
/usr/include/sys/*.h

/usr/info/libc.inf*.gz

%attr(755,root,root) /usr/lib/*.o
%attr(755,root,root) /usr/lib/*.so

/usr/lib/*.a

%attr(755,root,root) /usr/lib/gconv/*.so
%attr(644,root, man) /usr/man/man3/*

%changelog
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
      (rewrote invalid spec file -- follow the PLD policy)

* Wed Jul 16 1998 Wojtek ¦lusarczyk <wojtek@SHADOW.EU.ORG>
  [2.0.94-2d]
- added nscd.init and config
- fixed permision of pt_chown to 4711 
- added %defattr
- moved linux include links from kernel-headers to glibc-devel

* Tue Jun 2 1998 Wojtek Slusarczyk <wojtek@SHADOW.EU.ORG>
  [2.0.94-1d]
- updated to glibc 2.0.94

* Sun May 24 1998 Marcin Korzonek <mkorz@euler.mat.univ.szczecin.pl>
  [2.0.93-1d]
- updated for glibc 2.0.93
- build prepare for PLD-1.1 Tornado
- removed glibc-debug and glibc-profile packages generation (it took too
  long to compile the full featured version on my home linux box ;)
- compilation is now performed in compile directory as advised 
  in Glibc HOWTO

* Tue Mar 31 1998 Cristian Gafton <gafton@redhat.com>
- more patches to fix dlopen()/dlclose problems

* Tue Mar 24 1998 Cristian Gafton <gafton@redhat.com>
- fixed a dlclose() problem.
- updated the cvs snapshot

* Fri Mar 20 1998 Cristian Gafton <gafton@redhat.com>
- need a fairly recent version of texinfo (3.11 or later). Handle this
  through a Conflicts: header for the glibc-devel package

* Sat Mar 14 1998 Cristian Gafton <gafton@redhat.com>
- new package versioning for snapshots

* Sat Mar 14 1998 Cristian Gafton <gafton@redhat.com>
- new snapshot
- fixed a localedef bug
- reverted some changes in the new localedata ru_RU that caused locale files
  to be built incorrectly.

* Wed Mar 04 1998 Cristian Gafton <gafton@redhat.com>
- downgraded kernel headers to 2.1.76. tty changes in more recent kernels
  require too many programs to be recompiled against the new glibc.
- upgraded the dlfix patch for dlopen() to handle large shared objects
- updated the fix patch to make the source compile on alpha
- the new sources require binutils 2.8.1.0.21 or later to compile on alpha
- updated snapshot; lots of patches obsoleted
- added a patch to buold & install the localedata files correctly
- added yet another patch from H.J.Lu

* Sat Feb 28 1998 Cristian Gafton <gafton@redhat.com>
- updated the snapshot
- upgraded the kernel headers to 2.1.88
- replaced the full kernel source with a homebrew
  linux-include-2.1.88.tar.gz (it was way too hard to maintain glibc from
  home over my modem...)

* Wed Feb 18 1998 Cristian Gafton <gafton@redhat.com>
- added a dl-open fix for the RTLD_GLOBAL flag

* Sat Feb 07 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 2.0.7pre1
- modified spec file to include linuxthreads man pages and documentation

* Wed Jan 28 1998 Erik Troan <ewt@redhat.com>
- don't believe LD_PRELOAD if the app is setuid root

* Tue Jan 27 1998 Cristian Gafton <gafton@redhat.com>
- added (what else ?) more patches from Andreas Jaeger, Andreas Schwab,
  Ulrich Drepper and H J Lu

* Fri Jan 16 1998 Cristian Gafton <gafton@redhat.com>
- added nss patch to fix a problem of ignoring the NSS_STATUS_TRYAGAIN
  return value from the modules by getXXbyYY_r and getXXent_r functions
- added another patch for the nss_db from Andreas Schwab

* Wed Jan 14 1998 Cristian Gafton <gafton@redhat.com>
- added a patch to fix the problems with the nss_db lookups from Andreas
  Schwab
- added a patch to fix lookup problems with large entries (errno not being
  reset from ERANGE)
- added another two tiny patches from Andreas Jaeger
- added a header patch for the net/if.h file which failed to #define
  #IFF_* symbols
- fixed obsoletes header for linuxthreads
- added a patch for locale on big endian machines from Andreas Schwab
- added a config patch from Andreas Jaeger

* Wed Jan  7 1998 Cristian Gafton <gafton@redhat.com>
- figured out how to handle newer kernels on alpha - back to 2.1.76
- added a patch to address case-sensitve hosts and aliases lookup brokeness
- re-added the patch for alpha/net/route.h, which somehow escaped the
  official release
- added the threads and thread-signal patches from Andreas Jaeger

* Mon Dec 29 1997 Cristian Gafton <gafton@redhat.com>
- finally 2.0.6 final release is here...
- reverted to kernel headers 2.1.60. Although the latest one available
  should be used (2.1.76 at the moment), the new kernel headers break
  compilation on alpha (due to the rename of the __NR_sigaction to
  __NR_old_osf_sigaction). In two days I haven't figured out the correct
  place to modify this on glibc sources, so...

* Thu Dec 25 1997 Cristian Gafton <gafton@redhat.com>
- upgraded to pre6

* Tue Dec 23 1997 Cristian Gafton <gafton@redhat.com>
- upgraded to pre5
- added NIS patch fix

* Mon Dec 15 1997 Cristian Gafton <gafton@redhat.com>
- added security patch

* Fri Dec 12 1997 Cristian Gafton <gafton@redhat.com>
- updated to 2.0.6pre4
- cleaned up the spec file

* Sun Nov 09 1997 Erik Troan <ewt@redhat.com>
- added setlocale patch from Ulrich

* Wed Nov 05 1997 Erik Troan <ewt@redhat.com>
- added new glob.c from Ulrich

* Wed Oct 29 1997 Erik Troan <ewt@redhat.com>
- fixed timezone patch

* Tue Oct 28 1997 Erik Troan <ewt@redhat.com>
- added patch to fix sense on timezone global

* Sat Oct 25 1997 Erik Troan <ewt@redhat.com>
- build against included kernel headers
- added ld.so patch from ulrich

* Fri Oct 24 1997 Erik Troan <ewt@redhat.com>
- added documentation files as %doc
- improved obsoletes list

* Thu Oct 16 1997 Erik Troan <ewt@redhat.com>
- added patch to fix nfs inet_ntoa() memory leak
- create proper sysdeps/alpha/Implies
- create configparms w/ a here doc, not a separate patch file

* Thu Oct 09 1997 Erik Troan <ewt@redhat.com>
- added patch from Ulrich for rcmd() w/ IP number

* Tue Sep 16 1997 Erik Troan <ewt@redhat.com>
- added obsolete entries 

* Mon Sep 15 1997 Erik Troan <ewt@redhat.com>
- removed /usr/info/dir
- added support for install-info for devel package

* Wed Sep 10 1997 Erik Troan <ewt@redhat.com>
- updated to 2.0.5c

* Wed Sep 10 1997 Erik Troan <ewt@redhat.com>
- added getcwd() fix from Ulrich
- changed datadir to default /usr/share instead of /usr/lib

* Mon Sep 01 1997 Erik Troan <ewt@redhat.com>
- fixed some symlinks (which broke due to the buildroot)

* Thu Aug 28 1997 Erik Troan <ewt@redhat.com>
- removed extrneous symlinks invocation
- removed /etc/localtime from filelist

* Wed Aug 27 1997 Erik Troan <ewt@redhat.com>
- added patch to tcp.h from Ulrich

* Wed Aug 27 1997 Erik Troan <ewt@redhat.com>
- updated to 2.0.5
- removed zic symlink hack

* Sat Aug 23 1997 Erik Troan <ewt@redhat.com>
- minor hack for alpha (won't be necessary in next release)
- switched to use a build root
- dynamically builds file lists

* Tue Aug 19 1997 Erik Troan <ewt@redhat.com>
- 1) Updated to glibc 2.0.5pre5 (version of package is 2.0.4.9)

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- 1) Updated to glibc 2.0.4

* Thu May 15 1997 Erik Troan <ewt@redhat.com>
- 1) Updated to glibc 2.0.3, builds glibc on Intel as well.

* Tue Feb 18 1997 Erik Troan <ewt@redhat.com>
- 1) added patch for shadow to work w/ :: rather then :-1: entries
- 2) incorporated Richard Henderson's string operation fix
- 3) added default /etc/nsswitch.conf
  [2.1.1-1]
- based on RH spec,
- spec rewrited by PLD team,
  we start at GNU libc 2.0.92 one year ago ...
- pl translation by Wojtek ¦lusarczyk <wojtek@shadow.eu.org>.
