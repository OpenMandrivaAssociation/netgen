Name:		netgen
Group:		Sciences/Physics
Version:	4.9.13
Release:	3
Summary:	Automatic 3d tetrahedral mesh generator
License:	GPL
URL:		https://www.hpfem.jku.at/netgen/
Source0:	%{name}-%{version}.tar.gz
Patch0:		netgen-4.9.13-togl.patch
Patch1:		netgen-4.9.13-opencascade.patch

BuildRequires:	pkgconfig(glu)
BuildRequires:	opencascade
BuildRequires:	opencascade-devel
BuildRequires:	openmpi-devel
BuildRequires:	tcl-devel
BuildRequires:	tk-devel
BuildRequires:	togl
Requires:	tix

%description
NETGEN is an automatic 3d tetrahedral mesh generator. It accepts input from
constructive solid geometry (CSG) or boundary representation (BRep) from STL
file format. The connection to a geometry kernel allows the handling of IGES
and STEP files. NETGEN contains modules for mesh optimization and hierarchical
mesh refinement. Netgen is open source based on the LGPL license. It is
available for Unix/Linux and Windows.

NETGEN was developed mainly by Joachim Schöberl within project grants from
the Austrian Science Fund FWF ( Special Research Project "Numerical and
Symbolic Scientific Computing", Start Project "hp-FEM) at the Johannes
Kepler University Linz. Significant contributions were made by Johannes
Gerstmayr (STL geometry) Robert Gaisbauer (OpenCascade interface).

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure2_5x --with-occ=%{_datadir}/opencascade
%make

%install
%makeinstall_std

mkdir -p %{buildroot}%{_datadir}/%{name}/tutorials
mv -f %{buildroot}%{_datadir}/%{name}/*.{geo,in2d,step,stl,surf} %{buildroot}%{_datadir}/%{name}/tutorials
mv -f %{buildroot}%{_bindir}/* %{buildroot}%{_datadir}/%{name}
cat > %{buildroot}%{_bindir}/%{name} << EOF
#!/bin/sh

export NETGENDIR=%{_datadir}/%{name}
export PATH=\$NETGENDIR:\$PATH
[ -z "\$NETGEN_USER_DIR" ] && export NETGEN_USER_DIR=\$HOME
\$NETGENDIR/%{name} "\$@"
EOF
chmod +x %{buildroot}%{_bindir}/%{name}

%files
%{_bindir}/*
%{_includedir}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%dir %{_docdir}/%{name}/
%{_docdir}/%{name}/*
%{_libdir}/*.so

