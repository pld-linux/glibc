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
%bcond_with	pax		# apply PaX patches
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
%ifnarch %{ix86} %{x8664} ia64 alpha s390 s390x
# sparc64 sparcv9 ppc ppc64  -- disabled in AC (gcc < 3.4)
%undefine	with_tls
%endif
%endif

%if %{with nptl}
# on x86 uses cmpxchgl (available since i486)
# on sparc only sparcv9 is supported
%ifnarch i486 i586 i686 pentium3 pentium4 athlon %{x8664} ia64 alpha s390 s390x
# sparc64 sparcv9 ppc ppc64  -- disabled in AC (gcc < 3.4)
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
Summary(ja):	GNU libc ╔И╔╓╔ж╔И╔Й
Summary(pl):	GNU libc
Summary(ru):	GNU libc версии 2.3
Summary(tr):	GNU libc
Summary(uk):	GNU libc верс╕╖ 2.3
Name:		glibc
Version:	2.3.5
Release:	5
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
Source8:	%{name}-LD-path.c
Source9:	postshell.c
Patch0:		%{name}-info.patch
Patch1:		%{name}-pl.po-update.patch
Patch2:		%{name}-pld.patch
Patch3:		%{name}-crypt-blowfish.patch
Patch4:		%{name}-linuxthreads-lock.patch
Patch5:		%{name}-pthread_create-manpage.patch
Patch6:		%{name}-paths.patch
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
Patch28:	%{name}-sys-kd.patch
Patch29:	%{name}-cross-gcc_eh.patch
Patch30:	%{name}-pax_dl-execstack.patch
URL:		http://www.gnu.org/software/libc/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	binutils >= 2:2.15.90.0.3
BuildRequires:	gcc >= 5:3.2
BuildRequires:	gcc < 5:4.0
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
BuildRequires:	rpmbuild(macros) >= 1.213
BuildRequires:	sed >= 4.0.5
BuildRequires:	texinfo
BuildRequires:	dietlibc-static
AutoReq:	false
PreReq:		basesystem
Requires:	glibc-misc = %{epoch}:%{version}-%{release}
%{?with_tls:Provides:	glibc(tls)}
Provides:	ldconfig
Provides:	/sbin/ldconfig
Obsoletes:	glibc-common
Obsoletes:	glibc-debug
Obsoletes:	ldconfig
Conflicts:	kernel < %{min_kernel}
Conflicts:	ld.so < 1.9.9-10
Conflicts:	man-pages < 1.43
Conflicts:	poldek < 0.18.8-5
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
Contiene las bibliotecas estАndared que son usadas por varios
programas del sistema. Para ahorrar el espacio en el disco y la
memoria, igual que para facilitar actualizaciones, cСdigo comЗn del
sistema se guarda en un sitio y es compartido entre los programas.
Este paquete contiene las bibliotecas compartidas mАs importantes, es
decir la biblioteca C estАndar y la biblioteca estАndar de matemАtica.
Sin Иstas, un sistema Linux no podrА funcionar. TambiИn estА incluido
soporte de idiomas nacionales (locale) y bases de datos de zona de
tiempo.

Puede usarse con: nЗcleo Linux >= %{min_kernel}.

%description -l de
EnthДlt die Standard-Libraries, die von verschiedenen Programmen im
System benutzt werden. Um Festplatten- und Arbeitsspeicher zu sparen
und zur Vereinfachung von Upgrades ist der gemeinsame Systemcode an
einer einzigen Stelle gespeichert und wird von den Programmen
gemeinsam genutzt. Dieses Paket enthДlt die wichtigsten Sets der
shared Libraries, die Standard-C-Library und die
Standard-Math-Library, ohne die das Linux-System nicht funktioniert.
Ferner enthДlt es den Support fЭr die verschiedenen Sprachgregionen
(locale) und die Zeitzonen-Datenbank.

Can be used on: Linux kernel >= %{min_kernel}.

%description -l fr
Contient les bibliothХques standards utilisИes par de nombreux
programmes du systХme. Afin d'Иconomiser l'espace disque et mИmoire,
et de faciliter les mises Ю jour, le code commun au systХme est mis Ю
un endroit et partagИ entre les programmes. Ce paquetage contient les
bibliothХques partagИes les plus importantes, la bibliothХque standard
du C et la bibliothХque mathИmatique standard. Sans celles-ci, un
systХme Linux ne peut fonctionner. Il contient aussi la gestion des
langues nationales (locales) et les bases de donnИes des zones
horaires.

Can be used on: Linux kernel >= %{min_kernel}.

%description -l ja
glibc
╔я╔ц╔╠║╪╔╦╓о╔╥╔╧╔ф╔Ю╬Е╓нйё©Т╓н╔в╔М╔╟╔И╔Ю╓г╩х╓О╓Л╓Ки╦╫Ю╔И╔╓╔ж╔И╔Й╓Р
╓у╓╞╓ъ╓ч╓╧║ё╔г╔ё╔╧╔╞╔╧╔з║╪╔╧╓х╔А╔Б╔Й╓РюАлС╓╥╓©╓Й║╒╔╒╔ц╔в╔╟╔Л║╪╔и╓Р
мя╟у╓к╓╧╓К╓©╓А╓к║╒╤╕дл╓н╔╥╔╧╔ф╔Ю╔Ё║╪╔и╓о╟Л╓д╓н╬Л╫Й╓к╓╙╓╚╓Л║╒╔в╔М╔╟╔И╔Ю
╢ж╓г╤╕м╜╓╣╓Л╓ч╓╧║ё╓Ё╓ниТй╛е╙╓й╔я╔ц╔╠║╪╔╦╓о╔╥╔╖╔╒╔и╔И╔╓╔ж╔И╔Й╓н╓╚╓й╓Й
╫емв╓й╔╩╔ц╔х╓Р╓у╓╞╓ъ╓ч╓╧: и╦╫Ю C ╔И╔╓╔ж╔И╔Й╓хи╦╫Ю©Тцм╔И╔╓╔ж╔И╔Й╓г╓╧║ё
╓Ё╓нфС╓д╓н╔И╔╓╔ж╔И╔Йх╢╓╜╓г╓о║╒Linux ╔╥╔╧╔ф╔Ю╓о╣║г╫╓╥╓ч╓╩╓С║ё glibc
╔я╔ц╔╠║╪╔╦╓о╓ч╓©цо╟Х╦ю╦Л (locale) ╔╣╔щ║╪╔х╓х╔©╔╓╔Ю╔╬║╪╔С╔г║╪╔©╔ы║╪╔╧
╔╣╔щ║╪╔х╓Р╓у╓╞╓ъ╓ч╓╧║ё

Can be used on: Linux kernel >= %{min_kernel}.

%description -l pl
W pakiecie znajduj╠ siЙ podstawowe biblioteki, u©ywane przez rС©ne
programy w Twoim systemie. U©ywanie przez programy bibliotek z tego
pakietu oszczЙdza miejsce na dysku i pamiЙФ. WiЙkszo╤Ф kodu
systemowego jest usytuowane w jednym miejscu i dzielone miЙdzy wieloma
programami. Pakiet ten zawiera bardzo wa©ny zbiСr bibliotek
standardowych, wspСЁdzielonych (dynamicznych) bibliotek C i
matematycznych. Bez glibc system Linux nie jest w stanie funkcjonowaФ.
Znajduj╠ siЙ tutaj rСwnie© definicje rС©nych informacji dla wielu
jЙzykСw (locale) oraz definicje stref czasowych.

Przeznaczony dla j╠dra Linux >= %{min_kernel}.

%description -l ru
Содержит стандартные библиотеки, используемые многочисленными
программами в системе. Для того, чтобы сохранить дисковое пространство
и память, а также для простоты обновления, системный код, общий для
всех программ, хранится в одном месте и коллективно используется всеми
программами. Этот пакет содержит наиболее важные из разделяемых
библиотек - стандартную библиотеку C и стандартную библиотеку
математики. Без этих библиотек Linux функционировать не будет. Также
пакет содержит поддержку национальных языков (locale) и базы данных
временных зон (timezone databases).

Can be used on: Linux kernel >= %{min_kernel}.

%description -l tr
Bu paket, birГok programЩn kullandЩПЩ standart kitaplЩklarЩ iГerir.
Disk alanЩ ve bellek kullanЩmЩnЩ azaltmak ve aynЩ zamanda gЭncelleme
iЧlemlerini kolaylaЧtЩrmak iГin ortak sistem kodlarЩ tek bir yerde
tutulup programlar arasЩnda paylaЧtЩrЩlЩr. Bu paket en Жnemli ortak
kitaplЩklarЩ, standart C kitaplЩПЩnЩ ve standart matematik kitaplЩПЩnЩ
iГerir. Bu kitaplЩklar olmadan Linux sistemi ГalЩЧmayacaktЩr. Yerel
dil desteПi ve zaman dilimi veri tabanЩ da bu pakette yer alЩr.

Can be used on: Linux kernel >= %{min_kernel}.

%description -l uk
М╕стить стандартн╕ б╕бл╕отеки, котр╕ використовуються численними
програмами в систем╕. Для того, щоб зберегти дисковий прост╕р та
пам'ять, а також для простоти поновлення системи, системний код,
сп╕льний для вс╕х програм, збер╕га╓ться в одному м╕сц╕ ╕ колективно
використову╓ться вс╕ма програмами. Цей пакет м╕стить найб╕льш важлив╕
з динам╕чних б╕бл╕отек - стандартну б╕бл╕отеку С та стандартну
б╕бл╕отеку математики. Без цих б╕бл╕отек Linux функц╕онувати не буде.
Також пакет м╕стить п╕дтримку нац╕ональних мов (locale) та бази данних
часових зон (timezone databases).

Can be used on: Linux kernel >= %{min_kernel}.

%package misc
Summary:	Utilities and data used by glibc
Summary(pl):	NarzЙdzia i dane u©ywane przez glibc
Group:		Development/Libraries
AutoReq:	false
PreReq:		%{name} = %{epoch}:%{version}-%{release}

%description misc
Utilities and data used by glibc.

%description misc -l pl
NarzЙdzia i dane u©ywane przez glibc.

%package devel
Summary:	Additional libraries required to compile
Summary(de):	Weitere Libraries zum Kompilieren
Summary(es):	Bibliotecas adicionales necesarias para la compilaciСn
Summary(fr):	Librairies supplИmentaires nИcessaires Ю la compilation
Summary(ja):	и╦╫Ю C ╔И╔╓╔ж╔И╔Й╓г╩х╓О╓Л╓К╔ь╔ц╔ю║╪╓х╔╙╔ж╔╦╔╖╔╞╔х╔у╔║╔╓╔К
Summary(pl):	Dodatkowe biblioteki wymagane podczas kompilacji
Summary(ru):	Дополнительные библиотеки, необходимые для компиляции
Summary(tr):	GeliЧtirme iГin gerekli diПer kitaplЩklar
Summary(uk):	Додатков╕ б╕бл╕отеки, потр╕бн╕ для комп╕ляц╕╖
Group:		Development/Libraries
Provides:	%{name}-devel(%{_target_cpu}) = %{epoch}:%{version}-%{release}
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	%{name}-headers = %{epoch}:%{version}-%{release}
Requires:	%{name}-devel-utils = %{epoch}:%{version}-%{release}
Requires:	%{name}-devel-doc = %{epoch}:%{version}-%{release}
Obsoletes:	libiconv-devel

%description devel
To develop programs which use the standard C libraries (which nearly
all programs do), the system needs to have these standard header files
and object files available for creating the executables.

%description devel -l de
Bei der Entwicklung von Programmen, die die Standard-C-Libraries
verwenden (also fast alle), benЖtigt das System diese Standard-Header-
und Objektdateien zum Erstellen der ausfЭhrbaren Programme.

%description devel -l es
Para desarrollar programas que utilizan las bibliotecas C estАndar (lo
cual hacen prАcticamente todos los programas), el sistema necesita
disponer de estos ficheros de cabecera y de objetos para crear los
ejecutables.

%description devel -l fr
Pour dИvelopper des programmes utilisant les bibliothХques standard du
C (ce que presque tous les programmes font), le systХme doit possИder
ces fichiers en-tЙtes et objets standards pour crИer les exИcutables.

%description devel -l ja
glibc-devel ╔я╔ц╔╠║╪╔╦╓о(╓ш╓х╓С╓и╓╧╓ы╓ф╓н╔в╔М╔╟╔И╔Ю╓г╩х╓О╓Л╓К)и╦╫Ю C
╔И╔╓╔ж╔И╔Й╓Р╩хмя╓╥╓©╔в╔М╔╟╔И╔Ю╓РЁ╚х╞╓╧╓К╓©╓А╓н╔ь╔ц╔ю║╪╓х╔╙╔ж╔╦╔╖╔╞╔х
╔у╔║╔╓╔К╓Р╢ч╓ъ╓ч╓╧║ё╓Б╓╥и╦╫Ю C
╔И╔╓╔ж╔И╔Й╓Р╩хмя╓╧╓К╔в╔М╔╟╔И╔Ю╓РЁ╚х╞╓╧╓К╓й╓И
╪б╧т╔у╔║╔╓╔К╓Р╨Ню╝╓╧╓Клэе╙╓г╓Ё╓Л╓И╓ни╦╫Ю╔ь╔ц╔ю╓х╔╙╔ж╔╦╔╖╔╞╔х╔у╔║╔╓╔К
╓╛╩хмя╓г╓╜╓ч╓╧║ё

%description devel -l pl
Pakiet ten jest niezbЙdny przy tworzeniu wЁasnych programСw
korzystaj╠cych ze standardowej biblioteki C. Znajduj╠ siЙ tutaj pliki
nagЁСwkowe oraz pliki obiektowe, niezbЙdne do kompilacji programСw
wykonywalnych i innych bibliotek.

%description devel -l ru
Для разработки программ, использующих стандартные библиотеки C (а
практически все программы их используют), системе НЕОБХОДИМЫ хедеры и
объектные файлы, содержащиеся в этом пакете, чтобы создавать
исполняемые файлы.

%description devel -l tr
C kitaplЩПЩnЩ kullanan (ki hemen hemen hepsi kullanЩyor) programlar
geliЧtirmek iГin gereken standart baЧlЩk dosyalarЩ ve statik
kitaplЩklar.

%description devel -l uk
Для розробки програм, що використовують стандартн╕ б╕бл╕отеки C
(практично вс╕ програми ╖х використовують), систем╕ НЕОБХ╤ДН╤ хедери
та об'╓ктн╕ файли, що м╕стяться в цьому пакет╕, цоб створювати
виконуван╕ файли.

%package headers
Summary:	Header files for development using standard C libraries.
Group:		Development/Libraries
Provides:	%{name}-headers(%{_target_cpu}) = %{epoch}:%{version}-%{release}
%ifarch %{x8664}
# If both -m32 and -m64 is to be supported on AMD64, x86_64 package
# have to be installed, not ix86 one.
Obsoletes:	%{name}-headers(i386)
Obsoletes:	%{name}-headers(i486)
Obsoletes:	%{name}-headers(i586)
Obsoletes:	%{name}-headers(i686)
Obsoletes:	%{name}-headers(athlon)
Obsoletes:	%{name}-headers(pentium3)
Obsoletes:	%{name}-headers(pentium4)
%endif
%{!?with_kernelheaders:Requires:	linux-libc-headers >= %{llh_version}}

%description headers
The glibc-headers package contains the header files necessary
for developing programs which use the standard C libraries (which are
used by nearly all programs).  If you are developing programs which
will use the standard C libraries, your system needs to have these
standard header files available in order to create the
executables.

Install glibc-headers if you are going to develop programs which will
use the standard C libraries.

%package devel-utils
Summary:	Utilities needed for development using standard C libraries.
Group:		Development/Libraries
Provides:	%{name}-devel-utils(%{_target_cpu}) = %{epoch}:%{version}-%{release}
%ifarch %{x8664}
# If both -m32 and -m64 is to be supported on AMD64, x86_64 package
# have to be installed, not ix86 one.
Obsoletes:	%{name}-devel-utils(i386)
Obsoletes:	%{name}-devel-utils(i486)
Obsoletes:	%{name}-devel-utils(i586)
Obsoletes:	%{name}-devel-utils(i686)
Obsoletes:	%{name}-devel-utils(athlon)
Obsoletes:	%{name}-devel-utils(pentium3)
Obsoletes:	%{name}-devel-utils(pentium4)
%endif

%description devel-utils
The glibc-devel-utils package contains utilities necessary
for developing programs which use the standard C libraries (which are
used by nearly all programs).  If you are developing programs which
will use the standard C libraries, your system needs to have these
utilities available.

Install glibc-devel-utils if you are going to develop programs
which will use the standard C libraries.

%package devel-doc
Summary:	Documentation needed for development using standard C libraries.
Group:		Development/Libraries
Provides:	%{name}-devel-doc(%{_target_cpu}) = %{epoch}:%{version}-%{release}
%ifarch %{x8664}
# If both -m32 and -m64 is to be supported on AMD64, x86_64 package
# have to be installed, not ix86 one.
Obsoletes:	%{name}-devel-doc(i386)
Obsoletes:	%{name}-devel-doc(i486)
Obsoletes:	%{name}-devel-doc(i586)
Obsoletes:	%{name}-devel-doc(i686)
Obsoletes:	%{name}-devel-doc(athlon)
Obsoletes:	%{name}-devel-doc(pentium3)
Obsoletes:	%{name}-devel-doc(pentium4)
%endif

%description devel-doc
The glibc-devel-utils package contains info and manual pages necessary
for developing programs which use the standard C libraries (which are
used by nearly all programs).

Install glibc-devel-doc if you are going to develop programs
which will use the standard C libraries.

%package -n nscd
Summary:	Name Service Caching Daemon
Summary(es):	Demonio de cachИ del servicio de nombres
Summary(ja):	╔м║╪╔Ю╔╣║╪╔с╔╧╔╜╔Ц╔ц╔╥╔С╔╟╔г║╪╔Б╔С (nacd)
Summary(pl):	Demon zapamiЙtuj╠cy odpowiedzi serwisСw nazw
Summary(ru):	Кэширующий демон сервисов имен
Summary(uk):	Кешуючий демон сев╕с╕в ╕мен
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
nscd guarda las peticiones del servicio de nombres en una cachИ; eso
puede aumentar drАsticamente las prestaciones de NIS+, y tambiИn puede
ayudar con DNS.

%description -n nscd -l ja
Nscd ╓о╔м║╪╔Ю╔╣║╪╔с╔╧╩╡╬х╓Р╔╜╔Ц╔ц╔╥╔Е╓╥║╒NIS+ ╓н╔я╔у╔╘║╪╔ч╔С╔╧╓Р
╔и╔И╔ч╔ф╔ё╔ц╔╞╓к╡Ча╠╓╧╓К╓Ё╓х╓╛╓г╓╜║╒DNS ╓Рф╠мм╓кйД╫У╓╥╓ч╓╧║ё

%description -n nscd -l pl
nscd zapamiЙtuje zapytania i odpowiedzi NIS oraz DNS. Pozwala
drastycznie poprawiФ szybko╤Ф dziaЁania NIS+.

%description -n nscd -l ru
nscd кэширует результаты запросов к сервисам имен; это может резко
увеличить производительность работы с NIS+ и, также, может помочь с
DNS.

%description -n nscd -l uk
nscd кешу╓ результати запрос╕в до серв╕с╕в ╕мен; це може сильно
зб╕льшити швидк╕сть роботи з NIS+ ╕, також, може допомогти з DNS.

%package -n localedb-src
Summary:	locale database source code
Summary(es):	CСdigo fuente de la base de datos de los locales
Summary(pl):	Kod ╪rСdЁowy bazy locale
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
internacionalizaciСn de GNU libc.

%description -n localedb-src -l pl
Pakiet ten zawiera dane niezbЙdne do zbudowania binarnych plikСw
lokalizacyjnych, by mСc wykorzystaФ mo©liwo╤ci oferowane przez GNU
libc.

%package localedb-all
Summary:	locale database for all locales supported by glibc
Summary(es):	Base de datos de todos los locales soportados por glibc
Summary(pl):	Baza danych locale dla wszystkich lokalizacji obsЁugiwanych przez glibc
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
soportados por glibc. En glibc 2.3.x Иse es un fichero grande (aprox.
39 MB) -- si prefiere algo mАs pequeЯo, sСlo con soporte de unos
locales elegidos, considИrese instalar localedb-src y regenerar la
base de datos usando el escript localedb-gen (una vez que la base de
datos estИ creada, localedb-src se podrА desinstalar).

%description localedb-all -l pl
Ten pakiet zawiera bazЙ danych locale dla wszystkich lokalizacji
obsЁugiwanych przez glibc. W glibc 2.3.x jest to jeden du©y plik
(okoЁo 39MB); aby mieФ co╤ mniejszego, z obsЁug╠ tylko wybranych
lokalizacji, nale©y zainstalowaФ pakiet localedb-src i przegenerowaФ
bazЙ danych przy u©yciu skryptu localedb-gen (po wygenerowaniu bazy
pakiet localedb-src mo©na odinstalowaФ).

%package -n iconv
Summary:	Convert encoding of given files from one encoding to another
Summary(es):	Convierte entre varias codificaciones de los ficheros dados
Summary(pl):	Program do konwersji plikСw tekstowych z jednego kodowania do innego
Group:		Applications/Text
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n iconv
Convert encoding of given files from one encoding to another. You need
this package if you want to convert some document from one encoding to
another or if you have installed some programs which use Generic
Character Set Conversion Interface.

%description -n iconv -l es
Convierte la codificaciСn de dados ficheros. Necesita este paquete si
quiere convertir un documento entre una codificaciСn (juego de
caracteres) y otra, o si tiene instalado algЗn programa que usa el
Generic Character Set Conversion Interface (interfaz genИrica de
conversiСn de juegos de caracteres).

%description -n iconv -l pl
Program do konwersji plikСw tekstowych z jednego kodowania do innego.
Musisz mieФ zainstalowany ten pakiet je©eli wykonujesz konwersjЙ
dokumentСw z jednego kodowania do innego lub je©eli masz zainstalowane
jakie╤ programy, ktСre korzystaj╠ z Generic Character Set Conversion
Interface w glibc, czyli z zestawu funkcji z tej biblioteki, ktСre
umo©liwiaj╠ konwersjЙ kodowania danych z poziomu dowolnego programu.

%package static
Summary:	Static libraries
Summary(es):	Bibliotecas estАticas
Summary(pl):	Biblioteki statyczne
Summary(ru):	Статические библиотеки glibc
Summary(uk):	Статичн╕ б╕бл╕отеки glibc
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}
Obsoletes:	libiconv-static

%description static
GNU libc static libraries.

%description static -l es
Bibliotecas estАticas de GNU libc.

%description static -l pl
Biblioteki statyczne GNU libc.

%description static -l ru
Это отдельный пакет со статическими библиотеками, которые больше не
входят в glibc-devel.

%description static -l uk
Це окремий пакет з╕ статичними б╕бл╕отеками, що б╕льше не входять в
склад glibc-devel.

%package profile
Summary:	glibc with profiling support
Summary(de):	glibc mit Profil-UnterstЭtzung
Summary(es):	glibc con soporte de perfilamiento
Summary(fr):	glibc avec support pour profiling
Summary(pl):	glibc ze wsparciem dla profilowania
Summary(ru):	GNU libc с поддержкой профайлера
Summary(tr):	жlГЭm desteПi olan glibc
Summary(uk):	GNU libc з п╕дтримкою профайлера
Group:		Development/Libraries/Libc
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}
Obsoletes:	libc-profile

%description profile
When programs are being profiled using gprof, they must use these
libraries instead of the standard C libraries for gprof to be able to
profile them correctly.

%description profile -l de
Damit Programmprofile mit gprof richtig erstellt werden, mЭssen diese
Libraries anstelle der Эblichen C-Libraries verwendet werden.

%description profile -l es
Cuando programas son perfilidas usando gprof, tienen que usar estas
biblioteces en vez de las estАndares para que gprof pueda perfilarlas
correctamente.

%description profile -l pl
Programy profilowane za pomoc╠ gprof musz╠ u©ywaФ tych bibliotek
zamiast standardowych bibliotek C, aby gprof mСgЁ odpowiednio je
wyprofilowaФ.

%description profile -l uk
Коли програми досл╕джуються профайлером gprof, вони повинн╕
використовувати зам╕сть стандартних б╕бл╕отек б╕бл╕отеки, що м╕стяться
в цьому пакет╕. При використанн╕ стандартних б╕бл╕отек gprof зам╕сть
реальних результат╕в буде показувати ц╕ни на папайю в Гонолулу в
позаминулому роц╕...

%description profile -l tr
gprof kullanЩlarak ЖlГЭlen programlar standart C kitaplЩПЩ yerine bu
kitaplЩПЩ kullanmak zorundadЩrlar.

%description profile -l ru
Когда программы исследуются профайлером gprof, они должны
использовать, вместо стандартных библиотек, библиотеки, включенные в
этот пакет. При использовании стандартных библиотек gprof вместо
реальных результатов будет показывать цены на папайю в Гонолулу в
позапрошлом году...

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
mАs pequeЯo de la biblioteca libc compartida estАndar.

%description pic -l pl
Archiwum PIC biblioteki GNU C zawiera archiwaln╠ bibliotekЙ (plik ar)
zЁo©on╠ z pojedynczych obiektСw wspСЁdzielonych. U©ywana jest do
tworzenia biblioteki bЙd╠cej mniejszym podzestawem standardowej
biblioteki wspСЁdzielonej libc.

%package -n nss_compat
Summary:	Old style NYS NSS glibc module
Summary(es):	El antiguo mСdulo NYS NSS de glibc
Summary(pl):	Stary moduЁ NYS NSS glibc
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n nss_compat
Old style NYS NSS glibc module.

%description -n nss_compat -l es
El antiguo mСdulo NYS NSS de glibc

%description -n nss_compat -l pl
Stary moduЁ NYS NSS glibc.

%package -n nss_dns
Summary:	BIND NSS glibc module
Summary(es):	MСdulo BIND NSS de glibc
Summary(pl):	ModuЁ BIND NSS glibc
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n nss_dns
BIND NSS glibc module.

%description -n nss_dns -l es
MСdulo BIND NSS de glibc.

%description -n nss_dns -l pl
ModuЁ BIND NSS glibc.

%package -n nss_files
Summary:	Traditional files databases NSS glibc module
Summary(es):	MСdulo de tradicionales bases de datos en ficheros para glibc
Summary(pl):	ModuЁ tradycyjnych plikowych baz danych NSS glibc
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n nss_files
Traditional files databases NSS glibc module.

%description -n nss_files -l es
MСdulo de tradicionales bases de datos en ficheros para glibc.

%description -n nss_files -l pl
ModuЁ tradycyjnych plikowych baz danych NSS glibc.

%package -n nss_hesiod
Summary:	hesiod NSS glibc module
Summary(es):	MСdulo hesiod NSS de glibc
Summary(pl):	ModuЁ hesiod NSS glibc
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n nss_hesiod
glibc NSS (Name Service Switch) module for databases access.

%description -n nss_hesiod -l es
MСdulo hesiod NSS de glibc.

%description -n nss_hesiod -l pl
ModuЁ glibc NSS (Name Service Switch) dostЙpu do baz danych.

%package -n nss_nis
Summary:	NIS(YP) NSS glibc module
Summary(es):	MСdulo NIS(YP) NSS de glibc
Summary(pl):	ModuЁ NIS(YP) NSS glibc
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n nss_nis
glibc NSS (Name Service Switch) module for NIS(YP) databases access.

%description -n nss_nis -l es
MСdulo NSS de glibc para acceder las bases de datos NIS(YP).

%description -n nss_nis -l pl
ModuЁ glibc NSS (Name Service Switch) dostЙpu do baz danych NIS(YP).

%package -n nss_nisplus
Summary:	NIS+ NSS module
Summary(es):	MСdulo NIS+ NSS
Summary(pl):	ModuЁ NIS+ NSS
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n nss_nisplus
glibc NSS (Name Service Switch) module for NIS+ databases access.

%description -n nss_nisplus -l es
MСdulo NSS (Name Service Switch) de glibc para acceder las bases de
datos NIS+.

%description -n nss_nisplus -l pl
ModuЁ glibc NSS (Name Service Switch) dostЙpu do baz danych NIS+.

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
No lo necesita. EncontrarА los detalles en:
http://sources.redhat.com/ml/libc-alpha/2000-12/msg00068.html

%description zoneinfo_right -l pl
Nie potrzebujesz tego. SzczegСЁy pod:
http://sources.redhat.com/ml/libc-alpha/2000-12/msg00068.html

%package -n %{name}64
Summary:	GNU libc - 64-bit libraries
Summary(es):	GNU libc - bibliotecas de 64 bits
Summary(pl):	GNU libc - biblioteki 64-bitowe
Group:		Libraries
PreReq:		basesystem
Requires:	%{name}-misc = %{epoch}:%{version}-%{release}
Provides:	glibc = %{epoch}:%{version}-%{release}
%{?with_tls:Provides:	glibc(tls)}
Provides:	ldconfig
Obsoletes:	glibc-common
Obsoletes:	glibc-debug
Obsoletes:	ldconfig
Conflicts:	kernel < %{min_kernel}
Conflicts:	ld.so < 1.9.9-10
Conflicts:	man-pages < 1.43
Conflicts:	rc-scripts < 0.3.1-13
Conflicts:	rpm < 4.1
Conflicts:	poldek < 0.18.8-4

%description -n %{name}64
64-bit GNU libc libraries for 64bit architecture.

%description -n %{name}64 -l es
Bibliotecas GNU libc de 64 bits para la arquitectura 64bit.

%description -n %{name}64 -l pl
Biblioteki 64-bitowe GNU libc dla architektury 64bit.

%prep
%setup -q -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
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
%patch28 -p1
%{?with_cross:%patch29 -p1}
%{?with_pax:%patch30 -p1}

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

# compiling static using diet vs glibc saves 400k
diet -Os %{__cc} %{SOURCE9} %{rpmcflags} -static -o postshell
diet -Os %{__cc} %{SOURCE8} %{rpmcflags} -static -o glibc-postinst

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
cd ..

install postshell					$RPM_BUILD_ROOT/sbin
install glibc-postinst				$RPM_BUILD_ROOT/sbin

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

# Where should s390 go?
%ifarch %{ix86} ppc sparc
mv $RPM_BUILD_ROOT%{_includedir}/gnu/stubs.h $RPM_BUILD_ROOT%{_includedir}/gnu/stubs-32.h
%endif

%ifarch %{x8664} ppc64 sparc64 alpha
mv $RPM_BUILD_ROOT%{_includedir}/gnu/stubs.h $RPM_BUILD_ROOT%{_includedir}/gnu/stubs-64.h
%endif

cat <<EOF >$RPM_BUILD_ROOT%{_includedir}/gnu/stubs.h
/* This file selects the right generated file of '__stub_FUNCTION' macros
   based on the architecture being compiled for.  */

#include <bits/wordsize.h>

#if __WORDSIZE == 32
# include <gnu/stubs-32.h>
#elif __WORDSIZE == 64
# include <gnu/stubs-64.h>
#else
# error "unexpected value for __WORDSIZE macro"
#endif
EOF

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
# as (atk, gail)
# az_IR (gtk+)
# my (gaim)
# rm (gtkspell)
# tk, yo (used by GNOME)
#
# NOTES:
# bn is used for bn_BD or bn_IN?
# omitted here - already existing (with libc.mo):
#   be,ca,cs,da,de,el,en_GB,es,fi,fr,gl,hr,hu,it,ja,ko,nb,nl,pl,pt_BR,sk,sv,tr,zh_CN,zh_TW
for i in af am ang ar az bg bn br bs cy de_AT en en@boldquot en@quot en_AU \
    en_CA en_US eo es_AR es_MX et eu fa fo ga gu he hi hsb ia id is it_CH ka \
    kn ku leet lg li lo lt lv mi mk ml mn mr ms mt nds ne nn nso or pa pt ro \
    ru rw se sl sq sr sr@Latn sr@ije ss ta tg th tl tlh uk uz ve vi wa xh yi \
    zu ; do
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

%ifarch %{x8664} ppc64 s390x sparc64
%post	-n %{name}64 -p /sbin/postshell
%else
%post	-p /sbin/postshell
%endif
/sbin/glibc-postinst /%{_lib}/%{_host_cpu}
/sbin/ldconfig
-/sbin/telinit u

%ifarch %{x8664} ppc64 s390x sparc64
%postun	-n %{name}64 -p /sbin/postshell
%else
%postun	-p /sbin/postshell
%endif
/sbin/ldconfig
-/sbin/telinit u

%ifarch %{x8664} ppc64 s390x sparc64
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
%groupadd -P nscd -g 144 -r nscd
%useradd -P nscd -u 144 -r -d /tmp -s /bin/false -c "nscd" -g nscd nscd

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

%ifarch %{x8664} ppc64 s390x sparc64
%files -n %{name}64
%defattr(644,root,root,755)
%else
%files
%defattr(644,root,root,755)
%endif
%defattr(644,root,root,755)
%doc README NEWS FAQ BUGS
%attr(755,root,root) /sbin/postshell
%attr(755,root,root) /sbin/glibc-postinst
%attr(755,root,root) /sbin/ldconfig
# ld* and libc.so.6 SONAME symlinks must be in package because of
# chicken-egg problem (postshell is dynamically linked with libc);
# ld-*.so SONAME is:
#   ld.so.1 on ppc
#   ld64.so.1 on ppc64,s390x
#   ld-linux-ia64.so.2 on ia64
#   ld-linux-x86-64.so.2 on x86_64
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
%endif

%{_includedir}/gnu/stubs-*.h

%files headers
%{_includedir}/*.h
%ifarch alpha
%{_includedir}/alpha
%endif
%{_includedir}/arpa
%{_includedir}/bits
%{_includedir}/gnu/lib*.h
%{_includedir}/gnu/stubs.h
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

%if %{with dual}
%{_includedir}/nptl
%endif

%files devel-utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gencat
%attr(755,root,root) %{_bindir}/*prof*
%attr(755,root,root) %{_bindir}/*trace

%files devel-doc
%doc documentation/* NOTES PROJECTS
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
