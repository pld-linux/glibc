Summary:     GNU libc
Summary(de): GNU-Libc
Summary(fr): GNU libc
Summary(pl): GNU libc
Summary(tr): GNU libc
Name:        glibc
Version:     2.0.7
%define kheaders 2.1.76
%define version 981012
Release:     30
Copyright:   LGPL
Group:       Development/Libraries/Libc
Source0:     glibc-2.0.7-%{version}.tar.gz
Source1:     ftp://prep.ai.mit.edu/pub/gnu/glibc-localedata-2.0.7pre3.tar.gz
Source2:     ftp://prep.ai.mit.edu/pub/gnu/glibc-linuxthreads-2.0.7pre5.tar.gz
Source3:     ftp://prep.ai.mit.edu/pub/gnu/glibc-crypt-2.0.6.tar.gz 
Source4:     glibc-2.0.7-nsswhich.conf
Source5:     linux-include-%{kheaders}.tar.gz
Source6:     glibc-2.0.7-db-mans.tar.gz

Patch0:      glibc-2.0.7-preload.patch
Patch1:      glibc-2.0.7-nonmt.patch
Patch2:      glibc-2.0.7-localedata.patch
Patch3:      glibc-2.0.7-misc.patch
Patch4:      glibc-2.0.7-sparc.patch
Patch5:      glibc-2.0.7-sparc2.patch
Patch6:      glibc-2.0.7-sparc3.patch
Patch7:      glibc-2.0.7-tz.patch
Patch9:      glibc-2.0.7-sparc4.patch
Patch10:     glibc-2.0.6-threads.patch
Patch11:     glibc-2.0.7-pagesize.patch
Patch12:     glibc-2.0.7-getpagesize.patch
Patch13:     glibc-2.0.7-resolv.patch
Patch14: glibc-2.0.7-slovak.patch
Patch15: glibc-2.0.7-serbian.patch
Patch17: glibc-2.0.7-shaper.patch
Patch18: glibc-2.0.7-sparclongjmp2.patch
Patch19:     glibc-localedata_install.patch.gz
Patch100: glibc-2.0.7-kfd.patch

Buildroot:   /tmp/%{name}-%{PACKAGE_VERSION}-root
Obsoletes:   zoneinfo libc-static libc-devel libc-profile libc-headers linuxthreads
Autoreq:     false
%ifarch alpha
Provides: ld.so.2
%else
%endif
%ifarch sparc
Obsoletes: libc
%endif

%description
Contains the standard libraries that are used by multiple programs on
the system. In order to save disk space and memory, as well as to
ease upgrades, common system code is kept in one place and shared between
programs. This package contains the most important sets of shared libraries,
the standard C library and the standard math library. Without these, a
Linux system will not function. It also contains national language (locale)
support and timezone databases.

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
Pakiet ten zawiera standardowe biblioteki, u¿ywane przez ró¿ne programy w
twoim systemie. U¿ywanie przez programy bibliotek z tego pakietu oszczêdza
miejsce na dysku i pamiêæ. Wiekszo¶æ kodu systemowego jest usytu³owane w
jednym miejscu i dzielone miêdzy wieloma programami. Pakiet ten zawiera
bardzo wa¿ny zbiór bibliotek wspó³dzielonych, standardowych bibliotek C i
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

%package debug
Summary: glibc with debugging information
Summary(de): glibc mit Debugging-Info
Summary(fr): glibc contenant des informations pour le débuggage
Summary(tr): Hata ayýklama bilgileriyle oluþturulmuþ glibc
Group: Development/Libraries/Libc
Requires:    %{name} = %{PACKAGE_VERSION}

%description debug
These libraries have the debugging information debuggers use for tracing
the execution of programs. These are only needed when the shared libraries
themselves are being debugged -- they are not needed to debug programs which
use them.

%description -l de debug
Diese Libraries enthalten die Debugging-Daten, die Debuggers zum Verfolgen
der Ausführung von Programmen verwenden. Sie benötigen diese nur, wenn
die gemeinsam genutzten Libraries debugged werden - sie werden zum Debuggen
von Programmen, die sie benutzen, nicht benötigt.

%description -l fr debug
Ces bibliothèques disposent d'information de débuggage pour tracer l'exécution
des programmes. Elles ne sont nécessaires que lorsque les bibliothèques
partagées ont été elles-mêmes débuggées -- elles ne sont pas nécessaires pour
débugger les programmes qui les utilisent.

%description -l tr debug
Programlarýn çalýþmalarýný izlemek (trace) ve hata ayýklamak için kullanýlan
kitaplýklar. Bunlar sadece ortak kitaplýklarýn hatalarýný ayýklamak
isteyenlere gerekecektir.

%package devel
Summary:     Additional libraries required to compile
Summary(de): Weitere Libraries zum Kompilieren
Summary(fr): Librairies supplémentaires nécessaires à la compilation.
Summary(pl): Dodatkowe biblioteki wymagane podczas kompilacji
Summary(tr): Geliþtirme için gerekli diðer kitaplýklar
Group:       Development/Libraries/Libc
Requires:    kernel-headers
Conflicts:   texinfo < 3.11
Prereq:      /sbin/install-info
Requires:    %{name} = %{PACKAGE_VERSION}
Obsoletes:   libc-devel linuxthreads-devel

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
Pakiet ten jest niezbêdny przy tworzeniu w³±snych programów wykorzystuj±cych
standardowe biblioteki C. Znajduj± siê tutaj pliki nag³ówkowe i
pliki objektowe, niezbêdne do kompilacji plików wykonywalnych.

%description -l tr devel
C kitaplýðýný kullanan (ki hemen hemen hepsi kullanýyor) programlar
geliþtirmek için gereken standart baþlýk dosyalarý ve statik kitaplýklar.

%package profile
Summary:     glibc with profiling support
Summary(de): glibc mit Profil-Unterstützung
Summary(fr): glibc avec support pour profiling.
Summary(pl): wersje bibliotek glibc do profajlowania
Summary(tr): Ölçüm desteði olan glibc
Group:       Development/Libraries/Libc
Obsoletes:   libc-profile
Requires:    %{name} = %{PACKAGE_VERSION}

%description profile
When programs are being profiled used gprof, they must use these libraries
instrad of the standard C libraries for gprof to be able to profile
them correctly.

%description -l de profile
Damit Programmprofile mit gprof richtig erstellt werden, müssen diese
Libraries anstelle der üblichen C-Libraries verwendet werden.

%description -l pl profile
Je¿eli program ma byæ poddany badanion z u¿yciem profajlera gprof, to bêdzie
musia³ byæ linkowany z bibliotekami z tego pakietu.

%description -l tr profile
gprof kullanýlarak ölçülen programlar standart C kitaplýðý yerine bu
kitaplýðý kullanmak zorundadýrlar.

%prep
%setup -q -a 1 -a 2 -a 3 -a 5 -a 6
%patch0 -p1 -b .preload
#%patch1 -p0 -b .nonmt
%patch2 -p1 -b .localedata
%patch3 -p1 -b .misc
%ifarch sparc
%patch4 -p1 -b .sparc
%patch5 -p1 -b .sparc2
%patch6 -p1 -b .sparc3
%patch9 -p1 -b .sparc4
%patch12 -p1 -b .getpagesize
%patch18 -p1 -b .sparclongjmp2
%endif
%patch7 -p1 -b .tz
%patch10 -p1 -b .threads
%patch11 -p1 -b .pagesize
%patch14 -p1 -b .slovak
%patch15 -p1 -b .serbian
%patch17 -p1 -b .shaper
%patch19 -p1 -b .localedata_install

# this is the 3000 file descriptors patch...
#patch100 -p1 -b .kfd

ln -s asm-${RPM_ARCH} linux/include/asm
ln -s ../../../../linux/include/linux sysdeps/unix/sysv/linux/linux
ln -s ../../../../linux/include/asm sysdeps/unix/sysv/linux/asm

find . -type f -size 0 -exec rm -f {} \;

%build
autoconf
CFLAGS="$RPM_OPT_FLAGS -g -DNDEBUG=1" \
./configure \
	--enable-add-ons=yes --enable-profile --prefix=/usr
make -r

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/usr/man/man3

make install_root=$RPM_BUILD_ROOT install
make install_root=$RPM_BUILD_ROOT install-locales -C localedata

# the man pages for the linuxthreads require special attention
make -C linuxthreads/man
install linuxthreads/man/*.3thr $RPM_BUILD_ROOT/usr/man/man3
install db/*.3 $RPM_BUILD_ROOT/usr/man/man3

gzip -9nvf $RPM_BUILD_ROOT/usr/info/libc*

rm -rf $RPM_BUILD_ROOT/usr/share/zoneinfo/{localtime,posixtime,posixrules}
# this one conflicts badly with the kernel
rm -rf $RPM_BUILD_ROOT/usr/include/scsi
ln -sf ../../../etc/localtime $RPM_BUILD_ROOT/usr/share/zoneinfo/localtime
ln -sf localtime $RPM_BUILD_ROOT/usr/share/zoneinfo/posixtime
ln -sf localtime $RPM_BUILD_ROOT/usr/share/zoneinfo/posixrules
ln -sf ../../usr/lib/libbsd-compat.a $RPM_BUILD_ROOT/usr/lib/libbsd.a
rm -f $RPM_BUILD_ROOT/etc/localtime

install $RPM_SOURCE_DIR/glibc-2.0.7-nsswhich.conf $RPM_BUILD_ROOT/etc/nsswitch.conf

# This is for ncsd - in glibc 2.1
#install nscd/nscd.conf $RPM_BUILD_ROOT/etc
#mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
#install nscd/nscd.init $RPM_BUILD_ROOT/etc/rc.d/init.d/nscd

# the last bit: more documentation
rm -rf documentation
mkdir documentation
cp linuxthreads/ChangeLog  documentation/ChangeLog.threads
cp linuxthreads/Changes documentation/Changes.threads
cp linuxthreads/README documentation/README.threads
cp linuxthreads/FAQ.html documentation/FAQ-threads.html
cp -r linuxthreads/Examples documentation/examples.threads
cp crypt/README documentation/README.crypt
cp ChangeLog* documentation
gzip -9 documentation/ChangeLog*

strip $RPM_BUILD_ROOT/{lib/*,bin/*,sbin/*,usr/{bin/*,sbin/*}} || :

rm -f $RPM_BUILD_ROOT/usr/include/*.def

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel
/sbin/install-info /usr/info/libc.info.gz /usr/info/dir

%preun devel
if [ "$1" = 0 ]; then
    /sbin/install-info --delete /usr/info/libc.info.gz /usr/info/dir
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644, root, root, 755)
%config /etc/nsswhich.conf
%config /etc/rpc
/usr/share/i18n
/usr/share/locale
/usr/share/zoneinfo
%attr(755, root, root) /lib/*
%attr(755, root, root) /usr/bin/*
%attr(755, root, root) /usr/sbin/*

%files devel
%defattr(644, root, root, 755)
%doc README NEWS FAQ BUGS NOTES PROJECTS documentation/*
/usr/include/*
/usr/lib/*.o         
/usr/lib/lib*.so
/usr/info/*info*.gz
%attr(644, root, man) /usr/man/man3/*
/usr/lib/libBrokenLocale.a
/usr/lib/libbsd-compat.a
/usr/lib/libbsd.a
/usr/lib/libc.a
/usr/lib/libc_nonshared.a
/usr/lib/libcrypt.a
/usr/lib/libdb.a
/usr/lib/libdl.a
/usr/lib/libieee.a
/usr/lib/libm.a
/usr/lib/libmcheck.a
/usr/lib/libndbm.a
/usr/lib/libnsl.a
/usr/lib/libposix.a
/usr/lib/libpthread.a
/usr/lib/libresolv.a
/usr/lib/librpcsvc.a
/usr/lib/libutil.a

%files profile
%attr(644, root, root) /usr/lib/lib*_p.a

%files debug
%attr(644, root, root) /usr/lib/libg.a

%changelog
* Sat Oct 10 1998 Cristian Gafton <gafton@redhat.com>
- updated to fix some of the memory leaks in the dl code

* Wed Sep 30 1998 Cristian Gafton <gafton@redhat.com>
- ypall UDP socket leak fixed
- add if_shaper.h
- list ruffian as a supported arch
- serbian locale support
- slovak patches in

* Sun Sep 13 1998 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [2.0.7-24]
- changed Buildroot to /tmp/%%{name}-%%{version}-root,
- added using %%{name} and %%{version} in Source,
- changed dependencies to "Requires: %%{name} = %%{version}" in devel
  subpackage,
- added full %attr description in %files,
- removed INSTALL from %doc,
- added stripping programs and shared libraries,
- all %doc moved to devel.

* Thu Sep 10 1998 Cristian Gafton <gafton@redhat.com>
  [2.0.7-23]
- resolver timeout fix on un-networked systems

* Thu Aug 27 1998 Cristian Gafton <gafton@redhat.com>
- fix for tmp race condition on glibcbug
- fix for getpagesize() in sparc
- man pages for the db functions (from old db-1.85)

* Thu Aug 20 1998 Jeff Johnson <jbj@redhat.com>
- patches for debugging threads (http://odin.appliedtheory.com/).

* Mon Aug 17 1998 Cristian Gafton <gafton@redhat.com>
- new cvs version and patch top fix some typos

* Thu Aug 13 1998 Jakub Jelinek <jj@ultra.linux.cz>
- Fix SPARC longjmp to allow threaded apps (sparc4)
- install in localedata requires chroot to be in $PATH

* Thu Jul 23 1998 Cristian Gafton <gafton@redhat.com>
- upgraded the cvs snapshot to match the "official" pre5 release
- also upgraded the linuxthreads package
- changelog is not at the end of the spec file.

* Mon Jul 20 1998 Cristian Gafton <gafton@redhat.com>
- added patch for socketbits.h to define CMSG_LEN/ALIGN/SPACE

* Sat Jul 11 1998 Cristian Gafton <gafton@redhat.com>
- upgraded again from the cvs version to catch the paranoia env patch
- added a patch to fix the backport of the env paranoia found in the CVS

* Fri Jun 26 1998 Cristian Gafton <gafton@redhat.com>
- updated the cvs version
- added a (maybe way too paranoid) tz patch

* Wed Jun 03 1998 Jeff Johnson <jbj@redhat.com>
- Add sparc patches from davem.

* Sat May 23 1998 Cristian Gafton <gafton@redhat.com>
- updated again sbapshot to catch the latest rpc fixes

* Thu May 21 1998 Cristian Gafton <gafton@redhat.com>
- updated snapshot to include the fixed time patches
- added Jeff's sparc patch 

* Wed May 20 1998 Cristian Gafton <gafton@redhat.com>
- added time-related patches for tzset & friends

* Sat May 09 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu May 07 1998 Cristian Gafton <gafton@redhat.com>
- added a patch to fix the pow function (ulrich drepper, pointed out by
  andreas jaeger)
- updated snapshot

* Wed May 06 1998 Cristian Gafton <gafton@redhat.com>
- updated snapshot
- fixed sethostid which used to require the slack-dead /var/adm dir

* Sat May 02 1998 Cristian Gafton <gafton@redhat.com>
- fixed russian locale problem
- alpha should now link again statically. Patch from rth

* Sat Apr 18 1998 Cristian Gafton <gafton@redhat.com>
- updated snapchot and added a patch to fix a closelog() problem

* Tue Apr 14 1998 Cristian Gafton <gafton@redhat.com>
- updated snapshot and added a new patch to fix __open_catalog
- added AutoReqProv: false to help break some circular dependencies

* Mon Apr 06 1998 Cristian Gafton <gafton@redhat.com>
- updated glibc snapshot

* Sat Apr 04 1998 Cristian Gafton <gafton@redhat.com>
- updated snapshot; rebuilt package on alpha with egcs

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
- swhiched to use a build root
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
- 3) added default /etc/nsswhich.conf
  [2.1.1-1]
- based on RH spec,
- spec rewrited by PLD team,
  we start at GNU libc 2.0.92 one year ago ...
- pl translation by Wojtek ¦lusarczyk <wojtek@shadow.eu.org>.
