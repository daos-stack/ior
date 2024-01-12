%if (0%{?suse_version} >= 1500)
%global module_load() MODULEPATH=/usr/share/modules module load gnu-%{1}
%else
%global module_load() module load mpi/%{1}-%{_arch}
%endif

%global shortcommit %(c=%{commit};echo ${c:0:7})

Name:		ior
Version:	4.0.0
Release:	1%{?commit:.g%{shortcommit}}%{?dist}

Summary:	IOR-HPC

License:	GPL
URL:		https://github.com/hpc/%{name}/
Source0:    https://github.com/hpc/%{name}/releases/download/%{version}/%{name}-%{version}.tar.gz
%if "%{?commit}" != ""
Patch1: %{version}..%{commit}.patch
%endif
Patch3: daos-configure.patch

BuildRequires: mpich-devel
BuildRequires: hwloc-devel
BuildRequires: libevent-devel
BuildRequires: unzip
BuildRequires: autoconf, automake
BuildRequires: daos-devel
BuildRequires: hdf5-mpich-devel%{?_isa}
BuildRequires: mercury-devel
BuildRequires: chrpath
%if (0%{?suse_version} >= 1500)
BuildRequires: lua-lmod
%else
BuildRequires: Lmod
%endif

Obsoletes: mdtest < 2.0.0
Provides: mdtest = %{version}-%{release}
Provides: ior-hpc = %{version}-%{release}

%description
IOR-HPC

%if (0%{?suse_version} > 0)
%global __debug_package 1
%global _debuginfo_subpackages 0
%debug_package
%endif

%prep
%autosetup -p1
# we patched configure.ac
autoreconf

%build
export CC=mpicc
export CXX=mpicxx
export FC=mpif90
export F77=mpif77
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -fPIC"
export CXXFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -fPIC"
if [ ! -f configure ]; then
    # probably a git tarball
    ./bootstrap
fi

%module_load mpich
%if (0%{?suse_version} >= 1)
%configure --with-mpiio --with-daos=/usr --with-hdf5
%else
%configure --with-mpiio --with-daos=/usr --with-hdf5 --bindir=$MPI_BIN --mandir=$MPI_MAN --libdir=$MPI_LIB --includedir=$MPI_INCLUDE --datadir=%{_datadir}/doc/ior-mpich
%endif
%make_build

%install
%module_load mpich
%make_install

%if 0%{?suse_version}
MPI_LIB=%{_libdir}
MPI_BIN=%{_bindir}
mkdir -p %{buildroot}/%{_defaultdocdir}/%{name}/
mv %{buildroot}/usr/share/USER_GUIDE %{buildroot}%{_defaultdocdir}/%{name}/
%endif
chrpath --delete %{buildroot}/$MPI_BIN/{ior,md-workbench,mdtest}
rm -f %{buildroot}/$MPI_LIB/libaiori.a

%if (0%{?suse_version} < 1)
cat <<EOF >> files.mpich
$MPI_BIN/*
$MPI_MAN/man1/*
%{_datadir}/doc/ior-mpich/*
EOF
%endif


%if (0%{?suse_version} >= 1)
%files
%{_bindir}/*
%{_defaultdocdir}/%{name}/
%{_mandir}/man1/*
%else
%files -f files.mpich
%endif

%changelog
* Fri Jan 12 2024 Dalton A. Bohning <dalton.bohning@intel.com> - 4.0.0-1
- Update to 4.0.0 release

* Tue Jul 04 2023 Brian J. Murrell <brian.murrell@intel.com> - 3.3.0-20
- Add BR: mercury-devel
- Remove static library
- Set compiler environment variables

* Fri Mar 18 2022 Brian J. Murrell <brian.murrell@intel.com> - 3.3.0-19
- Update to d3574d536643475269d37211e283b49ebd6732d7

* Mon Mar 14 2022 Mohamad Chaarawi <mohamad.chaarawi@intel.com> - 3.3.0-18
- Update to build with HDF5 1.13.1

* Fri Dec 17 2021 Phillip Henderson <phillip.henderson@intel.com> - 3.3.0-17
- Enable building debuginfo package on SUSE platforms

* Fri Nov 12 2021 Wang Shilong <shilong.wang@intel.com> - 3.3.0-16
- Rebuilt for breaking DAOS API change

* Mon Nov 08 2021 Brian J. Murrell <brian.murrell@intel.com> - 3.3.0-15
- Update to eca135ce939e24c17a3a4a4b490c741bead43363

* Wed May 12 2021 Brian J. Murrell <brian.murrell@intel.com> - 3.3.0-14
- Build on EL8
- Temporarily add BR: libuuid-devel until daos-devel is fixed to R: it
- Install into environment-modules mpi-stack specific prefix on non-SUSE O/Ses

* Wed Jan 20 2021 Kenneth Cain <kenneth.c.cain@intel.com> - 3.3.0-13
- update to build with daos major api version 1

* Sat Nov 7 2020 Maureen Jean <maureen.jean@intel.com> - 3.3.0-12
- update to build with latest hdf5

* Tue Nov 03 2020 Mohamad Chaarawi <mohamad.chaarawi@intel.com> - 3.3.0-11
- Update to latest master to remove the legacy DAOS driver

* Mon Aug 17 2020 Maureen Jean <maureen.jean@intel.com> - 3.3.0-10
- Build with hdf5

* Tue May 26 2020 Brian J. Murrell <brian.murrell@intel.com> - 3.3.0-9
- Use lua-lmod for SLES/Leap 15.x

* Tue Dec 17 2019 Brian J. Murrell <brian.murrell@intel.com> - 3.3.0-8
- Rebuild with CaRT SO version 4
- Add Provides: to allow consumers to target cart and daos ABI versions

* Tue Dec 10 2019 Brian J. Murrell <brian.murrell@intel> -3.3.0-7
- Build on Leap 15.1

* Tue Nov 12 2019 Brian J. Murrell <brian.murrell@intel> -3.3.0-6
- Force rebuild to pick up cart/ompi changes

* Thu Nov 07 2019 Brian J. Murrell <brian.murrell@intel> -3.3.0-5
- Rebuild after repo mishap

* Thu Oct 31 2019 Brian J. Murrell <brian.murrell@intel> -3.3.0-4
- Use -dev version path

* Fri Jul 05 2019 Brian J. Murrell <brian.murrell@intel> -3.3.0-3
- Remove the BR for ompi-devel
- install mpi/mpich-x86_64 in the build environment

* Wed Jun 19 2019 Brian J. Murrell <brian.murrell@intel> -3.2.0-2
- Use daos-devel installed on the system
- Add daos-devel and cart-devel as BR
- Disable openmpi build option

* Mon Jan 21 2019 Brian J. Murrell <brian.murrell@intel> -3.2.0-1
- Initial package
