Name:		motorcar
Version:	v0.1
Release:	01%{?dist}
Summary:	Motorcar is a true 3d compositor built using wayland and qt.

Group:		Motorcar
License:	MIT
URL:		https://github.com/evil0sheep/motorcar
Source0:	http://thegreatpissant.com/repos/motorcar/motorcar-v0.1.tar.gz
Source1:	ovr_sdk_linux_0.2.3.tar.gz  
Source2:	sixenseSDK_linux_OSX.zip

#BuildRequires:	
#Requires:	

%description
Motorcar is a true 3D compositor built utilizing wayland and qt.  Offering a 
VR experince for your desktop and applications.

%package libs
Summary: Libs for motorcar
%description libs
%{summary}.

%package rift-hydra-compositor
Summary: example rift-hydra-compositor for motorcar
%description rift-hydra-compositor
%{summary}.

%package simple-compositor
Summary: example simple-compositor for motorcar
%description simple-compositor
%{summary}.


%package simple-egl-client
Summary: simple-egl-client example for motorcar
%description simple-egl-client
%{summary}.

%prep
%setup -q
tar -xf %{_sourcedir}/ovr_sdk_linux_0.2.3.tar.gz -C %{_builddir}/
unzip %{_sourcedir}/sixenseSDK_linux_OSX.zip -d %{_builddir}/

%build
##  Motorcar libs  ##
qmake-qt5 
make #%{?_smp_mflags} 


##  Motorcar Example Compositors ##
cd src/examples/compositors/rift-hydra-compositor
#make %{?_smp_mflags} LIBOVRPATH=%{_builddir}/OculusSDK/LibOVR SIXENSEPATH=%{_builddir}/sixenseSDK_linux_OSX MOTORCAR_DIR=%{_builddir}/motorcar-v0.1
make LIBOVRPATH=%{_builddir}/OculusSDK/LibOVR SIXENSEPATH=%{_builddir}/sixenseSDK_linux_OSX MOTORCAR_DIR=%{_builddir}/motorcar-v0.1
cd ../simple-compositor
make MOTORCAR_DIR=%{_builddir}/motorcar-v0.1

##  Motorcar Example Applications ##
cd ../../clients/simple-egl
make #%{?_smp_mflags} 

%install
#make install INSTALL_ROOT=%{buildroot}
rm -fr %{buildroot}
mkdir -p %{buildroot}/usr/lib64/motorcar
mkdir -p %{buildroot}/usr/sbin
cp -p %{_builddir}/motorcar-v0.1/lib/libmotorcar-compositor.so.1.0.0 %{buildroot}/usr/lib64/motorcar/
cp -p %{_builddir}/motorcar-v0.1/src/protocol/motorcar-client-protocol.h %{buildroot}/usr/lib64/motorcar/
cp -p %{_builddir}/motorcar-v0.1/src/protocol/motorcar-server-protocol.h %{buildroot}/usr/lib64/motorcar/
cp -p %{_builddir}/motorcar-v0.1/src/protocol/motorcar-wayland-extensions.c %{buildroot}/usr/lib64/motorcar/
cd %{buildroot}/usr/lib64/motorcar/
ln libmotorcar-compositor.so.1.0.0 libmotorcar-compositor.so.1.0
ln libmotorcar-compositor.so.1.0.0 libmotorcar-compositor.so.1
ln libmotorcar-compositor.so.1.0.0 libmotorcar-compositor.so
cd -
cp -p %{_builddir}/motorcar-v0.1/src/examples/compositors/rift-hydra-compositor/rift-hydra-compositor %{buildroot}/usr/sbin/
cp -p %{_builddir}/motorcar-v0.1/src/examples/compositors/simple-compositor/simple-compositor %{buildroot}/usr/sbin/
cp -p %{_builddir}/motorcar-v0.1/src/examples/clients/simple-egl/motorcar-demo-client %{buildroot}/usr/sbin/

mkdir -p %{buildroot}/etc/ld.so.conf.d/
echo /usr/lib64/motorcar >> %{buildroot}/etc/ld.so.conf.d/motorcar.x86_64.conf

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files

%dir /usr/lib64/motorcar
/usr/lib64/motorcar/libmotorcar-compositor.so.1.0.0
/usr/lib64/motorcar/libmotorcar-compositor.so.1.0
/usr/lib64/motorcar/libmotorcar-compositor.so.1
/usr/lib64/motorcar/libmotorcar-compositor.so
/usr/lib64/motorcar/motorcar-client-protocol.h
/usr/lib64/motorcar/motorcar-server-protocol.h
/usr/lib64/motorcar/motorcar-wayland-extensions.c
/etc/ld.so.conf.d/motorcar.x86_64.conf

%files rift-hydra-compositor
/usr/sbin/rift-hydra-compositor

%files simple-compositor
/usr/sbin/simple-compositor

%files simple-egl-client
/usr/sbin/motorcar-demo-client

%doc



%changelog
* Sun Jun 7 2015 James A. Feister <thegreatpissant@gmail.com> 0.1 
- init
