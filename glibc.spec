# TODO:
# - restore --with-pkgversion when tcl upstream fixes the #3599098 (broken platform::identify).
# - --enable-systemtap
# - look at locale fixes/updates in bugzilla
# - no more chicken-egg problem (postshell is no more dynamically linked with libc), remove SONAME symlinks? see files section.
# [OLD]
# - localedb-gen man pages(?)
# - math/{test-fenv,test-tgmath,test-float,test-ifloat}, debug/backtrace-tst(SEGV)  fail on alpha
#
# Conditional build:
# min_kernel	(default is 3.4.0 except for x86/x86_64 where 2.6.32 suffices)
%bcond_without	memusage	# don't build memusage utility
%bcond_without	selinux		# without SELinux support (in nscd)
%bcond_with	tests		# perform "make test"
%bcond_without	localedb	# don't build localedb-all (is time consuming)
%bcond_with	cross		# make a cross build, skip native programs
%bcond_without	nss_crypt	# disable crypt features based on Mozilla NSS library
%bcond_with	bash_nls	# use bash NLS in shell scripts (ldd, sotruss); restores /bin/bash dep
#
%ifarch %{ix86} %{x8664}
%{!?min_kernel:%global		min_kernel	2.6.32} 
%else
%{!?min_kernel:%global		min_kernel	3.4.0}
%endif

%ifarch sparc64
%undefine	with_memusage
%endif

%define		core_version	2.25
%define		llh_version	7:2.6.32.1-1

Summary:	GNU libc
Summary(de.UTF-8):	GNU libc
Summary(es.UTF-8):	GNU libc
Summary(fr.UTF-8):	GNU libc
Summary(ja.UTF-8):	GNU libc ライブラリ
Summary(pl.UTF-8):	GNU libc
Summary(ru.UTF-8):	GNU libc версии
Summary(tr.UTF-8):	GNU libc
Summary(uk.UTF-8):	GNU libc версії
Name:		glibc
Version:	%{core_version}
Release:	3
Epoch:		6
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://ftp.gnu.org/gnu/glibc/%{name}-%{version}.tar.xz
# Source0-md5:	1496c3bf41adf9db0ebd0af01f202eed
Source2:	nscd.init
Source3:	nscd.sysconfig
Source4:	nscd.logrotate
# from man-pages.spec --with tars
Source5:	%{name}-man-pages.tar.xz
# Source5-md5:	78a8f7f8dfc63123f47a614e99136e61
Source6:	%{name}-localedb-gen
Source7:	%{name}-LD-path.c
Source9:	nscd.tmpfiles
# use branch.sh to update glibc-git.patch
Patch0:		glibc-git.patch
# Patch0-md5:	568e88daf4507caed4fe8ef7154788c6
# against GNU TP (libc domain)
#Patch1:		%{name}-pl.po-update.patch
Patch2:		%{name}-pld.patch
Patch3:		%{name}-crypt-blowfish.patch
Patch4:		%{name}-no-bash-nls.patch
Patch5:		%{name}-sparc-softfp-gcc.patch
Patch6:		%{name}-paths.patch

Patch8:		%{name}-missing-nls.patch
Patch9:		%{name}-nss_include_dirs.patch
Patch10:	%{name}-info.patch
Patch11:	%{name}-autoconf.patch

Patch14:	%{name}-sparc-errno_fix.patch
Patch15:	%{name}-new-charsets.patch
Patch16:	%{name}-tzfile-noassert.patch
# additions pending for upstream merge or taken from other distros
Patch17:	%{name}-morelocales.patch
# fixes mostly pending for upstream merge
Patch18:	%{name}-locale_fixes.patch
Patch19:	%{name}-ZA_collate.patch
Patch20:	%{name}-thread_start.patch

Patch23:	%{name}-pt_pax.patch

# http://pkgs.fedoraproject.org/cgit/rpms/glibc.git/plain/glibc-c-utf8-locale.patch
Patch27:	%{name}-c-utf8-locale.patch

Patch29:	%{name}-arm-alignment-fix.patch
Patch30:	glibc-rh1124987.patch

Patch38:	1055_all_glibc-resolv-dynamic.patch
URL:		http://www.gnu.org/software/libc/
%{?with_selinux:BuildRequires:	audit-libs-devel}
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake
%ifarch alpha
BuildRequires:	binutils >= 2:2.17.50.0.7
%else
BuildRequires:	binutils >= 2:2.15.90.0.3
%endif
%{!?with_cross:BuildRequires:	dietlibc-static}
BuildRequires:	gawk
BuildRequires:	gcc >= 6:4.7
%{?with_memusage:BuildRequires:	gd-devel >= 2.0.1}
BuildRequires:	gettext-tools >= 0.10.36
%{?with_selinux:BuildRequires:	libselinux-devel >= 1.18}
BuildRequires:	linux-libc-headers >= %{llh_version}
%{?with_nss_crypt:BuildRequires:	nss-devel >= 1:3.15.1-2}
BuildRequires:	perl-base
BuildRequires:	rpm-build >= 4.3-0.20030610.28
BuildRequires:	rpmbuild(macros) >= 1.567
BuildRequires:	sed >= 4.0.5
BuildRequires:	texinfo
Requires(post):	ldconfig = %{epoch}:%{version}-%{release}
Requires:	filesystem
Requires:	uname(release) >= %{min_kernel}
Provides:	%{name}(%{_target_cpu}) = %{epoch}:%{version}-%{release}
%ifarch %{ix86}
Provides:	%{name}(ix86) = %{epoch}:%{version}-%{release}
%endif
Provides:	glibc(nptl)
Provides:	glibc(tls)
Provides:	rtld(GNU_HASH)
Obsoletes:	glibc-common
Obsoletes:	glibc-debug
%ifarch %{x8664} sparc64 ppc64
Provides:	glibc64
Obsoletes:	glibc64
%endif
Suggests:	localedb
Suggests:	tzdata
Conflicts:	%{name}-misc < %{epoch}:%{version}-%{release}
Conflicts:	SysVinit < 2.86-11
Conflicts:	kernel < %{min_kernel}
Conflicts:	kernel24
Conflicts:	kernel24-smp
Conflicts:	ld.so < 1.9.9-10
Conflicts:	man-pages < 4.00
Conflicts:	poldek < 0.30.1-9
Conflicts:	rc-scripts < 0.3.1-13
Conflicts:	rpm < 4.1
Conflicts:	xorg-driver-video-nvidia-libs < 1:295.33
ExclusiveArch:	i486 i586 i686 pentium3 pentium4 athlon %{x8664} x32 ia64 alpha s390 s390x sparc sparc64 sparcv9 ppc ppc64 armv5tel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# avoid -s here (ld.so must not be stripped to allow any program debugging)
%define		filterout_ld		(-Wl,)?-[sS] (-Wl,)?--strip.*
# disable -D_FORTIFY_SOURCE=X and -fstack-protector
%define		_fortify_cflags		%{nil}
%define		_ssp_cflags		%{nil}

%define		specflags_sparcv9	-mcpu=ultrasparc -mvis -fcall-used-g6
%define		specflags_sparc64	-mcpu=ultrasparc -mvis -fcall-used-g6

# ld.so needs not to be stripped to work
# gdb needs unstripped libpthread for some threading support
# ...but we can strip at least debuginfo from them
%define		_autostripdebug		.*/ld-[0-9.]*so\\|.*/libpthread-[0-9.]*so

# -m from CFLAGS or even LDFLAGS is not propagated to some *.o linking
%ifarch sparc sparcv9
%{expand:%%define	__cc	%{__cc} -m32}
%endif

# Xen-friendly glibc
%define		specflags_ia32		-mno-tls-direct-seg-refs
%define		specflags_x86_64	-mno-tls-direct-seg-refs -fasynchronous-unwind-tables
%define		specflags_amd64		-mno-tls-direct-seg-refs -fasynchronous-unwind-tables
%define		specflags_ia32e		-mno-tls-direct-seg-refs

# we don't want perl dependency in glibc-devel
%define		_noautoreqfiles		%{_bindir}/mtrace
# hack: don't depend on rpmlib(PartialHardlinkSets) for easier upgrade from Ra
# (hardlinks here are unlikely to be "partial"... and rpm 4.0.2 from Ra was
# patched not to crash on partial hardlinks too)
%define		_hack_dontneed_PartialHardlinkSets	1
%define		_noautochrpath		.*\\(ldconfig\\|sln\\)
# private symbols
%define		_noautoprov		.*\(GLIBC_PRIVATE\)
%define		_noautoreq		.*\(GLIBC_PRIVATE\)

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

Pakiet jest przeznaczony dla jądra Linuksa >= %{min_kernel}.

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
%ifarch %{ix86}
Conflicts:	%{name}(x32)
Conflicts:	%{name}(x86_64)
%endif
Conflicts:	man-pages < 4.00

%description misc
Utilities and data used by glibc.

%description misc -l pl.UTF-8
Narzędzia i dane używane przez glibc.

%package libcrypt
Summary:	glibc library for crypt(3)
Summary(pl.UTF-8):	Biblioteka glibc z funkcją crypt(3)
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Provides:	%{name}-libcrypt(%{_target_cpu}) = %{epoch}:%{version}-%{release}
%ifarch %{ix86}
Provides:	%{name}-libcrypt(ix86) = %{epoch}:%{version}-%{release}
%endif
Provides:	crypt(blowfish)

%description libcrypt
glibc library for crypt(3).

%description libcrypt -l pl.UTF-8
Biblioteka glibc z funkcją crypt(3).

%package -n ldconfig
Summary:	Create shared library cache and maintains symlinks
Summary(de.UTF-8):	Erstellt ein shared library cache und verwaltet symlinks
Summary(fr.UTF-8):	Crée un cache de bibliothčque partagée et gčre *.so
Summary(pl.UTF-8):	Tworzenie cache'u bibliotek dynamicznych i ich dowiązań symbolicznych
Summary(tr.UTF-8):	Ortak kitaplýk önbelleđi yaratýr ve bađlantýlarý kurar
Group:		Applications/System
Requires:	uname(release) >= %{min_kernel}
# This is needed because previous package (glibc) had autoreq false and had
# provided this manually. Probably poldek bug that have to have it here.
Provides:	/sbin/ldconfig
# we want FHS being installed before ldconfig, altho they are both unrelated to each-other.
Requires:	FHS

%description -n ldconfig
ldconfig scans a running system and sets up the symbolic links that
are used to load shared libraries properly. It also creates
/etc/ld.so.cache which speeds the loading programs which use shared
libraries.

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

%description -n ldconfig -l pl.UTF-8
ldconfig testuje uruchomiony system i tworzy dowiązania symboliczne,
które są następnie używane do poprawnego ładowania bibliotek
dynamicznych. Program ten tworzy plik /etc/ld.so.cache, który
przyśpiesza ładowanie programów korzystających z bibliotek
dynamicznych.

%description -n ldconfig -l tr.UTF-8
ldconfig, çalýţmakta olan sistemi araţtýrýr ve ortak kitaplýklarýn
düzgün bir ţekilde yüklenmesi için gereken simgesel bađlantýlarý
kurar. Ayrýca ortak kitaplýklarý kullanan programlarýn yüklenmesini
hýzlandýran /etc/ld.so.cache dosyasýný yaratýr.

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

%package -n nss_db
Summary:	NSS glibc module that uses hashed key-value database
Summary(pl.UTF-8):	Moduł NSS glibc wykorzystujący haszowaną bazę danych klucz-wartość
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n nss_db
NSS glibc module that uses hashed key-value database.

%description -n nss_db -l pl.UTF-8
Moduł NSS glibc wykorzystujący haszowaną bazę danych klucz-wartość.

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
Summary:	Memory usage profiler
Summary(pl.UTF-8):	Narzędzie do profilowania zużycia pamięci
Group:		Development/Tools
Requires:	%{name} = %{epoch}:%{version}-%{release}
Conflicts:	man-pages < 4.00

%description memusage
Memory usage profiler.

%description memusage -l pl.UTF-8
Narzędzie do profilowania zużycia pamięci.

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
Requires:	%{name}-libcrypt(%{_target_cpu}) = %{epoch}:%{version}-%{release}
Provides:	%{name}-devel(%{_target_cpu}) = %{epoch}:%{version}-%{release}
%ifarch %{ix86}
Provides:	%{name}-devel(ix86) = %{epoch}:%{version}-%{release}
%endif
Obsoletes:	libiconv-devel
%ifarch %{x8664}
# see http://lists.pld-linux.org/mailman/pipermail/pld-devel-en/2016-May/024902.html
%if "%(rpm -q --qf '%{E}:%{V}' binutils)" >= "4:2.26"
Conflicts: binutils < 4:2.26
%endif
%endif

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
%ifarch %{ix86}
Provides:	%{name}-headers(ix86) = %{epoch}:%{version}-%{release}
%endif
%ifarch %{x8664} x32
# If both -m32 and -m64 is to be supported on x86_64, x86_64 package
# have to be installed, not ix86 one.
Obsoletes:	glibc-headers(athlon)
Obsoletes:	glibc-headers(i386)
Obsoletes:	glibc-headers(i486)
Obsoletes:	glibc-headers(i586)
Obsoletes:	glibc-headers(i686)
Obsoletes:	glibc-headers(ix86)
Obsoletes:	glibc-headers(pentium3)
Obsoletes:	glibc-headers(pentium4)
%endif
%ifarch x32
Obsoletes:	glibc-headers(x86_64)
%endif
%ifarch ppc64
Obsoletes:	glibc-headers(ppc)
%endif
%ifarch s390x
Obsoletes:	glibc-headers(s390)
%endif
%ifarch sparc64
Obsoletes:	glibc-headers(sparc)
%endif
Requires:	linux-libc-headers >= %{llh_version}

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
%ifarch %{ix86}
Provides:	%{name}-devel-utils(ix86) = %{epoch}:%{version}-%{release}
%endif
%ifarch %{x8664} x32
# If both -m32 and -m64 is to be supported on AMD64, x86_64 package
# have to be installed, not ix86 one.
Obsoletes:	glibc-devel-utils(athlon)
Obsoletes:	glibc-devel-utils(i386)
Obsoletes:	glibc-devel-utils(i486)
Obsoletes:	glibc-devel-utils(i586)
Obsoletes:	glibc-devel-utils(i686)
Obsoletes:	glibc-devel-utils(ix86)
Obsoletes:	glibc-devel-utils(pentium3)
Obsoletes:	glibc-devel-utils(pentium4)
%endif
%ifarch x32
Obsoletes:	glibc-devel-utils(x86_64)
%endif
%ifarch ppc64
Obsoletes:	glibc-devel-utils(ppc)
%endif
%ifarch s390x
Obsoletes:	glibc-devel-utils(s390)
%endif
%ifarch sparc64
Obsoletes:	glibc-devel-utils(sparc)
%endif
Conflicts:	man-pages < 4.00

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
Conflicts:	man-pages < 4.09
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
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

%package static
Summary:	Static GNU libc libraries
Summary(es.UTF-8):	Bibliotecas estáticas
Summary(pl.UTF-8):	Biblioteki statyczne GNU libc
Summary(ru.UTF-8):	Статические библиотеки glibc
Summary(uk.UTF-8):	Статичні бібліотеки glibc
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}
Provides:	%{name}-static(%{_target_cpu}) = %{epoch}:%{version}-%{release}
%ifarch %{ix86}
Provides:	%{name}-static(ix86) = %{epoch}:%{version}-%{release}
%endif
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

%package -n nscd
Summary:	Name Service Caching Daemon
Summary(es.UTF-8):	Demonio de caché del servicio de nombres
Summary(ja.UTF-8):	ネームサービスキャッシングデーモン (nacd)
Summary(pl.UTF-8):	Demon zapamiętujący odpowiedzi serwisów nazw
Summary(ru.UTF-8):	Кэширующий демон сервисов имен
Summary(uk.UTF-8):	Кешуючий демон севісів імен
License:	GPL v2
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
Requires:	rc-scripts >= 0.4.3.0
Provides:	group(nscd)
Provides:	user(nscd)
Obsoletes:	gnscd
Obsoletes:	unscd

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
Provides:	iconv(%{_target_base_arch})
Conflicts:	man-pages < 4.00

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

%prep
%setup -q

%if "%{min_kernel}" < "2.6.32"
echo "Minimal supported kernel is 2.6.32" >&2
exit 1
%endif

%patch0 -p1

%patch2 -p1
%patch3 -p0
%{!?with_bash_nls:%patch4 -p1}
%patch5 -p1
%patch6 -p1

%patch8 -p1
%patch9 -p0

%patch10 -p1
%patch11 -p1

%patch14 -p0
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1

%patch23 -p0

%patch27 -p1

%patch29 -p1
%patch30 -p1

%patch38 -p1

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

chmod +x scripts/cpp

%build
# glibc has its own way to remove PLT relocations. / H. J. Lu.
unset LD_SYMBOLIC_FUNCTIONS || :

cp -f /usr/share/automake/config.sub scripts
%{__aclocal}
%{__autoconf}

rm -rf builddir
install -d builddir
cd builddir
%ifarch sparc64
CC="%{__cc} -m64 -mcpu=ultrasparc -mvis -fcall-used-g6"
%endif

# force ld bfd (instead of gold)
install -d alt-tools
ln -sf %{_bindir}/ld.bfd alt-tools/ld
PATH=$(pwd)/alt-tools:$PATH; export PATH

AWK="gawk" \
../%configure \
	--enable-add-ons=libidn \
	--enable-bind-now \
	--enable-experimental-malloc \
	--enable-hidden-plt \
	--enable-kernel="%{min_kernel}" \
	--enable-nss-crypt%{!?with_nss_crypt:=no} \
	--enable-obsolete-rpc \
	--enable-profile \
	--enable-stack-protector=strong \
	--enable-stackguard-randomization \
	--enable-tunables \
	--with-binutils=$(pwd)/alt-tools \
	--with-bugurl=http://bugs.pld-linux.org/ \
	--with-headers=%{_includedir} \
	--with-selinux%{!?with_selinux:=no} \
	--with-tls

%{__make} \
	AWK="gawk" \
	complocaledir=%{_prefix}/lib/locale \
	sLIBdir=%{_libdir}

cd ..

%if %{with tests}
env LANGUAGE=C LC_ALL=C \
%{__make} -j1 -C builddir tests
%endif

%if %{without cross}
CC="%{__cc}"
CC=${CC#*ccache }
CC=${CC#%{_libdir}/ccache/}
diet ${CC} %{SOURCE7} %{rpmcflags} -Os -static -o glibc-postinst
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig,default,logrotate.d} \
	$RPM_BUILD_ROOT{%{_mandir},/var/log,/var/{lib,run}/nscd} \
	$RPM_BUILD_ROOT{/var/cache/ldconfig,%{systemdtmpfilesdir}}

cd builddir
env LANGUAGE=C LC_ALL=C \
%{__make} install \
	install_root=$RPM_BUILD_ROOT \
	complocaledir=%{_prefix}/lib/locale \
	infodir=%{_infodir} \
	mandir=%{_mandir}

%if %{with localedb}
env LANGUAGE=C LC_ALL=C \
%{__make} localedata/install-locales \
	complocaledir=%{_prefix}/lib/locale \
	install_root=$RPM_BUILD_ROOT
%else
install -d $RPM_BUILD_ROOT%{_prefix}/lib/locale
%endif

PICFILES="libc_pic.a libc.map
	math/libm_pic.a libm.map
	resolv/libresolv_pic.a"

install -p $PICFILES				$RPM_BUILD_ROOT%{_libdir}
install -p elf/soinit.os				$RPM_BUILD_ROOT%{_libdir}/soinit.o
install -p elf/sofini.os				$RPM_BUILD_ROOT%{_libdir}/sofini.o

# Include %{_libdir}/gconv/gconv-modules.cache
$(pwd)/elf/ld.so --library-path $(pwd) ./iconv/iconvconfig --nostdlib --prefix=$RPM_BUILD_ROOT %{_libdir}/gconv -o $RPM_BUILD_ROOT%{_libdir}/gconv/gconv-modules.cache
cd ..

%if %{without cross}
install -p glibc-postinst				$RPM_BUILD_ROOT/sbin
%endif

%{?with_memusage:mv -f $RPM_BUILD_ROOT/%{_lib}/libmemusage.so $RPM_BUILD_ROOT%{_libdir}}
mv -f $RPM_BUILD_ROOT/%{_lib}/libpcprofile.so	$RPM_BUILD_ROOT%{_libdir}

# make symlinks across top-level directories absolute
for l in BrokenLocale anl cidn crypt dl \
%ifarch %{x8664} x32
	mvec \
%endif
	nsl resolv rt thread_db util; do
	test -L $RPM_BUILD_ROOT%{_libdir}/lib${l}.so || exit 1
	%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib${l}.so
	ln -sf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/lib${l}.so.*) $RPM_BUILD_ROOT%{_libdir}/lib${l}.so
done

# linking nss modules directly is not supported
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libnss_*.so

install -p %{SOURCE2}		$RPM_BUILD_ROOT/etc/rc.d/init.d/nscd
cp -a %{SOURCE3}		$RPM_BUILD_ROOT/etc/sysconfig/nscd
cp -a %{SOURCE4}		$RPM_BUILD_ROOT/etc/logrotate.d/nscd
cp -a nscd/nscd.conf		$RPM_BUILD_ROOT%{_sysconfdir}
cp -a posix/gai.conf		$RPM_BUILD_ROOT%{_sysconfdir}
cp -a nis/nss $RPM_BUILD_ROOT/etc/default/nss
sed -e 's#\([ \t]\)db\([ \t]\)#\1#g' nss/nsswitch.conf > $RPM_BUILD_ROOT%{_sysconfdir}/nsswitch.conf

xz -dc %{SOURCE5} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}
: > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.cache
install -d $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
echo 'include ld.so.conf.d/*.conf' > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf
: > $RPM_BUILD_ROOT/var/cache/ldconfig/aux-cache

# doesn't fit with out tzdata concept and configure.in is stupid assuming bash
# is first posix compatible shell making this script depend on bash.
%{__rm} $RPM_BUILD_ROOT%{_bindir}/tzselect
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man8/tzselect.8*
%{__rm} $RPM_BUILD_ROOT%{_mandir}/*/man8/tzselect.8*

: > $RPM_BUILD_ROOT/var/log/nscd
: > $RPM_BUILD_ROOT/var/lib/nscd/passwd
: > $RPM_BUILD_ROOT/var/lib/nscd/group
: > $RPM_BUILD_ROOT/var/lib/nscd/hosts

cp -p %{SOURCE9} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/nscd.conf

rm -rf documentation
install -d documentation

for f in ChangeLog.old DESIGN-systemtap-probes.txt TODO{,-kernel,-testing}; do
	cp -af nptl/$f documentation/$f.nptl
done
cp -af crypt/README.ufc-crypt ChangeLog* documentation

# Collect locale files and mark them with %%lang()
echo '%defattr(644,root,root,755)' > glibc.lang
for i in $RPM_BUILD_ROOT%{_localedir}/*; do
	if [ -d $i ]; then
		lang=$(basename $i)
		dir="${i#$RPM_BUILD_ROOT}"
		echo "%lang($lang) $dir" >> glibc.lang
	fi
done

# NOTES:
# Languages not supported by glibc locales, but usable via $LANGUAGE:
#   ang - Old English (gtk+, gnome)
#   ca@valencia (gtk+, gnome; as ca_ES@valencia in FileZilla; locale exists in Debian)
#   en@shaw - English with Shavian alphabet (gnome)
#   la - Latin
#   tlh - Klingon (bzflag)
#
# To be added when they become supported by glibc:
#   ach    (vlc, libreport)
#   aln    (vlc, libreport)
#   bal    (libosinfo, libreport, newt, pessulus)
#   cgg    (vlc)
#   co     (FileZilla, vlc)
#   frp    (xfce, lxlauncher, mate)
#   gn     (gn_BR in gnome, maybe gn_PY)
#   guc    (gtk-vnc)
#   haw    (iso-codes, stellarium)
#   hrx    (stellarium)
#   ilo    (kudzu, libosinfo, libreport)
#   io     (gtk+2, gnome, alacarte)
#   jv     (gmpc, avant-window-navigator, kdesudo, mate)
#   kab    (FileZilla)
#   kmr    (vlc)
#   ku_IQ  (mate)
#   kw@kkcor, kw@uccor (libosinfo - currently empty) - add as supported variants when non-empty?
#   man    (ccsm; incorrectly named md)
#   mus    (bluez-gnome)
#   nah    (mate)
#   nqo	   (mate)
#   pms    (deluge, mate-tweak)
#   sco    (gnomad2, picard, stellarium, mate)
#   son    (gtkspell3)
#   su     (terminator)
#   swg    (sim)
#   syr    (iso-codes)
#   tet    (vlc)
#   tpi    (mate-tweak)
#   tw     (libosinfo)
#   vec    (mate-applet-indicator)
#   wba    (libosinfo)
#
# To be removed (after fixing packages still using it):
#   sr@Latn (use sr@latin instead)
#   sr@ije (use sr@ijekavian instead)
#
# Short forms (omitted country code, used instead of long form) for ambiguous or unclear cases:
# aa=aa_ER
# ak=ak_GH
# anp=anp_IN
# ar=common? (AE, BH, DZ, EG, IQ, JO, KW, LB, LY, MA, OM, QA, SA, SD, SY, TN, YE)
# az=az_AZ
# bn=bn_BD
# bo=bo_CN? (or common for CN, IN?)
# ca=ca_ES
# ckb=ckb_IQ
# cv=cv_RU
# de=de_DE
# en=common? (en_AU, en_CA, en_GB, en_NZ, en_US are used for particular variants)
# eo=common
# es=es_ES
# eu=eu_ES
# fa=fa_IR
# ff=ff_SN
# fr=fr_FR
# fy=fy_NL
# gez=gez_ET (?)
# it=it_IT
# ku=ku_TR
# li=li_NL
# ln=ln_CD
# lo=lo_LA
# nds=nds_DE
# nl=nl_NL
# om=om_ET
# or=or_IN
# pa=pa_IN
# pt=pt_PT
# quz=quz_PE
# ru=ru_RU
# sd=sd_IN
# shn=shn_MM
# so=so_SO
# sr=sr_RS [cyrillic]
# sr@latin=sr_RS@latin
# sr@ijekavian=sr_BA@ijekavian
# sr@ijekavianlatin=sr_BA@ijekavianlatin
# sv=sv_SE
# sw=sw_TZ (or common for KE, TZ, UG?)
# ta=ta_IN
# te=te_IN
# ti=ti_ER (?)
# tr=tr_TR
# ur=ur_PK (?)
# zh: no short code used (use zh_CN, zh_HK, zh_SG[not included yet], zh_TW)
#
# Omitted here - already existing (with libc.mo):
#   be ca cs da de el en_GB es fi fr gl hr hu it ja ko nb nl pl pt_BR ru rw sk
#   sv tr zh_CN zh_TW
#
for i in aa aa@saaho af ak am an ang anp ar ar_TN as ast az az_IR be@latin be@tarask bem \
	bg bho bn bn_IN bo br brx bs byn ca@valencia ckb cmn crh csb cv cy de_AT de_CH doi dv dz en \
	en@boldquot en@quot en@shaw en_AU en_CA en_NZ en_US eo es_AR es_CL es_CO es_CR \
	es_DO es_EC es_GT es_HN es_MX es_NI es_PA es_PE es_PR es_SV es_UY \
	es_VE et eu fa ff fil fo fr_BE fr_CA fr_CH fur fy ga gd gez gu gv ha he \
	hi hne hsb hy ia id ig ik is it_CH iu ka kg kk kl km kn kok ks ku kw ky la lb \
	lg li ln lo lt lv mai mg mhr mi mk ml mn mni mr ms mt my nds ne nl_BE nn nr nso \
	oc om or pa pap ps pt ps quz rm ro sa sat sc sd se shn si sid sl so sq sr sr@Latn szl tl \
	sr@ije sr@ijekavian sr@ijekavianlatin sr@latin ss st sw ta te tg th ti \
	tig tk tl tlh tn ts tt tt@iqtelif ug uk ur uz uz@cyrillic ve vi wa wal wo xh yi yo \
	zh_HK zu; do
	if [ ! -d $RPM_BUILD_ROOT%{_localedir}/$i/LC_MESSAGES ]; then
		install -d $RPM_BUILD_ROOT%{_localedir}/$i/LC_MESSAGES
		# use lang() tags with ll_CC@variant (stripping charset and @quot|@boldquot)
		lang=$(echo $i | sed -e 's/@quot\>\|@boldquot\>//')
		echo "%lang($lang) %{_localedir}/$i" >> glibc.lang
	fi
done

# LC_TIME category, used for localized date formats (at least by coreutils)
for i in af be bg ca cs da de el en eo es et eu fi fr ga gl hr hu ia id it ja kk ko lg lt \
	ms nb nl pl pt pt_BR ro ru rw sk sl sr sv tr uk vi zh_CN zh_TW; do
	if [ ! -d $RPM_BUILD_ROOT%{_localedir}/$i ]; then
		echo "%lang($lang) %{_localedir}/$i" >> glibc.lang
	fi
	install -d $RPM_BUILD_ROOT%{_localedir}/$i/LC_TIME
done

# localedb-gen infrastructure
install -p %{SOURCE6} $RPM_BUILD_ROOT%{_bindir}/localedb-gen
cp -p localedata/SUPPORTED $RPM_BUILD_ROOT%{_datadir}/i18n

# shutup check-files
%{__rm} $RPM_BUILD_ROOT%{_mandir}/README.*
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

# stub for man page from man-pages package to make rpm consistency check happy
# don't package them here
install -d $RPM_BUILD_ROOT%{_mandir}{,/ru,/es,/fr,/ja}/man2
:>$RPM_BUILD_ROOT%{_mandir}/man2/syslog.2
:>$RPM_BUILD_ROOT%{_mandir}/ru/man2/syslog.2
:>$RPM_BUILD_ROOT%{_mandir}/es/man2/syslog.2
:>$RPM_BUILD_ROOT%{_mandir}/fr/man2/syslog.2
:>$RPM_BUILD_ROOT%{_mandir}/ja/man2/syslog.2

# remove links to non existant translations
%{__rm} $RPM_BUILD_ROOT%{_mandir}/pl/man3/{alphasort,cfgetispeed,cfgetospeed,cfmakeraw,cfsetispeed,cfsetospeed,closelog,dn_comp,dn_expand,fscanf}.3
%{__rm} $RPM_BUILD_ROOT%{_mandir}/tr/man3/{encrypt_r,setkey,setkey_r}.3

%clean
rm -rf $RPM_BUILD_ROOT

%if %{without cross}
%post	-p /sbin/postshell
/sbin/glibc-postinst /%{_lib}/%{_host_cpu} /%{_lib}/tls
/sbin/ldconfig

%postun	-p /sbin/ldconfig

%triggerpostun -p /sbin/postshell -- glibc-misc < 6:2.3.5-7.6
-/bin/cp -f /etc/ld.so.conf /etc/ld.so.conf.rpmsave
-/bin/sed -i -e '1iinclude ld.so.conf.d/*.conf' /etc/ld.so.conf
%endif

%triggerin -- cronie,vixie-cron,hc-cron,fcron,mcron
# restart crond if glibc is upgraded, LP#721338
if [ "$1" != 1 ]; then
	%service -q crond restart
fi

%triggerin -- apache-base
if [ "$1" != 1 ]; then
	%service -q httpd restart
fi

%ifarch %{x8664}
# when upgrading from glibc < 6:2.19-3 copy locale-archive
# from /usr/lib64/locale to /usr/lib/locale
# but only if the latter doesn't already exist
%triggerpostun -p /sbin/postshell -- %{name} < 6:2.19-3
-/bin/cp -an %{_libdir}/locale/locale-archive %{_prefix}/lib/locale/locale-archive
%endif

%post	libcrypt -p /sbin/ldconfig
%postun	libcrypt -p /sbin/ldconfig

%post	memusage -p /sbin/ldconfig
%postun	memusage -p /sbin/ldconfig

%post -n localedb-src
SUPPORTED_LOCALES=
[ -f /etc/sysconfig/i18n ] && . /etc/sysconfig/i18n
[ -f /etc/sysconfig/localedb ] && . /etc/sysconfig/localedb
if [ "$SUPPORTED_LOCALES" ]; then
	localedb-gen || :
fi

%post devel-doc	-p	/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun devel-doc	-p	/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%pre -n nscd
%groupadd -P nscd -g 144 -r nscd
%useradd -P nscd -u 144 -r -d /tmp -s /bin/false -c "Name Service Cache Daemon" -g nscd nscd

%post -n nscd
if [ ! -f /var/log/nscd ]; then
	umask 027
	touch /var/log/nscd
	chown root:root /var/log/nscd
	chmod 640 /var/log/nscd
fi
/sbin/chkconfig --add nscd
%service nscd restart "Name Service Cache Daemon"

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

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README NEWS BUGS CONFORMANCE
%if %{without cross}
%attr(755,root,root) /sbin/glibc-postinst
%endif
# TODO: package ldconfig symlinks as %ghost
%attr(755,root,root) /%{_lib}/ld-%{core_version}.so
# wildly arch-dependent ld.so SONAME symlink
%ifarch %{ix86} sparc sparcv9 sparc64 alpha sh
%attr(755,root,root) /%{_lib}/ld-linux.so.2
%endif
%ifarch ia64
%attr(755,root,root) /%{_lib}/ld-linux-ia64.so.2
%endif
%ifarch %{x8664}
%attr(755,root,root) /%{_lib}/ld-linux-x86-64.so.2
%endif
%ifarch x32
%attr(755,root,root) /%{_lib}/ld-linux-x32.so.2
%endif
%ifarch ppc64 s390x
%attr(755,root,root) /%{_lib}/ld64.so.1
%endif
%ifnarch %{ix86} sparc sparcv9 sparc64 alpha sh ia64 %{x8664} x32 ppc64 s390x %{arm}
%attr(755,root,root) /%{_lib}/ld.so.1
%endif
%attr(755,root,root) /%{_lib}/libBrokenLocale-%{core_version}.so
%ifarch alpha
%attr(755,root,root) /%{_lib}/libBrokenLocale.so.1.1
%else
%attr(755,root,root) /%{_lib}/libBrokenLocale.so.1
%endif
%attr(755,root,root) /%{_lib}/libSegFault.so
%attr(755,root,root) /%{_lib}/libanl-%{core_version}.so
%attr(755,root,root) /%{_lib}/libanl.so.1
%attr(755,root,root) /%{_lib}/libc-%{core_version}.so
%ifarch alpha ia64
%attr(755,root,root) /%{_lib}/libc.so.6.1
%else
%attr(755,root,root) /%{_lib}/libc.so.6
%endif
%attr(755,root,root) /%{_lib}/libcidn-%{core_version}.so
%attr(755,root,root) /%{_lib}/libcidn.so.1
%attr(755,root,root) /%{_lib}/libdl-%{core_version}.so
%ifarch alpha
%attr(755,root,root) /%{_lib}/libdl.so.2.1
%else
%attr(755,root,root) /%{_lib}/libdl.so.2
%endif
%attr(755,root,root) /%{_lib}/libm-%{core_version}.so
%ifarch alpha ia64
%attr(755,root,root) /%{_lib}/libm.so.6.1
%else
%attr(755,root,root) /%{_lib}/libm.so.6
%endif
%ifarch %{x8664} x32
%attr(755,root,root) /%{_lib}/libmvec-%{core_version}.so
%attr(755,root,root) /%{_lib}/libmvec.so.1
%endif
%attr(755,root,root) /%{_lib}/libnsl-%{core_version}.so
%ifarch alpha
%attr(755,root,root) /%{_lib}/libnsl.so.1.1
%else
%attr(755,root,root) /%{_lib}/libnsl.so.1
%endif
%attr(755,root,root) /%{_lib}/libpthread-%{core_version}.so
%attr(755,root,root) /%{_lib}/libpthread.so.0
%attr(755,root,root) /%{_lib}/libresolv-%{core_version}.so
%ifarch alpha
%attr(755,root,root) /%{_lib}/libresolv.so.2.1
%else
%attr(755,root,root) /%{_lib}/libresolv.so.2
%endif
%attr(755,root,root) /%{_lib}/librt-%{core_version}.so
%attr(755,root,root) /%{_lib}/librt.so.1
%attr(755,root,root) /%{_lib}/libthread_db-1.0.so
%attr(755,root,root) /%{_lib}/libthread_db.so.1
%attr(755,root,root) /%{_lib}/libutil-%{core_version}.so
%ifarch alpha
%attr(755,root,root) /%{_lib}/libutil.so.1.1
%else
%attr(755,root,root) /%{_lib}/libutil.so.1
%endif
%dir %{_prefix}/lib/locale

#%files -n nss_dns
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libnss_dns-%{core_version}.so
%attr(755,root,root) /%{_lib}/libnss_dns.so.2

#%files -n nss_files
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libnss_files-%{core_version}.so
%attr(755,root,root) /%{_lib}/libnss_files.so.2

%defattr(644,root,root,755)

%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nsswitch.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/gai.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/default/nss

%config %{_sysconfdir}/rpc

%attr(755,root,root) /sbin/sln
%attr(755,root,root) %{_bindir}/getconf
%attr(755,root,root) %{_bindir}/getent
%attr(755,root,root) %{_bindir}/iconv
%attr(755,root,root) %{_bindir}/locale
%attr(755,root,root) %{_bindir}/rpcgen
%attr(755,root,root) %{_sbindir}/zdump
%attr(755,root,root) %{_sbindir}/zic

%dir %{_libexecdir}/getconf
%attr(755,root,root) %{_libexecdir}/getconf/*

%dir %{_localedir}
%{_localedir}/locale.alias

%{_mandir}/man1/getconf.1*
%{_mandir}/man1/getent.1*
%{_mandir}/man1/iconv.1*
%{_mandir}/man1/locale.1*
%{_mandir}/man1/rpcgen.1*
%{_mandir}/man5/gai.conf.5*
%{_mandir}/man5/locale.5*
%{_mandir}/man5/nss.5*
%{_mandir}/man5/nsswitch.conf.5*
%{_mandir}/man5/repertoiremap.5*
%{_mandir}/man5/rpc.5*
%{_mandir}/man5/tzfile.5*
%{_mandir}/man7/armscii-8.7*
%{_mandir}/man7/ascii.7*
%{_mandir}/man7/charsets.7*
%{_mandir}/man7/cp1251.7*
%{_mandir}/man7/cp1252.7*
%{_mandir}/man7/iso-8859-*.7*
%{_mandir}/man7/iso_8859-*.7*
%{_mandir}/man7/iso_8859_*.7*
%{_mandir}/man7/koi8-*.7*
%{_mandir}/man7/latin*.7*
%{_mandir}/man7/locale.7*
%{_mandir}/man7/tis-620.7*
%{_mandir}/man7/unicode.7*
%{_mandir}/man7/utf-8.7*
%{_mandir}/man7/utf8.7*
%{_mandir}/man8/ld-linux.8*
%{_mandir}/man8/ld-linux.so.8*
%{_mandir}/man8/ld.so.8*
%{_mandir}/man8/sln.8*
%{_mandir}/man8/zdump.8*
%{_mandir}/man8/zic.8*
%lang(cs) %{_mandir}/cs/man7/ascii.7*
%lang(cs) %{_mandir}/cs/man7/locale.7*
%lang(cs) %{_mandir}/cs/man7/unicode.7*
%lang(cs) %{_mandir}/cs/man7/utf-8.7*
%lang(cs) %{_mandir}/cs/man7/utf8.7*
%lang(de) %{_mandir}/de/man5/rpc.5*
%lang(de) %{_mandir}/de/man5/tzfile.5*
%lang(de) %{_mandir}/de/man7/ascii.7*
%lang(de) %{_mandir}/de/man7/iso-8859-*.7*
%lang(de) %{_mandir}/de/man7/iso_8859-*.7*
%lang(de) %{_mandir}/de/man7/iso_8859_*.7*
%lang(de) %{_mandir}/de/man7/latin*.7*
%lang(de) %{_mandir}/de/man7/locale.7*
%lang(de) %{_mandir}/de/man7/unicode.7*
%lang(de) %{_mandir}/de/man7/utf-8.7*
%lang(de) %{_mandir}/de/man7/utf8.7*
%lang(es) %{_mandir}/es/man5/locale.5*
%lang(es) %{_mandir}/es/man5/nsswitch.conf.5*
%lang(es) %{_mandir}/es/man5/rpc.5*
%lang(es) %{_mandir}/es/man5/tzfile.5*
%lang(es) %{_mandir}/es/man7/ascii.7*
%lang(es) %{_mandir}/es/man7/charsets.7*
%lang(es) %{_mandir}/es/man7/iso-8859-*.7*
%lang(es) %{_mandir}/es/man7/iso_8859-*.7*
%lang(es) %{_mandir}/es/man7/iso_8859_*.7*
%lang(es) %{_mandir}/es/man7/latin*.7*
%lang(es) %{_mandir}/es/man7/locale.7*
%lang(es) %{_mandir}/es/man7/unicode.7*
%lang(es) %{_mandir}/es/man7/utf-8.7*
%lang(es) %{_mandir}/es/man7/utf8.7*
%lang(es) %{_mandir}/es/man8/ld-linux.8*
%lang(es) %{_mandir}/es/man8/ld-linux.so.8*
%lang(es) %{_mandir}/es/man8/ld.so.8*
%lang(es) %{_mandir}/es/man8/zdump.8*
%lang(es) %{_mandir}/es/man8/zic.8*
%lang(fr) %{_mandir}/fr/man5/locale.5*
%lang(fr) %{_mandir}/fr/man5/nsswitch.conf.5*
%lang(fr) %{_mandir}/fr/man5/rpc.5*
%lang(fr) %{_mandir}/fr/man5/tzfile.5*
%lang(fr) %{_mandir}/fr/man7/ascii.7*
%lang(fr) %{_mandir}/fr/man7/charsets.7*
%lang(fr) %{_mandir}/fr/man7/iso-8859-*.7*
%lang(fr) %{_mandir}/fr/man7/iso_8859-*.7*
%lang(fr) %{_mandir}/fr/man7/iso_8859_*.7*
%lang(fr) %{_mandir}/fr/man7/koi8-r.7*
%lang(fr) %{_mandir}/fr/man7/latin*.7*
%lang(fr) %{_mandir}/fr/man7/locale.7*
%lang(fr) %{_mandir}/fr/man7/unicode.7*
%lang(fr) %{_mandir}/fr/man7/utf-8.7*
%lang(fr) %{_mandir}/fr/man7/utf8.7*
%lang(fr) %{_mandir}/fr/man8/ld-linux.8*
%lang(fr) %{_mandir}/fr/man8/ld-linux.so.8*
%lang(fr) %{_mandir}/fr/man8/ld.so.8*
%lang(fr) %{_mandir}/fr/man8/zdump.8*
%lang(fr) %{_mandir}/fr/man8/zic.8*
%lang(hu) %{_mandir}/hu/man7/ascii.7*
%lang(hu) %{_mandir}/hu/man7/iso-8859-*.7*
%lang(hu) %{_mandir}/hu/man7/iso_8859-*.7*
%lang(hu) %{_mandir}/hu/man7/iso_8859_*.7*
%lang(hu) %{_mandir}/hu/man7/latin*.7*
%lang(hu) %{_mandir}/hu/man7/locale.7*
%lang(hu) %{_mandir}/hu/man7/utf-8.7*
%lang(hu) %{_mandir}/hu/man7/utf8.7*
%lang(hu) %{_mandir}/hu/man8/ld-linux.8*
%lang(hu) %{_mandir}/hu/man8/ld-linux.so.8*
%lang(hu) %{_mandir}/hu/man8/ld.so.8*
%lang(hu) %{_mandir}/hu/man8/zdump.8*
%lang(it) %{_mandir}/it/man5/locale.5*
%lang(it) %{_mandir}/it/man7/ascii.7*
%lang(it) %{_mandir}/it/man7/charsets.7*
%lang(it) %{_mandir}/it/man7/iso-8859-*.7*
%lang(it) %{_mandir}/it/man7/iso_8859-*.7*
%lang(it) %{_mandir}/it/man7/iso_8859_*.7*
%lang(it) %{_mandir}/it/man7/latin*.7*
%lang(it) %{_mandir}/it/man7/locale.7*
%lang(it) %{_mandir}/it/man7/unicode.7*
%lang(it) %{_mandir}/it/man7/utf-8.7*
%lang(it) %{_mandir}/it/man7/utf8.7*
%lang(it) %{_mandir}/it/man8/zdump.8*
%lang(ja) %{_mandir}/ja/man1/getent.1*
%lang(ja) %{_mandir}/ja/man1/iconv.1*
%lang(ja) %{_mandir}/ja/man1/locale.1*
%lang(ja) %{_mandir}/ja/man1/rpcgen.1*
%lang(ja) %{_mandir}/ja/man5/gai.conf.5*
%lang(ja) %{_mandir}/ja/man5/locale.5*
%lang(ja) %{_mandir}/ja/man5/nss.5*
%lang(ja) %{_mandir}/ja/man5/nsswitch.conf.5*
%lang(ja) %{_mandir}/ja/man5/repertoiremap.5*
%lang(ja) %{_mandir}/ja/man5/rpc.5*
%lang(ja) %{_mandir}/ja/man5/tzfile.5*
%lang(ja) %{_mandir}/ja/man7/armscii-8.7*
%lang(ja) %{_mandir}/ja/man7/ascii.7*
%lang(ja) %{_mandir}/ja/man7/charsets.7*
%lang(ja) %{_mandir}/ja/man7/cp1251.7*
%lang(ja) %{_mandir}/ja/man7/cp1252.7*
%lang(ja) %{_mandir}/ja/man7/iso-8859-*.7*
%lang(ja) %{_mandir}/ja/man7/iso_8859-*.7*
%lang(ja) %{_mandir}/ja/man7/iso_8859_*.7*
%lang(ja) %{_mandir}/ja/man7/koi8-*.7*
%lang(ja) %{_mandir}/ja/man7/latin*.7*
%lang(ja) %{_mandir}/ja/man7/locale.7*
%lang(ja) %{_mandir}/ja/man7/tis-620.7*
%lang(ja) %{_mandir}/ja/man7/unicode.7*
%lang(ja) %{_mandir}/ja/man7/utf-8.7*
%lang(ja) %{_mandir}/ja/man7/utf8.7*
%lang(ja) %{_mandir}/ja/man8/ld-linux.8*
%lang(ja) %{_mandir}/ja/man8/ld-linux.so.8*
%lang(ja) %{_mandir}/ja/man8/ld.so.8*
%lang(ja) %{_mandir}/ja/man8/sln.8*
%lang(ja) %{_mandir}/ja/man8/zdump.8*
%lang(ja) %{_mandir}/ja/man8/zic.8*
%lang(ko) %{_mandir}/ko/man5/nsswitch.conf.5*
%lang(ko) %{_mandir}/ko/man5/rpc.5*
%lang(ko) %{_mandir}/ko/man5/tzfile.5*
%lang(ko) %{_mandir}/ko/man7/ascii.7*
%lang(ko) %{_mandir}/ko/man7/iso-8859-*.7*
%lang(ko) %{_mandir}/ko/man7/iso_8859-*.7*
%lang(ko) %{_mandir}/ko/man7/iso_8859_*.7*
%lang(ko) %{_mandir}/ko/man7/latin*.7*
%lang(ko) %{_mandir}/ko/man8/zdump.8*
%lang(pl) %{_mandir}/pl/man5/locale.5*
%lang(pl) %{_mandir}/pl/man5/rpc.5*
%lang(pl) %{_mandir}/pl/man7/ascii.7*
%lang(pl) %{_mandir}/pl/man7/iso-8859-*.7*
%lang(pl) %{_mandir}/pl/man7/iso_8859-*.7*
%lang(pl) %{_mandir}/pl/man7/iso_8859_*.7*
%lang(pl) %{_mandir}/pl/man7/koi8-*.7*
%lang(pl) %{_mandir}/pl/man7/latin*.7*
%lang(pl) %{_mandir}/pl/man7/locale.7*
%lang(pl) %{_mandir}/pl/man7/unicode.7*
%lang(pl) %{_mandir}/pl/man7/utf-8.7*
%lang(pl) %{_mandir}/pl/man7/utf8.7*
%lang(pl) %{_mandir}/pl/man8/ld-linux.8*
%lang(pl) %{_mandir}/pl/man8/ld-linux.so.8*
%lang(pl) %{_mandir}/pl/man8/ld.so.8*
%lang(pt) %{_mandir}/pt/man5/locale.5*
%lang(pt) %{_mandir}/pt/man5/nsswitch.conf.5*
%lang(pt) %{_mandir}/pt/man5/rpc.5*
%lang(pt) %{_mandir}/pt/man5/tzfile.5*
%lang(pt) %{_mandir}/pt/man7/ascii.7*
%lang(pt) %{_mandir}/pt/man7/charsets.7*
%lang(pt) %{_mandir}/pt/man7/iso-8859-*.7*
%lang(pt) %{_mandir}/pt/man7/iso_8859-*.7*
%lang(pt) %{_mandir}/pt/man7/iso_8859_*.7*
%lang(pt) %{_mandir}/pt/man7/koi8-*.7*
%lang(pt) %{_mandir}/pt/man7/latin*.7*
%lang(pt) %{_mandir}/pt/man7/locale.7*
%lang(pt) %{_mandir}/pt/man7/unicode.7*
%lang(pt) %{_mandir}/pt/man7/utf-8.7*
%lang(pt) %{_mandir}/pt/man7/utf8.7*
%lang(pt) %{_mandir}/pt/man8/zdump.8*
%lang(pt) %{_mandir}/pt/man8/zic.8*
%lang(ru) %{_mandir}/ru/man1/getent.1*
%lang(ru) %{_mandir}/ru/man1/iconv.1*
%lang(ru) %{_mandir}/ru/man1/locale.1*
%lang(ru) %{_mandir}/ru/man1/rpcgen.1*
%lang(ru) %{_mandir}/ru/man5/locale.5*
%lang(ru) %{_mandir}/ru/man5/nsswitch.conf.5*
%lang(ru) %{_mandir}/ru/man5/rpc.5*
%lang(ru) %{_mandir}/ru/man5/tzfile.5*
%lang(ru) %{_mandir}/ru/man7/ascii.7*
%lang(ru) %{_mandir}/ru/man7/charsets.7*
%lang(ru) %{_mandir}/ru/man7/iso-8859-*.7*
%lang(ru) %{_mandir}/ru/man7/iso_8859-*.7*
%lang(ru) %{_mandir}/ru/man7/iso_8859_*.7*
%lang(ru) %{_mandir}/ru/man7/koi8-*.7*
%lang(ru) %{_mandir}/ru/man7/latin*.7*
%lang(ru) %{_mandir}/ru/man7/locale.7*
%lang(ru) %{_mandir}/ru/man7/unicode.7*
%lang(ru) %{_mandir}/ru/man7/utf-8.7*
%lang(ru) %{_mandir}/ru/man7/utf8.7*
%lang(ru) %{_mandir}/ru/man8/ld-linux.so.8*
%lang(ru) %{_mandir}/ru/man8/ld.so.8*
%lang(ru) %{_mandir}/ru/man8/zdump.8*
%lang(ru) %{_mandir}/ru/man8/zic.8*
%lang(tr) %{_mandir}/tr/man1/iconv.1*
%lang(uk) %{_mandir}/uk/man5/rpc.5*
%lang(zh_CN) %{_mandir}/zh_CN/man1/iconv.1*
%lang(zh_CN) %{_mandir}/zh_CN/man5/locale.5*
%lang(zh_CN) %{_mandir}/zh_CN/man5/rpc.5*
%lang(zh_CN) %{_mandir}/zh_CN/man5/tzfile.5*
%lang(zh_CN) %{_mandir}/zh_CN/man7/ascii.7*
%lang(zh_CN) %{_mandir}/zh_CN/man7/charsets.7*
%lang(zh_CN) %{_mandir}/zh_CN/man7/locale.7*
%lang(zh_CN) %{_mandir}/zh_CN/man7/unicode.7*
%lang(zh_CN) %{_mandir}/zh_CN/man7/utf-8.7*
%lang(zh_CN) %{_mandir}/zh_CN/man7/utf8.7*
%lang(zh_CN) %{_mandir}/zh_CN/man8/zdump.8*
%lang(zh_CN) %{_mandir}/zh_CN/man8/zic.8*

%files misc
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/catchsegv
%attr(755,root,root) %{_bindir}/ldd
%attr(755,root,root) %{_bindir}/pldd
%ifarch %{ix86} m68k sparc sparcv9
%attr(755,root,root) %{_bindir}/lddlibc4
%endif
%attr(755,root,root) %{_bindir}/sotruss
%dir %{_libdir}/audit
%attr(755,root,root) %{_libdir}/audit/sotruss-lib.so

%{_mandir}/man1/catchsegv.1*
%{_mandir}/man1/ldd.1*
%{_mandir}/man1/pldd.1*
%lang(cs) %{_mandir}/cs/man1/ldd.1*
%lang(es) %{_mandir}/es/man1/ldd.1*
%lang(fi) %{_mandir}/fi/man1/ldd.1*
%lang(fr) %{_mandir}/fr/man1/ldd.1*
%lang(hu) %{_mandir}/hu/man1/ldd.1*
%lang(it) %{_mandir}/it/man1/ldd.1*
%lang(ja) %{_mandir}/ja/man1/ldd.1*
%lang(ja) %{_mandir}/ja/man1/pldd.1*
%lang(ko) %{_mandir}/ko/man1/ldd.1*
%lang(pl) %{_mandir}/pl/man1/ldd.1*
%lang(ru) %{_mandir}/ru/man1/ldd.1*
%lang(tr) %{_mandir}/tr/man1/ldd.1*
%lang(zh_CN) %{_mandir}/zh_CN/man1/ldd.1*

%files libcrypt
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libcrypt-%{core_version}.so
%ifarch alpha
%attr(755,root,root) %ghost /%{_lib}/libcrypt.so.1.1
%else
%attr(755,root,root) %ghost /%{_lib}/libcrypt.so.1
%endif

%files -n ldconfig
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ld.so.conf
%dir %{_sysconfdir}/ld.so.conf.d
%ghost %{_sysconfdir}/ld.so.cache
%attr(755,root,root) /sbin/ldconfig
%{_mandir}/man8/ldconfig.8*
%lang(es) %{_mandir}/es/man8/ldconfig.8*
%lang(fr) %{_mandir}/fr/man8/ldconfig.8*
%lang(hu) %{_mandir}/hu/man8/ldconfig.8*
%lang(ja) %{_mandir}/ja/man8/ldconfig.8*
%lang(pl) %{_mandir}/pl/man8/ldconfig.8*
%lang(pt) %{_mandir}/pt/man8/ldconfig.8*
%lang(ru) %{_mandir}/ru/man8/ldconfig.8*
%dir %attr(700,root,root) /var/cache/ldconfig
%attr(600,root,root) %ghost /var/cache/ldconfig/aux-cache

%files -n nss_compat
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libnss_compat-%{core_version}.so
%attr(755,root,root) /%{_lib}/libnss_compat.so.2

%files -n nss_db
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/makedb
%attr(755,root,root) /%{_lib}/libnss_db-%{core_version}.so
%attr(755,root,root) /%{_lib}/libnss_db.so.2
%{_var}/db/Makefile

%files -n nss_hesiod
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libnss_hesiod-%{core_version}.so
%attr(755,root,root) /%{_lib}/libnss_hesiod.so.2

%files -n nss_nis
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libnss_nis-%{core_version}.so
%attr(755,root,root) /%{_lib}/libnss_nis.so.2

%files -n nss_nisplus
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libnss_nisplus-%{core_version}.so
%attr(755,root,root) /%{_lib}/libnss_nisplus.so.2

%if %{with memusage}
%files memusage
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/memusage
%attr(755,root,root) %{_bindir}/memusagestat
%attr(755,root,root) %{_libdir}/libmemusage.so
%{_mandir}/man1/memusage.1*
%{_mandir}/man1/memusagestat.1*
%lang(ja) %{_mandir}/ja/man1/memusage.1*
%lang(ja) %{_mandir}/ja/man1/memusagestat.1*
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libBrokenLocale.so
%attr(755,root,root) %{_libdir}/libanl.so
%attr(755,root,root) %{_libdir}/libcrypt.so
%attr(755,root,root) %{_libdir}/libcidn.so
%attr(755,root,root) %{_libdir}/libdl.so
%attr(755,root,root) %{_libdir}/libm.so
%ifarch %{x8664} x32
%attr(755,root,root) %{_libdir}/libmvec.so
%endif
%attr(755,root,root) %{_libdir}/libnsl.so
%attr(755,root,root) %{_libdir}/libpcprofile.so
%attr(755,root,root) %{_libdir}/libresolv.so
%attr(755,root,root) %{_libdir}/librt.so
%attr(755,root,root) %{_libdir}/libthread_db.so
%attr(755,root,root) %{_libdir}/libutil.so
%{_libdir}/crt[1in].o
%{_libdir}/[MSg]crt1.o
# ld scripts
%{_libdir}/libc.so
%{_libdir}/libpthread.so
# static-only libs
%ifarch %{x8664} x32
%{_libdir}/libmvec_nonshared.a
%endif
%{_libdir}/libc_nonshared.a
%{_libdir}/libg.a
%{_libdir}/libieee.a
%ifarch alpha ppc sparc
%{_libdir}/libnldbl_nonshared.a
%endif
%{_libdir}/libpthread_nonshared.a
%{_libdir}/librpcsvc.a
%ifarch %{ix86} %{x8664} x32 ppc ppc64 s390 s390x sparc sparcv9 sparc64
# ABI-dependent headers
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
%{_includedir}/netiucv
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

%files devel-utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gencat
%attr(755,root,root) %{_bindir}/mtrace
%attr(755,root,root) %{_bindir}/pcprofiledump
%attr(755,root,root) %{_bindir}/sprof
%attr(755,root,root) %{_bindir}/xtrace
%{_mandir}/man1/mtrace.1*
%lang(ja) %{_mandir}/ja/man1/mtrace.1*

%files devel-doc
%defattr(644,root,root,755)
%doc documentation/*
%{_infodir}/libc.info*

%{_mandir}/man1/sprof.1*
# just a link to getcwd.3
%{_mandir}/man2/getcwd.2*
# just a link to killpg.3
%{_mandir}/man2/killpg.2*
%{_mandir}/man3/*
%{_mandir}/man7/aio.7*
%{_mandir}/man7/attributes.7*
%{_mandir}/man7/complex.7*
%{_mandir}/man7/feature_test_macros.7*
%{_mandir}/man7/glibc.7*
%{_mandir}/man7/glob.7*
%{_mandir}/man7/libc.7*
%{_mandir}/man7/math_error.7*
%{_mandir}/man7/nptl.7*
%{_mandir}/man7/posixoptions.7*
%{_mandir}/man7/pthreads.7*
%{_mandir}/man7/rtld-audit.7*
%{_mandir}/man7/sem_overview.7*
%{_mandir}/man7/shm_overview.7*
%lang(cs) %{_mandir}/cs/man3/*
%lang(de) %{_mandir}/de/man2/killpg.2*
%lang(de) %{_mandir}/de/man3/*
%lang(es) %{_mandir}/es/man2/killpg.2*
%lang(es) %{_mandir}/es/man3/*
%lang(es) %{_mandir}/es/man7/glob.7*
%lang(fr) %{_mandir}/fr/man2/getcwd.2*
%lang(fr) %{_mandir}/fr/man2/killpg.2*
%lang(fr) %{_mandir}/fr/man3/*
%lang(fr) %{_mandir}/fr/man7/complex.7*
%lang(fr) %{_mandir}/fr/man7/feature_test_macros.7*
%lang(fr) %{_mandir}/fr/man7/glob.7*
%lang(fr) %{_mandir}/fr/man7/posixoptions.7*
%lang(fr) %{_mandir}/fr/man7/pthreads.7*
%lang(fr) %{_mandir}/fr/man7/sem_overview.7*
%lang(fr) %{_mandir}/fr/man7/shm_overview.7*
%lang(hu) %{_mandir}/hu/man3/*
%lang(it) %{_mandir}/it/man3/*
%lang(it) %{_mandir}/it/man7/glob.7*
%lang(ja) %{_mandir}/ja/man1/sprof.1*
%lang(ja) %{_mandir}/ja/man2/getcwd.2*
%lang(ja) %{_mandir}/ja/man2/killpg.2*
%lang(ja) %{_mandir}/ja/man3/*
%lang(ja) %{_mandir}/ja/man7/aio.7*
%lang(ja) %{_mandir}/ja/man7/complex.7*
%lang(ja) %{_mandir}/ja/man7/feature_test_macros.7*
%lang(ja) %{_mandir}/ja/man7/glibc.7*
%lang(ja) %{_mandir}/ja/man7/glob.7*
%lang(ja) %{_mandir}/ja/man7/libc.7*
%lang(ja) %{_mandir}/ja/man7/math_error.7*
%lang(ja) %{_mandir}/ja/man7/posixoptions.7*
%lang(ja) %{_mandir}/ja/man7/pthreads.7*
%lang(ja) %{_mandir}/ja/man7/sem_overview.7*
%lang(ja) %{_mandir}/ja/man7/shm_overview.7*
%lang(ko) %{_mandir}/ko/man2/killpg.2*
%lang(ko) %{_mandir}/ko/man3/*
%lang(nl) %{_mandir}/nl/man3/*
%lang(pl) %{_mandir}/pl/man2/killpg.2*
%lang(pl) %{_mandir}/pl/man3/*
%lang(pt) %{_mandir}/pt/man2/killpg.2*
%lang(pt) %{_mandir}/pt/man3/*
%lang(pt) %{_mandir}/pt/man7/glob.7*
%lang(ru) %{_mandir}/ru/man1/sprof.1*
%lang(ru) %{_mandir}/ru/man2/killpg.2*
%lang(ru) %{_mandir}/ru/man3/*
%lang(ru) %{_mandir}/ru/man7/glob.7*
%lang(tr) %{_mandir}/tr/man3/*
%lang(uk) %{_mandir}/uk/man3/*
%lang(zh_CN) %{_mandir}/zh_CN/man3/*
%lang(zh_CN) %{_mandir}/zh_CN/man7/glob.7*

%files static
%defattr(644,root,root,755)
%{_libdir}/libanl.a
%{_libdir}/libBrokenLocale.a
%{_libdir}/libc.a
%{_libdir}/libcrypt.a
%{_libdir}/libdl.a
%{_libdir}/libm.a
%{_libdir}/libmcheck.a
%ifarch %{x8664} x32
%{_libdir}/libm-%{core_version}.a
%{_libdir}/libmvec.a
%endif
%{_libdir}/libnsl.a
%{_libdir}/libpthread.a
%{_libdir}/libresolv.a
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

%files -n nscd
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/nscd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nscd.*
%attr(754,root,root) /etc/rc.d/init.d/nscd
%attr(755,root,root) %{_sbindir}/nscd*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/nscd
%attr(640,root,root) %ghost /var/log/nscd
%{systemdtmpfilesdir}/nscd.conf
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
%{_prefix}/lib/locale/locale-archive
%endif

%files -n iconv
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/iconvconfig
%dir %{_libdir}/gconv
%{_libdir}/gconv/gconv-modules
%verify(not md5 mtime size) %{_libdir}/gconv/gconv-modules.cache
%attr(755,root,root) %{_libdir}/gconv/*.so
%{_mandir}/man8/iconvconfig.8*
%lang(ja) %{_mandir}/ja/man8/iconvconfig.8*
