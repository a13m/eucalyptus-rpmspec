%global axis2c_home       %{_libdir}/wso2-axis2
%global axis2c_services   %{_libdir}/%{name}/axis2
%global eucalibexecdir    %{_libexecdir}/%{name}
%global eucadatadir       %{_datadir}/%{name}
%global eucajavalibdir    %{_datadir}/%{name}
%global helperdir         %{_datadir}/%{name}
%global gittag            b8c109b4
%global with_axis2v14     0
%global _hardened_build   1

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary:       Elastic Utility Computing Architecture
Name:          eucalyptus
Version:       3.1.2
Release:       0.4.20120917git%{gittag}%{?dist}
License:       GPLv3 and (GPLv3 and ASL 2.0) and (GPLv3 and BSD)
URL:           http://www.eucalyptus.com
Group:         Applications/System

BuildRequires: help2man
BuildRequires: java-devel >= 1:1.6.0
BuildRequires: jpackage-utils
BuildRequires: libvirt-devel >= 0.6
BuildRequires: libxslt-devel
BuildRequires: openssl-devel
BuildRequires: python-boto >= 2.1
BuildRequires: python-devel
BuildRequires: python-setuptools
BuildRequires: swig
BuildRequires: wso2-axis2-devel
BuildRequires: wso2-rampart-devel
BuildRequires: wso2-wsf-cpp-devel
BuildRequires: iscsi-initiator-utils
BuildRequires: curl-devel
BuildRequires: systemd-units

BuildRequires: activemq-core
BuildRequires: ant >= 1.7
BuildRequires: antlr-tool
BuildRequires: apache-commons-codec
BuildRequires: apache-commons-compress
BuildRequires: apache-commons-fileupload
BuildRequires: apache-commons-io
BuildRequires: apache-commons-lang
BuildRequires: axiom
# BuildRequires: axis2
BuildRequires: backport-util-concurrent
BuildRequires: batik
BuildRequires: bcel
BuildRequires: bouncycastle
BuildRequires: btm
BuildRequires: dnsjava
# Should be a json-lib Requires
BuildRequires: ezmorph
BuildRequires: geronimo-jta
BuildRequires: groovy
BuildRequires: guava >= 9
BuildRequires: ha-jdbc
BuildRequires: hamcrest12
BuildRequires: hibernate3
BuildRequires: hibernate3-ehcache
BuildRequires: hibernate3-entitymanager
BuildRequires: hibernate3-jbosscache
BuildRequires: hibernate3-proxool
BuildRequires: hibernate-jpa-2.0-api
BuildRequires: jakarta-commons-httpclient
# NOTE: jasperreports is not yet used, but will be soon
BuildRequires: jasperreports 
BuildRequires: javamail
BuildRequires: jetty
BuildRequires: jgroups212
BuildRequires: jibx
BuildRequires: jsch
BuildRequires: json-lib
BuildRequires: junit
BuildRequires: log4j
BuildRequires: mule-module-builders
BuildRequires: mule-module-client
BuildRequires: mule-module-xml
BuildRequires: mule-transport-vm
BuildRequires: netty31
BuildRequires: springframework-context-support
BuildRequires: springframework-web
BuildRequires: tomcat-servlet-3.0-api
BuildRequires: velocity
BuildRequires: woodstox-core
BuildRequires: wsdl4j
BuildRequires: wss4j
BuildRequires: xalan-j2
BuildRequires: xml-commons-apis
BuildRequires: xml-security
# Should be a json-lib Requires
BuildRequires: xom

%if %with_axis2v14
BuildRequires: axis2v14
%endif

Requires:      vconfig
Requires:      wget
Requires:      rsync
Requires:      which
Requires:      libselinux-python
Requires:      perl(Crypt::OpenSSL::RSA)
Requires:      perl(Crypt::OpenSSL::Random)
Requires:      sudo
Requires(pre):  %{_sbindir}/groupadd
Requires(pre):  %{_sbindir}/useradd
Requires(post): %{_sbindir}/euca_conf

# git clone https://github.com/eucalyptus/eucalyptus.git; cd eucalyptus
# git archive --prefix=eucalyptus-3.1.2gitb8c109b4/ -o eucalyptus-3.1.2gitb8c109b4.tar.gz b8c109b4
Source0:       eucalyptus-%{version}git%{gittag}.tar.gz
# A version of WSDL2C.sh that respects standard classpaths
Source1:       euca-WSDL2C.sh
Source2:       eucalyptus-jarlinks.txt

# XXX: these system units should go in the source tree
Source3:       eucalyptus-cloud.service
Source4:       eucalyptus-cc.service
Source5:       eucalyptus-nc.service

# These are sources that greatly simplify CC/NC startup,
# Removing dynamic config file generation and needless
# guesswork about where axis2 files are.
Source6:       axis2.xml
Source7:       eucalyptus-cc.init
Source8:       eucalyptus-nc.init
# Note that these needed to be adapted for httpd 2.4
# See http://httpd.apache.org/docs/2.4/upgrading.html
Source9:       httpd-cc.conf
Source10:      httpd-nc.conf
Source11:      httpd-common.conf

# Axis2/Java code generation is broken with v1.6
# To regenerate this code:
# 1) yum install http://arg.fedorapeople.org/axis2v14/noarch/axis2v14-1.4.1-1.fc18.noarch.rpm
# 2) Set with_axis2v14 to 1
# 3) fedpkg prep
# 4) pushd eucalyptus-<version>git<tag>
# 5) run configure from this spec (use rpmspec to fill in macros)
# 6) for x in gatherlog cluster node; do pushd $x; make generated/stubs; popd; done
# 7) popd
# 8) tar czf eucalyptus-<version>git<tag>-generated.tgz \
#            eucalyptus-<version>git<tag>/{node,cluster,gatherlog}/generated
%if !%with_axis2v14
Source12:      eucalyptus-%{version}git%{gittag}-generated.tgz
%endif

# Add a separate "clean" script for the CC
Source13:      eucalyptus-clean-cc

# Add a new-style polkit rule
Source14:      eucalyptus-nc-libvirt.rules

# Add tmpfiles config
Source15:      eucalyptus.tmpfiles

# https://eucalyptus.atlassian.net/browse/EUCA-2364
Patch0:        eucalyptus-jdk7.patch
# https://eucalyptus.atlassian.net/browse/EUCA-3253
Patch2:        eucalyptus-jetty8.patch
# https://eucalyptus.atlassian.net/browse/EUCA-2993
Patch4:        eucalyptus-groovy18.patch

# Three separate patches to disable gwt
Patch9:        eucalyptus-disable-gwt.patch
Patch10:        eucalyptus-disable-gwt-in-buildxml.patch
Patch11:        eucalyptus-disable-gwt-in-makefile.patch

# Make install paths configurable
# https://eucalyptus.atlassian.net/browse/EUCA-3531
Patch13:       eucalyptus-configurable-paths.patch

# Make one repo per service of Axis2 services
Patch14:       eucalyptus-axis2-services.patch

# Fix rootwrap path in python files 
Patch15:       eucalyptus-rootwrap-python.patch

# Fix include location for axis2 libs
Patch16:       eucalyptus-wso2-axis2-configure.patch

# Use System.load with an absolute path for JNI lib load
Patch18:       eucalyptus-jni-abspath.patch

# Move version file out of /etc
Patch20:       eucalyptus-move-version-file.patch

# Respect LDFLAGS when building setuid binaries
Patch21:       eucalyptus-respect-ldflags.patch

%description
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains the common parts; you will need to install at
least one of the cloud controller (cloud), cluster controller (cc),
node controller (nc), storage controller (sc), or walrus packages as well.

%package common-java
Summary:      Elastic Utility Computing Architecture - ws java stack
Requires:     %{name} = %{version}-%{release}
Requires:     jpackage-utils
Requires:     java >= 1:1.6.0
Requires:     lvm2
Requires:     activemq-core
Requires:     ant
Requires:     antlr-tool
Requires:     apache-commons-codec
Requires:     apache-commons-collections
Requires:     apache-commons-compress
Requires:     apache-commons-fileupload
Requires:     apache-commons-io
Requires:     axiom
Requires:     backport-util-concurrent
Requires:     batik
Requires:     bcel
Requires:     bouncycastle
Requires:     btm
Requires:     dnsjava
Requires:     dom4j
Requires:     ezmorph
Requires:     geronimo-jms
Requires:     geronimo-jta
Requires:     groovy
Requires:     guava >= 9
Requires:     ha-jdbc
Requires:     hamcrest12
Requires:     hibernate3
Requires:     hibernate3-ehcache
Requires:     hibernate3-entitymanager
Requires:     hibernate3-jbosscache
Requires:     hibernate3-proxool
Requires:     hibernate-commons-annotations
Requires:     hibernate-jpa-2.0-api
Requires:     jakarta-commons-httpclient
Requires:     jasperreports
Requires:     javamail
Requires:     jetty
Requires:     jgroups212
Requires:     jibx
Requires:     jsch
Requires:     json-lib
Requires:     jsr-305
Requires:     log4j
Requires:     mule-module-builders
Requires:     mule-module-client
Requires:     mule-module-management
Requires:     mule-module-spring-config
Requires:     mule-module-xml
Requires:     mule-transport-vm
Requires:     mx4j
Requires:     netty31
Requires:     postgresql-jdbc
Requires:     proxool
Requires:     springframework-context-support
Requires:     springframework-web
Requires:     stax-utils
Requires:     tomcat-servlet-3.0-api
Requires:     velocity
Requires:     woodstox-core
Requires:     wsdl4j
Requires:     wss4j
Requires:     xalan-j2
Requires:     xml-commons-apis
Requires:     xml-security
Requires:     xom
Requires:     %{_sbindir}/euca_conf
Requires(preun): systemd-units
Requires(post): systemd-units

%description common-java
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains the java WS stack.

%package walrus
Summary:      Elastic Utility Computing Architecture - walrus
Requires:     %{name}             = %{version}-%{release}
Requires:     %{name}-common-java = %{version}-%{release}
Requires:     drbd-utils
Requires:     lvm2

%description walrus
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains storage component for your cloud: images and buckets
are handled by walrus. Typically this package is installed alongside the
cloud controller.

%package sc
Summary:      Elastic Utility Computing Architecture - storage controller
Requires:     %{name}             = %{version}-%{release}
Requires:     %{name}-common-java = %{version}-%{release}
Requires:     lvm2
Requires:     iscsi-initiator-utils
Requires:     scsi-target-utils

%description sc
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains the storage controller part of eucalyptus, which
handles the elastic blocks for a given cluster. Typically you install it
alongside the cluster controller.

%package cloud
Summary:      Elastic Utility Computing Architecture - cloud controller
Requires:     %{name}                     = %{version}-%{release}
Requires:     %{name}-common-java%{?_isa} = %{version}-%{release}
Requires:     euca2ools >= 2.0
Requires:     lvm2
Requires:     perl(Getopt::Long)
Requires:     postgresql
Requires:     postgresql-server

# For reporting web UI
# Requires:     dejavu-serif-fonts

%description cloud
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains the cloud controller part of eucalyptus. The cloud
controller needs to be reachable by both the cluster controller and from
the cloud clients.

%package cc
Summary:      Elastic Utility Computing Architecture - cluster controller
Requires:     %{name}    = %{version}-%{release}
Requires:     %{name}-gl = %{version}-%{release}
Requires:     bridge-utils
Requires:     iptables
Requires:     vtun
Requires:     dhcp
Requires:     httpd
Requires:     %{_sbindir}/euca_conf
Requires:     mod_wso2-axis2
# XXX: I wish this were not "devel", but some modules are being
# loaded without a version
Requires:     wso2-axis2-devel
Requires:     wso2-axis2-modules
Requires:     %{_sbindir}/euca_conf
Requires(preun): systemd-units
Requires(post): systemd-units

%description cc
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains the cluster controller part of eucalyptus. It
handles a group of node controllers.

%package nc
Summary:      Elastic Utility Computing Architecture - node controller
Requires:     %{name}    = %{version}-%{release}
Requires:     %{name}-gl = %{version}-%{release}
Requires:     bridge-utils
Requires:     device-mapper
Requires:     euca2ools >= 2.0
# The next six come from storage/diskutil.c, which shells out to lots of stuff.
Requires:     coreutils
Requires:     e2fsprogs
Requires:     file
Requires:     grub2
Requires:     parted
Requires:     util-linux
Requires:     curl
Requires:     httpd
Requires:     kvm
Requires:     iscsi-initiator-utils
Requires:     libvirt
Requires:     mod_wso2-axis2
# XXX: I wish this were not "devel", but some modules are being
# loaded without a version
Requires:     wso2-axis2-devel
Requires:     wso2-axis2-modules
Requires:     %{_sbindir}/euca_conf
Requires(preun): systemd-units
Requires(post): systemd-units

%description nc
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains the node controller part of eucalyptus. This
component handles instances.

%package gl
Summary:      Elastic Utility Computing Architecture - log service
Requires:     %{name} = %{version}-%{release}
Requires:     httpd

%description gl
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains the internal log service of eucalyptus.

%package admin-tools
Summary:      Elastic Utility Computing Architecture - admin CLI tools
License:      BSD
Requires:     %{name} = %{version}-%{release}
Requires:     python-eucadmin = %{version}-%{release}
Requires:     rsync
BuildArch:    noarch

%description admin-tools
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains command line tools necessary for managing a
Eucalyptus cluster.

%package -n python-eucadmin
Summary:      Elastic Utility Computing Architecture - administration Python library
License:      BSD
Requires:     PyGreSQL
Requires:     python-boto >= 2.1
Requires:     rsync
BuildArch:    noarch

%description -n python-eucadmin
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains the Python library used by Eucalyptus administration
tools.  It is neither intended nor supported for use by any other programs.

%package axis2-clients
Summary:      Axis2/C web service clients for Eucalyptus services
License:      GPLv3
Requires:     wso2-axis2
Requires:     %{name}-cc = %{version}-%{release}

%description axis2-clients
This package contains three debugging programs for testing Eucalyptus
components which run as Axis2/C webservices.

%prep
%setup -q -n %{name}-%{version}git%{gittag}
%if !%with_axis2v14
tar --strip-components=1 -xvzf %{SOURCE12}
touch gatherlog/generated/stubs cluster/generated/stubs node/generated/stubs
%endif
%patch0 -p1
%patch2 -p1
%patch4 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch18 -p1
%patch20 -p1
%patch21 -p1

# remove classes which depend on junit
# This is because junit on Fedora bundles hamcrest 1.1, which has conflicts
# with hamcrest 1.2.  And regardless, these should not be bundled into our
# production jars.
pushd clc/modules
rm core/src/main/java/edu/ucsb/eucalyptus/util/XMLParserTest.java
rm dns/src/main/java/com/eucalyptus/cloud/ws/tests/DNSControlTest.java
rm dns/src/main/java/com/eucalyptus/cloud/ws/tests/RemoveARecordTest.java
rm storage-controller/src/main/java/edu/ucsb/eucalyptus/cloud/ws/tests/CreateVolumeFromSnapshotTest.java
rm storage-controller/src/main/java/edu/ucsb/eucalyptus/cloud/ws/tests/StorageTests.java
rm storage-controller/src/main/java/edu/ucsb/eucalyptus/cloud/ws/tests/VolumeTest.java
rm storage-controller/src/main/java/edu/ucsb/eucalyptus/cloud/ws/tests/DeleteSnapshotTest.java
rm storage-controller/src/main/java/edu/ucsb/eucalyptus/cloud/ws/tests/CreateSnapshotTest.java
rm walrus/src/main/java/edu/ucsb/eucalyptus/cloud/ws/tests/ImageCacheTest.java
rm walrus/src/main/java/edu/ucsb/eucalyptus/cloud/ws/tests/BukkitImageTest.java
rm walrus/src/main/java/edu/ucsb/eucalyptus/cloud/ws/tests/BukkitTest.java
rm walrus/src/main/java/edu/ucsb/eucalyptus/cloud/ws/tests/ObjectTest.java
rm walrus/src/main/java/edu/ucsb/eucalyptus/cloud/ws/tests/WalrusBucketTests.java
popd

# Do not redistribute a binary floppy image
# We should have a script to reconstruct this
echo -n > tools/floppy

%build
export CFLAGS="%{optflags}"
export LDFLAGS="$RPM_LD_FLAGS"

# TODO: we should use %%configure now, except that "prefix" is still broken
# Also, helperdir sould be a config option, unless we decide that
# it's always eucadatadir
./configure --with-axis2=%{_datadir}/axis2-* \
            --with-axis2c=%{axis2c_home} \
            --with-axis2c-services=%{axis2c_services} \
            --with-wsdl2c-sh=%{SOURCE1} \
            --enable-debug \
            --prefix=/ \
            --sbindir=%{_sbindir} \
            --libexecdir=%{_libexecdir} \
            --libdir=%{_libdir} \
            --datarootdir=%{_datadir} \
            --localstatedir=%{_localstatedir} \
            --sysconfdir=%{_sysconfdir} \
            --with-apache2-module-dir=%{_libdir}/httpd/modules  \
            --with-db-home=/usr \
            --with-extra-version=%{release}

# symlink java deps
mkdir clc/lib
for x in $( cat %{SOURCE2} ); 
do 
  if [ ! -e $x ]; then
    echo "Could not find $x"
    exit 1
  fi
  ln -s $x clc/lib/;
done

# FIXME: storage/Makefile breaks with parallel make
make # %{?_smp_mflags}
pushd clc/eucadmin
( export PYTHONPATH=.; python gen_manpages.py )
popd

%install
make install DESTDIR=$RPM_BUILD_ROOT
for x in $( cat %{SOURCE2} | grep -v junit4 );
do
  rm $RPM_BUILD_ROOT%{eucajavalibdir}/$( basename $x )
  ln -s $x $RPM_BUILD_ROOT%{eucajavalibdir}
done
rm $RPM_BUILD_ROOT%{eucajavalibdir}/junit4*

# Fix jar paths and replace them with symlinks
mkdir -p $RPM_BUILD_ROOT%{_javadir}/%{name}
for x in $RPM_BUILD_ROOT%{eucajavalibdir}/eucalyptus-*.jar; do
  if [ $( basename $x ) == "eucalyptus-storagecontroller-%{version}.jar" ]; then
    DESTFILE=%{_libdir}/%{name}/$( basename $x )
  else
    DESTFILE=%{_javadir}/%{name}/$( basename $x )
  fi
  mv $x $RPM_BUILD_ROOT$DESTFILE
  ln -s $DESTFILE $RPM_BUILD_ROOT/%{eucajavalibdir}/
done

# Link jars not needed at build time
for jar in mule/mule-module-management \
           postgresql-jdbc \
           avalon-framework-impl \
           avalon-logkit \
           proxool \
           mx4j/mx4j-impl \
           mx4j/mx4j \
           mx4j/mx4j-jmx \
           mx4j/mx4j-remote \
           mx4j/mx4j-tools; do
  ln -s /usr/share/java/${jar}.jar $RPM_BUILD_ROOT%{eucajavalibdir}
done

pushd clc/eucadmin/man
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
cp -p * $RPM_BUILD_ROOT/%{_mandir}/man1
popd

sed -i -e 's#.*EUCALYPTUS=.*#EUCALYPTUS="/"#' \
       -e 's#.*HYPERVISOR=.*#HYPERVISOR="kvm"#' \
       -e 's#.*INSTANCE_PATH=.*#INSTANCE_PATH="/var/lib/%{name}/instances"#' \
       -e 's#.*VNET_BRIDGE=.*#VNET_BRIDGE="br0"#' \
       -e 's#.*USE_VIRTIO_DISK=.*#USE_VIRTIO_DISK="1"#' \
       -e 's#.*USE_VIRTIO_ROOT=.*#USE_VIRTIO_ROOT="1"#' \
       -e 's#.*VNET_PUBINTERFACE=.*#VNET_PUBINTERFACE="em1"#' \
       -e 's#.*VNET_PRIVINTERFACE=.*#VNET_PRIVINTERFACE="em1"#' \
       $RPM_BUILD_ROOT/etc/%{name}/eucalyptus.conf

# Move init scripts into sbindir and call them from systemd
mv $RPM_BUILD_ROOT/etc/init.d/eucalyptus-cloud \
   $RPM_BUILD_ROOT/%{_libexecdir}/%{name}/eucalyptus-cloud.init
rm -rf $RPM_BUILD_ROOT/etc/init.d
cp -p %{SOURCE7} $RPM_BUILD_ROOT/%{_libexecdir}/%{name}/eucalyptus-cc.init
cp -p %{SOURCE8} $RPM_BUILD_ROOT/%{_libexecdir}/%{name}/eucalyptus-nc.init
sed -i -e "s#@LIBDIR@#%{_libdir}#" $RPM_BUILD_ROOT/%{_libexecdir}/%{name}/eucalyptus-cc.init
sed -i -e "s#@LIBDIR@#%{_libdir}#" $RPM_BUILD_ROOT/%{_libexecdir}/%{name}/eucalyptus-nc.init

cp -p %{SOURCE13} $RPM_BUILD_ROOT/%{_sbindir}/eucalyptus-clean-cc

# Make a server root for apache
mkdir -p $RPM_BUILD_ROOT/etc/%{name}/httpd/conf/
cp -p %{SOURCE9} $RPM_BUILD_ROOT/etc/%{name}/httpd/conf/httpd-cc.conf
cp -p %{SOURCE10} $RPM_BUILD_ROOT/etc/%{name}/httpd/conf/httpd-nc.conf
cp -p %{SOURCE11} $RPM_BUILD_ROOT/etc/%{name}/httpd/conf/httpd-common.conf
ln -s %{_libdir}/httpd/modules $RPM_BUILD_ROOT/etc/%{name}/httpd/modules
rm $RPM_BUILD_ROOT/etc/%{name}/httpd.conf

sed -i -e "s#@EUCAAXIS2HOME@#%{axis2c_services}#" $RPM_BUILD_ROOT/etc/%{name}/httpd/conf/httpd-nc.conf
sed -i -e "s#@EUCAAXIS2HOME@#%{axis2c_services}#" $RPM_BUILD_ROOT/etc/%{name}/httpd/conf/httpd-cc.conf

# Create the directories where components store their data
mkdir -p $RPM_BUILD_ROOT/var/lib/%{name}
touch $RPM_BUILD_ROOT/var/lib/%{name}/services
for dir in bukkits CC db keys ldap upgrade vmware volumes webapps; do
    install -d -m 0700 $RPM_BUILD_ROOT/var/lib/%{name}/$dir
done
install -d -m 0771 $RPM_BUILD_ROOT/var/lib/%{name}/instances

# Add PolicyKit config on systems that support it
mkdir -p $RPM_BUILD_ROOT/usr/share/polkit-1/rules.d/
cp -p %{SOURCE14} $RPM_BUILD_ROOT/usr/share/polkit-1/rules.d/eucalyptus-nc-libvirt.rules

# Install systemd service files
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
install -p -m 644 %{SOURCE3} \
        $RPM_BUILD_ROOT%{_unitdir}/eucalyptus-cloud.service
install -p -m 644 %{SOURCE4} \
        $RPM_BUILD_ROOT%{_unitdir}/eucalyptus-cc.service
install -p -m 644 %{SOURCE5} \
        $RPM_BUILD_ROOT%{_unitdir}/eucalyptus-nc.service

# Copy axis2.xml into /etc for now, and symlink it
install -m 644 %{SOURCE6} \
        $RPM_BUILD_ROOT/etc/%{name}/axis2.xml

# add a mess of symlinks
ln -s /etc/%{name}/axis2.xml $RPM_BUILD_ROOT%{axis2c_services}/cc/
ln -s /etc/%{name}/axis2.xml $RPM_BUILD_ROOT%{axis2c_services}/nc/
ln -s %{_libdir}/wso2-axis2/modules $RPM_BUILD_ROOT%{axis2c_services}/cc/
ln -s %{_libdir}/wso2-axis2/modules $RPM_BUILD_ROOT%{axis2c_services}/nc/
ln -s %{_libdir} $RPM_BUILD_ROOT%{axis2c_services}/cc/lib
ln -s %{_libdir} $RPM_BUILD_ROOT%{axis2c_services}/nc/lib
ln -s %{axis2c_services}/gl/services/EucalyptusGL $RPM_BUILD_ROOT%{axis2c_services}/cc/services
ln -s %{axis2c_services}/gl/services/EucalyptusGL $RPM_BUILD_ROOT%{axis2c_services}/nc/services

# Install axis2 test client files
install -d -m 755 $RPM_BUILD_ROOT%{_bindir}
install -m 755 gatherlog/GLclient $RPM_BUILD_ROOT%{_bindir}
install -m 755 node/NCclient $RPM_BUILD_ROOT%{_bindir}
install -m 755 cluster/CCclient_full $RPM_BUILD_ROOT%{_bindir}/CCclient

# Fix some file permissions found by rpmlint
chmod -x $RPM_BUILD_ROOT/var/lib/%{name}/keys/nc-client-policy.xml
chmod -x $RPM_BUILD_ROOT/var/lib/%{name}/keys/cc-client-policy.xml
chmod -x $RPM_BUILD_ROOT%{axis2c_services}/cc/services/EucalyptusCC/eucalyptus_cc.wsdl
chmod -x $RPM_BUILD_ROOT%{axis2c_services}/cc/services/EucalyptusCC/services.xml
chmod -x $RPM_BUILD_ROOT%{axis2c_services}/gl/services/EucalyptusGL/eucalyptus_gl.wsdl
chmod -x $RPM_BUILD_ROOT%{axis2c_services}/gl/services/EucalyptusGL/services.xml
chmod -x $RPM_BUILD_ROOT%{axis2c_services}/nc/services/EucalyptusNC/services.xml

# This file is no longer needed, and was not even ported from MySQL to PostGreSQL
rm $RPM_BUILD_ROOT%{python_sitelib}/eucadmin/local.py*

# This is not the ideal way to set kernel parameters.  We'll deal with this
# via documentation for now.
rm $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/cloud.d/init.d/01_pg_kernel_params

# Move cloud.d directories which aren't config files.  We need symlinks
# for now, though.
mv $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/cloud.d/scripts \
   $RPM_BUILD_ROOT%{_libexecdir}/%{name}/scripts
mv $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/cloud.d/upgrade \
   $RPM_BUILD_ROOT%{_libexecdir}/%{name}/upgrade
ln -s %{_libexecdir}/%{name}/scripts \
   $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/cloud.d/
ln -s %{_libexecdir}/%{name}/upgrade \
   $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/cloud.d/

# doc fixups
mv $RPM_BUILD_ROOT%{_docdir}/%{name} $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
mv $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/drbd.conf.example \
   $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/

# install tmpfiles config
install -d -m 755 $RPM_BUILD_ROOT/etc/tmpfiles.d
install -m 0644 %{SOURCE15} $RPM_BUILD_ROOT/etc/tmpfiles.d/%{name}

%files
%doc LICENSE INSTALL README CHANGELOG
# Eucalyptus initialization fails if the eucalyptus user
# cannot write this file.  
%config(noreplace) %attr(-,eucalyptus,eucalyptus) /etc/%{name}/eucalyptus.conf
%{_datadir}/%{name}/eucalyptus-version
%config(noreplace) /etc/%{name}/axis2.xml
%dir /etc/%{name}/httpd
%dir /etc/%{name}/httpd/conf
%config(noreplace) /etc/%{name}/httpd/conf/httpd-common.conf
%config /etc/tmpfiles.d/%{name}
/etc/%{name}/httpd/modules
%attr(-,root,eucalyptus) %dir %{eucalibexecdir}
%attr(4750,root,eucalyptus) %{eucalibexecdir}/euca_mountwrap
%attr(4750,root,eucalyptus) %{eucalibexecdir}/euca_rootwrap
%dir %{eucadatadir}
%{_sbindir}/euca_sync_key

# helperdir is either eucadatadir or eucalibexecdir
%{helperdir}/add_key.pl
%{helperdir}/connect_iscsitarget.pl
%{helperdir}/create-loop-devices
%{helperdir}/disconnect_iscsitarget.pl
%{helperdir}/euca_ipt
%{helperdir}/euca_upgrade
%{helperdir}/floppy
%{helperdir}/get_iscsitarget.pl
%{helperdir}/populate_arp.pl
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/%{name}
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/%{name}/db
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/%{name}/keys
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/%{name}/upgrade
# Can this file go into a single-component package?  What uses it?
/var/lib/%{name}/keys/cc-client-policy.xml
%attr(-,eucalyptus,eucalyptus) %dir /var/log/%{name}
%attr(-,eucalyptus,eucalyptus) %dir /var/run/%{name}

%files common-java
%{_unitdir}/eucalyptus-cloud.service
%{_libexecdir}/%{name}/eucalyptus-cloud.init
# cloud.d contains random stuff used by every Java component.  Most of it
# probably belongs in /usr/share, but moving it will be painful.
%{_sysconfdir}/%{name}/cloud.d/
%{_libexecdir}/%{name}/scripts/
%{_libexecdir}/%{name}/upgrade/
%{_sbindir}/eucalyptus-cloud
%{eucajavalibdir}/*jar*
%{_javadir}/%{name}/*jar*
%{_libdir}/%{name}/eucalyptus-storagecontroller-%{version}.jar
%ghost /var/lib/%{name}/services
%attr(-,eucalyptus,eucalyptus) /var/lib/%{name}/webapps/

%files cloud
%{_sbindir}/euca-lictool
%{eucadatadir}/lic_default
%{eucadatadir}/lic_template

%files walrus
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/%{name}/bukkits
%doc %{_docdir}/%{name}-%{version}/drbd.conf.example

%files sc
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/%{name}/volumes
%{helperdir}/connect_iscsitarget_sc.pl
%{helperdir}/disconnect_iscsitarget_sc.pl
%{_libdir}/eucalyptus/liblvm2control.so

%files cc
%{_unitdir}/eucalyptus-cc.service
%{_libexecdir}/%{name}/eucalyptus-cc.init
%{axis2c_services}/cc
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/%{name}/CC
%config(noreplace) /etc/%{name}/httpd/conf/httpd-cc.conf
%{_datadir}/%{name}/vtunall.conf.template
%{_libexecdir}/eucalyptus/shutdownCC
%{_sbindir}/eucalyptus-clean-cc
%{helperdir}/dynserv.pl
# Is this used?
/var/lib/%{name}/keys/nc-client-policy.xml

%files nc
%config(noreplace) /etc/%{name}/libvirt.xsl
%dir /etc/%{name}/nc-hooks
/etc/%{name}/nc-hooks/example.sh
%{_unitdir}/eucalyptus-nc.service
%{_libexecdir}/%{name}/eucalyptus-nc.init
%{axis2c_services}/nc
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/%{name}/instances
%config(noreplace) /etc/%{name}/httpd/conf/httpd-nc.conf
%{_sbindir}/euca_test_nc
%{helperdir}/detach.pl
%{helperdir}/gen_kvm_libvirt_xml
%{helperdir}/gen_libvirt_xml
%{helperdir}/getstats.pl
%{helperdir}/get_sys_info
%{helperdir}/get_xen_info
%{helperdir}/partition2disk
/usr/share/polkit-1/rules.d/eucalyptus-nc-libvirt.rules
%{_docdir}/%{name}-%{version}/libvirt*

%files gl
%{axis2c_services}/gl

# NB: the vmware tools packaged here only work against Eucalyptus
# Enterprise plugins, but the client and server may be different
# systems, so it's reasonable to package these commands here.
%files admin-tools
%{_sbindir}/euca_conf
%{_sbindir}/euca-configure-vmware
%{_sbindir}/euca-deregister-arbitrator
%{_sbindir}/euca-deregister-cloud
%{_sbindir}/euca-deregister-cluster
%{_sbindir}/euca-deregister-storage-controller
%{_sbindir}/euca-deregister-vmware-broker
%{_sbindir}/euca-deregister-walrus
%{_sbindir}/euca-describe-arbitrators
%{_sbindir}/euca-describe-clouds
%{_sbindir}/euca-describe-clusters
%{_sbindir}/euca-describe-components
%{_sbindir}/euca-describe-nodes
%{_sbindir}/euca-describe-properties
%{_sbindir}/euca-describe-services
%{_sbindir}/euca-describe-storage-controllers
%{_sbindir}/euca-describe-vmware-brokers
%{_sbindir}/euca-describe-walruses
%{_sbindir}/euca-get-credentials
%{_sbindir}/euca-modify-cluster
%{_sbindir}/euca-modify-property
%{_sbindir}/euca-modify-service
%{_sbindir}/euca-modify-storage-controller
%{_sbindir}/euca-modify-walrus
%{_sbindir}/euca-register-arbitrator
%{_sbindir}/euca-register-cloud
%{_sbindir}/euca-register-cluster
%{_sbindir}/euca-register-storage-controller
%{_sbindir}/euca-register-vmware-broker
%{_sbindir}/euca-register-walrus
%{_mandir}/man1/*

%files -n python-eucadmin
%{python_sitelib}/eucadmin*

%files axis2-clients
%{_bindir}/NCclient
%{_bindir}/CCclient
%{_bindir}/GLclient

%pre
getent group eucalyptus >/dev/null || groupadd -r eucalyptus
## FIXME:  Make QA (and Eucalyptus proper?) work with /sbin/nologin as the shell [RT:2092]
#getent passwd eucalyptus >/dev/null || \
#    useradd -r -g eucalyptus -d /var/lib/%{name} -s /sbin/nologin \
#    -c 'Eucalyptus' eucalyptus
getent passwd eucalyptus >/dev/null || \
    useradd -r -g eucalyptus -d /var/lib/%{name} \
    -c 'Eucalyptus' eucalyptus

%post
udevadm control --reload-rules

%{_sbindir}/euca_conf -d / --instances /var/lib/%{name}/instances --hypervisor kvm --bridge br0

%post common-java
%{systemd_post} eucalyptus-cloud.service

%post cc
%{systemd_post} eucalyptus-cc.service

%post nc
usermod -a -G kvm eucalyptus
%{systemd_post} eucalyptus-nc.service

%preun common-java
%{systemd_preun} eucalyptus-cloud.service

%preun cc
%{systemd_preun} eucalyptus-cc.service

%preun nc
%{systemd_preun} eucalyptus-nc.service

%changelog
* Thu Sep 20 2012 Andy Grimm <agirmm@gmail.com> - 3.1.2-0.4.20120917gitb8c109b4
- Enable reporting

* Mon Sep 17 2012 Andy Grimm <agrimm@gmail.com> - 3.1.2-0.3.20120917gitb8c109b4
- tmpfiles.d entry
- remove eucadmin/local.pyc
- truncate binary floppy file in prep

* Mon Sep 17 2012 Andy Grimm <agrimm@gmail.com> - 3.1.2-0.2.20120917gitb8c109b4
- add with_axis2v14 variable to generate C code
- Incorporate ESA updates

* Mon Sep 10 2012 Andy Grimm <agrimm@gmail.com> - 3.1.2-0.1.20120913gitad123963
- Update to 3.1.2 development code
- Switch to a git snapshot
- Remove several patches which are now present in git
- Remove upgrade logic for now

* Fri Sep  7 2012 Andy Grimm <agrimm@gmail.com> - 3.1.0-20
- Create a new polkit rule
- Add a patch to ignore missing grub-install
- Add some missing Requires

* Mon Aug 27 2012 Andy Grimm <agrimm@gmail.com> - 3.1.0-19
- Package review fixes, round one

* Fri Aug 24 2012 Andy Grimm <agrimm@gmail.com> - 3.1.0-18
- Fix httpd configs
- Fix image registration via pg-hibernate patch update

* Fri Aug 24 2012 Andy Grimm <agrimm@gmail.com> - 3.1.0-17
- prune transitive BuildRequires and Requires
- remove some macros from the spec file
- improve systemd units

* Thu Aug 23 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.1.0-16
- file permission fixes
- generate man pages for admin tools

* Wed Aug 22 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.1.0-15
- Init script fixes
- a few fixes to the macro patch
- add generated code tarball

* Tue Aug 21 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.1.0-14
- add axis2-clients subpackage
- adapt apache configs for 2.4

* Sat Aug 18 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.1.0-13
- fix to allow axis2 / rampart includedir outside to axis2c_home

* Fri Aug 17 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.1.0-12
- fix axis2 symlinks
- deal with broken Lob entities

* Thu Aug 16 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.1.0-11
- comment out systemd macros; they don't work yet
- fix more path substitution fallout

* Thu Aug 16 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.1.0-10
- add custom init scripts and axis2 httpd configs
- fix undefined functions in NC
- fix rootwrap path in eucadmin scripts
- fix errors in Java lib dir path calculation in cloud boostrapper

* Wed Aug 15 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.1.0-9
- Add patch for separating axis2 services into contained repos

* Tue Aug 14 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.1.0-8
- Add patch for macro-ized directory paths throughout the code

* Sat Aug 11 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.1.0-7
- add systemd units

* Fri Aug 10 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.1.0-6
- add a few more jar links

* Fri Aug 10 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.1.0-5
- switch to spring 3.0.3

* Wed Aug 08 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.1.0-4
- Hibernate fixes

* Tue Aug 07 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.1.0-3.2
- Jetty 8 fixes

* Tue Aug 07 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.1.0-3.1
- Change gwt disablement to match debian

* Tue Aug 07 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.1.0-3
- Release bump for additional jar links

* Mon Aug 06 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.1.0-2
- Sync several fixes from official 3.x spec file

* Mon Aug 06 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.1.0-1
- Experimental Fedora build
