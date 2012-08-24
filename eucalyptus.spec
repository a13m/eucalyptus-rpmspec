%global axis2c_home       %{_libdir}/wso2-axis2
%global axis2c_services   %{_libdir}/eucalyptus/axis2
%global eucaconfdir       %{_sysconfdir}/eucalyptus
%global eucalibexecdir    %{_libexecdir}/eucalyptus
%global eucalogdir        %{_localstatedir}/log/eucalyptus
%global eucarundir        %{_localstatedir}/run/eucalyptus
%global eucastatedir      %{_localstatedir}/lib/eucalyptus
%global eucadatadir       %{_datadir}/eucalyptus
%global eucajavalibdir    %{_datadir}/eucalyptus
%global helperdir         %{_datadir}/eucalyptus

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary:       Elastic Utility Computing Architecture
Name:          eucalyptus
Version:       3.1.0
Release:       18%{?dist}
License:       GPLv3
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
BuildRequires: guava >= 12
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

Source0:       http://downloads.eucalyptus.com/software/eucalyptus/3.1/source/eucalyptus-3.1.0.tar.gz
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
# This code was generated using 1.4; note that 1.5 should also work, and 
# the 1.5 source is included in wso2-wsf-cpp package, but not currently
# built into a subpackage. 
Source12:      eucalyptus-3.1.0-generated.tgz

# https://eucalyptus.atlassian.net/browse/EUCA-2364
Patch0:        eucalyptus-jdk7.patch
# https://eucalyptus.atlassian.net/browse/EUCA-3253
Patch2:        eucalyptus-jetty8.patch
# Reporting module requires activemq, which is not yet packaged
Patch3:        eucalyptus-no-reporting.patch
# https://eucalyptus.atlassian.net/browse/EUCA-2993
Patch4:        eucalyptus-groovy18.patch
# https://eucalyptus.atlassian.net/browse/EUCA-2997
Patch5:        eucalyptus-guava-11.patch
Patch6:        eucalyptus-guava-13.patch
# This patch is required if we used Axis2/Java 1.6 for code generation.
# Patch7:        eucalyptus-axis2-java-1.6.patch
# Minor log4j interface change
Patch8:        eucalyptus-log4j-fix.patch

# Three separate patches to disable gwt
Patch9:        eucalyptus-disable-gwt.patch
Patch10:        eucalyptus-disable-gwt-in-buildxml.patch
Patch11:        eucalyptus-disable-gwt-in-makefile.patch

# https://eucalyptus.atlassian.net/browse/EUCA-2998
Patch12:       eucalyptus-pg-hibernate.patch

# Kill all hardcoded paths
# https://eucalyptus.atlassian.net/browse/EUCA-3331
Patch13:       eucalyptus-macro-fix.patch

# Make one repo per service of Axis2 services
Patch14:       eucalyptus-axis2-services.patch

# Fix rootwrap path in python files 
Patch15:       eucalyptus-rootwrap-python.patch

# Fix include location for axis2 libs
Patch16:       eucalyptus-wso2-axis2-configure.patch

# Fix postgres config and improve logging for pg startup
# Related: https://eucalyptus.atlassian.net/browse/EUCA-3334
Patch17:       eucalyptus-fix-setupdb.patch

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
Requires:     guava
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
Requires(preun): systemd-units
Requires(postun): systemd-units
Requires(post): systemd-units

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
# bc is needed for /etc/eucalyptus/cloud.d/init.d/01_pg_kernel_params
Requires:     bc
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
Requires(preun): systemd-units
Requires(postun): systemd-units
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
Requires:     %{_sbindir}/euca_conf
Requires(preun): systemd-units
Requires(postun): systemd-units
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
%setup -q
pushd ..
tar xzf %{SOURCE12}
popd
%patch0 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
# %patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1

# disable modules by removing their build.xml files
rm clc/modules/reporting/build.xml

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

%build
export CFLAGS="%{optflags}"

# TODO: we should use %%configure now
# Also, helperdir sould be a config option, unless we decide that
# it's always eucadatadir
./configure --with-axis2=%{_datadir}/axis2-* \
            --with-axis2c=%{axis2c_home} \
            --with-axis2c-services=%{axis2c_services} \
            --with-wsdl2c-sh=%{S:1} \
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
for x in $( cat %{S:2} ); 
do 
  if [ ! -e $x ]; then
    echo "Could not find $x"
    exit 1
  fi
  ln -s $x clc/lib/;
done

# FIXME: storage/Makefile breaks with parallel make
LANG=en_US.UTF-8 make # %{?_smp_mflags}
pushd clc/eucadmin
( export PYTHONPATH=.; python gen_manpages.py )
popd

%install
make install DESTDIR=$RPM_BUILD_ROOT
for x in $( cat %{S:2} | grep -v junit4 );
do
  rm $RPM_BUILD_ROOT%{eucajavalibdir}/$( basename $x )
  ln -s $x $RPM_BUILD_ROOT%{eucajavalibdir}
done
rm $RPM_BUILD_ROOT%{eucajavalibdir}/junit4*

# Link jars not needed at build time
ln -s /usr/share/java/mule/mule-module-management.jar $RPM_BUILD_ROOT%{eucajavalibdir}
ln -s /usr/share/java/postgresql-jdbc.jar $RPM_BUILD_ROOT%{eucajavalibdir}
ln -s /usr/share/java/avalon-framework-impl.jar $RPM_BUILD_ROOT%{eucajavalibdir}
ln -s /usr/share/java/avalon-logkit.jar $RPM_BUILD_ROOT%{eucajavalibdir}
ln -s /usr/share/java/proxool.jar $RPM_BUILD_ROOT%{eucajavalibdir}

pushd clc/eucadmin/man
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
cp -p * $RPM_BUILD_ROOT/%{_mandir}/man1
popd

sed -i -e 's#.*EUCALYPTUS=.*#EUCALYPTUS="/"#' \
       -e 's#.*HYPERVISOR=.*#HYPERVISOR="kvm"#' \
       -e 's#.*INSTANCE_PATH=.*#INSTANCE_PATH="%{eucastatedir}/instances"#' \
       -e 's#.*VNET_BRIDGE=.*#VNET_BRIDGE="br0"#' \
       -e 's#.*USE_VIRTIO_DISK=.*#USE_VIRTIO_DISK="1"#' \
       -e 's#.*USE_VIRTIO_ROOT=.*#USE_VIRTIO_ROOT="1"#' \
       $RPM_BUILD_ROOT%{eucaconfdir}/eucalyptus.conf

# Move init scripts into sbindir and call them from systemd
mv $RPM_BUILD_ROOT/etc/init.d/eucalyptus-cloud $RPM_BUILD_ROOT/%{_sbindir}/eucalyptus-cloud.init
rm -rf $RPM_BUILD_ROOT/etc/init.d
cp -p %{SOURCE7} $RPM_BUILD_ROOT/%{_sbindir}/eucalyptus-cc.init
cp -p %{SOURCE8} $RPM_BUILD_ROOT/%{_sbindir}/eucalyptus-nc.init

# Make a server root for apache
mkdir -p $RPM_BUILD_ROOT/%{eucaconfdir}/httpd/conf/
cp -p %{SOURCE9} $RPM_BUILD_ROOT/%{eucaconfdir}/httpd/conf/httpd-cc.conf
cp -p %{SOURCE10} $RPM_BUILD_ROOT/%{eucaconfdir}/httpd/conf/httpd-nc.conf
cp -p %{SOURCE11} $RPM_BUILD_ROOT/%{eucaconfdir}/httpd/conf/httpd-common.conf
ln -s %{_libdir}/httpd/modules $RPM_BUILD_ROOT/%{eucaconfdir}/httpd/modules
rm $RPM_BUILD_ROOT/%{eucaconfdir}/httpd.conf

sed -i -e "s#@EUCAAXIS2HOME@#%{axis2c_services}#" $RPM_BUILD_ROOT/%{eucaconfdir}/httpd/conf/httpd-nc.conf
sed -i -e "s#@EUCAAXIS2HOME@#%{axis2c_services}#" $RPM_BUILD_ROOT/%{eucaconfdir}/httpd/conf/httpd-cc.conf

# Create the directories where components store their data
mkdir -p $RPM_BUILD_ROOT%{eucastatedir}
touch $RPM_BUILD_ROOT%{eucastatedir}/services
for dir in bukkits CC db keys ldap upgrade vmware volumes webapps; do
    install -d -m 0700 $RPM_BUILD_ROOT%{eucastatedir}/$dir
done
install -d -m 0771 $RPM_BUILD_ROOT%{eucastatedir}/instances

# Add PolicyKit config on systems that support it
mkdir -p $RPM_BUILD_ROOT/var/lib/polkit-1/localauthority/10-vendor.d
cp -p tools/eucalyptus-nc-libvirt.pkla $RPM_BUILD_ROOT/var/lib/polkit-1/localauthority/10-vendor.d/eucalyptus-nc-libvirt.pkla

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
        $RPM_BUILD_ROOT%{eucaconfdir}/axis2.xml

# add a mess of symlinks
ln -s %{eucaconfdir}/axis2.xml $RPM_BUILD_ROOT%{axis2c_services}/cc/
ln -s %{eucaconfdir}/axis2.xml $RPM_BUILD_ROOT%{axis2c_services}/nc/
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
chmod -x $RPM_BUILD_ROOT%{eucastatedir}/keys/nc-client-policy.xml
chmod -x $RPM_BUILD_ROOT%{eucastatedir}/keys/cc-client-policy.xml
chmod -x $RPM_BUILD_ROOT%{axis2c_services}/cc/services/EucalyptusCC/eucalyptus_cc.wsdl
chmod -x $RPM_BUILD_ROOT%{axis2c_services}/cc/services/EucalyptusCC/services.xml
chmod -x $RPM_BUILD_ROOT%{axis2c_services}/gl/services/EucalyptusGL/eucalyptus_gl.wsdl
chmod -x $RPM_BUILD_ROOT%{axis2c_services}/gl/services/EucalyptusGL/services.xml
chmod -x $RPM_BUILD_ROOT%{axis2c_services}/nc/services/EucalyptusNC/services.xml
chmod +x $RPM_BUILD_ROOT%{python_sitelib}/eucadmin/local.py

%files
%doc LICENSE INSTALL README CHANGELOG
%attr(-,eucalyptus,eucalyptus) %{eucaconfdir}/eucalyptus.conf
%{eucaconfdir}/eucalyptus-version
%{eucaconfdir}/axis2.xml
%dir %{eucaconfdir}/httpd
%dir %{eucaconfdir}/httpd/conf
%{eucaconfdir}/httpd/conf/httpd-common.conf
%{eucaconfdir}/httpd/modules
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
%doc %{_docdir}/eucalyptus
%{helperdir}/euca_ipt
%{helperdir}/euca_upgrade
%{helperdir}/floppy
%{helperdir}/get_iscsitarget.pl
%{helperdir}/populate_arp.pl
%attr(-,eucalyptus,eucalyptus) %dir %{eucastatedir}
%attr(-,eucalyptus,eucalyptus) %dir %{eucastatedir}/db
%attr(-,eucalyptus,eucalyptus) %dir %{eucastatedir}/keys
%attr(-,eucalyptus,eucalyptus) %dir %{eucastatedir}/upgrade
# Can this file go into a single-component package?  What uses it?
%{eucastatedir}/keys/cc-client-policy.xml
%attr(-,eucalyptus,eucalyptus) %dir %{eucalogdir}
%attr(-,eucalyptus,eucalyptus) %dir %{eucarundir}

%files common-java
%{_unitdir}/eucalyptus-cloud.service
%{_sbindir}/eucalyptus-cloud.init
# cloud.d contains random stuff used by every Java component.  Most of it
# probably belongs in /usr/share, but moving it will be painful.
%{eucaconfdir}/cloud.d/
%{_sbindir}/eucalyptus-cloud
%{eucajavalibdir}/*jar*
%ghost %{eucastatedir}/services
%attr(-,eucalyptus,eucalyptus) %{eucastatedir}/webapps/

%files cloud
%{eucaconfdir}/cloud.d/init.d/01_pg_kernel_params
%{_sbindir}/euca-lictool
%{eucadatadir}/lic_default
%{eucadatadir}/lic_template

%files walrus
%attr(-,eucalyptus,eucalyptus) %dir %{eucastatedir}/bukkits
%{eucaconfdir}/drbd.conf.example

%files sc
%attr(-,eucalyptus,eucalyptus) %dir %{eucastatedir}/volumes
%{helperdir}/connect_iscsitarget_sc.pl
%{helperdir}/disconnect_iscsitarget_sc.pl
%{_libdir}/eucalyptus/liblvm2control.so

%files cc
%{_unitdir}/eucalyptus-cc.service
%{_sbindir}/eucalyptus-cc.init
%{axis2c_services}/cc
%attr(-,eucalyptus,eucalyptus) %dir %{eucastatedir}/CC
%{eucaconfdir}/httpd/conf/httpd-cc.conf
%{eucaconfdir}/vtunall.conf.template
%{_libexecdir}/eucalyptus/shutdownCC
%{helperdir}/dynserv.pl
# Is this used?
%{eucastatedir}/keys/nc-client-policy.xml

%files nc
%config(noreplace) %{eucaconfdir}/libvirt.xsl
%dir %{eucaconfdir}/nc-hooks
%{eucaconfdir}/nc-hooks/example.sh
%{_unitdir}/eucalyptus-nc.service
%{_sbindir}/eucalyptus-nc.init
%{axis2c_services}/nc
%attr(-,eucalyptus,eucalyptus) %dir %{eucastatedir}/instances
%{eucaconfdir}/httpd/conf/httpd-nc.conf
%{_sbindir}/euca_test_nc
%{helperdir}/detach.pl
%{helperdir}/gen_kvm_libvirt_xml
%{helperdir}/gen_libvirt_xml
%{helperdir}/getstats.pl
%{helperdir}/get_sys_info
%{helperdir}/get_xen_info
%{helperdir}/partition2disk
/var/lib/polkit-1/localauthority/10-vendor.d/eucalyptus-nc-libvirt.pkla

%files gl
%{axis2c_services}/gl

# NB: the vmware tools packaged here only work against Eucalyptus
# Enterprise Edition, but the client and server may be different
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
#    useradd -r -g eucalyptus -d /var/lib/eucalyptus -s /sbin/nologin \
#    -c 'Eucalyptus' eucalyptus
getent passwd eucalyptus >/dev/null || \
    useradd -r -g eucalyptus -d %{eucastatedir} \
    -c 'Eucalyptus' eucalyptus

if [ "$1" = "2" ]; then
    # Stop all old services
    if [ -x %{_initrddir}/eucalyptus-cloud ]; then
         /sbin/service eucalyptus-cloud stop
    fi
    if [ -x %{_initrddir}/eucalyptus-cc ]; then
         /sbin/service eucalyptus-cc cleanstop
    fi
    if [ -x %{_initrddir}/eucalyptus-nc ]; then
         /sbin/service eucalyptus-nc stop
    fi

    # Back up important data as well as all of the previous installation's jars.
    BACKUPDIR="%{eucastatedir}/upgrade/eucalyptus.backup.`date +%%s`"
    mkdir -p "$BACKUPDIR"
    EUCABACKUPS=""
    for i in %{eucastatedir}/keys/ %{eucastatedir}/db/ %{eucastatedir}/services %{eucaconfidr}/eucalyptus.conf %{eucaconfdir}/eucalyptus-version %{eucajavalibdir} %{eucahelperdir}; do
        if [ -e $i ]; then
            EUCABACKUPS="$EUCABACKUPS $i"
        fi
    done

    OLD_EUCA_VERSION=`cat %{eucaconfdir}/eucalyptus-version`
    echo "# This file was automatically generated by Eucalyptus packaging." > %{eucaconfdir}/.upgrade
    echo "$OLD_EUCA_VERSION:$BACKUPDIR" >> %{eucaconfdir}/.upgrade

    tar cf - $EUCABACKUPS 2>/dev/null | tar xf - -C "$BACKUPDIR" 2>/dev/null
fi
exit 0

%post
udevadm control --reload-rules

%{_sbindir}/euca_conf -d / --instances %{eucastatedir}/instances --hypervisor kvm --bridge br0

if [ "$1" = "2" ]; then
    if [ -f %{eucaconfdir}/.upgrade ]; then
        while IFS=: read -r a b; do
            OLD_EUCA_VERSION=$a
            OLD_EUCA_PATH=$b
        done < $EUCALYPTUS/etc/eucalyptus/.upgrade
        %{helperdir}/euca_upgrade --old $OLD_EUCA_PATH --new / --conf >%{eucalogdir}/upgrade-config.log 2>&1
    fi
fi

exit 0

%post common-java
%{systemd_post} eucalyptus-cloud.service

%post sc
# XXX: this should be represented by systemd deps
# The sc may need its own unit for this?
chkconfig --add tgtd
/sbin/service tgtd start

%post cc
%{systemd_post} eucalyptus-cc.service

%post nc
usermod -a -G kvm eucalyptus
%{systemd_post} eucalyptus-nc.service

%postun common-java
# XXX: This is probably superfluous, because at least one of
# sc / walrus / cloud will do a restart here, too.
%{systemd_postun_with_restart} eucalyptus-cloud.service

%postun cloud
%{systemd_postun_with_restart} eucalyptus-cloud.service

%postun walrus
%{systemd_postun_with_restart} eucalyptus-cloud.service

%postun sc
%{systemd_postun_with_restart} eucalyptus-cloud.service

%preun common-java
%{systemd_preun} eucalyptus-cloud.service

%preun cc
%{_sbindir}/eucalyptus-cc.init cleanstop
%{systemd_preun} eucalyptus-cc.service

%preun nc
%{systemd_preun} eucalyptus-nc.service

%changelog
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
