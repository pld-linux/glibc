#
# You can define min_kernel macro by "rpm --define 'min_kernel version'"
# default is 2.4.6 for linuxthreads, 2.6.0 for NPTL
#
# Conditional build:
%bcond_with	omitfp		# build without frame pointer (pass \--enable-omitfp)
%bcond_without	memusage	# don't build memusage utility
%bcond_with	kernelheaders	# use headers from %{_kernelsrcdir} instead of
				# linux-libc-headers (evil, breakage etc., don't use)
%bcond_without	linuxthreads	# don't build linuxthreads version (NPTL only)
%bcond_without	nptl		# don't build NPTL version (linuxthreads only)
%bcond_without	tls		# don't support TLS at all (implies no NPTL)
%bcond_with	__thread	# use TLS in linuxthreads
%bcond_without	selinux		# without SELinux support (in nscd)
%bcond_with	tests		# perform "make test"
%bcond_with	tests_nptl	# perform NPTL tests on dual build (requires 2.6.x kernel)
%bcond_without	localedb	# don't build localedb-all (is time consuming)
%bcond_with	cross		# build using crossgcc (without libgcc_eh)
#
# TODO:
# - look at locale fixes/updates in bugzilla
# [OLD]
# - localedb-gen man pages(?)
# - fix what trojan broke while upgreading (getaddrinfo-workaround)
# - math/{test-fenv,test-tgmath,test-float,test-ifloat},
#   linuxthreads/tst-cancel8, debug/backtrace-tst(SEGV)  fail on alpha
# - problem compiling with --enable-bounded (must be reported to libc-alpha)
#   (is this comment still valid???)
#

%{!?min_kernel:%global          min_kernel      2.4.6}
%if "%{min_kernel}" < "2.6.0"
%global		nptl_min_kernel	2.6.0
%else
%global		nptl_min_kernel	%{min_kernel}
%endif

%if %{with tls}
# sparc temporarily removed (broken)
%ifnarch %{ix86} amd64 ia64 alpha s390 s390x sparc64 sparcv9 ppc ppc64
%undefine	with_tls
%endif
%endif

%if %{with nptl}
# on x86 uses cmpxchgl (available since i486)
# on sparc only sparcv9 is supported
%ifnarch i486 i586 i686 pentium3 pentium4 athlon amd64 ia64 alpha s390 s390x sparc64 sparcv9 ppc ppc64
%undefine	with_nptl
%else
%if %{without tls}
%undefine	with_nptl
%endif
%endif
%endif

%ifarch sparc64
%undefine	with_memusage
%endif

%if %{with linuxthreads} && %{with nptl}
%define		with_dual	1
%endif

%define		llh_version	7:2.6.10.0-3

Summary:	GNU libc
Summary(de):	GNU libc
Summary(es):	GNU libc
Summary(fr):	GNU libc
Summary(ja):	GNU libc ¥é¥¤¥Ö¥é¥ê
Summary(pl):	GNU libc
Summary(ru):	GNU libc ×ÅÒÓÉÉ 2.3
Summary(tr):	GNU libc
Summary(uk):	GNU libc ×ÅÒÓ¦§ 2.3
Name:		glibc
Version:	2.3.5
Release:	0.1
Epoch:		6
License:	LGPL
Group:		Libraries
Source0:	ftp://sources.redhat.com/pub/glibc/releases/%{name}-%{version}.tar.bz2
# Source0-md5:	93d9c51850e0513aa4846ac0ddcef639
Source1:	ftp://sources.redhat.com/pub/glibc/releases/%{name}-linuxthreads-%{version}.tar.bz2
# Source1-md5:	77011b0898393c56b799bc011a0f37bf
Source2:	nscd.init
Source3:	nscd.sysconfig
Source4:	nscd.logrotate
#Source5:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-man-pages.tar.bz2
Source5:	%{name}-man-pages.tar.bz2
# Source5-md5:	03bee93e9786b3e7dad2570ccb0cbc5c
#Source6:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-non-english-man-pages.tar.bz2
Source6:	%{name}-non-english-man-pages.tar.bz2
# Source6-md5:	6159f0a9b6426b5f6fc1b0d8d21b9b76
Source7:	%{name}-localedb-gen
Patch0:		%{name}-info.patch
Patch1:		%{name}-pl.po-update.patch
Patch2:		%{name}-pld.patch
Patch3:		%{name}-crypt-blowfish.patch
Patch4:		%{name}-linuxthreads-lock.patch
Patch5:		%{name}-pthread_create-manpage.patch
Patch6:		%{name}-paths.patch
Patch7:		%{name}-postshell.patch
Patch8:		%{name}-missing-nls.patch
Patch9:		%{name}-java-libc-wait.patch
Patch10:	%{name}-lthrds_noomit.patch
Patch11:	%{name}-no_opt_override.patch
Patch12:	%{name}-includes.patch
Patch13:	%{name}-soinit-EH_FRAME.patch
Patch14:	%{name}-sparc-errno_fix.patch
Patch15:	%{name}-csu-quotes.patch
Patch16:	%{name}-tests-noproc.patch
Patch17:	%{name}-new-charsets.patch
Patch18:	%{name}-sr_CS.patch
Patch19:	%{name}-sparc64-dl-machine.patch
Patch20:	%{name}-tzfile-noassert.patch
Patch21:	%{name}-morelocales.patch
Patch22:	%{name}-locale_ZA.patch
Patch23:	%{name}-locale_fixes.patch
Patch24:	%{name}-ZA_collate.patch
Patch25:	%{name}-tls_fix.patch
Patch26:	%{name}-iconvconfig-nxstack.patch
Patch27:	%{name}-execvp.patch
Patch28:	%{name}-cross-gcc_eh.patch
Patch29:	%{name}-gcc4.patch
Patch30:	%{name}-no_uint128_t.patch
# PaX hack (dropped)
#PatchX:	%{name}-pax_dl-execstack.patch
URL:		http://www.gnu.org/software/libc/
BuildRequires:	automake
BuildRequires:	binutils >= 2:2.15.90.0.3
BuildRequires:	gcc >= 3.2
%ifarch ppc ppc64 sparc sparcv9 sparc64
%if %{with nptl} || %{with __thread}
BuildRequires:	gcc >= 5:3.4
%endif
%endif
%{?with_memusage:BuildRequires:	gd-devel >= 2.0.1}
BuildRequires:	gettext-devel >= 0.10.36
%if %{without kernelheaders}
BuildRequires:	linux-libc-headers >= %{llh_version}
%endif
%{?with_selinux:BuildRequires:	libselinux-devel >= 1.18}
BuildRequires:	perl-base
BuildRequires:	rpm-build >= 4.3-0.20030610.28
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.159
BuildRequires:	sed >= 4.0.5
BuildRequires:	texinfo
AutoReq:	false
PreReq:		basesystem
Requires:	glibc-misc = %{epoch}:%{version}-%{release}
%{?with_tls:Provides:	glibc(tls)}
Provides:	ldconfig
Provides:	/sbin/ldconfig
Obsoletes:	%{name}-common
Obsoletes:	%{name}-debug
Obsoletes:	ldconfig
Conflicts:	kernel < %{min_kernel}
Conflicts:	ld.so < 1.9.9-10
Conflicts:	man-pages < 1.43
Conflicts:	rc-scripts < 0.3.1-13
Conflicts:	rpm < 4.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		debugcflags	-O1 -g
# avoid -s here (ld.so must not be stripped to allow any program debugging)
%define		rpmldflags	%{nil}
%define 	specflags_sparc64	-mcpu=ultrasparc -mvis -fcall-used-g6
# we don't want perl dependency in glibc-devel
%define		_noautoreqfiles		%{_bindir}/mtrace
# hack: don't depend on rpmlib(PartialHardlinkSets) for easier upgrade from Ra
# (hardlinks here are unlikely to be "partial"... and rpm 4.0.2 from Ra was
# patched not to crash on partial hardlinks too)
%define		_hack_dontneed_PartialHardlinkSets	1
%define		_noautochrpath		.*\\(ldconfig\\|sln\\)
%if %{with kernelheaders}
%define		sysheaders	%{_kernelsrcdir}/include
%else
%define		sysheaders	%{_includedir}
%endif

%description
Contains the standard libraries that are used by multiple programs on
the system. In order to save disk space and memory, as well as to ease
upgrades, common system code is kept in one place and shared between
programs. This package contains the most important sets of shared
libraries, the standard C library and the standard math library.
Without these, a Linux system will not function. It also contains
national language (locale) support and timezone databases.

Can be used on: Linux kernel >= %{min_kernel}.

%description -l es
Contiene las bibliotecas estándared que son usadas por varios
programas del sistema. Para ahorrar el espacio en el disco y la
memoria, igual que para facilitar actualizaciones, código común del
sistema se guarda en un sitio y es compartido entre los programas.
Este paquete contiene las bibliotecas compartidas más importantes, es
decir la biblioteca C estándar y la biblioteca estándar de matemática.
Sin éstas, un sistema Linux no podrá funcionar. También está incluido
soporte de idiomas nacionales (locale) y bases de datos de zona de
tiempo.

Puede usarse con: núcleo Linux >= %{min_kernel}.

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

Can be used on: Linux kernel >= %{min_kernel}.

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

Can be used on: Linux kernel >= %{min_kernel}.

%description -l ja
glibc
¥Ñ¥Ã¥±¡¼¥¸¤Ï¥·¥¹¥Æ¥à¾å¤ÎÊ£¿ô¤Î¥×¥í¥°¥é¥à¤Ç»È¤ï¤ì¤ëÉ¸½à¥é¥¤¥Ö¥é¥ê¤ò
¤Õ¤¯¤ß¤Þ¤¹¡£¥Ç¥£¥¹¥¯¥¹¥Ú¡¼¥¹¤È¥á¥â¥ê¤òÀáÌó¤·¤¿¤ê¡¢¥¢¥Ã¥×¥°¥ì¡¼¥É¤ò
ÍÑ°Õ¤Ë¤¹¤ë¤¿¤á¤Ë¡¢¶¦ÄÌ¤Î¥·¥¹¥Æ¥à¥³¡¼¥É¤Ï°ì¤Ä¤Î¾ì½ê¤Ë¤ª¤«¤ì¡¢¥×¥í¥°¥é¥à
´Ö¤Ç¶¦Í­¤µ¤ì¤Þ¤¹¡£¤³¤ÎÉôÊ¬Åª¤Ê¥Ñ¥Ã¥±¡¼¥¸¤Ï¥·¥§¥¢¥É¥é¥¤¥Ö¥é¥ê¤Î¤«¤Ê¤ê
½ÅÍ×¤Ê¥»¥Ã¥È¤ò¤Õ¤¯¤ß¤Þ¤¹: É¸½à C ¥é¥¤¥Ö¥é¥ê¤ÈÉ¸½à¿ôÃÍ¥é¥¤¥Ö¥é¥ê¤Ç¤¹¡£
¤³¤ÎÆó¤Ä¤Î¥é¥¤¥Ö¥é¥êÈ´¤­¤Ç¤Ï¡¢Linux ¥·¥¹¥Æ¥à¤Ïµ¡Ç½¤·¤Þ¤»¤ó¡£ glibc
¥Ñ¥Ã¥±¡¼¥¸¤Ï¤Þ¤¿ÃÏ°è¸À¸ì (locale) ¥µ¥Ý¡¼¥È¤È¥¿¥¤¥à¥¾¡¼¥ó¥Ç¡¼¥¿¥Ù¡¼¥¹
¥µ¥Ý¡¼¥È¤ò¤Õ¤¯¤ß¤Þ¤¹¡£

Can be used on: Linux kernel >= %{min_kernel}.

%description -l pl
W pakiecie znajduj± siê podstawowe biblioteki, u¿ywane przez ró¿ne
programy w Twoim systemie. U¿ywanie przez programy bibliotek z tego
pakietu oszczêdza miejsce na dysku i pamiêæ. Wiêkszo¶æ kodu
systemowego jest usytuowane w jednym miejscu i dzielone miêdzy wieloma
programami. Pakiet ten zawiera bardzo wa¿ny zbiór bibliotek
standardowych, wspó³dzielonych (dynamicznych) bibliotek C i
matematycznych. Bez glibc system Linux nie jest w stanie funkcjonowaæ.
Znajduj± siê tutaj równie¿ definicje ró¿nych informacji dla wielu
jêzyków (locale) oraz definicje stref czasowych.

Przeznaczony dla j±dra Linux >= %{min_kernel}.

%description -l ru
óÏÄÅÒÖÉÔ ÓÔÁÎÄÁÒÔÎÙÅ ÂÉÂÌÉÏÔÅËÉ, ÉÓÐÏÌØÚÕÅÍÙÅ ÍÎÏÇÏÞÉÓÌÅÎÎÙÍÉ
ÐÒÏÇÒÁÍÍÁÍÉ × ÓÉÓÔÅÍÅ. äÌÑ ÔÏÇÏ, ÞÔÏÂÙ ÓÏÈÒÁÎÉÔØ ÄÉÓËÏ×ÏÅ ÐÒÏÓÔÒÁÎÓÔ×Ï
É ÐÁÍÑÔØ, Á ÔÁËÖÅ ÄÌÑ ÐÒÏÓÔÏÔÙ ÏÂÎÏ×ÌÅÎÉÑ, ÓÉÓÔÅÍÎÙÊ ËÏÄ, ÏÂÝÉÊ ÄÌÑ
×ÓÅÈ ÐÒÏÇÒÁÍÍ, ÈÒÁÎÉÔÓÑ × ÏÄÎÏÍ ÍÅÓÔÅ É ËÏÌÌÅËÔÉ×ÎÏ ÉÓÐÏÌØÚÕÅÔÓÑ ×ÓÅÍÉ
ÐÒÏÇÒÁÍÍÁÍÉ. üÔÏÔ ÐÁËÅÔ ÓÏÄÅÒÖÉÔ ÎÁÉÂÏÌÅÅ ×ÁÖÎÙÅ ÉÚ ÒÁÚÄÅÌÑÅÍÙÈ
ÂÉÂÌÉÏÔÅË - ÓÔÁÎÄÁÒÔÎÕÀ ÂÉÂÌÉÏÔÅËÕ C É ÓÔÁÎÄÁÒÔÎÕÀ ÂÉÂÌÉÏÔÅËÕ
ÍÁÔÅÍÁÔÉËÉ. âÅÚ ÜÔÉÈ ÂÉÂÌÉÏÔÅË Linux ÆÕÎËÃÉÏÎÉÒÏ×ÁÔØ ÎÅ ÂÕÄÅÔ. ôÁËÖÅ
ÐÁËÅÔ ÓÏÄÅÒÖÉÔ ÐÏÄÄÅÒÖËÕ ÎÁÃÉÏÎÁÌØÎÙÈ ÑÚÙËÏ× (locale) É ÂÁÚÙ ÄÁÎÎÙÈ
×ÒÅÍÅÎÎÙÈ ÚÏÎ (timezone databases).

Can be used on: Linux kernel >= %{min_kernel}.

%description -l tr
Bu paket, birçok programýn kullandýðý standart kitaplýklarý içerir.
Disk alaný ve bellek kullanýmýný azaltmak ve ayný zamanda güncelleme
iþlemlerini kolaylaþtýrmak için ortak sistem kodlarý tek bir yerde
tutulup programlar arasýnda paylaþtýrýlýr. Bu paket en önemli ortak
kitaplýklarý, standart C kitaplýðýný ve standart matematik kitaplýðýný
içerir. Bu kitaplýklar olmadan Linux sistemi çalýþmayacaktýr. Yerel
dil desteði ve zaman dilimi veri tabaný da bu pakette yer alýr.

Can be used on: Linux kernel >= %{min_kernel}.

%description -l uk
í¦ÓÔÉÔØ ÓÔÁÎÄÁÒÔÎ¦ Â¦ÂÌ¦ÏÔÅËÉ, ËÏÔÒ¦ ×ÉËÏÒÉÓÔÏ×ÕÀÔØÓÑ ÞÉÓÌÅÎÎÉÍÉ
ÐÒÏÇÒÁÍÁÍÉ × ÓÉÓÔÅÍ¦. äÌÑ ÔÏÇÏ, ÝÏÂ ÚÂÅÒÅÇÔÉ ÄÉÓËÏ×ÉÊ ÐÒÏÓÔ¦Ò ÔÁ
ÐÁÍ'ÑÔØ, Á ÔÁËÏÖ ÄÌÑ ÐÒÏÓÔÏÔÉ ÐÏÎÏ×ÌÅÎÎÑ ÓÉÓÔÅÍÉ, ÓÉÓÔÅÍÎÉÊ ËÏÄ,
ÓÐ¦ÌØÎÉÊ ÄÌÑ ×Ó¦È ÐÒÏÇÒÁÍ, ÚÂÅÒ¦ÇÁ¤ÔØÓÑ × ÏÄÎÏÍÕ Í¦ÓÃ¦ ¦ ËÏÌÅËÔÉ×ÎÏ
×ÉËÏÒÉÓÔÏ×Õ¤ÔØÓÑ ×Ó¦ÍÁ ÐÒÏÇÒÁÍÁÍÉ. ãÅÊ ÐÁËÅÔ Í¦ÓÔÉÔØ ÎÁÊÂ¦ÌØÛ ×ÁÖÌÉ×¦
Ú ÄÉÎÁÍ¦ÞÎÉÈ Â¦ÂÌ¦ÏÔÅË - ÓÔÁÎÄÁÒÔÎÕ Â¦ÂÌ¦ÏÔÅËÕ ó ÔÁ ÓÔÁÎÄÁÒÔÎÕ
Â¦ÂÌ¦ÏÔÅËÕ ÍÁÔÅÍÁÔÉËÉ. âÅÚ ÃÉÈ Â¦ÂÌ¦ÏÔÅË Linux ÆÕÎËÃ¦ÏÎÕ×ÁÔÉ ÎÅ ÂÕÄÅ.
ôÁËÏÖ ÐÁËÅÔ Í¦ÓÔÉÔØ Ð¦ÄÔÒÉÍËÕ ÎÁÃ¦ÏÎÁÌØÎÉÈ ÍÏ× (locale) ÔÁ ÂÁÚÉ ÄÁÎÎÉÈ
ÞÁÓÏ×ÉÈ ÚÏÎ (timezone databases).

Can be used on: Linux kernel >= %{min_kernel}.

%package misc
Summary:	Utilities and data used by glibc
Summary(pl):	Narzêdzia i dane u¿ywane przez glibc
Group:		Development/Libraries
AutoReq:	false
PreReq:		%{name} = %{epoch}:%{version}-%{release}

%description misc
Utilities and data used by glibc.

%description misc -l pl
Narzêdzia i dane u¿ywane przez glibc.

%package devel
Summary:	Additional libraries required to compile
Summary(de):	Weitere Libraries zum Kompilieren
Summary(es):	Bibliotecas adicionales necesarias para la compilación
Summary(fr):	Librairies supplémentaires nécessaires à la compilation
Summary(ja):	É¸½à C ¥é¥¤¥Ö¥é¥ê¤Ç»È¤ï¤ì¤ë¥Ø¥Ã¥À¡¼¤È¥ª¥Ö¥¸¥§¥¯¥È¥Õ¥¡¥¤¥ë
Summary(pl):	Dodatkowe biblioteki wymagane podczas kompilacji
Summary(ru):	äÏÐÏÌÎÉÔÅÌØÎÙÅ ÂÉÂÌÉÏÔÅËÉ, ÎÅÏÂÈÏÄÉÍÙÅ ÄÌÑ ËÏÍÐÉÌÑÃÉÉ
Summary(tr):	Geliþtirme için gerekli diðer kitaplýklar
Summary(uk):	äÏÄÁÔËÏ×¦ Â¦ÂÌ¦ÏÔÅËÉ, ÐÏÔÒ¦ÂÎ¦ ÄÌÑ ËÏÍÐ¦ÌÑÃ¦§
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
%{!?with_kernelheaders:Requires:	linux-libc-headers >= %{llh_version}}
Obsoletes:	libiconv-devel
Obsoletes:	glibc-headers

%description devel
To develop programs which use the standard C libraries (which nearly
all programs do), the system needs to have these standard header files
and object files available for creating the executables.

%description devel -l de
Bei der Entwicklung von Programmen, die die Standard-C-Libraries
verwenden (also fast alle), benötigt das System diese Standard-Header-
und Objektdateien zum Erstellen der ausführbaren Programme.

%description devel -l es
Para desarrollar programas que utilizan las bibliotecas C estándar (lo
cual hacen prácticamente todos los programas), el sistema necesita
disponer de estos ficheros de cabecera y de objetos para crear los
ejecutables.

%description devel -l fr
Pour développer des programmes utilisant les bibliothèques standard du
C (ce que presque tous les programmes font), le système doit posséder
ces fichiers en-têtes et objets standards pour créer les exécutables.

%description devel -l ja
glibc-devel ¥Ñ¥Ã¥±¡¼¥¸¤Ï(¤Û¤È¤ó¤É¤¹¤Ù¤Æ¤Î¥×¥í¥°¥é¥à¤Ç»È¤ï¤ì¤ë)É¸½à C
¥é¥¤¥Ö¥é¥ê¤ò»ÈÍÑ¤·¤¿¥×¥í¥°¥é¥à¤ò³«È¯¤¹¤ë¤¿¤á¤Î¥Ø¥Ã¥À¡¼¤È¥ª¥Ö¥¸¥§¥¯¥È
¥Õ¥¡¥¤¥ë¤ò´Þ¤ß¤Þ¤¹¡£¤â¤·É¸½à C
¥é¥¤¥Ö¥é¥ê¤ò»ÈÍÑ¤¹¤ë¥×¥í¥°¥é¥à¤ò³«È¯¤¹¤ë¤Ê¤é
¼Â¹Ô¥Õ¥¡¥¤¥ë¤òºîÀ®¤¹¤ëÌÜÅª¤Ç¤³¤ì¤é¤ÎÉ¸½à¥Ø¥Ã¥À¤È¥ª¥Ö¥¸¥§¥¯¥È¥Õ¥¡¥¤¥ë
¤¬»ÈÍÑ¤Ç¤­¤Þ¤¹¡£

%description devel -l pl
Pakiet ten jest niezbêdny przy tworzeniu w³asnych programów
korzystaj±cych ze standardowej biblioteki C. Znajduj± siê tutaj pliki
nag³ówkowe oraz pliki obiektowe, niezbêdne do kompilacji programów
wykonywalnych i innych bibliotek.

%description devel -l ru
äÌÑ ÒÁÚÒÁÂÏÔËÉ ÐÒÏÇÒÁÍÍ, ÉÓÐÏÌØÚÕÀÝÉÈ ÓÔÁÎÄÁÒÔÎÙÅ ÂÉÂÌÉÏÔÅËÉ C (Á
ÐÒÁËÔÉÞÅÓËÉ ×ÓÅ ÐÒÏÇÒÁÍÍÙ ÉÈ ÉÓÐÏÌØÚÕÀÔ), ÓÉÓÔÅÍÅ îåïâèïäéíù ÈÅÄÅÒÙ É
ÏÂßÅËÔÎÙÅ ÆÁÊÌÙ, ÓÏÄÅÒÖÁÝÉÅÓÑ × ÜÔÏÍ ÐÁËÅÔÅ, ÞÔÏÂÙ ÓÏÚÄÁ×ÁÔØ
ÉÓÐÏÌÎÑÅÍÙÅ ÆÁÊÌÙ.

%description devel -l tr
C kitaplýðýný kullanan (ki hemen hemen hepsi kullanýyor) programlar
geliþtirmek için gereken standart baþlýk dosyalarý ve statik
kitaplýklar.

%description devel -l uk
äÌÑ ÒÏÚÒÏÂËÉ ÐÒÏÇÒÁÍ, ÝÏ ×ÉËÏÒÉÓÔÏ×ÕÀÔØ ÓÔÁÎÄÁÒÔÎ¦ Â¦ÂÌ¦ÏÔÅËÉ C
(ÐÒÁËÔÉÞÎÏ ×Ó¦ ÐÒÏÇÒÁÍÉ §È ×ÉËÏÒÉÓÔÏ×ÕÀÔØ), ÓÉÓÔÅÍ¦ îåïâè¶äî¶ ÈÅÄÅÒÉ
ÔÁ ÏÂ'¤ËÔÎ¦ ÆÁÊÌÉ, ÝÏ Í¦ÓÔÑÔØÓÑ × ÃØÏÍÕ ÐÁËÅÔ¦, ÃÏÂ ÓÔ×ÏÒÀ×ÁÔÉ
×ÉËÏÎÕ×ÁÎ¦ ÆÁÊÌÉ.

%package -n nscd
Summary:	Name Service Caching Daemon
Summary(es):	Demonio de caché del servicio de nombres
Summary(ja):	¥Í¡¼¥à¥µ¡¼¥Ó¥¹¥­¥ã¥Ã¥·¥ó¥°¥Ç¡¼¥â¥ó (nacd)
Summary(pl):	Demon zapamiêtuj±cy odpowiedzi serwisów nazw
Summary(ru):	ëÜÛÉÒÕÀÝÉÊ ÄÅÍÏÎ ÓÅÒ×ÉÓÏ× ÉÍÅÎ
Summary(uk):	ëÅÛÕÀÞÉÊ ÄÅÍÏÎ ÓÅ×¦Ó¦× ¦ÍÅÎ
Group:		Networking/Daemons
PreReq:		rc-scripts >= 0.2.0
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(post,preun):	/sbin/chkconfig
Requires(post):	fileutils
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires:	%{name} = %{epoch}:%{version}-%{release}
%{?with_selinux:Requires:	libselinux >= 1.18}
Provides:	group(nscd)
Provides:	user(nscd)

%description -n nscd
nscd caches name service lookups; it can dramatically improve
performance with NIS+, and may help with DNS as well.

%description -n nscd -l es
nscd guarda las peticiones del servicio de nombres en una caché; eso
puede aumentar drásticamente las prestaciones de NIS+, y también puede
ayudar con DNS.

%description -n nscd -l ja
Nscd ¤Ï¥Í¡¼¥à¥µ¡¼¥Ó¥¹»²¾È¤ò¥­¥ã¥Ã¥·¥å¤·¡¢NIS+ ¤Î¥Ñ¥Õ¥©¡¼¥Þ¥ó¥¹¤ò
¥É¥é¥Þ¥Æ¥£¥Ã¥¯¤Ë²þÁ±¤¹¤ë¤³¤È¤¬¤Ç¤­¡¢DNS ¤òÆ±ÍÍ¤ËÊä½õ¤·¤Þ¤¹¡£

%description -n nscd -l pl
nscd zapamiêtuje zapytania i odpowiedzi NIS oraz DNS. Pozwala
drastycznie poprawiæ szybko¶æ dzia³ania NIS+.

%description -n nscd -l ru
nscd ËÜÛÉÒÕÅÔ ÒÅÚÕÌØÔÁÔÙ ÚÁÐÒÏÓÏ× Ë ÓÅÒ×ÉÓÁÍ ÉÍÅÎ; ÜÔÏ ÍÏÖÅÔ ÒÅÚËÏ
Õ×ÅÌÉÞÉÔØ ÐÒÏÉÚ×ÏÄÉÔÅÌØÎÏÓÔØ ÒÁÂÏÔÙ Ó NIS+ É, ÔÁËÖÅ, ÍÏÖÅÔ ÐÏÍÏÞØ Ó
DNS.

%description -n nscd -l uk
nscd ËÅÛÕ¤ ÒÅÚÕÌØÔÁÔÉ ÚÁÐÒÏÓ¦× ÄÏ ÓÅÒ×¦Ó¦× ¦ÍÅÎ; ÃÅ ÍÏÖÅ ÓÉÌØÎÏ
ÚÂ¦ÌØÛÉÔÉ Û×ÉÄË¦ÓÔØ ÒÏÂÏÔÉ Ú NIS+ ¦, ÔÁËÏÖ, ÍÏÖÅ ÄÏÐÏÍÏÇÔÉ Ú DNS.

%package -n localedb-src
Summary:	locale database source code
Summary(es):	Código fuente de la base de datos de los locales
Summary(pl):	Kod ¼ród³owy bazy locale
Group:		Daemons
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	gzip
Requires:	sed

%description -n localedb-src
This add-on package contains the data needed to build the locale data
files to use the internationalization features of the GNU libc.

%description -n localedb-src -l es
Este paquete adicional contiene los datos necesarios para construir
los ficheros de locale, imprescindibles para usar las cualidades de
internacionalización de GNU libc.

%description -n localedb-src -l pl
Pakiet ten zawiera dane niezbêdne do zbudowania binarnych plików
lokalizacyjnych, by móc wykorzystaæ mo¿liwo¶ci oferowane przez GNU
libc.

%package localedb-all
Summary:	locale database for all locales supported by glibc
Summary(es):	Base de datos de todos los locales soportados por glibc
Summary(pl):	Baza danych locale dla wszystkich lokalizacji obs³ugiwanych przez glibc
Group:		Libraries
Requires:	iconv = %{epoch}:%{version}-%{release}
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description localedb-all
This package contains locale database for all locales supported by
glibc. In glibc 2.3.x it's one large file (about 39MB) - if you want
something smaller with support for chosen locales only, consider
installing localedb-src and regenerating database using localedb-gen
script (when database is generated, localedb-src can be uninstalled).

%description localedb-all -l es
Este paquete contiene una base de datos de todos los locales
soportados por glibc. En glibc 2.3.x ése es un fichero grande (aprox.
39 MB) -- si prefiere algo más pequeño, sólo con soporte de unos
locales elegidos, considérese instalar localedb-src y regenerar la
base de datos usando el escript localedb-gen (una vez que la base de
datos esté creada, localedb-src se podrá desinstalar).

%description localedb-all -l pl
Ten pakiet zawiera bazê danych locale dla wszystkich lokalizacji
obs³ugiwanych przez glibc. W glibc 2.3.x jest to jeden du¿y plik
(oko³o 39MB); aby mieæ co¶ mniejszego, z obs³ug± tylko wybranych
lokalizacji, nale¿y zainstalowaæ pakiet localedb-src i przegenerowaæ
bazê danych przy u¿yciu skryptu localedb-gen (po wygenerowaniu bazy
pakiet localedb-src mo¿na odinstalowaæ).

%package -n iconv
Summary:	Convert encoding of given files from one encoding to another
Summary(es):	Convierte entre varias codificaciones de los ficheros dados
Summary(pl):	Program do konwersji plików tekstowych z jednego kodowania do innego
Group:		Applications/Text
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n iconv
Convert encoding of given files from one encoding to another. You need
this package if you want to convert some document from one encoding to
another or if you have installed some programs which use Generic
Character Set Conversion Interface.

%description -n iconv -l es
Convierte la codificación de dados ficheros. Necesita este paquete si
quiere convertir un documento entre una codificación (juego de
caracteres) y otra, o si tiene instalado algún programa que usa el
Generic Character Set Conversion Interface (interfaz genérica de
conversión de juegos de caracteres).

%description -n iconv -l pl
Program do konwersji plików tekstowych z jednego kodowania do innego.
Musisz mieæ zainstalowany ten pakiet je¿eli wykonujesz konwersjê
dokumentów z jednego kodowania do innego lub je¿eli masz zainstalowane
jakie¶ programy, które korzystaj± z Generic Character Set Conversion
Interface w glibc, czyli z zestawu funkcji z tej biblioteki, które
umo¿liwiaj± konwersjê kodowania danych z poziomu dowolnego programu.

%package static
Summary:	Static libraries
Summary(es):	Bibliotecas estáticas
Summary(pl):	Biblioteki statyczne
Summary(ru):	óÔÁÔÉÞÅÓËÉÅ ÂÉÂÌÉÏÔÅËÉ glibc
Summary(uk):	óÔÁÔÉÞÎ¦ Â¦ÂÌ¦ÏÔÅËÉ glibc
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}
Obsoletes:	libiconv-static

%description static
GNU libc static libraries.

%description static -l es
Bibliotecas estáticas de GNU libc.

%description static -l pl
Biblioteki statyczne GNU libc.

%description static -l ru
üÔÏ ÏÔÄÅÌØÎÙÊ ÐÁËÅÔ ÓÏ ÓÔÁÔÉÞÅÓËÉÍÉ ÂÉÂÌÉÏÔÅËÁÍÉ, ËÏÔÏÒÙÅ ÂÏÌØÛÅ ÎÅ
×ÈÏÄÑÔ × glibc-devel.

%description static -l uk
ãÅ ÏËÒÅÍÉÊ ÐÁËÅÔ Ú¦ ÓÔÁÔÉÞÎÉÍÉ Â¦ÂÌ¦ÏÔÅËÁÍÉ, ÝÏ Â¦ÌØÛÅ ÎÅ ×ÈÏÄÑÔØ ×
ÓËÌÁÄ glibc-devel.

%package profile
Summary:	glibc with profiling support
Summary(de):	glibc mit Profil-Unterstützung
Summary(es):	glibc con soporte de perfilamiento
Summary(fr):	glibc avec support pour profiling
Summary(pl):	glibc ze wsparciem dla profilowania
Summary(ru):	GNU libc Ó ÐÏÄÄÅÒÖËÏÊ ÐÒÏÆÁÊÌÅÒÁ
Summary(tr):	Ölçüm desteði olan glibc
Summary(uk):	GNU libc Ú Ð¦ÄÔÒÉÍËÏÀ ÐÒÏÆÁÊÌÅÒÁ
Group:		Development/Libraries/Libc
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}
Obsoletes:	libc-profile

%description profile
When programs are being profiled using gprof, they must use these
libraries instead of the standard C libraries for gprof to be able to
profile them correctly.

%description profile -l de
Damit Programmprofile mit gprof richtig erstellt werden, müssen diese
Libraries anstelle der üblichen C-Libraries verwendet werden.

%description profile -l es
Cuando programas son perfilidas usando gprof, tienen que usar estas
biblioteces en vez de las estándares para que gprof pueda perfilarlas
correctamente.

%description profile -l pl
Programy profilowane za pomoc± gprof musz± u¿ywaæ tych bibliotek
zamiast standardowych bibliotek C, aby gprof móg³ odpowiednio je
wyprofilowaæ.

%description profile -l uk
ëÏÌÉ ÐÒÏÇÒÁÍÉ ÄÏÓÌ¦ÄÖÕÀÔØÓÑ ÐÒÏÆÁÊÌÅÒÏÍ gprof, ×ÏÎÉ ÐÏ×ÉÎÎ¦
×ÉËÏÒÉÓÔÏ×Õ×ÁÔÉ ÚÁÍ¦ÓÔØ ÓÔÁÎÄÁÒÔÎÉÈ Â¦ÂÌ¦ÏÔÅË Â¦ÂÌ¦ÏÔÅËÉ, ÝÏ Í¦ÓÔÑÔØÓÑ
× ÃØÏÍÕ ÐÁËÅÔ¦. ðÒÉ ×ÉËÏÒÉÓÔÁÎÎ¦ ÓÔÁÎÄÁÒÔÎÉÈ Â¦ÂÌ¦ÏÔÅË gprof ÚÁÍ¦ÓÔØ
ÒÅÁÌØÎÉÈ ÒÅÚÕÌØÔÁÔ¦× ÂÕÄÅ ÐÏËÁÚÕ×ÁÔÉ Ã¦ÎÉ ÎÁ ÐÁÐÁÊÀ × çÏÎÏÌÕÌÕ ×
ÐÏÚÁÍÉÎÕÌÏÍÕ ÒÏÃ¦...

%description profile -l tr
gprof kullanýlarak ölçülen programlar standart C kitaplýðý yerine bu
kitaplýðý kullanmak zorundadýrlar.

%description profile -l ru
ëÏÇÄÁ ÐÒÏÇÒÁÍÍÙ ÉÓÓÌÅÄÕÀÔÓÑ ÐÒÏÆÁÊÌÅÒÏÍ gprof, ÏÎÉ ÄÏÌÖÎÙ
ÉÓÐÏÌØÚÏ×ÁÔØ, ×ÍÅÓÔÏ ÓÔÁÎÄÁÒÔÎÙÈ ÂÉÂÌÉÏÔÅË, ÂÉÂÌÉÏÔÅËÉ, ×ËÌÀÞÅÎÎÙÅ ×
ÜÔÏÔ ÐÁËÅÔ. ðÒÉ ÉÓÐÏÌØÚÏ×ÁÎÉÉ ÓÔÁÎÄÁÒÔÎÙÈ ÂÉÂÌÉÏÔÅË gprof ×ÍÅÓÔÏ
ÒÅÁÌØÎÙÈ ÒÅÚÕÌØÔÁÔÏ× ÂÕÄÅÔ ÐÏËÁÚÙ×ÁÔØ ÃÅÎÙ ÎÁ ÐÁÐÁÊÀ × çÏÎÏÌÕÌÕ ×
ÐÏÚÁÐÒÏÛÌÏÍ ÇÏÄÕ...

%package pic
Summary:	glibc PIC archive
Summary(es):	Archivo PIC de glibc
Summary(pl):	Archiwum PIC glibc
Group:		Development/Libraries/Libc
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description pic
GNU C Library PIC archive contains an archive library (ar file)
composed of individual shared objects. This is used for creating a
library which is a smaller subset of the standard libc shared library.

%description pic -l es
El archivo PIC de la biblioteca glibc contiene una biblioteca
archivada (un fichero ar) compuesta de individuales objetos
compartidos. Es usado para crear una biblioteca que sea un subconjunto
más pequeño de la biblioteca libc compartida estándar.

%description pic -l pl
Archiwum PIC biblioteki GNU C zawiera archiwaln± bibliotekê (plik ar)
z³o¿on± z pojedynczych obiektów wspó³dzielonych. U¿ywana jest do
tworzenia biblioteki bêd±cej mniejszym podzestawem standardowej
biblioteki wspó³dzielonej libc.

%package -n nss_compat
Summary:	Old style NYS NSS glibc module
Summary(es):	El antiguo módulo NYS NSS de glibc
Summary(pl):	Stary modu³ NYS NSS glibc
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n nss_compat
Old style NYS NSS glibc module.

%description -n nss_compat -l es
El antiguo módulo NYS NSS de glibc

%description -n nss_compat -l pl
Stary modu³ NYS NSS glibc.

%package -n nss_dns
Summary:	BIND NSS glibc module
Summary(es):	Módulo BIND NSS de glibc
Summary(pl):	Modu³ BIND NSS glibc
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n nss_dns
BIND NSS glibc module.

%description -n nss_dns -l es
Módulo BIND NSS de glibc.

%description -n nss_dns -l pl
Modu³ BIND NSS glibc.

%package -n nss_files
Summary:	Traditional files databases NSS glibc module
Summary(es):	Módulo de tradicionales bases de datos en ficheros para glibc
Summary(pl):	Modu³ tradycyjnych plikowych baz danych NSS glibc
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n nss_files
Traditional files databases NSS glibc module.

%description -n nss_files -l es
Módulo de tradicionales bases de datos en ficheros para glibc.

%description -n nss_files -l pl
Modu³ tradycyjnych plikowych baz danych NSS glibc.

%package -n nss_hesiod
Summary:	hesiod NSS glibc module
Summary(es):	Módulo hesiod NSS de glibc
Summary(pl):	Modu³ hesiod NSS glibc
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n nss_hesiod
glibc NSS (Name Service Switch) module for databases access.

%description -n nss_hesiod -l es
Módulo hesiod NSS de glibc.

%description -n nss_hesiod -l pl
Modu³ glibc NSS (Name Service Switch) dostêpu do baz danych.

%package -n nss_nis
Summary:	NIS(YP) NSS glibc module
Summary(es):	Módulo NIS(YP) NSS de glibc
Summary(pl):	Modu³ NIS(YP) NSS glibc
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n nss_nis
glibc NSS (Name Service Switch) module for NIS(YP) databases access.

%description -n nss_nis -l es
Módulo NSS de glibc para acceder las bases de datos NIS(YP).

%description -n nss_nis -l pl
Modu³ glibc NSS (Name Service Switch) dostêpu do baz danych NIS(YP).

%package -n nss_nisplus
Summary:	NIS+ NSS module
Summary(es):	Módulo NIS+ NSS
Summary(pl):	Modu³ NIS+ NSS
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n nss_nisplus
glibc NSS (Name Service Switch) module for NIS+ databases access.

%description -n nss_nisplus -l es
Módulo NSS (Name Service Switch) de glibc para acceder las bases de
datos NIS+.

%description -n nss_nisplus -l pl
Modu³ glibc NSS (Name Service Switch) dostêpu do baz danych NIS+.

%package memusage
Summary:	A toy
Summary(es):	Un juguete
Summary(pl):	Zabawka
Group:		Applications
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description memusage
A toy.

%description memusage -l es
Un juguete.

%description memusage -l pl
Zabawka.

%package zoneinfo_right
Summary:	Non-POSIX (real) time zones
Summary(es):	Zonas de tiempo reales (no de POSIX)
Summary(pl):	Nie-POSIX-owe (prawdziwe) strefy czasowe
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description zoneinfo_right
You don't want this. Details at:
http://sources.redhat.com/ml/libc-alpha/2000-12/msg00068.html

%description zoneinfo_right -l es
No lo necesita. Encontrará los detalles en:
http://sources.redhat.com/ml/libc-alpha/2000-12/msg00068.html

%description zoneinfo_right -l pl
Nie potrzebujesz tego. Szczegó³y pod:
http://sources.redhat.com/ml/libc-alpha/2000-12/msg00068.html

%package -n %{name}64
Summary:	GNU libc - 64-bit libraries
Summary(es):	GNU libc - bibliotecas de 64 bits
Summary(pl):	GNU libc - biblioteki 64-bitowe
Group:		Libraries
%ifarch amd64 ppc64 s390x sparc64
Provides:	glibc = %{epoch}:%{version}-%{release}
Requires:	glibc-misc = %{epoch}:%{version}-%{release}
%else
Requires:	%{name} = %{epoch}:%{version}-%{release}
%endif

%description -n %{name}64
64-bit GNU libc libraries for 64bit architecture.

%description -n %{name}64 -l es
Bibliotecas GNU libc de 64 bits para la arquitectura 64bit.

%description -n %{name}64 -l pl
Biblioteki 64-bitowe GNU libc dla architektury 64bit.

%package -n %{name}64-devel
Summary:	Development files for 64-bit GNU libc libraries
Summary(es):	Ficheros de desarrollo para bibliotecas GNU libc de 64 bits
Summary(pl):	Pliki do programowania z u¿yciem 64-bitowych bibliotek GNU libc
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description -n %{name}64-devel
Development files for 64-bit GNU libc libraries for 64bit
architecture.

%description -n %{name}64-devel -l es
Ficheros de desarrollo para las bibliotecas GNU libc de 64 bits para
la arquitectura 64bit.

%description -n %{name}64-devel -l pl
Pliki do programowania z u¿yciem 64-bitowych bibliotek GNU libc dla
architektury 64bit.

%package -n %{name}64-static
Summary:	Static 64-bit GNU libc libraries
Summary(es):	Bibliotecas estáticas GNU libc de 64 bits
Summary(pl):	Statyczne 64-bitowe biblioteki GNU libc
Group:		Development/Libraries
Requires:	%{name}64-devel = %{epoch}:%{version}-%{release}

%description -n %{name}64-static
Static 64-bit GNU libc libraries.

%description -n %{name}64-static -l es
Bibliotecas estáticas GNU libc de 64 bits.

%description -n %{name}64-static -l pl
Statyczne 64-bitowe biblioteki GNU libc.

%prep
%setup -q -a1
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
# don't know, if it is good idea, for brave ones
#%patch11 -p1
%{!?with_kernelheaders:%patch12 -p1}
%patch13 -p1
%patch14 -p0
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%{?with_cross:%patch28 -p1}
#%patch29 -p1
#%patch30 -p1

chmod +x scripts/cpp

# i786 (aka pentium4) hack
cd nptl/sysdeps/i386 && ln -s i686 i786 && cd -
cd nptl/sysdeps/unix/sysv/linux/i386 && ln -s i686 i786 && cd -

%build
# Build glibc
cp -f /usr/share/automake/config.sub scripts
%{__aclocal}
%{__autoconf}
rm -rf builddir
install -d builddir
cd builddir
%ifarch sparc64
CC="%{__cc} -m64 -mcpu=ultrasparc -mvis -fcall-used-g6"
%endif
%if %{with linuxthreads}
../%configure \
	--enable-kernel="%{min_kernel}" \
	--%{?with_omitfp:en}%{!?with_omitfp:dis}able-omitfp \
	--with%{!?with___thread:out}-__thread \
	--with-headers=%{sysheaders} \
	--with%{!?with_selinux:out}-selinux \
	--with%{!?with_tls:out}-tls \
        --enable-add-ons=linuxthreads \
	--enable-profile
%{__make}
%endif
%if %{with nptl}
%if %{with dual}
cd ..
rm -rf builddir-nptl
install -d builddir-nptl
cd builddir-nptl
%endif
../%configure \
	--enable-kernel="%{nptl_min_kernel}" \
	--%{?with_omitfp:en}%{!?with_omitfp:dis}able-omitfp \
	--with-headers=%{sysheaders} \
	--with%{!?with_selinux:out}-selinux \
	--with-tls \
        --enable-add-ons=nptl \
	--enable-profile
# simulate cross-compiling so we can perform dual builds on 2.4.x kernel
%{__make} \
	%{?with_dual:cross-compiling=yes}
%endif
cd ..

%if %{with linuxthreads}
%{__make} -C linuxthreads/man
%endif

%if %{with tests}
for d in builddir %{?with_tests_nptl:builddir-nptl} ; do
cd $d
env LANGUAGE=C LC_ALL=C \
%{__make} tests 2>&1 | awk '
BEGIN { file = "" }
{
	if (($0 ~ /\*\*\* \[.*\.out\] Error/) && ($0 !~ /annexc/) && (file == "")) {
		file=$0;
		gsub(/.*\[/, NIL, file);
		gsub(/\].*/, NIL, file);
	}
	print $0;
}
END { if (file != "") { print "ERROR OUTPUT FROM " file; system("cat " file); exit(1); } }'
cd ..
done
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{logrotate.d,rc.d/init.d,sysconfig},%{_mandir}/man{3,8},/var/log,/var/{lib,run}/nscd}

cd builddir
env LANGUAGE=C LC_ALL=C \
%{__make} install \
	install_root=$RPM_BUILD_ROOT \
	infodir=%{_infodir} \
	mandir=%{_mandir}

%if %{with localedb}
env LANGUAGE=C LC_ALL=C \
%{__make} localedata/install-locales \
	install_root=$RPM_BUILD_ROOT
%endif

PICFILES="libc_pic.a libc.map
	math/libm_pic.a libm.map
	resolv/libresolv_pic.a"

install $PICFILES				$RPM_BUILD_ROOT%{_libdir}
install elf/soinit.os				$RPM_BUILD_ROOT%{_libdir}/soinit.o
install elf/sofini.os				$RPM_BUILD_ROOT%{_libdir}/sofini.o

install elf/postshell				$RPM_BUILD_ROOT/sbin
cd ..

%if %{with dual}
env LANGUAGE=C LC_ALL=C \
%{__make} -C builddir-nptl install \
	cross-compiling=yes \
	install_root=$RPM_BUILD_ROOT/nptl

install -d $RPM_BUILD_ROOT{/%{_lib}/tls,%{_libdir}/nptl,%{_includedir}/nptl}
for f in libc libm libpthread libthread_db librt; do
	mv -f $RPM_BUILD_ROOT/nptl/%{_lib}/${f}[-.]* $RPM_BUILD_ROOT/%{_lib}/tls
done
$RPM_BUILD_ROOT/sbin/ldconfig -n $RPM_BUILD_ROOT/%{_lib}/tls

for f in libc.so libpthread.so ; do
	cat $RPM_BUILD_ROOT/nptl%{_libdir}/$f | sed \
		-e "s|/libc.so.6|/tls/libc.so.6|g" \
		-e "s|/libpthread.so.0|/tls/libpthread.so.0|g" \
		-e "s|/libpthread_nonshared.a|/nptl/libpthread_nonshared.a|g" \
		> $RPM_BUILD_ROOT%{_libdir}/nptl/$f
done
for f in libc.a libpthread.a libpthread_nonshared.a; do
	mv -f $RPM_BUILD_ROOT/nptl%{_libdir}/$f $RPM_BUILD_ROOT%{_libdir}/nptl
done
cd $RPM_BUILD_ROOT/nptl%{_prefix}/include
	for f in `find . -type f`; do
		if ! [ -f $RPM_BUILD_ROOT%{_prefix}/include/$f ] \
		   || ! cmp -s $f $RPM_BUILD_ROOT%{_prefix}/include/$f ; then
			install -d $RPM_BUILD_ROOT%{_prefix}/include/nptl/`dirname $f`
			cp -a $f $RPM_BUILD_ROOT%{_prefix}/include/nptl/$f
		fi
	done
cd -
rm -rf $RPM_BUILD_ROOT/nptl
%endif

%{?with_memusage:mv -f $RPM_BUILD_ROOT/%{_lib}/libmemusage.so	$RPM_BUILD_ROOT%{_libdir}}
mv -f $RPM_BUILD_ROOT/%{_lib}/libpcprofile.so	$RPM_BUILD_ROOT%{_libdir}

%if %{with linuxthreads}
install linuxthreads/man/*.3thr		$RPM_BUILD_ROOT%{_mandir}/man3
%endif

rm -rf $RPM_BUILD_ROOT%{_datadir}/zoneinfo/{localtime,posixtime,posixrules,posix/*}

#cd $RPM_BUILD_ROOT%{_datadir}/zoneinfo
#for i in [A-Z]*; do
#	ln -s ../$i posix
#done
#cd -

ln -sf %{_sysconfdir}/localtime	$RPM_BUILD_ROOT%{_datadir}/zoneinfo/localtime
ln -sf localtime		$RPM_BUILD_ROOT%{_datadir}/zoneinfo/posixtime
ln -sf localtime		$RPM_BUILD_ROOT%{_datadir}/zoneinfo/posixrules
ln -sf libbsd-compat.a		$RPM_BUILD_ROOT%{_libdir}/libbsd.a

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/localtime

# make symlinks across top-level directories absolute
for l in anl BrokenLocale crypt dl m nsl resolv rt thread_db util ; do
	rm -f $RPM_BUILD_ROOT%{_libdir}/lib${l}.so
	ln -sf /%{_lib}/`cd $RPM_BUILD_ROOT/%{_lib} ; echo lib${l}.so.*` $RPM_BUILD_ROOT%{_libdir}/lib${l}.so
done

install %{SOURCE2}		$RPM_BUILD_ROOT/etc/rc.d/init.d/nscd
install %{SOURCE3}		$RPM_BUILD_ROOT/etc/sysconfig/nscd
install %{SOURCE4}		$RPM_BUILD_ROOT/etc/logrotate.d/nscd
install nscd/nscd.conf	$RPM_BUILD_ROOT%{_sysconfdir}
install nss/nsswitch.conf	$RPM_BUILD_ROOT%{_sysconfdir}

bzip2 -dc %{SOURCE5} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}
bzip2 -dc %{SOURCE6} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}
> $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.cache
> $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf
rm -f $RPM_BUILD_ROOT%{_mandir}/hu/man7/man.7

:> $RPM_BUILD_ROOT/var/log/nscd
:> $RPM_BUILD_ROOT/var/lib/nscd/passwd
:> $RPM_BUILD_ROOT/var/lib/nscd/group
:> $RPM_BUILD_ROOT/var/lib/nscd/hosts

rm -rf documentation
install -d documentation

%if %{with linuxthreads}
for f in ChangeLog Changes README ; do
	cp -f linuxthreads/$f documentation/${f}.linuxthreads
done
%endif
%if %{with nptl}
for f in ANNOUNCE ChangeLog DESIGN-{barrier,condvar,rwlock,sem}.txt TODO{,-kernel,-testing} ;  do
	cp -f nptl/$f documentation/${f}.nptl
done
%endif
cp -f crypt/README.ufc-crypt documentation

cp -f ChangeLog* documentation

rm -f $RPM_BUILD_ROOT%{_libdir}/libnss_*.so

# strip ld.so with --strip-debug only (other ELFs are stripped by rpm):
%{!?debug:strip -g -R .comment -R .note $RPM_BUILD_ROOT/%{_lib}/ld-*.so}

# Collect locale files and mark them with %%lang()
rm -f glibc.lang
echo '%defattr(644,root,root,755)' > glibc.lang
for i in $RPM_BUILD_ROOT%{_datadir}/locale/* $RPM_BUILD_ROOT%{_libdir}/locale/* ; do
	if [ -d $i ]; then
		lang=`echo $i | sed -e 's/.*locale\///' -e 's/\/.*//'`
		twochar=1
		# list of long %%lang values we do support
		for j in de_AT de_BE de_CH de_LU es_AR es_MX pt_BR \
			 zh_CN zh_CN.gbk zh_HK zh_TW ; do
			if [ $j = "$lang" ]; then
				twochar=
			fi
		done
		if [ -n "$twochar" ]; then
			if [ `echo $lang | sed "s,_.*,,"` = "zh" ]; then
				lang=`echo $lang | sed "s,\..*,,"`
			else
				lang=`echo $lang | sed "s,_.*,,"`
			fi
		fi
		dir=`echo $i | sed "s#$RPM_BUILD_ROOT##"`
		echo "%lang($lang) $dir" >> glibc.lang
	fi
done
# XXX: to be added when become supported by glibc
# tk, yo (used by GNOME)
# ven -> ve (used by KDE)
# NOTES:
# bn is used for bn_BD or bn_IN?
# omitted here - already existing (with libc.mo):
#   be,ca,cs,da,de,el,en_GB,es,fi,fr,gl,hr,hu,it,ja,ko,nb,nl,pl,pt_BR,sk,sv,tr,zh_CN,zh_TW
for i in af am ang ar az bg bn br bs cy de_AT en en@boldquot en@quot en_AU \
    en_CA en_US eo es_AR es_MX et eu fa fo ga gu he hi hsb ia id is ka kn \
    leet lg li lo lt lv mi mk ml mn mr ms mt nds ne nn nso or pa pt ro ru se \
    sl sq sr sr@Latn sr@ije ss ta tg th tlh uk uz ve vi wa xh yi zu ; do
	if [ ! -d $RPM_BUILD_ROOT%{_datadir}/locale/$i/LC_MESSAGES ]; then
		install -d $RPM_BUILD_ROOT%{_datadir}/locale/$i/LC_MESSAGES
		lang=`echo $i | sed -e 's/_.*//'`
		echo "%lang($lang) %{_datadir}/locale/$i" >> glibc.lang
	fi
done
cd $RPM_BUILD_ROOT%{_datadir}/locale
ln -s zh_CN zh_SG
ln -s zh_CN zh_HK
cd -

# localedb-gen infrastructure
install %{SOURCE7} $RPM_BUILD_ROOT%{_bindir}/localedb-gen
install localedata/SUPPORTED $RPM_BUILD_ROOT%{_datadir}/i18n

# shutup check-files
rm -f $RPM_BUILD_ROOT%{_mandir}/README.*
rm -f $RPM_BUILD_ROOT%{_mandir}/diff.*
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
# we don't support kernel without ptys support
rm -f $RPM_BUILD_ROOT%{_libdir}/pt_chown

%clean
rm -rf $RPM_BUILD_ROOT

# don't run iconvconfig in %%postun -n iconv because iconvconfig doesn't exist
# when %%postun is run

%ifarch amd64 ppc64 s390x sparc64
%post	-n %{name}64 -p /sbin/postshell
%else
%post	-p /sbin/postshell
%endif
/sbin/ldconfig
-/sbin/telinit u

%ifarch amd64 ppc64 s390x sparc64
%postun	-n %{name}64 -p /sbin/postshell
%else
%postun	-p /sbin/postshell
%endif
/sbin/ldconfig
-/sbin/telinit u

%ifarch amd64 ppc64 s390x sparc64
%triggerpostun -n %{name}64 -p /sbin/postshell -- glibc-misc < 6:2.3.4-0.20040505.1
%else
%triggerpostun -p /sbin/postshell -- glibc-misc < 6:2.3.4-0.20040505.1
%endif
-/bin/mv %{_sysconfdir}/ld.so.conf.rpmsave %{_sysconfdir}/ld.so.conf

%post	memusage -p /sbin/ldconfig
%postun memusage -p /sbin/ldconfig

%post -n iconv -p %{_sbindir}/iconvconfig

%post devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%pre -n nscd
if [ -n "`/usr/bin/getgid nscd`" ]; then
	if [ "`/usr/bin/getgid nscd`" != "144" ]; then
		echo "Error: group nscd doesn't have gid=144. Correct this before installing nscd." 1>&2
		exit 1
	fi
else
	/usr/sbin/groupadd -g 144 -r nscd
fi
if [ -n "`/bin/id -u nscd 2>/dev/null`" ]; then
	if [ "`/bin/id -u nscd`" != "144" ]; then
		echo "Error: user nscd doesn't have uid=144. Correct this before installing nscd." 1>&2
		exit 1
	fi
else
	/usr/sbin/useradd -u 144 -r -d /tmp -s /bin/false -c "nscd" -g nscd nscd 1>&2
fi

%post -n nscd
/sbin/chkconfig --add nscd
touch /var/log/nscd
chmod 000 /var/log/nscd
chown root:root /var/log/nscd
chmod 640 /var/log/nscd
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

%postun -n nscd
if [ "$1" = "0" ]; then
	%userremove nscd
	%groupremove nscd
fi

%ifarch amd64 ppc64 s390x sparc64
%files -n glibc64
%defattr(644,root,root,755)
%else
%files
%defattr(644,root,root,755)
%endif
%defattr(644,root,root,755)
%doc README NEWS FAQ BUGS
%attr(755,root,root) /sbin/postshell
%attr(755,root,root) /sbin/ldconfig
# ld* and libc.so.6 SONAME symlinks must be in package because of
# chicken-egg problem (postshell is dynamically linked with libc);
# ld-*.so SONAME is:
#   ld.so.1 on ppc
#   ld64.so.1 on ppc64,s390x
#   ld-linux-ia64.so.2 on ia64
#   ld-linux-x86-64.so.2 on amd64
#   ld-linux.so.2 on other archs
%attr(755,root,root) /%{_lib}/ld*
%attr(755,root,root) /%{_lib}/libanl*
%attr(755,root,root) /%{_lib}/libdl*
%attr(755,root,root) /%{_lib}/libnsl*
%attr(755,root,root) /%{_lib}/lib[BScmprtu]*
%if %{with dual}
%dir /%{_lib}/tls
%attr(755,root,root) /%{_lib}/tls/lib[cmprt]*
%endif
%{?with_localedb:%dir %{_libdir}/locale}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ld.so.conf
%ghost %{_sysconfdir}/ld.so.cache

#%files -n nss_dns
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libnss_dns*.so*

#%files -n nss_files
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libnss_files*.so*

%files misc -f %{name}.lang
%defattr(644,root,root,755)

%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nsswitch.conf
%config %{_sysconfdir}/rpc

%attr(755,root,root) /sbin/sln
%attr(755,root,root) %{_bindir}/catchsegv
%attr(755,root,root) %{_bindir}/getconf
%attr(755,root,root) %{_bindir}/getent
%attr(755,root,root) %{_bindir}/iconv
%attr(755,root,root) %{_bindir}/ldd
%ifarch %{ix86} m68k sparc sparcv9
%attr(755,root,root) %{_bindir}/lddlibc4
%endif
%attr(755,root,root) %{_bindir}/locale
%attr(755,root,root) %{_bindir}/rpcgen
%attr(755,root,root) %{_bindir}/tzselect

%attr(755,root,root) %{_sbindir}/rpcinfo
%attr(755,root,root) %{_sbindir}/zdump
%attr(755,root,root) %{_sbindir}/zic

%dir %{_libexecdir}/getconf
%attr(755,root,root) %{_libexecdir}/getconf/*

%dir %{_datadir}/locale
%{_datadir}/locale/locale.alias
%{_datadir}/zoneinfo
%exclude %{_datadir}/zoneinfo/right

%{_mandir}/man1/catchsegv.1*
%{_mandir}/man1/getconf.1*
%{_mandir}/man1/getent.1*
%{_mandir}/man1/iconv.1*
%{_mandir}/man1/ldd.1*
%{_mandir}/man1/locale.1*
%{_mandir}/man1/rpcgen.1*
%{_mandir}/man5/locale.5*
%{_mandir}/man5/nsswitch.conf.5*
%{_mandir}/man5/tzfile.5*
%{_mandir}/man7/*
%{_mandir}/man8/ld*.8*
%{_mandir}/man8/rpcinfo.8*
%{_mandir}/man8/sln.8*
%{_mandir}/man8/tzselect.8*
%{_mandir}/man8/zdump.8*
%{_mandir}/man8/zic.8*
%lang(cs) %{_mandir}/cs/man7/*
%lang(de) %{_mandir}/de/man5/tzfile.5*
%lang(de) %{_mandir}/de/man7/*
%lang(es) %{_mandir}/es/man5/locale.5*
%lang(es) %{_mandir}/es/man5/nsswitch.conf.5*
%lang(es) %{_mandir}/es/man5/tzfile.5*
%lang(es) %{_mandir}/es/man7/*
%lang(es) %{_mandir}/es/man8/ld*.8*
%lang(es) %{_mandir}/es/man8/tzselect.8*
%lang(es) %{_mandir}/es/man8/zdump.8*
%lang(es) %{_mandir}/es/man8/zic.8*
%lang(fi) %{_mandir}/fi/man1/ldd.1*
%lang(fr) %{_mandir}/fr/man1/ldd.1*
%lang(fr) %{_mandir}/fr/man5/locale.5*
%lang(fr) %{_mandir}/fr/man5/nsswitch.conf.5*
%lang(fr) %{_mandir}/fr/man5/tzfile.5*
%lang(fr) %{_mandir}/fr/man7/*
%lang(fr) %{_mandir}/fr/man8/ld*.8*
%lang(fr) %{_mandir}/fr/man8/tzselect.8*
%lang(fr) %{_mandir}/fr/man8/zdump.8*
%lang(fr) %{_mandir}/fr/man8/zic.8*
%lang(hu) %{_mandir}/hu/man1/ldd.1*
%lang(hu) %{_mandir}/hu/man7/*
%lang(hu) %{_mandir}/hu/man8/ld*.8*
%lang(hu) %{_mandir}/hu/man8/zdump.8*
%lang(it) %{_mandir}/it/man5/locale.5*
%lang(it) %{_mandir}/it/man7/*
%lang(it) %{_mandir}/it/man8/tzselect.8*
%lang(it) %{_mandir}/it/man8/zdump.8*
%lang(ja) %{_mandir}/ja/man1/ldd.1*
%lang(ja) %{_mandir}/ja/man1/rpcgen.1*
%lang(ja) %{_mandir}/ja/man5/locale.5*
%lang(ja) %{_mandir}/ja/man5/nsswitch.conf.5*
%lang(ja) %{_mandir}/ja/man5/tzfile.5*
%lang(ja) %{_mandir}/ja/man7/*
%lang(ja) %{_mandir}/ja/man8/ld*.8*
%lang(ja) %{_mandir}/ja/man8/rpcinfo.8*
%lang(ja) %{_mandir}/ja/man8/sln.8*
%lang(ja) %{_mandir}/ja/man8/tzselect.8*
%lang(ja) %{_mandir}/ja/man8/zdump.8*
%lang(ja) %{_mandir}/ja/man8/zic.8*
%lang(ko) %{_mandir}/ko/man5/nsswitch.conf.5*
%lang(ko) %{_mandir}/ko/man5/tzfile.5*
%lang(ko) %{_mandir}/ko/man7/*
%lang(ko) %{_mandir}/ko/man8/tzselect.8*
%lang(ko) %{_mandir}/ko/man8/zdump.8*
%lang(pl) %{_mandir}/pl/man1/ldd.1*
%lang(pl) %{_mandir}/pl/man5/locale.5*
%lang(pl) %{_mandir}/pl/man7/*
%lang(pl) %{_mandir}/pl/man8/ld*.8*
%lang(pt) %{_mandir}/pt/man5/locale.5*
%lang(pt) %{_mandir}/pt/man5/nsswitch.conf.5*
%lang(pt) %{_mandir}/pt/man5/tzfile.5*
%lang(pt) %{_mandir}/pt/man7/*
%lang(pt) %{_mandir}/pt/man8/ld*.8*
%lang(pt) %{_mandir}/pt/man8/tzselect.8*
%lang(pt) %{_mandir}/pt/man8/zdump.8*
%lang(pt) %{_mandir}/pt/man8/zic.8*
%lang(ru) %{_mandir}/ru/man5/nsswitch.conf.5*
%lang(ru) %{_mandir}/ru/man5/tzfile.5*
%lang(ru) %{_mandir}/ru/man7/*
%lang(ru) %{_mandir}/ru/man8/tzselect.8*
%lang(ru) %{_mandir}/ru/man8/zdump.8*
%lang(ru) %{_mandir}/ru/man8/zic.8*
%lang(zh_CN) %{_mandir}/zh_CN/man1/iconv.1*
%lang(zh_CN) %{_mandir}/zh_CN/man1/ldd.1*
%lang(zh_CN) %{_mandir}/zh_CN/man5/locale.5*
%lang(zh_CN) %{_mandir}/zh_CN/man5/tzfile.5*
%lang(zh_CN) %{_mandir}/zh_CN/man7/*
%lang(zh_CN) %{_mandir}/zh_CN/man8/tzselect.8*
%lang(zh_CN) %{_mandir}/zh_CN/man8/zdump.8*
%lang(zh_CN) %{_mandir}/zh_CN/man8/zic.8*

%files zoneinfo_right
%defattr(644,root,root,755)
%{_datadir}/zoneinfo/right

%files -n nss_compat
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libnss_compat*.so*

%files -n nss_hesiod
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libnss_hesiod*.so*

%files -n nss_nis
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libnss_nis.so.*
%attr(755,root,root) /%{_lib}/libnss_nis-*.so

%files -n nss_nisplus
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libnss_nisplus*.so*

%if %{with memusage}
%files memusage
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/memusage*
%attr(755,root,root) %{_libdir}/libmemusage.so
%endif

%files devel
%defattr(644,root,root,755)
%doc documentation/* NOTES PROJECTS
%attr(755,root,root) %{_bindir}/gencat
%attr(755,root,root) %{_bindir}/*prof*
%attr(755,root,root) %{_bindir}/*trace

%attr(755,root,root) %{_libdir}/lib[!cmp]*.so
%attr(755,root,root) %{_libdir}/libcrypt.so
%attr(755,root,root) %{_libdir}/libm.so
%attr(755,root,root) %{_libdir}/libpcprofile.so
%attr(755,root,root) %{_libdir}/*crt*.o
# ld scripts
%{_libdir}/libc.so
%{_libdir}/libpthread.so

%{_libdir}/libbsd-compat.a
%{_libdir}/libbsd.a
%{_libdir}/libc_nonshared.a
%{_libdir}/libg.a
%{_libdir}/libieee.a
%{_libdir}/libpthread_nonshared.a
%{_libdir}/librpcsvc.a

%if %{with dual}
%dir %{_libdir}/nptl
# ld scripts
%{_libdir}/nptl/libc.so
%{_libdir}/nptl/libpthread.so
%{_libdir}/nptl/libpthread_nonshared.a
%{_includedir}/nptl
%endif

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

%{_infodir}/libc.info*

%{_mandir}/man1/sprof.1*
%{_mandir}/man3/*
%lang(cs) %{_mandir}/cs/man3/*
%lang(de) %{_mandir}/de/man3/*
%lang(es) %{_mandir}/es/man3/*
%lang(fr) %{_mandir}/fr/man3/*
%lang(hu) %{_mandir}/hu/man3/*
%lang(it) %{_mandir}/it/man3/*
%lang(ja) %{_mandir}/ja/man3/*
%lang(ko) %{_mandir}/ko/man3/*
%lang(nl) %{_mandir}/nl/man3/*
%lang(pl) %{_mandir}/pl/man3/*
%lang(pt) %{_mandir}/pt/man3/*
%lang(ru) %{_mandir}/ru/man3/*
%lang(uk) %{_mandir}/uk/man3/*
%lang(zh_CN) %{_mandir}/zh_CN/man3/*

%files -n nscd
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/nscd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nscd.*
%attr(754,root,root) /etc/rc.d/init.d/nscd
%attr(755,root,root) %{_sbindir}/nscd*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/nscd
%attr(640,root,root) %ghost /var/log/nscd
%dir /var/run/nscd
%dir /var/lib/nscd
%attr(600,root,root) %ghost /var/lib/nscd/passwd
%attr(600,root,root) %ghost /var/lib/nscd/group
%attr(600,root,root) %ghost /var/lib/nscd/hosts
%{_mandir}/man5/nscd.conf.5*
%{_mandir}/man8/nscd.8*
%{_mandir}/man8/nscd_nischeck.8*
%lang(fr) %{_mandir}/fr/man5/nscd.conf.5*
%lang(fr) %{_mandir}/fr/man8/nscd.8*
%lang(ja) %{_mandir}/ja/man5/nscd.conf.5*
%lang(ja) %{_mandir}/ja/man8/nscd.8*
%lang(pt) %{_mandir}/pt/man5/nscd.conf.5*
%lang(pt) %{_mandir}/pt/man8/nscd.8*

%files -n localedb-src
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/localedef
%attr(755,root,root) %{_bindir}/localedb-gen
%{_datadir}/i18n
%{_mandir}/man1/localedef.1*

%if %{with localedb}
%files localedb-all
%defattr(644,root,root,755)
%{_libdir}/locale/locale-archive
%endif

%files -n iconv
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/iconvconfig
%dir %{_libdir}/gconv
%{_libdir}/gconv/gconv-modules
%attr(755,root,root) %{_libdir}/gconv/*.so

%files static
%defattr(644,root,root,755)
%{_libdir}/libanl.a
%{_libdir}/libBrokenLocale.a
%{_libdir}/libc.a
%{_libdir}/libcrypt.a
%{_libdir}/libdl.a
%{_libdir}/libm.a
%{_libdir}/libmcheck.a
%{_libdir}/libnsl.a
%{_libdir}/libpthread.a
%{_libdir}/libresolv.a
%{_libdir}/librt.a
%{_libdir}/libutil.a
%if %{with dual}
%{_libdir}/nptl/libc.a
%{_libdir}/nptl/libpthread.a
%endif

%files profile
%defattr(644,root,root,755)
#{?with_dual:%{_libdir}/nptl/lib*_p.a}
%{_libdir}/lib*_p.a

%files pic
%defattr(644,root,root,755)
%{_libdir}/lib*_pic.a
%{_libdir}/lib*.map
%{_libdir}/soinit.o
%{_libdir}/sofini.o
