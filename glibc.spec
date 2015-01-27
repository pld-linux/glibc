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
%bcond_with	boot64		# bootstrap *64 using cross* (sparc64 currently)
%bcond_with	pax		# build in PaX enabled environment (PaX hack is default BTW)
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
%if %{with boot64}
%define		with_cross	1
%undefine	with_selinux
%ifarch sparc64
%define		__cc	sparc64-pld-linux-gcc
%endif
%endif

%if %{with linuxthreads} && %{with nptl}
%define		with_dual	1
%endif

%define		llh_version	7:2.6.10.0-3

Summary:	GNU libc
Summary(de.UTF-8):	GNU libc
Summary(es.UTF-8):	GNU libc
Summary(fr.UTF-8):	GNU libc
Summary(ja.UTF-8):	GNU libc ライブラリ
Summary(pl.UTF-8):	GNU libc
Summary(ru.UTF-8):	GNU libc версии 2.3
Summary(tr.UTF-8):	GNU libc
Summary(uk.UTF-8):	GNU libc версії 2.3
Name:		glibc
Version:	2.3.6
Release:	21
Epoch:		6
License:	LGPL
Group:		Libraries
Source0:	ftp://sources.redhat.com/pub/glibc/releases/%{name}-%{version}.tar.bz2
# Source0-md5:	bfdce99f82d6dbcb64b7f11c05d6bc96
Source1:	ftp://sources.redhat.com/pub/glibc/releases/%{name}-linuxthreads-%{version}.tar.bz2
# Source1-md5:	d4eeda37472666a15cc1f407e9c987a9
Source2:	nscd.init
Source3:	nscd.sysconfig
Source4:	nscd.logrotate
#Source5:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-man-pages.tar.bz2
Source5:	http://qboosh.cs.net.pl/man/%{name}-man-pages.tar.bz2
# Source5-md5:	f464eadf3cf06761f65639e44a179e6b
Source6:	%{name}-localedb-gen
Source7:	%{name}-LD-path.c
Source8:	inotify.h
Patch0:		%{name}-info.patch
Patch1:		%{name}-pl.po-update.patch
Patch2:		%{name}-pld.patch
Patch3:		%{name}-crypt-blowfish.patch
Patch4:		%{name}-linuxthreads-lock.patch
Patch5:		%{name}-pthread_create-manpage.patch
Patch6:		%{name}-paths.patch
Patch7:		%{name}-dl-execstack.patch
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
Patch27:	%{name}-sys-kd.patch
Patch28:	%{name}-cross-gcc_eh.patch
# WARNING: do not comment or delete pax_dl-execstack.patch, please. If you think
#          that this is a good idea send some info to pld-devel-{pl,en}
Patch29:	%{name}-pax_dl-execstack.patch
Patch30:	%{name}-pax-build.patch
Patch31:	%{name}-large_collate_tables.patch
Patch32:	%{name}-ctype-compat.patch
Patch33:	%{name}-sparc-mman.h.patch
Patch34:	%{name}-dl-tls.patch
Patch35:	%{name}-bindresvport2.patch
Patch36:	%{name}-nis+-leaks2.patch
Patch37:	%{name}-nis+-batch2.patch
Patch38:	%{name}-bz2226.patch
Patch39:	%{name}-rh197790.patch
Patch40:	%{name}-rh215572.patch
Patch41:	%{name}-nis+-getenv.patch
Patch42:	%{name}-rh228103.patch
Patch43:	%{name}-rh219145.patch
Patch44:	%{name}-posix-sh.patch
Patch45:	%{name}-bug-2644.patch
Patch46:	binutils-2.20.patch
Patch47:	CVE-2015-0235.patch
URL:		http://www.gnu.org/software/libc/
%{?with_selinux:BuildRequires:	audit-libs-devel}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	binutils >= 2:2.15.90.0.3
%{!?with_cross:BuildRequires:	dietlibc-static}
BuildRequires:	gcc >= 5:3.2
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
%{?with_pax:BuildRequires:	paxctl}
BuildRequires:	perl-base
BuildRequires:	rpm-build >= 4.3-0.20030610.28
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0.5
BuildRequires:	texinfo
Requires(post):	ldconfig = %{epoch}:%{version}-%{release}
Requires:	%{name}-misc = %{epoch}:%{version}-%{release}
Requires:	basesystem
%{?with_tls:Provides:	glibc(tls)}
Obsoletes:	glibc-common
Obsoletes:	glibc-debug
Conflicts:	SysVinit < 2.86-11
Conflicts:	kernel < %{min_kernel}
Conflicts:	ld.so < 1.9.9-10
Conflicts:	man-pages < 1.43
Conflicts:	poldek < 0.18.8-5
Conflicts:	rc-scripts < 0.3.1-13
Conflicts:	rpm < 4.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
AutoReq:	false

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
national language (locale) support.

Can be used on: Linux kernel >= %{min_kernel}.

%description -l es.UTF-8
Contiene las bibliotecas estándared que son usadas por varios
programas del sistema. Para ahorrar el espacio en el disco y la
memoria, igual que para facilitar actualizaciones, código común del
sistema se guarda en un sitio y es compartido entre los programas.
Este paquete contiene las bibliotecas compartidas más importantes, es
decir la biblioteca C estándar y la biblioteca estándar de matemática.
Sin éstas, un sistema Linux no podrá funcionar. También está incluido
soporte de idiomas nacionales (locale).

Puede usarse con: núcleo Linux >= %{min_kernel}.

%description -l de.UTF-8
Enthält die Standard-Libraries, die von verschiedenen Programmen im
System benutzt werden. Um Festplatten- und Arbeitsspeicher zu sparen
und zur Vereinfachung von Upgrades ist der gemeinsame Systemcode an
einer einzigen Stelle gespeichert und wird von den Programmen
gemeinsam genutzt. Dieses Paket enthält die wichtigsten Sets der
shared Libraries, die Standard-C-Library und die
Standard-Math-Library, ohne die das Linux-System nicht funktioniert.
Ferner enthält es den Support für die verschiedenen Sprachgregionen
(locale).

Can be used on: Linux kernel >= %{min_kernel}.

%description -l fr.UTF-8
Contient les bibliothèques standards utilisées par de nombreux
programmes du système. Afin d'économiser l'espace disque et mémoire,
et de faciliter les mises à jour, le code commun au système est mis à
un endroit et partagé entre les programmes. Ce paquetage contient les
bibliothèques partagées les plus importantes, la bibliothèque standard
du C et la bibliothèque mathématique standard. Sans celles-ci, un
système Linux ne peut fonctionner. Il contient aussi la gestion des
langues nationales (locales).

Can be used on: Linux kernel >= %{min_kernel}.

%description -l ja.UTF-8
glibc
パッケージはシステム上の複数のプログラムで使われる標準ライブラリを
ふくみます。ディスクスペースとメモリを節約したり、アップグレードを
用意にするために、共通のシステムコードは一つの場所におかれ、プログラム
間で共有されます。この部分的なパッケージはシェアドライブラリのかなり
重要なセットをふくみます: 標準 C ライブラリと標準数値ライブラリです。
この二つのライブラリ抜きでは、Linux システムは機能しません。 glibc
パッケージはまた地域言語 (locale) サポートとタイムゾーンデータベース
サポートをふくみます。

Can be used on: Linux kernel >= %{min_kernel}.

%description -l pl.UTF-8
W pakiecie znajdują się podstawowe biblioteki, używane przez różne
programy w Twoim systemie. Używanie przez programy bibliotek z tego
pakietu oszczędza miejsce na dysku i pamięć. Większość kodu
systemowego jest usytuowane w jednym miejscu i dzielone między wieloma
programami. Pakiet ten zawiera bardzo ważny zbiór bibliotek
standardowych, współdzielonych (dynamicznych) bibliotek C i
matematycznych. Bez glibc system Linux nie jest w stanie funkcjonować.
Znajdują się tutaj również definicje różnych informacji dla wielu
języków (locale).

Przeznaczony dla jądra Linux >= %{min_kernel}.

%description -l ru.UTF-8
Содержит стандартные библиотеки, используемые многочисленными
программами в системе. Для того, чтобы сохранить дисковое пространство
и память, а также для простоты обновления, системный код, общий для
всех программ, хранится в одном месте и коллективно используется всеми
программами. Этот пакет содержит наиболее важные из разделяемых
библиотек - стандартную библиотеку C и стандартную библиотеку
математики. Без этих библиотек Linux функционировать не будет. Также
пакет содержит поддержку национальных языков (locale).

Can be used on: Linux kernel >= %{min_kernel}.

%description -l tr.UTF-8
Bu paket, birçok programın kullandığı standart kitaplıkları içerir.
Disk alanı ve bellek kullanımını azaltmak ve aynı zamanda güncelleme
işlemlerini kolaylaştırmak için ortak sistem kodları tek bir yerde
tutulup programlar arasında paylaştırılır. Bu paket en önemli ortak
kitaplıkları, standart C kitaplığını ve standart matematik kitaplığını
içerir. Bu kitaplıklar olmadan Linux sistemi çalışmayacaktır. Yerel
dil desteği ve zaman dilimi veri tabanı da bu pakette yer alır.

Can be used on: Linux kernel >= %{min_kernel}.

%description -l uk.UTF-8
Містить стандартні бібліотеки, котрі використовуються численними
програмами в системі. Для того, щоб зберегти дисковий простір та
пам'ять, а також для простоти поновлення системи, системний код,
спільний для всіх програм, зберігається в одному місці і колективно
використовується всіма програмами. Цей пакет містить найбільш важливі
з динамічних бібліотек - стандартну бібліотеку С та стандартну
бібліотеку математики. Без цих бібліотек Linux функціонувати не буде.
Також пакет містить підтримку національних мов (locale).

Can be used on: Linux kernel >= %{min_kernel}.

%package misc
Summary:	Utilities and data used by glibc
Summary(pl.UTF-8):	Narzędzia i dane używane przez glibc
Group:		Applications/System
Requires:	%{name} = %{epoch}:%{version}-%{release}
Suggests:	localedb
Suggests:	tzdata
AutoReq:	false

%description misc
Utilities and data used by glibc.

%description misc -l pl.UTF-8
Narzędzia i dane używane przez glibc.

%package -n ldconfig
Summary:	Creates shared library cache and maintains symlinks
Summary(de.UTF-8):	Erstellt ein shared library cache und verwaltet symlinks
Summary(fr.UTF-8):	Crée un cache de bibliothčque partagée et gčre *.so
Summary(pl.UTF-8):	Tworzy cache bibliotek dynamicznych i ich symlinki
Summary(tr.UTF-8):	Ortak kitaplýk önbelleđi yaratýr ve bađlantýlarý kurar
Group:		Applications/System
# This is needed because previous package (glibc) had autoreq false and had
# provided this manually. Probably poldek bug that have to have it here.
Provides:	/sbin/ldconfig

%description -n ldconfig
ldconfig scans a running system and sets up the symbolic links that
are used to load shared libraries properly. It also creates
/etc/ld.so.cache which speeds the loading programs which use shared
libraries.

%description -n ldconfig -l pl.UTF-8
Ldconfig testuje uruchominy system i tworzy symboliczne linki, które
są następnie używane do poprawnego ładowania bibliotek dynamicznych.
Program ten tworzy plik /etc/ld.so.cache, który przyśpiesza wywołanie
dowolnego programu korzystającego z bibliotek dynamicznych.

%description -n ldconfig -l de.UTF-8
ldconfig scannt ein laufendes System und richtet die symbolischen
Verknüpfungen zum Laden der gemeinsam genutzten Libraries ein.
Außerdem erstellt es /etc/ld.so.cache, was das Laden von Programmen
mit gemeinsam genutzten Libraries beschleunigt.

%description -n ldconfig -l fr.UTF-8
ldconfig analyse un systčme et configure les liens symboliques
utilisés pour charger correctement les bibliothčques partagées. Il
crée aussi /etc/ld.so.cache qui accélčre le chargement des programmes
utilisant les bibliothčques partagées.

%description -n ldconfig -l tr.UTF-8
ldconfig, çalýţmakta olan sistemi araţtýrýr ve ortak kitaplýklarýn
düzgün bir ţekilde yüklenmesi için gereken simgesel bađlantýlarý
kurar. Ayrýca ortak kitaplýklarý kullanan programlarýn yüklenmesini
hýzlandýran /etc/ld.so.cache dosyasýný yaratýr.

%package devel
Summary:	Additional libraries required to compile
Summary(de.UTF-8):	Weitere Libraries zum Kompilieren
Summary(es.UTF-8):	Bibliotecas adicionales necesarias para la compilación
Summary(fr.UTF-8):	Librairies supplémentaires nécessaires à la compilation
Summary(ja.UTF-8):	標準 C ライブラリで使われるヘッダーとオブジェクトファイル
Summary(pl.UTF-8):	Dodatkowe biblioteki wymagane podczas kompilacji
Summary(ru.UTF-8):	Дополнительные библиотеки, необходимые для компиляции
Summary(tr.UTF-8):	Geliştirme için gerekli diğer kitaplıklar
Summary(uk.UTF-8):	Додаткові бібліотеки, потрібні для компіляції
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	%{name}-devel-utils = %{epoch}:%{version}-%{release}
Requires:	%{name}-headers = %{epoch}:%{version}-%{release}
Provides:	%{name}-devel(%{_target_cpu}) = %{epoch}:%{version}-%{release}
Obsoletes:	libiconv-devel

%description devel
To develop programs which use the standard C libraries (which nearly
all programs do), the system needs to have these standard header files
and object files available for creating the executables.

%description devel -l de.UTF-8
Bei der Entwicklung von Programmen, die die Standard-C-Libraries
verwenden (also fast alle), benötigt das System diese Standard-Header-
und Objektdateien zum Erstellen der ausführbaren Programme.

%description devel -l es.UTF-8
Para desarrollar programas que utilizan las bibliotecas C estándar (lo
cual hacen prácticamente todos los programas), el sistema necesita
disponer de estos ficheros de cabecera y de objetos para crear los
ejecutables.

%description devel -l fr.UTF-8
Pour développer des programmes utilisant les bibliothèques standard du
C (ce que presque tous les programmes font), le système doit posséder
ces fichiers en-têtes et objets standards pour créer les exécutables.

%description devel -l ja.UTF-8
glibc-devel パッケージは(ほとんどすべてのプログラムで使われる)標準 C
ライブラリを使用したプログラムを開発するためのヘッダーとオブジェクト
ファイルを含みます。もし標準 C
ライブラリを使用するプログラムを開発するなら
実行ファイルを作成する目的でこれらの標準ヘッダとオブジェクトファイル
が使用できます。

%description devel -l pl.UTF-8
Pakiet ten jest niezbędny przy tworzeniu własnych programów
korzystających ze standardowej biblioteki C. Znajdują się tutaj pliki
nagłówkowe oraz pliki obiektowe, niezbędne do kompilacji programów
wykonywalnych i innych bibliotek.

%description devel -l ru.UTF-8
Для разработки программ, использующих стандартные библиотеки C (а
практически все программы их используют), системе НЕОБХОДИМЫ хедеры и
объектные файлы, содержащиеся в этом пакете, чтобы создавать
исполняемые файлы.

%description devel -l tr.UTF-8
C kitaplığını kullanan (ki hemen hemen hepsi kullanıyor) programlar
geliştirmek için gereken standart başlık dosyaları ve statik
kitaplıklar.

%description devel -l uk.UTF-8
Для розробки програм, що використовують стандартні бібліотеки C
(практично всі програми їх використовують), системі НЕОБХІДНІ хедери
та об'єктні файли, що містяться в цьому пакеті, цоб створювати
виконувані файли.

%package headers
Summary:	Header files for development using standard C libraries
Summary(pl.UTF-8):	Pliki nagłówkowe do tworzenia programów przy użyciu standardowych bibliotek C
Group:		Development/Building
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
%ifarch ppc64
Obsoletes:	%{name}-headers(ppc)
%endif
%ifarch s390x
Obsoletes:	%{name}-headers(s390)
%endif
%ifarch sparc64
Obsoletes:	%{name}-headers(sparc)
%endif
%{!?with_kernelheaders:Requires:	linux-libc-headers >= %{llh_version}}

%description headers
The glibc-headers package contains the header files necessary for
developing programs which use the standard C libraries (which are used
by nearly all programs). If you are developing programs which will use
the standard C libraries, your system needs to have these standard
header files available in order to create the executables.

Install glibc-headers if you are going to develop programs which will
use the standard C libraries.

%description headers -l pl.UTF-8
Pakiet glibc-headers zawiera pliki nagłówkowe niezbędne do rozwijania
programów używających standardowych bibliotek C (używanych przez
prawie wszystkie programy). Jeśli tworzymy programy korzystające ze
standardowych bibliotek C, system wymaga dostępności tych
standardowych plików nagłówkowych do tworzenia programów
wykonywalnych.

Ten pakiet należy zainstalować jeśli zamierzamy tworzyć programy
korzystające ze standardowych bibliotek C.

%package devel-utils
Summary:	Utilities needed for development using standard C libraries
Summary(pl.UTF-8):	Narzędzia do tworzenia programów przy użyciu standardowych bibliotek C
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
%ifarch ppc64
Obsoletes:	%{name}-devel-utils(ppc)
%endif
%ifarch s390x
Obsoletes:	%{name}-devel-utils(s390)
%endif
%ifarch sparc64
Obsoletes:	%{name}-devel-utils(sparc)
%endif

%description devel-utils
The glibc-devel-utils package contains utilities necessary for
developing programs which use the standard C libraries (which are used
by nearly all programs). If you are developing programs which will use
the standard C libraries, your system needs to have these utilities
available.

Install glibc-devel-utils if you are going to develop programs which
will use the standard C libraries.

%description devel-utils -l pl.UTF-8
Pakiet glibc-devel-utils zawiera narzędzia niezbędne do rozwijania
programów używających standardowych bibliotek C (używanych przez
prawie wszystkie programy). Jeśli tworzymy programy korzystające ze
standardowych bibliotek C, system wymaga dostępności tych narzędzi do
tworzenia programów wykonywalnych.

Ten pakiet należy zainstalować jeśli zamierzamy tworzyć programy
korzystające ze standardowych bibliotek C.

%package devel-doc
Summary:	Documentation needed for development using standard C libraries
Summary(pl.UTF-8):	Dokumentacja do tworzenia programów przy użyciu standardowych bibliotek C
Group:		Documentation
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
%ifarch ppc64
Obsoletes:	%{name}-devel-doc(ppc)
%endif
%ifarch s390x
Obsoletes:	%{name}-devel-doc(s390)
%endif
%ifarch sparc64
Obsoletes:	%{name}-devel-doc(sparc)
%endif

%description devel-doc
The glibc-devel-doc package contains info and manual pages necessary
for developing programs which use the standard C libraries (which are
used by nearly all programs).

Install glibc-devel-doc if you are going to develop programs which
will use the standard C libraries.

%description devel-doc -l pl.UTF-8
Pakiet glibc-devel-doc zawiera strony info i manuala przydatne do
rozwijania programów używających standardowych bibliotek C (używanych
przez prawie wszystkie programy).

Ten pakiet należy zainstalować jeśli zamierzamy tworzyć programy
korzystające ze standardowych bibliotek C.

%package -n nscd
Summary:	Name Service Caching Daemon
Summary(es.UTF-8):	Demonio de caché del servicio de nombres
Summary(ja.UTF-8):	ネームサービスキャッシングデーモン (nacd)
Summary(pl.UTF-8):	Demon zapamiętujący odpowiedzi serwisów nazw
Summary(ru.UTF-8):	Кэширующий демон сервисов имен
Summary(uk.UTF-8):	Кешуючий демон севісів імен
Group:		Networking/Daemons
Requires(post):	fileutils
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	%{name} = %{epoch}:%{version}-%{release}
%{?with_selinux:Requires:	libselinux >= 1.18}
Requires:	rc-scripts >= 0.2.0
Provides:	group(nscd)
Provides:	user(nscd)

%description -n nscd
nscd caches name service lookups; it can dramatically improve
performance with NIS+, and may help with DNS as well.

%description -n nscd -l es.UTF-8
nscd guarda las peticiones del servicio de nombres en una caché; eso
puede aumentar drásticamente las prestaciones de NIS+, y también puede
ayudar con DNS.

%description -n nscd -l ja.UTF-8
Nscd はネームサービス参照をキャッシュし、NIS+ のパフォーマンスを
ドラマティックに改善することができ、DNS を同様に補助します。

%description -n nscd -l pl.UTF-8
nscd zapamiętuje zapytania i odpowiedzi NIS oraz DNS. Pozwala
drastycznie poprawić szybkość działania NIS+.

%description -n nscd -l ru.UTF-8
nscd кэширует результаты запросов к сервисам имен; это может резко
увеличить производительность работы с NIS+ и, также, может помочь с
DNS.

%description -n nscd -l uk.UTF-8
nscd кешує результати запросів до сервісів імен; це може сильно
збільшити швидкість роботи з NIS+ і, також, може допомогти з DNS.

%package -n localedb-src
Summary:	locale database source code
Summary(es.UTF-8):	Código fuente de la base de datos de los locales
Summary(pl.UTF-8):	Kod źródłowy bazy locale
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	gzip
Requires:	sed
Provides:	localedb

%description -n localedb-src
This add-on package contains the data needed to build the locale data
files to use the internationalization features of the GNU libc.

%description -n localedb-src -l es.UTF-8
Este paquete adicional contiene los datos necesarios para construir
los ficheros de locale, imprescindibles para usar las cualidades de
internacionalización de GNU libc.

%description -n localedb-src -l pl.UTF-8
Pakiet ten zawiera dane niezbędne do zbudowania binarnych plików
lokalizacyjnych, by móc wykorzystać możliwości oferowane przez GNU
libc.

%package localedb-all
Summary:	locale database for all locales supported by glibc
Summary(es.UTF-8):	Base de datos de todos los locales soportados por glibc
Summary(pl.UTF-8):	Baza danych locale dla wszystkich lokalizacji obsługiwanych przez glibc
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	iconv = %{epoch}:%{version}-%{release}
Provides:	localedb

%description localedb-all
This package contains locale database for all locales supported by
glibc. In glibc 2.3.x it's one large file (about 39MB) - if you want
something smaller with support for chosen locales only, consider
installing localedb-src and regenerating database using localedb-gen
script (when database is generated, localedb-src can be uninstalled).

%description localedb-all -l es.UTF-8
Este paquete contiene una base de datos de todos los locales
soportados por glibc. En glibc 2.3.x ése es un fichero grande (aprox.
39 MB) -- si prefiere algo más pequeño, sólo con soporte de unos
locales elegidos, considérese instalar localedb-src y regenerar la
base de datos usando el escript localedb-gen (una vez que la base de
datos esté creada, localedb-src se podrá desinstalar).

%description localedb-all -l pl.UTF-8
Ten pakiet zawiera bazę danych locale dla wszystkich lokalizacji
obsługiwanych przez glibc. W glibc 2.3.x jest to jeden duży plik
(około 39MB); aby mieć coś mniejszego, z obsługą tylko wybranych
lokalizacji, należy zainstalować pakiet localedb-src i przegenerować
bazę danych przy użyciu skryptu localedb-gen (po wygenerowaniu bazy
pakiet localedb-src można odinstalować).

%package -n iconv
Summary:	Convert encoding of given files from one encoding to another
Summary(es.UTF-8):	Convierte entre varias codificaciones de los ficheros dados
Summary(pl.UTF-8):	Moduły do konwersji plików tekstowych z jednego kodowania do innego
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n iconv
Convert encoding of given files from one encoding to another. You need
this package if you want to convert some document from one encoding to
another or if you have installed some programs which use Generic
Character Set Conversion Interface.

%description -n iconv -l es.UTF-8
Convierte la codificación de dados ficheros. Necesita este paquete si
quiere convertir un documento entre una codificación (juego de
caracteres) y otra, o si tiene instalado algún programa que usa el
Generic Character Set Conversion Interface (interfaz genérica de
conversión de juegos de caracteres).

%description -n iconv -l pl.UTF-8
Moduły do konwersji plików tekstowych z jednego kodowania do innego.
Trzeba mieć zainstalowany ten pakiet, aby wykonywać konwersję
dokumentów z jednego kodowania do innego lub do używania programów
korzystających z Generic Character Set Conversion Interface w glibc,
czyli z zestawu funkcji z tej biblioteki, które umożliwiają konwersję
kodowania danych z poziomu dowolnego programu.

%package static
Summary:	Static libraries
Summary(es.UTF-8):	Bibliotecas estáticas
Summary(pl.UTF-8):	Biblioteki statyczne
Summary(ru.UTF-8):	Статические библиотеки glibc
Summary(uk.UTF-8):	Статичні бібліотеки glibc
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}
Provides:	%{name}-static(%{_target_cpu}) = %{epoch}:%{version}-%{release}
Obsoletes:	libiconv-static

%description static
GNU libc static libraries.

%description static -l es.UTF-8
Bibliotecas estáticas de GNU libc.

%description static -l pl.UTF-8
Biblioteki statyczne GNU libc.

%description static -l ru.UTF-8
Это отдельный пакет со статическими библиотеками, которые больше не
входят в glibc-devel.

%description static -l uk.UTF-8
Це окремий пакет зі статичними бібліотеками, що більше не входять в
склад glibc-devel.

%package profile
Summary:	glibc with profiling support
Summary(de.UTF-8):	glibc mit Profil-Unterstützung
Summary(es.UTF-8):	glibc con soporte de perfilamiento
Summary(fr.UTF-8):	glibc avec support pour profiling
Summary(pl.UTF-8):	glibc ze wsparciem dla profilowania
Summary(ru.UTF-8):	GNU libc с поддержкой профайлера
Summary(tr.UTF-8):	Ölçüm desteği olan glibc
Summary(uk.UTF-8):	GNU libc з підтримкою профайлера
Group:		Development/Libraries/Libc
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}
Obsoletes:	libc-profile

%description profile
When programs are being profiled using gprof, they must use these
libraries instead of the standard C libraries for gprof to be able to
profile them correctly.

%description profile -l de.UTF-8
Damit Programmprofile mit gprof richtig erstellt werden, müssen diese
Libraries anstelle der üblichen C-Libraries verwendet werden.

%description profile -l es.UTF-8
Cuando programas son perfilidas usando gprof, tienen que usar estas
biblioteces en vez de las estándares para que gprof pueda perfilarlas
correctamente.

%description profile -l pl.UTF-8
Programy profilowane za pomocą gprof muszą używać tych bibliotek
zamiast standardowych bibliotek C, aby gprof mógł odpowiednio je
wyprofilować.

%description profile -l uk.UTF-8
Коли програми досліджуються профайлером gprof, вони повинні
використовувати замість стандартних бібліотек бібліотеки, що містяться
в цьому пакеті. При використанні стандартних бібліотек gprof замість
реальних результатів буде показувати ціни на папайю в Гонолулу в
позаминулому році...

%description profile -l tr.UTF-8
gprof kullanılarak ölçülen programlar standart C kitaplığı yerine bu
kitaplığı kullanmak zorundadırlar.

%description profile -l ru.UTF-8
Когда программы исследуются профайлером gprof, они должны
использовать, вместо стандартных библиотек, библиотеки, включенные в
этот пакет. При использовании стандартных библиотек gprof вместо
реальных результатов будет показывать цены на папайю в Гонолулу в
позапрошлом году...

%package pic
Summary:	glibc PIC archive
Summary(es.UTF-8):	Archivo PIC de glibc
Summary(pl.UTF-8):	Archiwum PIC glibc
Group:		Development/Libraries/Libc
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description pic
GNU C Library PIC archive contains an archive library (ar file)
composed of individual shared objects. This is used for creating a
library which is a smaller subset of the standard libc shared library.

%description pic -l es.UTF-8
El archivo PIC de la biblioteca glibc contiene una biblioteca
archivada (un fichero ar) compuesta de individuales objetos
compartidos. Es usado para crear una biblioteca que sea un subconjunto
más pequeño de la biblioteca libc compartida estándar.

%description pic -l pl.UTF-8
Archiwum PIC biblioteki GNU C zawiera archiwalną bibliotekę (plik ar)
złożoną z pojedynczych obiektów współdzielonych. Używana jest do
tworzenia biblioteki będącej mniejszym podzestawem standardowej
biblioteki współdzielonej libc.

%package -n nss_compat
Summary:	Old style NYS NSS glibc module
Summary(es.UTF-8):	El antiguo módulo NYS NSS de glibc
Summary(pl.UTF-8):	Stary moduł NYS NSS glibc
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n nss_compat
Old style NYS NSS glibc module.

%description -n nss_compat -l es.UTF-8
El antiguo módulo NYS NSS de glibc

%description -n nss_compat -l pl.UTF-8
Stary moduł NYS NSS glibc.

%package -n nss_dns
Summary:	BIND NSS glibc module
Summary(es.UTF-8):	Módulo BIND NSS de glibc
Summary(pl.UTF-8):	Moduł BIND NSS glibc
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n nss_dns
BIND NSS glibc module.

%description -n nss_dns -l es.UTF-8
Módulo BIND NSS de glibc.

%description -n nss_dns -l pl.UTF-8
Moduł BIND NSS glibc.

%package -n nss_files
Summary:	Traditional files databases NSS glibc module
Summary(es.UTF-8):	Módulo de tradicionales bases de datos en ficheros para glibc
Summary(pl.UTF-8):	Moduł tradycyjnych plikowych baz danych NSS glibc
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n nss_files
Traditional files databases NSS glibc module.

%description -n nss_files -l es.UTF-8
Módulo de tradicionales bases de datos en ficheros para glibc.

%description -n nss_files -l pl.UTF-8
Moduł tradycyjnych plikowych baz danych NSS glibc.

%package -n nss_hesiod
Summary:	hesiod NSS glibc module
Summary(es.UTF-8):	Módulo hesiod NSS de glibc
Summary(pl.UTF-8):	Moduł hesiod NSS glibc
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n nss_hesiod
glibc NSS (Name Service Switch) module for databases access.

%description -n nss_hesiod -l es.UTF-8
Módulo hesiod NSS de glibc.

%description -n nss_hesiod -l pl.UTF-8
Moduł glibc NSS (Name Service Switch) dostępu do baz danych.

%package -n nss_nis
Summary:	NIS(YP) NSS glibc module
Summary(es.UTF-8):	Módulo NIS(YP) NSS de glibc
Summary(pl.UTF-8):	Moduł NIS(YP) NSS glibc
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n nss_nis
glibc NSS (Name Service Switch) module for NIS(YP) databases access.

%description -n nss_nis -l es.UTF-8
Módulo NSS de glibc para acceder las bases de datos NIS(YP).

%description -n nss_nis -l pl.UTF-8
Moduł glibc NSS (Name Service Switch) dostępu do baz danych NIS(YP).

%package -n nss_nisplus
Summary:	NIS+ NSS module
Summary(es.UTF-8):	Módulo NIS+ NSS
Summary(pl.UTF-8):	Moduł NIS+ NSS
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n nss_nisplus
glibc NSS (Name Service Switch) module for NIS+ databases access.

%description -n nss_nisplus -l es.UTF-8
Módulo NSS (Name Service Switch) de glibc para acceder las bases de
datos NIS+.

%description -n nss_nisplus -l pl.UTF-8
Moduł glibc NSS (Name Service Switch) dostępu do baz danych NIS+.

%package memusage
Summary:	A toy
Summary(es.UTF-8):	Un juguete
Summary(pl.UTF-8):	Zabawka
Group:		Applications
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description memusage
A toy.

%description memusage -l es.UTF-8
Un juguete.

%description memusage -l pl.UTF-8
Zabawka.

%package -n %{name}64
Summary:	GNU libc - 64-bit libraries
Summary(es.UTF-8):	GNU libc - bibliotecas de 64 bits
Summary(pl.UTF-8):	GNU libc - biblioteki 64-bitowe
Group:		Libraries
Requires(post):	ldconfig = %{epoch}:%{version}-%{release}
Requires:	%{name}-misc = %{epoch}:%{version}-%{release}
Requires:	basesystem
Provides:	glibc = %{epoch}:%{version}-%{release}
%{?with_tls:Provides:	glibc(tls)}
Obsoletes:	glibc-common
Obsoletes:	glibc-debug
Conflicts:	SysVinit < 2.86-11
Conflicts:	kernel < %{min_kernel}
Conflicts:	ld.so < 1.9.9-10
Conflicts:	man-pages < 1.43
Conflicts:	poldek < 0.18.8-4
Conflicts:	rc-scripts < 0.3.1-13
Conflicts:	rpm < 4.1

%description -n %{name}64
64-bit GNU libc libraries for 64bit architecture.

%description -n %{name}64 -l es.UTF-8
Bibliotecas GNU libc de 64 bits para la arquitectura 64bit.

%description -n %{name}64 -l pl.UTF-8
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
#%patch7 -p1 UPDATE/DROP (which kernels cause problems?)
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
#
# WARNING - disabling the glibc-pax_dl-execstack.patch will screw up PaX enabled machines.
#
%patch29 -p1
#
# ... and remember we will find you ;-)
#
%{?with_pax:%patch30 -p1}
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1
%patch40 -p1
%patch41 -p1
%patch42 -p1
%patch43 -p1
%patch44 -p1
%patch45 -p0
%patch46 -p1
%patch47 -p1

chmod +x scripts/cpp

# i786 (aka pentium4) hack
ln -s i686 nptl/sysdeps/i386/i786
ln -s i686 nptl/sysdeps/unix/sysv/linux/i386/i786

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
	%{?configure_cache:--cache-file=%{configure_cache_file:-%{buildroot}.configure.cache}-nptl.cache} \
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

%if %{without cross}
CC="%{__cc}"
diet ${CC#*ccache } %{SOURCE7} %{rpmcflags} -Os -static -o glibc-postinst
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

cp -p $PICFILES				$RPM_BUILD_ROOT%{_libdir}
cp -p elf/soinit.os				$RPM_BUILD_ROOT%{_libdir}/soinit.o
cp -p elf/sofini.os				$RPM_BUILD_ROOT%{_libdir}/sofini.o
cd ..

%if %{without cross}
%ifarch %{x8664} ppc64 s390x sparc64
install -p glibc-postinst				$RPM_BUILD_ROOT/sbin/glibc-postinst64
%else
install -p glibc-postinst				$RPM_BUILD_ROOT/sbin/glibc-postinst
%endif
%endif

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

for f in libc.so libpthread.so; do
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
cp -p linuxthreads/man/*.3thr		$RPM_BUILD_ROOT%{_mandir}/man3
%endif

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/localtime
# moved to tzdata package
rm -rf $RPM_BUILD_ROOT%{_datadir}/zoneinfo

%ifarch %{ix86} ppc s390 sparc sparcv9
mv $RPM_BUILD_ROOT%{_includedir}/gnu/stubs.h $RPM_BUILD_ROOT%{_includedir}/gnu/stubs-32.h
%endif

%ifarch %{x8664} ppc64 s390x sparc64
mv $RPM_BUILD_ROOT%{_includedir}/gnu/stubs.h $RPM_BUILD_ROOT%{_includedir}/gnu/stubs-64.h
%endif

%ifarch %{ix86} %{x8664} ppc ppc64 s390 s390x sparc sparcv9 sparc64
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
%endif

cp -p %{SOURCE8} $RPM_BUILD_ROOT%{_includedir}/sys/inotify.h

ln -sf libbsd-compat.a		$RPM_BUILD_ROOT%{_libdir}/libbsd.a

# make symlinks across top-level directories absolute
for l in anl BrokenLocale crypt dl m nsl resolv rt thread_db util ; do
	rm -f $RPM_BUILD_ROOT%{_libdir}/lib${l}.so
	ln -sf /%{_lib}/`cd $RPM_BUILD_ROOT/%{_lib} ; echo lib${l}.so.*` $RPM_BUILD_ROOT%{_libdir}/lib${l}.so
done

install -p %{SOURCE2}		$RPM_BUILD_ROOT/etc/rc.d/init.d/nscd
cp -p %{SOURCE3}		$RPM_BUILD_ROOT/etc/sysconfig/nscd
cp -p %{SOURCE4}		$RPM_BUILD_ROOT/etc/logrotate.d/nscd
cp -p nscd/nscd.conf	$RPM_BUILD_ROOT%{_sysconfdir}
cp -p nss/nsswitch.conf	$RPM_BUILD_ROOT%{_sysconfdir}

bzip2 -dc %{SOURCE5} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}
> $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.cache
install -d $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
echo 'include ld.so.conf.d/*.conf'> $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf
rm -f $RPM_BUILD_ROOT%{_mandir}/hu/man7/man.7

:> $RPM_BUILD_ROOT/var/log/nscd
:> $RPM_BUILD_ROOT/var/lib/nscd/passwd
:> $RPM_BUILD_ROOT/var/lib/nscd/group
:> $RPM_BUILD_ROOT/var/lib/nscd/hosts

rm -rf documentation
install -d documentation

%if %{with linuxthreads}
for f in ChangeLog Changes README ; do
	cp -pf linuxthreads/$f documentation/${f}.linuxthreads
done
%endif
%if %{with nptl}
for f in ANNOUNCE ChangeLog DESIGN-{barrier,condvar,rwlock,sem}.txt TODO{,-kernel,-testing} ;  do
	cp -pf nptl/$f documentation/${f}.nptl
done
%endif
cp -pf crypt/README.ufc-crypt documentation

cp -pf ChangeLog* documentation

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
# dv, haw, kok, ps (iso-codes)
# my (gaim)
# tk, ug, yo (used by GNOME)
#
# NOTES:
# bn is used for bn_BD or bn_IN? Assume bn_IN as nothing for bn_BD appeared
#   till now
#
# omitted here - already existing (with libc.mo):
#   be,ca,cs,da,de,el,en_GB,es,fi,fr,gl,hr,hu,it,ja,ko,nb,nl,pl,pt_BR,sk,sv,
#   tr,zh_CN,zh_TW
#
for i in aa af am ang ar az bg bn bn_IN br bs byn cy de_AT dz en en@boldquot \
    en@quot en_AU en_CA en_US eo es_AR es_MX es_NI et eu fa fo fr_BE fy ga \
    gez gu gv he hi hsb hy ia id is it_CH iu ka kk kl km kn ku kw ky leet lg li \
    lo lt lv mg mi mk ml mn mr ms mt nds ne nl_BE nn nso oc om or pa pt rm ro \
    ru rw sa se sid sl so sq sr sr@Latn sr@ije ss syr sw ta te tg th ti tig \
    tl tlh tt uk ur uz ve vi wa wal xh yi zh_HK zu ; do
	if [ ! -d $RPM_BUILD_ROOT%{_datadir}/locale/$i/LC_MESSAGES ]; then
		install -d $RPM_BUILD_ROOT%{_datadir}/locale/$i/LC_MESSAGES
		lang=`echo $i | sed -e 's/_.*//'`
		echo "%lang($lang) %{_datadir}/locale/$i" >> glibc.lang
	fi
done

# localedb-gen infrastructure
sed -e 's,@localedir@,%{_libdir}/locale,' %{SOURCE6} > $RPM_BUILD_ROOT%{_bindir}/localedb-gen
chmod +x $RPM_BUILD_ROOT%{_bindir}/localedb-gen
cp -p localedata/SUPPORTED $RPM_BUILD_ROOT%{_datadir}/i18n

# shutup check-files
rm -f $RPM_BUILD_ROOT%{_mandir}/README.*
rm -f $RPM_BUILD_ROOT%{_mandir}/diff.*
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
# we don't support kernel without ptys support
rm -f $RPM_BUILD_ROOT%{_libdir}/pt_chown

# stub for man page from man-pages package to make rpm consistency check happy
# don't package them here
install -d $RPM_BUILD_ROOT%{_mandir}{/,/ru,/es,/fr,/ja}/man2
:>$RPM_BUILD_ROOT%{_mandir}/man2/syslog.2
:>$RPM_BUILD_ROOT%{_mandir}/ru/man2/syslog.2
:>$RPM_BUILD_ROOT%{_mandir}/es/man2/syslog.2
:>$RPM_BUILD_ROOT%{_mandir}/fr/man2/syslog.2
:>$RPM_BUILD_ROOT%{_mandir}/ja/man2/syslog.2

# remove links to non existant translations
%{__rm} $RPM_BUILD_ROOT%{_mandir}/pl/man3/{alphasort,cfgetispeed,cfgetospeed,cfmakeraw,cfsetispeed,cfsetospeed,closelog,dn_comp,dn_expand,fscanf}.3
%{__rm} $RPM_BUILD_ROOT%{_mandir}/it/man7/latin2.7

%clean
rm -rf $RPM_BUILD_ROOT

# don't run iconvconfig in %%postun -n iconv because iconvconfig doesn't exist
# when %%postun is run

%if %{without cross}
%ifarch %{x8664} ppc64 s390x sparc64
%post	-n %{name}64 -p /sbin/postshell
%else
%post	-p /sbin/postshell
%endif
%ifarch %{x8664} ppc64 s390x sparc64
/sbin/glibc-postinst64 /%{_lib}/%{_host_cpu}
%else
/sbin/glibc-postinst /%{_lib}/%{_host_cpu}
%endif
/sbin/ldconfig

%ifarch %{x8664} ppc64 s390x sparc64
%postun	-n %{name}64 -p /sbin/postshell
%else
%postun	-p /sbin/postshell
%endif
/sbin/ldconfig

%ifarch %{x8664} ppc64 s390x sparc64
%triggerpostun -n %{name}64 -p /sbin/postshell -- glibc-misc < 6:2.3.4-0.20040505.1
%else
%triggerpostun -p /sbin/postshell -- glibc-misc < 6:2.3.4-0.20040505.1
%endif
-/bin/mv %{_sysconfdir}/ld.so.conf.rpmsave %{_sysconfdir}/ld.so.conf

%ifarch %{x8664} ppc64 s390x sparc64
%triggerpostun -n %{name}64 -p /sbin/postshell -- %{name}64 < 6:2.3.5-7.6
%else
%triggerpostun -p /sbin/postshell -- %{name} < 6:2.3.5-7.6
%endif
-/bin/cp -f /etc/ld.so.conf /etc/ld.so.conf.rpmsave
-/bin/sed -i -e '1iinclude ld.so.conf.d/*.conf' /etc/ld.so.conf
%endif

%post	memusage -p /sbin/ldconfig
%postun memusage -p /sbin/ldconfig

%post -n iconv -p %{_sbindir}/iconvconfig

%post -n localedb-src
SUPPORTED_LOCALES=
[ -f /etc/sysconfig/i18n ] && . /etc/sysconfig/i18n
[ -f /etc/sysconfig/localedb ] && . /etc/sysconfig/localedb
if [ "$SUPPORTED_LOCALES" ]; then
	localedb-gen || :
fi

%post devel	-p	/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun devel	-p	/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%pre -n nscd
%groupadd -P nscd -g 144 -r nscd
%useradd -P nscd -u 144 -r -d /tmp -s /bin/false -c "Name Service Cache Daemon" -g nscd nscd

%post -n nscd
/sbin/chkconfig --add nscd
touch /var/log/nscd
chmod 000 /var/log/nscd
chown root:root /var/log/nscd
chmod 640 /var/log/nscd
%service nscd restart "nscd daemon"

%preun -n nscd
if [ "$1" = "0" ]; then
	%service nscd stop
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
%if %{without cross}
%attr(755,root,root) /sbin/glibc-postinst*
%endif
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

#%files -n nss_dns
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libnss_dns*.so*

#%files -n nss_files
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libnss_files*.so*

%files -n ldconfig
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ld.so.conf
%dir %{_sysconfdir}/ld.so.conf.d
%ghost %{_sysconfdir}/ld.so.cache
%attr(755,root,root) /sbin/ldconfig

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
%lang(es) %{_mandir}/es/man1/ldd.1*
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
%lang(ko) %{_mandir}/ko/man1/ldd.1*
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
%lang(ru) %{_mandir}/ru/man1/getent.1*
%lang(ru) %{_mandir}/ru/man1/iconv.1*
%lang(ru) %{_mandir}/ru/man1/ldd.1*
%lang(ru) %{_mandir}/ru/man1/locale.1*
%lang(ru) %{_mandir}/ru/man1/rpcgen.1*
%lang(ru) %{_mandir}/ru/man5/locale.5*
%lang(ru) %{_mandir}/ru/man5/nsswitch.conf.5*
%lang(ru) %{_mandir}/ru/man5/tzfile.5*
%lang(ru) %{_mandir}/ru/man7/*
%lang(ru) %{_mandir}/ru/man8/ld*.8*
%lang(ru) %{_mandir}/ru/man8/rpcinfo.8*
%lang(ru) %{_mandir}/ru/man8/tzselect.8*
%lang(ru) %{_mandir}/ru/man8/zdump.8*
%lang(ru) %{_mandir}/ru/man8/zic.8*
%lang(tr) %{_mandir}/tr/man1/iconv.1*
%lang(tr) %{_mandir}/tr/man1/ldd.1*
%lang(zh_CN) %{_mandir}/zh_CN/man1/iconv.1*
%lang(zh_CN) %{_mandir}/zh_CN/man1/ldd.1*
%lang(zh_CN) %{_mandir}/zh_CN/man5/locale.5*
%lang(zh_CN) %{_mandir}/zh_CN/man5/tzfile.5*
%lang(zh_CN) %{_mandir}/zh_CN/man7/*
%lang(zh_CN) %{_mandir}/zh_CN/man8/tzselect.8*
%lang(zh_CN) %{_mandir}/zh_CN/man8/zdump.8*
%lang(zh_CN) %{_mandir}/zh_CN/man8/zic.8*

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

%ifarch %{ix86} %{x8664} ppc ppc64 s390 s390x sparc sparcv9 sparc64
%{_includedir}/gnu/stubs-*.h
%endif

%files headers
%defattr(644,root,root,755)
%{_includedir}/*.h
%ifarch alpha
%{_includedir}/alpha
%endif
%{_includedir}/arpa
%{_includedir}/bits
%dir %{_includedir}/gnu
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
%defattr(644,root,root,755)
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
%lang(ru) %{_mandir}/ru/man1/sprof.1*
%lang(ru) %{_mandir}/ru/man3/*
%lang(tr) %{_mandir}/tr/man3/*
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
%lang(es) %{_mandir}/es/man5/nscd.conf.5*
%lang(es) %{_mandir}/es/man8/nscd.8*
%lang(fr) %{_mandir}/fr/man5/nscd.conf.5*
%lang(fr) %{_mandir}/fr/man8/nscd.8*
%lang(ja) %{_mandir}/ja/man5/nscd.conf.5*
%lang(ja) %{_mandir}/ja/man8/nscd.8*
%lang(pt) %{_mandir}/pt/man5/nscd.conf.5*
%lang(pt) %{_mandir}/pt/man8/nscd.8*
%lang(ru) %{_mandir}/ru/man5/nscd.conf.5*
%lang(ru) %{_mandir}/ru/man8/nscd.8*
%lang(zh_CN) %{_mandir}/zh_CN/man5/nscd.conf.5*

%files -n localedb-src
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/localedef
%attr(755,root,root) %{_bindir}/localedb-gen
%{_datadir}/i18n
%{_mandir}/man1/localedef.1*
%lang(ru) %{_mandir}/ru/man1/localedef.1*

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
