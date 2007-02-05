# TODO:
# - files?
#   (debuggable libraries built with frame pointers - -debug package?)
#   %{_libdir}/libBrokenLocale_g.a
#   %{_libdir}/libanl_g.a
#   %{_libdir}/libc_g.a
#   %{_libdir}/libcrypt_g.a
#   %{_libdir}/libdl_g.a
#   %{_libdir}/libm_g.a
#   %{_libdir}/libnsl_g.a
#   %{_libdir}/libpthread_g.a
#   %{_libdir}/libresolv_g.a
#   %{_libdir}/librpcsvc_g.a
#   %{_libdir}/librt_g.a
#   %{_libdir}/libutil_g.a
#
# Conditional build:
# min_kernel	(default is 2.6.12)
%bcond_without	memusage	# don't build memusage utility
%bcond_without	selinux		# without SELinux support (in nscd)
%bcond_with	tests		# perform "make test"
%bcond_without	localedb	# don't build localedb-all (is time consuming)
%bcond_with	cross		# build using crossgcc (without libgcc_eh)
#
# TODO:
# - look at locale fixes/updates in bugzilla
# - no more chicken-egg problem (postshell is no more dynamically linked with libc), remove SONAME symlinks? see files section.
# [OLD]
# - localedb-gen man pages(?)
# - math/{test-fenv,test-tgmath,test-float,test-ifloat},
#   debug/backtrace-tst(SEGV)  fail on alpha
%{!?min_kernel:%global		min_kernel	2.6.12}

%ifarch sparc64
%undefine	with_memusage
%endif

%define		llh_version	7:2.6.12.0-10

Summary:	GNU libc
Summary(de):	GNU libc
Summary(es):	GNU libc
Summary(fr):	GNU libc
Summary(ja):	GNU libc �饤�֥��
Summary(pl):	GNU libc
Summary(ru):	GNU libc ������ 2.3
Summary(tr):	GNU libc
Summary(uk):	GNU libc ���Ӧ� 2.3
Name:		glibc
Version:	2.5
Release:	0.4
Epoch:		6
License:	LGPL
Group:		Libraries
Source0:	ftp://sources.redhat.com/pub/glibc/releases/%{name}-%{version}.tar.bz2
# Source0-md5:	1fb29764a6a650a4d5b409dda227ac9f
Source1:	ftp://sources.redhat.com/pub/glibc/releases/%{name}-libidn-%{version}.tar.bz2
# Source1-md5:	8787868ba8962d9b125997ec2f25ac01
Source2:	nscd.init
Source3:	nscd.sysconfig
Source4:	nscd.logrotate
#Source5:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-man-pages.tar.bz2
Source5:	http://qboosh.cs.net.pl/man/%{name}-man-pages.tar.bz2
# Source5-md5:	f464eadf3cf06761f65639e44a179e6b
Source6:	%{name}-localedb-gen
Source7:	%{name}-LD-path.c
Patch0:		%{name}-info.patch
Patch1:		%{name}-pl.po-update.patch
Patch2:		%{name}-pld.patch
Patch3:		%{name}-crypt-blowfish.patch
Patch4:		%{name}-alpha-ev6-opcodes.patch
Patch5:		%{name}-sparc-softfp-gcc.patch
Patch6:		%{name}-paths.patch
Patch7:		%{name}-sparc64-fixes.patch
Patch8:		%{name}-missing-nls.patch
Patch9:		%{name}-java-libc-wait.patch

Patch11:	%{name}-no_opt_override.patch
Patch12:	%{name}-includes.patch
Patch13:	%{name}-ppc-inline-fsqrt.patch
Patch14:	%{name}-sparc-errno_fix.patch

Patch17:	%{name}-new-charsets.patch

Patch20:	%{name}-tzfile-noassert.patch
Patch21:	%{name}-morelocales.patch
Patch22:	%{name}-locale_fixes.patch
Patch23:	%{name}-ZA_collate.patch
Patch24:	%{name}-iconvconfig-nxstack.patch
Patch25:	%{name}-cross-gcc_eh.patch
# PaX hack (dropped)
#Patch30:	%{name}-pax_dl-execstack.patch
URL:		http://www.gnu.org/software/libc/
%{?with_selinux:BuildRequires:	audit-libs-devel}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	binutils >= 2:2.15.90.0.3
BuildRequires:	gcc >= 5:3.4
BuildRequires:	gawk
%{?with_memusage:BuildRequires:	gd-devel >= 2.0.1}
BuildRequires:	gettext-devel >= 0.10.36
%{!?with_cross:BuildRequires:	dietlibc-static}
%{?with_selinux:BuildRequires:	libselinux-devel >= 1.18}
BuildRequires:	linux-libc-headers >= %{llh_version}
BuildRequires:	perl-base
BuildRequires:	rpm-build >= 4.3-0.20030610.28
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.315
BuildRequires:	sed >= 4.0.5
BuildRequires:	texinfo
AutoReq:	false
Requires:	%{name}-misc = %{epoch}:%{version}-%{release}
Requires:	basesystem
Requires:	uname(release) >= %{min_kernel}
Provides:	/sbin/ldconfig
Provides:	glibc(nptl)
Provides:	glibc(tls)
Provides:	glibc64
Provides:	ldconfig
Obsoletes:	glibc-common
Obsoletes:	glibc-debug
Obsoletes:	glibc64
Obsoletes:	ldconfig
Conflicts:	kernel < %{min_kernel}
Conflicts:	kernel24
Conflicts:	kernel24-smp
Conflicts:	ld.so < 1.9.9-10
Conflicts:	man-pages < 1.43
Conflicts:	poldek < 0.18.8-5
Conflicts:	rc-scripts < 0.3.1-13
Conflicts:	rpm < 4.1
ExclusiveArch:	i486 i586 i686 pentium3 pentium4 athlon %{x8664} ia64 alpha s390 s390x sparc sparc64 sparcv9 ppc ppc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# avoid -s here (ld.so must not be stripped to allow any program debugging)
%define		filterout_ld		(-Wl,)?-[sS] (-Wl,)?--strip.*
%define 	specflags_sparc64	-mcpu=ultrasparc -mvis -fcall-used-g6

# -m from CFLAGS or even LDFLAGS is not propagated to some *.o linking
%ifarch sparc sparcv9
%{expand:%%define	__cc	%{__cc} -m32}
%endif

# Xen-friendly glibc
%define		specflags_ia32		-mno-tls-direct-seg-refs
%define		specflags_x86_64	-mno-tls-direct-seg-refs
%define		specflags_amd64		-mno-tls-direct-seg-refs
%define		specflags_ia32e		-mno-tls-direct-seg-refs

# we don't want perl dependency in glibc-devel
%define		_noautoreqfiles		%{_bindir}/mtrace
# hack: don't depend on rpmlib(PartialHardlinkSets) for easier upgrade from Ra
# (hardlinks here are unlikely to be "partial"... and rpm 4.0.2 from Ra was
# patched not to crash on partial hardlinks too)
%define		_hack_dontneed_PartialHardlinkSets	1
%define		_noautochrpath		.*\\(ldconfig\\|sln\\)

%description
Contains the standard libraries that are used by multiple programs on
the system. In order to save disk space and memory, as well as to ease
upgrades, common system code is kept in one place and shared between
programs. This package contains the most important sets of shared
libraries, the standard C library and the standard math library.
Without these, a Linux system will not function. It also contains
national language (locale) support.

Can be used on: Linux kernel >= %{min_kernel}.

%description -l es
Contiene las bibliotecas est�ndared que son usadas por varios
programas del sistema. Para ahorrar el espacio en el disco y la
memoria, igual que para facilitar actualizaciones, c�digo com�n del
sistema se guarda en un sitio y es compartido entre los programas.
Este paquete contiene las bibliotecas compartidas m�s importantes, es
decir la biblioteca C est�ndar y la biblioteca est�ndar de matem�tica.
Sin �stas, un sistema Linux no podr� funcionar. Tambi�n est� incluido
soporte de idiomas nacionales (locale).

Puede usarse con: n�cleo Linux >= %{min_kernel}.

%description -l de
Enth�lt die Standard-Libraries, die von verschiedenen Programmen im
System benutzt werden. Um Festplatten- und Arbeitsspeicher zu sparen
und zur Vereinfachung von Upgrades ist der gemeinsame Systemcode an
einer einzigen Stelle gespeichert und wird von den Programmen
gemeinsam genutzt. Dieses Paket enth�lt die wichtigsten Sets der
shared Libraries, die Standard-C-Library und die
Standard-Math-Library, ohne die das Linux-System nicht funktioniert.
Ferner enth�lt es den Support f�r die verschiedenen Sprachgregionen
(locale).

Can be used on: Linux kernel >= %{min_kernel}.

%description -l fr
Contient les biblioth�ques standards utilis�es par de nombreux
programmes du syst�me. Afin d'�conomiser l'espace disque et m�moire,
et de faciliter les mises � jour, le code commun au syst�me est mis �
un endroit et partag� entre les programmes. Ce paquetage contient les
biblioth�ques partag�es les plus importantes, la biblioth�que standard
du C et la biblioth�que math�matique standard. Sans celles-ci, un
syst�me Linux ne peut fonctionner. Il contient aussi la gestion des
langues nationales (locales).

Can be used on: Linux kernel >= %{min_kernel}.

%description -l ja
glibc
�ѥå������ϥ����ƥ���ʣ���Υץ������ǻȤ���ɸ��饤�֥���
�դ��ߤޤ����ǥ��������ڡ����ȥ�������󤷤��ꡢ���åץ��졼�ɤ�
�Ѱդˤ��뤿��ˡ����̤Υ����ƥॳ���ɤϰ�Ĥξ��ˤ����졢�ץ������
�֤Ƕ�ͭ����ޤ���������ʬŪ�ʥѥå������ϥ������ɥ饤�֥��Τ��ʤ�
���פʥ��åȤ�դ��ߤޤ�: ɸ�� C �饤�֥���ɸ����ͥ饤�֥��Ǥ���
������ĤΥ饤�֥��ȴ���Ǥϡ�Linux �����ƥ�ϵ�ǽ���ޤ��� glibc
�ѥå������Ϥޤ��ϰ���� (locale) ���ݡ��Ȥȥ����ॾ����ǡ����١���
���ݡ��Ȥ�դ��ߤޤ���

Can be used on: Linux kernel >= %{min_kernel}.

%description -l pl
W pakiecie znajduj� si� podstawowe biblioteki, u�ywane przez r�ne
programy w Twoim systemie. U�ywanie przez programy bibliotek z tego
pakietu oszcz�dza miejsce na dysku i pami��. Wi�kszo�� kodu
systemowego jest usytuowane w jednym miejscu i dzielone mi�dzy wieloma
programami. Pakiet ten zawiera bardzo wa�ny zbi�r bibliotek
standardowych, wsp�dzielonych (dynamicznych) bibliotek C i
matematycznych. Bez glibc system Linux nie jest w stanie funkcjonowa�.
Znajduj� si� tutaj r�wnie� definicje r�nych informacji dla wielu
j�zyk�w (locale).

Pakiet jest przeznaczony dla j�dra Linuksa >= %{min_kernel}.

%description -l ru
�������� ����������� ����������, ������������ ���������������
����������� � �������. ��� ����, ����� ��������� �������� ������������
� ������, � ����� ��� �������� ����������, ��������� ���, ����� ���
���� ��������, �������� � ����� ����� � ����������� ������������ �����
�����������. ���� ����� �������� �������� ������ �� �����������
��������� - ����������� ���������� C � ����������� ����������
����������. ��� ���� ��������� Linux ��������������� �� �����. �����
����� �������� ��������� ������������ ������ (locale).

Can be used on: Linux kernel >= %{min_kernel}.

%description -l tr
Bu paket, bir�ok program�n kulland��� standart kitapl�klar� i�erir.
Disk alan� ve bellek kullan�m�n� azaltmak ve ayn� zamanda g�ncelleme
i�lemlerini kolayla�t�rmak i�in ortak sistem kodlar� tek bir yerde
tutulup programlar aras�nda payla�t�r�l�r. Bu paket en �nemli ortak
kitapl�klar�, standart C kitapl���n� ve standart matematik kitapl���n�
i�erir. Bu kitapl�klar olmadan Linux sistemi �al��mayacakt�r. Yerel
dil deste�i ve zaman dilimi veri taban� da bu pakette yer al�r.

Can be used on: Linux kernel >= %{min_kernel}.

%description -l uk
������� ��������Φ ¦�̦�����, ���Ҧ ���������������� ����������
���������� � �����ͦ. ��� ����, ��� �������� �������� ����Ԧ� ��
���'���, � ����� ��� �������� ���������� �������, ��������� ���,
�Ц����� ��� �Ӧ� �������, ���Ҧ������� � ������ ͦ�æ � ����������
����������դ���� �Ӧ�� ����������. ��� ����� ͦ����� ���¦��� �����צ
� ����ͦ���� ¦�̦���� - ���������� ¦�̦����� � �� ����������
¦�̦����� ����������. ��� ��� ¦�̦���� Linux ����æ������� �� ����.
����� ����� ͦ����� Ц������� ��æ�������� ��� (locale).

Can be used on: Linux kernel >= %{min_kernel}.

%package misc
Summary:	Utilities and data used by glibc
Summary(pl):	Narz�dzia i dane u�ywane przez glibc
Group:		Applications/System
AutoReq:	false
Requires(pre):	%{name} = %{epoch}:%{version}-%{release}
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	tzdata >= 2006g-2

%description misc
Utilities and data used by glibc.

%description misc -l pl
Narz�dzia i dane u�ywane przez glibc.

%package devel
Summary:	Additional libraries required to compile
Summary(de):	Weitere Libraries zum Kompilieren
Summary(es):	Bibliotecas adicionales necesarias para la compilaci�n
Summary(fr):	Librairies suppl�mentaires n�cessaires � la compilation
Summary(ja):	ɸ�� C �饤�֥��ǻȤ���إå����ȥ��֥������ȥե�����
Summary(pl):	Dodatkowe biblioteki wymagane podczas kompilacji
Summary(ru):	�������������� ����������, ����������� ��� ����������
Summary(tr):	Geli�tirme i�in gerekli di�er kitapl�klar
Summary(uk):	�������צ ¦�̦�����, ���Ҧ�Φ ��� ���Ц��æ�
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

%description devel -l de
Bei der Entwicklung von Programmen, die die Standard-C-Libraries
verwenden (also fast alle), ben�tigt das System diese Standard-Header-
und Objektdateien zum Erstellen der ausf�hrbaren Programme.

%description devel -l es
Para desarrollar programas que utilizan las bibliotecas C est�ndar (lo
cual hacen pr�cticamente todos los programas), el sistema necesita
disponer de estos ficheros de cabecera y de objetos para crear los
ejecutables.

%description devel -l fr
Pour d�velopper des programmes utilisant les biblioth�ques standard du
C (ce que presque tous les programmes font), le syst�me doit poss�der
ces fichiers en-t�tes et objets standards pour cr�er les ex�cutables.

%description devel -l ja
glibc-devel �ѥå�������(�ۤȤ�ɤ��٤ƤΥץ������ǻȤ���)ɸ�� C
�饤�֥�����Ѥ����ץ�������ȯ���뤿��Υإå����ȥ��֥�������
�ե������ޤߤޤ����⤷ɸ�� C
�饤�֥�����Ѥ���ץ�������ȯ����ʤ�
�¹ԥե���������������Ū�Ǥ�����ɸ��إå��ȥ��֥������ȥե�����
�����ѤǤ��ޤ���

%description devel -l pl
Pakiet ten jest niezb�dny przy tworzeniu w�asnych program�w
korzystaj�cych ze standardowej biblioteki C. Znajduj� si� tutaj pliki
nag��wkowe oraz pliki obiektowe, niezb�dne do kompilacji program�w
wykonywalnych i innych bibliotek.

%description devel -l ru
��� ���������� ��������, ������������ ����������� ���������� C (�
����������� ��� ��������� �� ����������), ������� ���������� ������ �
��������� �����, ������������ � ���� ������, ����� ���������
����������� �����.

%description devel -l tr
C kitapl���n� kullanan (ki hemen hemen hepsi kullan�yor) programlar
geli�tirmek i�in gereken standart ba�l�k dosyalar� ve statik
kitapl�klar.

%description devel -l uk
��� �������� �������, �� �������������� ��������Φ ¦�̦����� C
(��������� �Ӧ �������� �� ��������������), �����ͦ ������� ������
�� ��'���Φ �����, �� ͦ������� � ����� ����Ԧ, ��� ����������
��������Φ �����.

%package headers
Summary:	Header files for development using standard C libraries
Summary(pl):	Pliki nag��wkowe do tworzenia program�w przy u�yciu standardowych bibliotek C
Group:		Development/Building
Provides:	%{name}-headers(%{_target_cpu}) = %{epoch}:%{version}-%{release}
%ifarch %{x8664}
# If both -m32 and -m64 is to be supported on x86_64, x86_64 package
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
Requires:	linux-libc-headers >= %{llh_version}

%description headers
The glibc-headers package contains the header files necessary for
developing programs which use the standard C libraries (which are used
by nearly all programs). If you are developing programs which will use
the standard C libraries, your system needs to have these standard
header files available in order to create the executables.

Install glibc-headers if you are going to develop programs which will
use the standard C libraries.

%description headers -l pl
Pakiet glibc-headers zawiera pliki nag��wkowe niezb�dne do rozwijania
program�w u�ywaj�cych standardowych bibliotek C (u�ywanych przez
prawie wszystkie programy). Je�li tworzymy programy korzystaj�ce ze
standardowych bibliotek C, system wymaga dost�pno�ci tych
standardowych plik�w nag��wkowych do tworzenia program�w
wykonywalnych.

Ten pakiet nale�y zainstalowa� je�li zamierzamy tworzy� programy
korzystaj�ce ze standardowych bibliotek C.

%package devel-utils
Summary:	Utilities needed for development using standard C libraries
Summary(pl):	Narz�dzia do tworzenia program�w przy u�yciu standardowych bibliotek C
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

%description devel-utils -l pl
Pakiet glibc-devel-utils zawiera narz�dzia niezb�dne do rozwijania
program�w u�ywaj�cych standardowych bibliotek C (u�ywanych przez
prawie wszystkie programy). Je�li tworzymy programy korzystaj�ce ze
standardowych bibliotek C, system wymaga dost�pno�ci tych narz�dzi do
tworzenia program�w wykonywalnych.

Ten pakiet nale�y zainstalowa� je�li zamierzamy tworzy� programy
korzystaj�ce ze standardowych bibliotek C.

%package devel-doc
Summary:	Documentation needed for development using standard C libraries
Summary(pl):	Dokumentacja do tworzenia program�w przy u�yciu standardowych bibliotek C
Group:		Documentation
Provides:	%{name}-devel-doc(%{_target_cpu}) = %{epoch}:%{version}-%{release}
%ifarch %{x8664}
# If both -m32 and -m64 is to be supported on x86_64, x86_64 package
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

%description devel-doc -l pl
Pakiet glibc-devel-doc zawiera strony info i manuala przydatne do
rozwijania program�w u�ywaj�cych standardowych bibliotek C (u�ywanych
przez prawie wszystkie programy).

Ten pakiet nale�y zainstalowa� je�li zamierzamy tworzy� programy
korzystaj�ce ze standardowych bibliotek C.

%package -n nscd
Summary:	Name Service Caching Daemon
Summary(es):	Demonio de cach� del servicio de nombres
Summary(ja):	�͡��ॵ���ӥ�����å��󥰥ǡ���� (nacd)
Summary(pl):	Demon zapami�tuj�cy odpowiedzi serwis�w nazw
Summary(ru):	���������� ����� �������� ����
Summary(uk):	�������� ����� ��צӦ� ����
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

%description -n nscd -l es
nscd guarda las peticiones del servicio de nombres en una cach�; eso
puede aumentar dr�sticamente las prestaciones de NIS+, y tambi�n puede
ayudar con DNS.

%description -n nscd -l ja
Nscd �ϥ͡��ॵ���ӥ����Ȥ򥭥�å��夷��NIS+ �Υѥե����ޥ󥹤�
�ɥ�ޥƥ��å��˲������뤳�Ȥ��Ǥ���DNS ��Ʊ�ͤ�������ޤ���

%description -n nscd -l pl
nscd zapami�tuje zapytania i odpowiedzi NIS oraz DNS. Pozwala
drastycznie poprawi� szybko�� dzia�ania NIS+.

%description -n nscd -l ru
nscd �������� ���������� �������� � �������� ����; ��� ����� �����
��������� ������������������ ������ � NIS+ �, �����, ����� ������ �
DNS.

%description -n nscd -l uk
nscd ���դ ���������� �����Ӧ� �� ���צӦ� ����; �� ���� ������
�¦������ ����˦��� ������ � NIS+ �, �����, ���� ��������� � DNS.

%package -n localedb-src
Summary:	locale database source code
Summary(es):	C�digo fuente de la base de datos de los locales
Summary(pl):	Kod �r�d�owy bazy locale
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	gzip
Requires:	sed

%description -n localedb-src
This add-on package contains the data needed to build the locale data
files to use the internationalization features of the GNU libc.

%description -n localedb-src -l es
Este paquete adicional contiene los datos necesarios para construir
los ficheros de locale, imprescindibles para usar las cualidades de
internacionalizaci�n de GNU libc.

%description -n localedb-src -l pl
Pakiet ten zawiera dane niezb�dne do zbudowania binarnych plik�w
lokalizacyjnych, by m�c wykorzysta� mo�liwo�ci oferowane przez GNU
libc.

%package localedb-all
Summary:	locale database for all locales supported by glibc
Summary(es):	Base de datos de todos los locales soportados por glibc
Summary(pl):	Baza danych locale dla wszystkich lokalizacji obs�ugiwanych przez glibc
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	iconv = %{epoch}:%{version}-%{release}

%description localedb-all
This package contains locale database for all locales supported by
glibc. In glibc 2.3.x it's one large file (about 39MB) - if you want
something smaller with support for chosen locales only, consider
installing localedb-src and regenerating database using localedb-gen
script (when database is generated, localedb-src can be uninstalled).

%description localedb-all -l es
Este paquete contiene una base de datos de todos los locales
soportados por glibc. En glibc 2.3.x �se es un fichero grande (aprox.
39 MB) -- si prefiere algo m�s peque�o, s�lo con soporte de unos
locales elegidos, consid�rese instalar localedb-src y regenerar la
base de datos usando el escript localedb-gen (una vez que la base de
datos est� creada, localedb-src se podr� desinstalar).

%description localedb-all -l pl
Ten pakiet zawiera baz� danych locale dla wszystkich lokalizacji
obs�ugiwanych przez glibc. W glibc 2.3.x jest to jeden du�y plik
(oko�o 39MB); aby mie� co� mniejszego, z obs�ug� tylko wybranych
lokalizacji, nale�y zainstalowa� pakiet localedb-src i przegenerowa�
baz� danych przy u�yciu skryptu localedb-gen (po wygenerowaniu bazy
pakiet localedb-src mo�na odinstalowa�).

%package -n iconv
Summary:	Convert encoding of given files from one encoding to another
Summary(es):	Convierte entre varias codificaciones de los ficheros dados
Summary(pl):	Modu�y do konwersji plik�w tekstowych z jednego kodowania do innego
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n iconv
Convert encoding of given files from one encoding to another. You need
this package if you want to convert some document from one encoding to
another or if you have installed some programs which use Generic
Character Set Conversion Interface.

%description -n iconv -l es
Convierte la codificaci�n de dados ficheros. Necesita este paquete si
quiere convertir un documento entre una codificaci�n (juego de
caracteres) y otra, o si tiene instalado alg�n programa que usa el
Generic Character Set Conversion Interface (interfaz gen�rica de
conversi�n de juegos de caracteres).

%description -n iconv -l pl
Modu�y do konwersji plik�w tekstowych z jednego kodowania do innego.
Trzeba mie� zainstalowany ten pakiet, aby wykonywa� konwersj�
dokument�w z jednego kodowania do innego lub do u�ywania program�w
korzystaj�cych z Generic Character Set Conversion Interface w glibc,
czyli z zestawu funkcji z tej biblioteki, kt�re umo�liwiaj� konwersj�
kodowania danych z poziomu dowolnego programu.

%package static
Summary:	Static libraries
Summary(es):	Bibliotecas est�ticas
Summary(pl):	Biblioteki statyczne
Summary(ru):	����������� ���������� glibc
Summary(uk):	������Φ ¦�̦����� glibc
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}
Provides:	%{name}-static(%{_target_cpu}) = %{epoch}:%{version}-%{release}
Obsoletes:	libiconv-static

%description static
GNU libc static libraries.

%description static -l es
Bibliotecas est�ticas de GNU libc.

%description static -l pl
Biblioteki statyczne GNU libc.

%description static -l ru
��� ��������� ����� �� ������������ ������������, ������� ������ ��
������ � glibc-devel.

%description static -l uk
�� ������� ����� ڦ ���������� ¦�̦�������, �� ¦���� �� ������� �
����� glibc-devel.

%package profile
Summary:	glibc with profiling support
Summary(de):	glibc mit Profil-Unterst�tzung
Summary(es):	glibc con soporte de perfilamiento
Summary(fr):	glibc avec support pour profiling
Summary(pl):	glibc ze wsparciem dla profilowania
Summary(ru):	GNU libc � ���������� ����������
Summary(tr):	�l��m deste�i olan glibc
Summary(uk):	GNU libc � Ц�������� ����������
Group:		Development/Libraries/Libc
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}
Obsoletes:	libc-profile

%description profile
When programs are being profiled using gprof, they must use these
libraries instead of the standard C libraries for gprof to be able to
profile them correctly.

%description profile -l de
Damit Programmprofile mit gprof richtig erstellt werden, m�ssen diese
Libraries anstelle der �blichen C-Libraries verwendet werden.

%description profile -l es
Cuando programas son perfilidas usando gprof, tienen que usar estas
biblioteces en vez de las est�ndares para que gprof pueda perfilarlas
correctamente.

%description profile -l pl
Programy profilowane za pomoc� gprof musz� u�ywa� tych bibliotek
zamiast standardowych bibliotek C, aby gprof m�g� odpowiednio je
wyprofilowa�.

%description profile -l uk
���� �������� ���̦�������� ����������� gprof, ���� �����Φ
��������������� ��ͦ��� ����������� ¦�̦���� ¦�̦�����, �� ͦ�������
� ����� ����Ԧ. ��� ����������Φ ����������� ¦�̦���� gprof ��ͦ���
�������� ��������Ԧ� ���� ���������� æ�� �� ������ � �������� �
������������ ��æ...

%description profile -l tr
gprof kullan�larak �l��len programlar standart C kitapl��� yerine bu
kitapl��� kullanmak zorundad�rlar.

%description profile -l ru
����� ��������� ����������� ����������� gprof, ��� ������
������������, ������ ����������� ���������, ����������, ���������� �
���� �����. ��� ������������� ����������� ��������� gprof ������
�������� ����������� ����� ���������� ���� �� ������ � �������� �
����������� ����...

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
m�s peque�o de la biblioteca libc compartida est�ndar.

%description pic -l pl
Archiwum PIC biblioteki GNU C zawiera archiwaln� bibliotek� (plik ar)
z�o�on� z pojedynczych obiekt�w wsp�dzielonych. U�ywana jest do
tworzenia biblioteki b�d�cej mniejszym podzestawem standardowej
biblioteki wsp�dzielonej libc.

%package -n nss_compat
Summary:	Old style NYS NSS glibc module
Summary(es):	El antiguo m�dulo NYS NSS de glibc
Summary(pl):	Stary modu� NYS NSS glibc
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n nss_compat
Old style NYS NSS glibc module.

%description -n nss_compat -l es
El antiguo m�dulo NYS NSS de glibc

%description -n nss_compat -l pl
Stary modu� NYS NSS glibc.

%package -n nss_dns
Summary:	BIND NSS glibc module
Summary(es):	M�dulo BIND NSS de glibc
Summary(pl):	Modu� BIND NSS glibc
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n nss_dns
BIND NSS glibc module.

%description -n nss_dns -l es
M�dulo BIND NSS de glibc.

%description -n nss_dns -l pl
Modu� BIND NSS glibc.

%package -n nss_files
Summary:	Traditional files databases NSS glibc module
Summary(es):	M�dulo de tradicionales bases de datos en ficheros para glibc
Summary(pl):	Modu� tradycyjnych plikowych baz danych NSS glibc
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n nss_files
Traditional files databases NSS glibc module.

%description -n nss_files -l es
M�dulo de tradicionales bases de datos en ficheros para glibc.

%description -n nss_files -l pl
Modu� tradycyjnych plikowych baz danych NSS glibc.

%package -n nss_hesiod
Summary:	hesiod NSS glibc module
Summary(es):	M�dulo hesiod NSS de glibc
Summary(pl):	Modu� hesiod NSS glibc
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n nss_hesiod
glibc NSS (Name Service Switch) module for databases access.

%description -n nss_hesiod -l es
M�dulo hesiod NSS de glibc.

%description -n nss_hesiod -l pl
Modu� glibc NSS (Name Service Switch) dost�pu do baz danych.

%package -n nss_nis
Summary:	NIS(YP) NSS glibc module
Summary(es):	M�dulo NIS(YP) NSS de glibc
Summary(pl):	Modu� NIS(YP) NSS glibc
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n nss_nis
glibc NSS (Name Service Switch) module for NIS(YP) databases access.

%description -n nss_nis -l es
M�dulo NSS de glibc para acceder las bases de datos NIS(YP).

%description -n nss_nis -l pl
Modu� glibc NSS (Name Service Switch) dost�pu do baz danych NIS(YP).

%package -n nss_nisplus
Summary:	NIS+ NSS module
Summary(es):	M�dulo NIS+ NSS
Summary(pl):	Modu� NIS+ NSS
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n nss_nisplus
glibc NSS (Name Service Switch) module for NIS+ databases access.

%description -n nss_nisplus -l es
M�dulo NSS (Name Service Switch) de glibc para acceder las bases de
datos NIS+.

%description -n nss_nisplus -l pl
Modu� glibc NSS (Name Service Switch) dost�pu do baz danych NIS+.

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

%prep
%setup -q -a1
ln -s glibc-libidn-%{version} libidn
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

%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p0

%patch17 -p1

%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%{?with_cross:%patch25 -p1}

# these would be copied to localedb-src
rm -f localedata/locales/*{.orig,~}

chmod +x scripts/cpp

# i786 (aka pentium4) hack
cd nptl/sysdeps/i386 && ln -s i686 i786 && cd -
cd nptl/sysdeps/unix/sysv/linux/i386 && ln -s i686 i786 && cd -

# Hack till glibc-kernheaders get updated, argh
%define min_kernel_ver	%(echo %{min_kernel} | cut -f 1 -d .)
%define min_kernel_patc %(echo %{min_kernel} | cut -f 2 -d .)
%define min_kernel_subl	%(echo %{min_kernel} | cut -f 3 -d .)
%define min_kernel_code	%(expr %{min_kernel_ver} \\* 65536 + %{min_kernel_patc} \\* 256 + %{min_kernel_subl})
mkdir -p override_headers/linux
cat > override_headers/linux/version.h <<EOF
#define UTS_RELEASE "%{min_kernel}"
#define LINUX_VERSION_CODE %{min_kernel_code}
#define KERNEL_VERSION(a,b,c) (((a) << 16) + ((b) << 8) + (c))
EOF
mkdir -p override_headers/asm
cat > override_headers/asm/unistd.h <<EOF
#ifndef _HACK_ASM_UNISTD_H
#include_next <asm/unistd.h>
%ifarch alpha
#ifndef __NR_stat64
#define __NR_stat64			425
#define __NR_lstat64			426
#define __NR_fstat64			427
#endif
#ifndef __NR_mq_open
#define __NR_mq_open			432
#define __NR_mq_unlink			433
#define __NR_mq_timedsend		434
#define __NR_mq_timedreceive		435
#define __NR_mq_notify			436
#define __NR_mq_getsetattr		437
#endif
#ifndef __NR_waitid
#define __NR_waitid			438
#endif
#ifndef __NR_inotify_init
#define __NR_inotify_init		444
#define __NR_inotify_add_watch		445
#define __NR_inotify_rm_watch		446
#endif
%endif
%ifarch %{ix86}
#ifndef __NR_mq_open
#define __NR_mq_open 		277
#define __NR_mq_unlink		(__NR_mq_open+1)
#define __NR_mq_timedsend	(__NR_mq_open+2)
#define __NR_mq_timedreceive	(__NR_mq_open+3)
#define __NR_mq_notify		(__NR_mq_open+4)
#define __NR_mq_getsetattr	(__NR_mq_open+5)
#endif
#ifndef __NR_waitid
#define __NR_waitid		284
#endif
#ifndef __NR_inotify_init
#define __NR_inotify_init	291
#define __NR_inotify_add_watch	292
#define __NR_inotify_rm_watch	293
#endif
#ifndef __NR_openat
#define __NR_openat		295
#define __NR_mkdirat		296
#define __NR_mknodat		297
#define __NR_fchownat		298
#define __NR_futimesat		299
#define __NR_unlinkat		301
#define __NR_renameat		302
#define __NR_linkat		303
#define __NR_symlinkat		304
#define __NR_readlinkat		305
#define __NR_fchmodat		306
#define __NR_faccessat		307
#endif
#ifndef __NR_fstatat64
#define __NR_fstatat64		300
#endif
#ifndef __NR_pselect6
#define __NR_pselect6		308
#define __NR_ppoll		309
#endif
#ifndef __NR_unshare
#define __NR_unshare		310
#endif
#ifndef __NR_set_robust_list
#define __NR_set_robust_list	311
#define __NR_get_robust_list	312
#endif
#ifndef __NR_splice
#define __NR_splice		313
#endif
#ifndef __NR_sync_file_range
#define __NR_sync_file_range	314
#endif
#ifndef __NR_tee
#define __NR_tee		315
#endif
#ifndef __NR_vmsplice
#define __NR_vmsplice		316
#endif
%endif
%ifarch ia64
#ifndef __NR_timer_create
#define __NR_timer_create	1248
#define __NR_timer_settime	1249
#define __NR_timer_gettime	1250
#define __NR_timer_getoverrun	1251
#define __NR_timer_delete	1252
#define __NR_clock_settime	1253
#define __NR_clock_gettime	1254
#define __NR_clock_getres	1255
#define __NR_clock_nanosleep	1256
#endif
#ifndef __NR_mq_open
#define __NR_mq_open		1262
#define __NR_mq_unlink		1263
#define __NR_mq_timedsend	1264
#define __NR_mq_timedreceive	1265
#define __NR_mq_notify		1266
#define __NR_mq_getsetattr	1267
#endif
#ifndef __NR_waitid
#define __NR_waitid		1270
#endif
#ifndef __NR_inotify_init
#define __NR_inotify_init	1277
#define __NR_inotify_add_watch	1278
#define __NR_inotify_rm_watch	1279
#endif
#ifndef __NR_openat
#define __NR_openat		1281
#define __NR_mkdirat		1282
#define __NR_mknodat		1283
#define __NR_fchownat		1284
#define __NR_futimesat		1285
#define __NR_newfstatat		1286
#define __NR_unlinkat		1287
#define __NR_renameat		1288
#define __NR_linkat		1289
#define __NR_symlinkat		1290
#define __NR_readlinkat		1291
#define __NR_fchmodat		1292
#define __NR_faccessat		1293
#endif
#if 0
#ifndef __NR_pselect6
#define __NR_pselect6		1294
#define __NR_ppoll		1295
#endif
#endif
#ifndef __NR_unshare
#define __NR_unshare		1296
#endif
#ifndef __NR_splice
#define __NR_splice		1297
#endif
#ifndef __NR_set_robust_list
#define __NR_set_robust_list	1298
#define __NR_get_robust_list	1299
#endif
#ifndef __NR_sync_file_range
#define __NR_sync_file_range	1300
#endif
#ifndef __NR_tee
#define __NR_tee		1301
#endif
#ifndef __NR_vmsplice
#define __NR_vmsplice		1302
#endif
%endif
%ifarch ppc
#ifndef __NR_utimes
#define __NR_utimes		251
#endif
#ifndef __NR_statfs64
#define __NR_statfs64		252
#define __NR_fstatfs64		253
#endif
#ifndef __NR_fadvise64_64
#define __NR_fadvise64_64	254
#endif
#ifndef __NR_mq_open
#define __NR_mq_open		262
#define __NR_mq_unlink		263
#define __NR_mq_timedsend	264
#define __NR_mq_timedreceive	265
#define __NR_mq_notify		266
#define __NR_mq_getsetattr	267
#endif
#ifndef __NR_waitid
#define __NR_waitid		272
#endif
#ifndef __NR_inotify_init
#define __NR_inotify_init	275
#define __NR_inotify_add_watch	276
#define __NR_inotify_rm_watch	277
#endif
#ifndef __NR_pselect6
#define __NR_pselect6		280
#define __NR_ppoll		281
#endif
#ifndef __NR_unshare
#define __NR_unshare		282
#endif
#ifndef __NR_splice
#define __NR_splice		283
#endif
#ifndef __NR_tee
#define __NR_tee		284
#endif
#ifndef __NR_vmsplice
#define __NR_vmsplice		285
#endif
#ifndef __NR_openat
#define __NR_openat		286
#define __NR_mkdirat		287
#define __NR_mknodat		288
#define __NR_fchownat		289
#define __NR_futimesat		290
#define __NR_fstatat64		291
#define __NR_unlinkat		292
#define __NR_renameat		293
#define __NR_linkat		294
#define __NR_symlinkat		295
#define __NR_readlinkat		296
#define __NR_fchmodat		297
#define __NR_faccessat		298
#endif
%endif
%ifarch ppc64
#ifndef __NR_utimes
#define __NR_utimes		251
#endif
#ifndef __NR_mq_open
#define __NR_mq_open		262
#define __NR_mq_unlink		263
#define __NR_mq_timedsend	264
#define __NR_mq_timedreceive	265
#define __NR_mq_notify		266
#define __NR_mq_getsetattr	267
#endif
#ifndef __NR_waitid
#define __NR_waitid		272
#endif
#ifndef __NR_inotify_init
#define __NR_inotify_init	275
#define __NR_inotify_add_watch	276
#define __NR_inotify_rm_watch	277
#endif
#ifndef __NR_pselect6
#define __NR_pselect6		280
#define __NR_ppoll		281
#endif
#ifndef __NR_unshare
#define __NR_unshare		282
#endif
#ifndef __NR_splice
#define __NR_splice		283
#endif
#ifndef __NR_tee
#define __NR_tee		284
#endif
#ifndef __NR_vmsplice
#define __NR_vmsplice		285
#endif
#ifndef __NR_openat
#define __NR_openat		286
#define __NR_mkdirat		287
#define __NR_mknodat		288
#define __NR_fchownat		289
#define __NR_futimesat		290
#define __NR_newfstatat		291
#define __NR_unlinkat		292
#define __NR_renameat		293
#define __NR_linkat		294
#define __NR_symlinkat		295
#define __NR_readlinkat		296
#define __NR_fchmodat		297
#define __NR_faccessat		298
#endif
%endif
%ifarch s390
#ifndef __NR_timer_create
#define __NR_timer_create	254
#define __NR_timer_settime	(__NR_timer_create+1)
#define __NR_timer_gettime	(__NR_timer_create+2)
#define __NR_timer_getoverrun	(__NR_timer_create+3)
#define __NR_timer_delete	(__NR_timer_create+4)
#define __NR_clock_settime	(__NR_timer_create+5)
#define __NR_clock_gettime	(__NR_timer_create+6)
#define __NR_clock_getres	(__NR_timer_create+7)
#define __NR_clock_nanosleep	(__NR_timer_create+8)
#endif
#ifndef __NR_fadvise64_64
#define __NR_fadvise64_64	264
#endif
#ifndef __NR_statfs64
#define __NR_statfs64		265
#define __NR_fstatfs64		266
#endif
#ifndef __NR_mq_open
#define __NR_mq_open		271
#define __NR_mq_unlink		272
#define __NR_mq_timedsend	273
#define __NR_mq_timedreceive	274
#define __NR_mq_notify		275
#define __NR_mq_getsetattr	276
#endif
#ifndef __NR_waitid
#define __NR_waitid		281
#endif
#ifndef __NR_inotify_init
#define __NR_inotify_init	284
#define __NR_inotify_add_watch	285
#define __NR_inotify_rm_watch	286
#endif
#ifndef __NR_openat
#define __NR_openat		288
#define __NR_mkdirat		289
#define __NR_mknodat		290
#define __NR_fchownat		291
#define __NR_futimesat		292
#define __NR_fstatat64		293
#define __NR_unlinkat		294
#define __NR_renameat		295
#define __NR_linkat		296
#define __NR_symlinkat		297
#define __NR_readlinkat		298
#define __NR_fchmodat		299
#define __NR_faccessat		300
#endif
#ifndef __NR_pselect6
#define __NR_pselect6		301
#define __NR_ppoll		302
#endif
#ifndef __NR_unshare
#define __NR_unshare		303
#endif
%endif
%ifarch s390x
#ifndef __NR_timer_create
#define __NR_timer_create	254
#define __NR_timer_settime	(__NR_timer_create+1)
#define __NR_timer_gettime	(__NR_timer_create+2)
#define __NR_timer_getoverrun	(__NR_timer_create+3)
#define __NR_timer_delete	(__NR_timer_create+4)
#define __NR_clock_settime	(__NR_timer_create+5)
#define __NR_clock_gettime	(__NR_timer_create+6)
#define __NR_clock_getres	(__NR_timer_create+7)
#define __NR_clock_nanosleep	(__NR_timer_create+8)
#endif
#ifndef __NR_mq_open
#define __NR_mq_open		271
#define __NR_mq_unlink		272
#define __NR_mq_timedsend	273
#define __NR_mq_timedreceive	274
#define __NR_mq_notify		275
#define __NR_mq_getsetattr	276
#endif
#ifndef __NR_waitid
#define __NR_waitid		281
#endif
#ifndef __NR_inotify_init
#define __NR_inotify_init	284
#define __NR_inotify_add_watch	285
#define __NR_inotify_rm_watch	286
#endif
#ifndef __NR_openat
#define __NR_openat		288
#define __NR_mkdirat		289
#define __NR_mknodat		290
#define __NR_fchownat		291
#define __NR_futimesat		292
#define __NR_newfstatat		293
#define __NR_unlinkat		294
#define __NR_renameat		295
#define __NR_linkat		296
#define __NR_symlinkat		297
#define __NR_readlinkat		298
#define __NR_fchmodat		299
#define __NR_faccessat		300
#endif
#ifndef __NR_pselect6
#define __NR_pselect6		301
#define __NR_ppoll		302
#endif
#ifndef __NR_unshare
#define __NR_unshare		303
#endif
%endif
%ifarch sparc sparcv9 sparc64
#ifndef __NR_mq_open
#define __NR_mq_open		273
#define __NR_mq_unlink		274
#define __NR_mq_timedsend	275
#define __NR_mq_timedreceive	276
#define __NR_mq_notify		277
#define __NR_mq_getsetattr	278
#endif
#ifndef __NR_waitid
#define __NR_waitid		279
#endif
#ifndef __NR_stat64
#define __NR_fstat64		63
#define __NR_lstat64		132
#define __NR_stat64		139
#endif
#ifndef __NR_inotify_init
#define __NR_inotify_init	151
#define __NR_inotify_add_watch	152
#define __NR_inotify_rm_watch	156
#endif
#ifndef __NR_openat
#define __NR_openat		284
#define __NR_mkdirat		285
#define __NR_mknodat		286
#define __NR_fchownat		287
#define __NR_futimesat		288
#define __NR_newfstatat		289
#define __NR_unlinkat		290
#define __NR_renameat		291
#define __NR_linkat		292
#define __NR_symlinkat		293
#define __NR_readlinkat		294
#define __NR_fchmodat		295
#define __NR_faccessat		296
#endif
#ifndef __NR_pselect6
#define __NR_pselect6		297
#define __NR_ppoll		298
#endif
#ifndef __NR_unshare
#define __NR_unshare		299
#endif
%endif
%ifarch x86_64
#ifndef __NR_mq_open
#define __NR_mq_open		240
#define __NR_mq_unlink		241
#define __NR_mq_timedsend	242
#define __NR_mq_timedreceive	243
#define __NR_mq_notify		244
#define __NR_mq_getsetattr	245
#endif
#ifndef __NR_waitid
#define __NR_waitid		247
#endif
#ifndef __NR_inotify_init
#define __NR_inotify_init	253
#define __NR_inotify_add_watch	254
#define __NR_inotify_rm_watch	255
#endif
#ifndef __NR_openat
#define __NR_openat		257
#define __NR_mkdirat		258
#define __NR_mknodat		259
#define __NR_fchownat		260
#define __NR_futimesat		261
#define __NR_newfstatat		262
#define __NR_unlinkat		263
#define __NR_renameat		264
#define __NR_linkat		265
#define __NR_symlinkat		266
#define __NR_readlinkat		267
#define __NR_fchmodat		268
#define __NR_faccessat		269
#endif
#ifndef __NR_pselect6
#define __NR_pselect6		270
#define __NR_ppoll		271
#endif
#ifndef __NR_unshare
#define __NR_unshare		272
#endif
#ifndef __NR_set_robust_list
#define __NR_set_robust_list	273
#define __NR_get_robust_list	274
#endif
#ifndef __NR_splice
#define __NR_splice		275
#endif
#ifndef __NR_tee
#define __NR_tee		276
#endif
#ifndef __NR_sync_file_range
#define __NR_sync_file_range	277
#endif
#ifndef __NR_vmsplice
#define __NR_vmsplice		278
#endif
%endif
#endif
EOF
cat > override_headers/asm/errno.h <<EOF
#ifndef _HACK_ASM_ERRNO_H
#include_next <asm/errno.h>
%ifarch alpha
#ifndef ENOKEY
#define ENOKEY		132
#define EKEYEXPIRED	133
#define EKEYREVOKED	134
#define EKEYREJECTED	135
#endif
#ifndef EOWNERDEAD
#define EOWNERDEAD	136
#define ENOTRECOVERABLE	137
#endif
%endif
%ifarch %{ix86} ia64 ppc ppc64 s390 s390x x86_64
#ifndef ENOKEY
#define ENOKEY		126
#define EKEYEXPIRED	127
#define EKEYREVOKED	128
#define EKEYREJECTED	129
#endif
#ifndef EOWNERDEAD
#define EOWNERDEAD	130
#define ENOTRECOVERABLE	131
#endif
%endif
%ifarch sparc sparcv9 sparc64
#ifndef ENOKEY
#define ENOKEY		128
#define EKEYEXPIRED	129
#define EKEYREVOKED	130
#define EKEYREJECTED	131
#endif
#ifndef EOWNERDEAD
#define EOWNERDEAD	132
#define ENOTRECOVERABLE	133
#endif
%endif
#endif
EOF

# A lot of programs still misuse memcpy when they have to use
# memmove. The memcpy implementation below is not tolerant at
# all.
rm -f sysdeps/alpha/alphaev6/memcpy.S

%build
cp -f /usr/share/automake/config.sub scripts
%{__aclocal}
%{__autoconf}

rm -rf builddir
install -d builddir
cd builddir
%ifarch sparc64
CC="%{__cc} -m64 -mcpu=ultrasparc -mvis -fcall-used-g6"
%endif
AWK="gawk" \
../%configure \
	--enable-kernel="%{min_kernel}" \
	--enable-omitfp \
	--with-headers=`cd ..; pwd`/override_headers:%{_includedir} \
	--with%{!?with_selinux:out}-selinux \
	--with-tls \
	--enable-add-ons=nptl,libidn \
	--enable-stackguard-randomization \
	--enable-hidden-plt \
	--enable-profile

%{__make}
cd ..

%if %{with tests}
for d in builddir; do
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

%if !%{with cross}
diet %{__cc} %{SOURCE7} %{rpmcflags} -Os -static -o glibc-postinst
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
cd ..

%if !%{with cross}
install glibc-postinst				$RPM_BUILD_ROOT/sbin
%endif

%{?with_memusage:mv -f $RPM_BUILD_ROOT/%{_lib}/libmemusage.so $RPM_BUILD_ROOT%{_libdir}}
mv -f $RPM_BUILD_ROOT/%{_lib}/libpcprofile.so	$RPM_BUILD_ROOT%{_libdir}

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/localtime
# moved to tzdata package
rm -rf $RPM_BUILD_ROOT%{_datadir}/zoneinfo

ln -sf libbsd-compat.a		$RPM_BUILD_ROOT%{_libdir}/libbsd.a

# make symlinks across top-level directories absolute
for l in anl BrokenLocale crypt dl m nsl resolv rt thread_db util ; do
	rm -f $RPM_BUILD_ROOT%{_libdir}/lib${l}.so
	ln -sf /%{_lib}/`cd $RPM_BUILD_ROOT/%{_lib} ; echo lib${l}.so.*` $RPM_BUILD_ROOT%{_libdir}/lib${l}.so
done

install %{SOURCE2}		$RPM_BUILD_ROOT/etc/rc.d/init.d/nscd
install %{SOURCE3}		$RPM_BUILD_ROOT/etc/sysconfig/nscd
install %{SOURCE4}		$RPM_BUILD_ROOT/etc/logrotate.d/nscd
install nscd/nscd.conf		$RPM_BUILD_ROOT%{_sysconfdir}
sed -e 's#\([ \t]\)db\([ \t]\)#\1#g' nss/nsswitch.conf > $RPM_BUILD_ROOT%{_sysconfdir}/nsswitch.conf
install posix/gai.conf		$RPM_BUILD_ROOT%{_sysconfdir}

bzip2 -dc %{SOURCE5} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}
> $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.cache
install -d $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
echo 'include ld.so.conf.d/*.conf' > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf
rm -f $RPM_BUILD_ROOT%{_mandir}/hu/man7/man.7

:> $RPM_BUILD_ROOT/var/log/nscd
:> $RPM_BUILD_ROOT/var/lib/nscd/passwd
:> $RPM_BUILD_ROOT/var/lib/nscd/group
:> $RPM_BUILD_ROOT/var/lib/nscd/hosts

rm -rf documentation
install -d documentation

for f in ANNOUNCE ChangeLog DESIGN-{barrier,condvar,rwlock,sem}.txt TODO{,-kernel,-testing}; do
	cp -f nptl/$f documentation/$f.nptl
done
cp -f crypt/README.ufc-crypt ChangeLog* documentation

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
# az_IR (gtk+)
# gn (gn_BR in gnome, maybe gn_PY)
# dv, haw, kok, ps (iso-codes)
# my (gaim)
#
# NOTES:
# what about sr@ije? it used to be sr_CS@ije (should be @[i]jekavian?), but
# now this dialect uses sr_ME locale - rename dir to sr_ME?
#
# bn is used for bn_BD or bn_IN? Assume bn_IN as nothing for bn_BD appeared
#   till now
#
# omitted here - already existing (with libc.mo):
#   be,ca,cs,da,de,el,en_GB,es,fi,fr,gl,hr,hu,it,ja,ko,nb,nl,pl,pt_BR,sk,sv,
#   tr,zh_CN,zh_TW
#
for i in aa af am ang ar as az bg bn bn_IN br bs byn cy de_AT dz en en@boldquot \
    en@quot en_AU en_CA en_US eo es_AR es_MX es_NI et eu fa fo fr_BE fy ga \
    gez gu gv he hi hsb hy ia id is it_CH iu ka kk kl km kn ku kw ky leet lg li \
    lo lt lv mg mi mk ml mn mr ms mt nds ne nl_BE nn nso oc om or pa pt rm ro \
    ru rw sa se si sid sl so sq sr sr@Latn sr@ije ss syr sw ta te tg th ti tig \
    tk tl tlh tt ug uk ur uz ve vi wa wal wo xh yi yo zh_HK zu ; do
	if [ ! -d $RPM_BUILD_ROOT%{_datadir}/locale/$i/LC_MESSAGES ]; then
		install -d $RPM_BUILD_ROOT%{_datadir}/locale/$i/LC_MESSAGES
		lang=`echo $i | sed -e 's/_.*//'`
		echo "%lang($lang) %{_datadir}/locale/$i" >> glibc.lang
	fi
done

# localedb-gen infrastructure
sed -e 's,@localedir@,%{_libdir}/locale,' %{SOURCE6} > $RPM_BUILD_ROOT%{_bindir}/localedb-gen
chmod +x $RPM_BUILD_ROOT%{_bindir}/localedb-gen
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

%if !%{with cross}
%post	-p /sbin/postshell
/sbin/glibc-postinst /%{_lib}/%{_host_cpu}
/sbin/ldconfig
-/sbin/telinit u

%postun	-p /sbin/postshell
/sbin/ldconfig
-/sbin/telinit u

%triggerpostun -p /sbin/postshell -- glibc-misc < 6:2.3.5-7.6
-/bin/cp -f /etc/ld.so.conf /etc/ld.so.conf.rpmsave
-/bin/sed -i -e '1iinclude ld.so.conf.d/*.conf' /etc/ld.so.conf
%endif

%post	memusage -p /sbin/ldconfig
%postun	memusage -p /sbin/ldconfig

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

%files
%defattr(644,root,root,755)
%doc README NEWS FAQ BUGS
%if !%{with cross}
%attr(755,root,root) /sbin/glibc-postinst
%endif
%attr(755,root,root) /sbin/ldconfig
# ld* and libc.so.6 SONAME symlinks must be in package because of
# chicken-egg problem (postshell is dynamically linked with libc);
# NOTE: postshell is now linked statically with diet
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
%{?with_localedb:%dir %{_libdir}/locale}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ld.so.conf
%dir %{_sysconfdir}/ld.so.conf.d
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
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/gai.conf

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
%ifarch alpha ppc sparc
%{_libdir}/libnldbl_nonshared.a
%endif
%{_libdir}/libpthread_nonshared.a
%{_libdir}/librpcsvc.a
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

%files profile
%defattr(644,root,root,755)
%{_libdir}/lib*_p.a

%files pic
%defattr(644,root,root,755)
%{_libdir}/lib*_pic.a
%{_libdir}/lib*.map
%{_libdir}/soinit.o
%{_libdir}/sofini.o
