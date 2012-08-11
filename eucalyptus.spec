%global axis2c_home       /usr
%global euca_dhcp         dhcp
%global euca_bridge       br0
%global euca_build_req    vconfig, wget, rsync
%global euca_curl         curl
%global euca_httpd        httpd
%global euca_hypervisor   kvm
%global euca_iscsi_client iscsi-initiator-utils
%global euca_iscsi_server scsi-target-utils
%global euca_libcurl      curl-devel
%global euca_libvirt      libvirt
%global euca_which        which
%global spring            springframework303

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%define provide_abi() \
%{!?abi_version: %define abi_version %{version}-%{release}} \
%if 0%# \
Provides: %{name}-abi(%1) = %{abi_version} \
%else \
Provides: %{name}-abi = %{abi_version} \
%endif \
%{nil}


Summary:       Elastic Utility Computing Architecture
Name:          eucalyptus
Version:       3.1.0
Release:       7%{?dist}
License:       GPLv3
URL:           http://www.eucalyptus.com
Group:         Applications/System

BuildRequires: ant >= 1.7
BuildRequires: ant-nodeps >= 1.7
BuildRequires: axis2
BuildRequires: java-devel >= 1:1.6.0
BuildRequires: jpackage-utils
BuildRequires: libvirt-devel >= 0.6
BuildRequires: libxml2-devel
BuildRequires: libxslt-devel
BuildRequires: openssl-devel
BuildRequires: python%{?pybasever}-devel
BuildRequires: python%{?pybasever}-setuptools
BuildRequires: swig
BuildRequires: velocity
BuildRequires: wso2-axis2-devel
BuildRequires: wso2-rampart-devel
BuildRequires: wso2-wsf-cpp-devel
BuildRequires: /usr/bin/awk

BuildRequires: %{euca_iscsi_client}
BuildRequires: %{euca_libvirt}-devel
BuildRequires: %{euca_libvirt}
BuildRequires: %{euca_libcurl}

# Java stuff moving out of cloud-lib
BuildRequires: ant
BuildRequires: antlr-tool
BuildRequires: apache-commons-beanutils
BuildRequires: apache-commons-cli
BuildRequires: apache-commons-codec
BuildRequires: apache-commons-collections
BuildRequires: apache-commons-compress
BuildRequires: apache-commons-digester
BuildRequires: apache-commons-discovery
BuildRequires: apache-commons-fileupload
BuildRequires: apache-commons-io
BuildRequires: apache-commons-jxpath
BuildRequires: apache-commons-lang
BuildRequires: apache-commons-logging
BuildRequires: apache-commons-pool
BuildRequires: avalon-framework
BuildRequires: avalon-logkit
BuildRequires: axiom
BuildRequires: backport-util-concurrent
BuildRequires: batik
BuildRequires: bcel
BuildRequires: bouncycastle
BuildRequires: bsf
BuildRequires: btm
BuildRequires: cglib
BuildRequires: dnsjava
BuildRequires: dom4j
BuildRequires: ehcache-core
BuildRequires: ezmorph
BuildRequires: geronimo-ejb
BuildRequires: geronimo-jms
BuildRequires: geronimo-jta
BuildRequires: groovy
BuildRequires: guava
BuildRequires: ha-jdbc
BuildRequires: hamcrest12
BuildRequires: hibernate3
BuildRequires: hibernate3-ehcache
BuildRequires: hibernate3-entitymanager
BuildRequires: hibernate3-jbosscache
BuildRequires: hibernate3-proxool
BuildRequires: hibernate-commons-annotations
BuildRequires: hibernate-jpa-2.0-api
BuildRequires: hsqldb
BuildRequires: jakarta-commons-httpclient
BuildRequires: javamail
BuildRequires: javassist
BuildRequires: java-uuid-generator
BuildRequires: jaxen
BuildRequires: jbosscache-core
BuildRequires: jboss-common-core
BuildRequires: jboss-connector-1.6-api
BuildRequires: jboss-logging
BuildRequires: jboss-marshalling
BuildRequires: jcip-annotations
BuildRequires: jettison
BuildRequires: jetty
BuildRequires: jetty-ajp
BuildRequires: jetty-annotations
BuildRequires: jetty-client
BuildRequires: jetty-continuation
BuildRequires: jetty-deploy
BuildRequires: jetty-http
BuildRequires: jetty-io
BuildRequires: jetty-jmx
BuildRequires: jetty-jndi
BuildRequires: jetty-overlay-deployer
BuildRequires: jetty-plus
BuildRequires: jetty-policy
BuildRequires: jetty-rewrite
BuildRequires: jetty-security
BuildRequires: jetty-server
BuildRequires: jetty-servlet
BuildRequires: jetty-servlets
BuildRequires: jetty-util
BuildRequires: jetty-webapp
BuildRequires: jetty-websocket
BuildRequires: jetty-xml
BuildRequires: jgroups212
BuildRequires: jibx
BuildRequires: jna
BuildRequires: jsch
BuildRequires: json-lib
BuildRequires: jsr-305
BuildRequires: junit
BuildRequires: log4j
BuildRequires: mule
BuildRequires: mule-module-builders
BuildRequires: mule-module-client
BuildRequires: mule-module-management
BuildRequires: mule-module-spring-config
BuildRequires: mule-module-xml
BuildRequires: mule-transport-vm
BuildRequires: netty31
BuildRequires: objectweb-asm
BuildRequires: postgresql-jdbc
BuildRequires: proxool
BuildRequires: quartz
BuildRequires: regexp
BuildRequires: slf4j
BuildRequires: %{spring} 
BuildRequires: %{spring}-beans
BuildRequires: %{spring}-context
BuildRequires: %{spring}-context-support
BuildRequires: %{spring}-web
BuildRequires: stax2-api
BuildRequires: tomcat-el-2.2-api
BuildRequires: tomcat-servlet-3.0-api
BuildRequires: velocity
BuildRequires: woodstox-core
BuildRequires: wsdl4j
BuildRequires: wss4j
BuildRequires: xalan-j2
BuildRequires: xerces-j2
BuildRequires: xml-commons-apis
BuildRequires: xml-security
BuildRequires: xom
BuildRequires: xpp3

Requires:      %{euca_build_req}
Requires:      %{euca_which}
Requires:      libselinux-python
Requires:      perl(Crypt::OpenSSL::RSA)
Requires:      perl(Crypt::OpenSSL::Random)
Requires:      sudo
Requires(pre):  %{_sbindir}/groupadd
Requires(pre):  %{_sbindir}/useradd
Requires(post): %{_sbindir}/euca_conf

%provide_abi

Source0:       %{name}-%{version}.tar.gz
# A version of WSDL2C.sh that respects standard classpaths
Source1:       euca-WSDL2C.sh
Source2:       eucalyptus-jarlinks.txt
# XXX: these system units should go in the source tree
Source3:       eucalyptus-cloud.service
Source4:       eucalyptus-cc.service
Source5:       eucalyptus-nc.service
Patch0:        eucalyptus-jdk7.patch
Patch1:        eucalyptus-jgroups3.patch
Patch2:        eucalyptus-jetty8.patch
Patch3:        eucalyptus-no-reporting.patch
Patch4:        eucalyptus-groovy18.patch
Patch5:        eucalyptus-build-against-new-guava.patch
Patch6:        eucalyptus-wso2-axis2.patch
Patch7:        eucalyptus-log4j-fix.patch

# Three separate patches to disable gwt
Patch8:        eucalyptus-disable-gwt.patch
Patch9:        eucalyptus-disable-gwt-in-buildxml.patch
Patch10:        eucalyptus-disable-gwt-in-makefile.patch

# Hibernate patches for debian
Patch11:       eucalyptus-pg-hibernate.patch
Patch12:       eucalyptus-hibernate-3.6.patch

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
Requires: ant
Requires: antlr-tool
Requires: apache-commons-beanutils
Requires: apache-commons-cli
Requires: apache-commons-codec
Requires: apache-commons-collections
Requires: apache-commons-compress
Requires: apache-commons-digester
Requires: apache-commons-discovery
Requires: apache-commons-fileupload
Requires: apache-commons-io
Requires: apache-commons-jxpath
Requires: apache-commons-lang
Requires: apache-commons-logging
Requires: apache-commons-pool
Requires: avalon-framework
Requires: avalon-logkit
Requires: axiom
Requires: backport-util-concurrent
Requires: batik
Requires: bcel
Requires: bouncycastle
Requires: bsf
Requires: btm
Requires: cglib
Requires: dnsjava
Requires: dom4j
Requires: ehcache-core
Requires: ezmorph
Requires: geronimo-ejb
Requires: geronimo-jms
Requires: geronimo-jta
Requires: groovy
Requires: guava
Requires: ha-jdbc
Requires: hamcrest12
Requires: hibernate3
Requires: hibernate3-ehcache
Requires: hibernate3-entitymanager
Requires: hibernate3-jbosscache
Requires: hibernate3-proxool
Requires: hibernate-commons-annotations
Requires: hibernate-jpa-2.0-api
Requires: hsqldb
Requires: jakarta-commons-httpclient
Requires: javamail
Requires: javassist
Requires: java-uuid-generator
Requires: jaxen
Requires: jbosscache-core
Requires: jboss-common-core
Requires: jboss-connector-1.6-api
Requires: jboss-logging
Requires: jboss-marshalling
Requires: jcip-annotations
Requires: jettison
Requires: jetty
Requires: jetty-ajp
Requires: jetty-annotations
Requires: jetty-client
Requires: jetty-continuation
Requires: jetty-deploy
Requires: jetty-http
Requires: jetty-io
Requires: jetty-jmx
Requires: jetty-jndi
Requires: jetty-overlay-deployer
Requires: jetty-plus
Requires: jetty-policy
Requires: jetty-rewrite
Requires: jetty-security
Requires: jetty-server
Requires: jetty-servlet
Requires: jetty-servlets
Requires: jetty-util
Requires: jetty-webapp
Requires: jetty-websocket
Requires: jetty-xml
Requires: jgroups212
Requires: jibx
Requires: jna
Requires: jsch
Requires: json-lib
Requires: jsr-305
Requires: log4j
Requires: mule
Requires: mule-module-builders
Requires: mule-module-client
Requires: mule-module-spring-config
Requires: mule-module-xml
Requires: mule-transport-vm
Requires: netty31
Requires: objectweb-asm
Requires: postgresql-jdbc
Requires: proxool
Requires: quartz
Requires: regexp
Requires: slf4j
Requires: springframework
Requires: springframework-beans
Requires: springframework-context
Requires: springframework-context-support
Requires: springframework-expression
Requires: springframework-web
Requires: stax2-api
Requires: tomcat-el-2.2-api
Requires: tomcat-servlet-3.0-api
Requires: velocity
Requires: woodstox-core
Requires: wsdl4j
Requires: wss4j
Requires: xalan-j2
Requires: xerces-j2
Requires: xml-commons-apis
Requires: xml-security
Requires: xom
Requires: xpp3
Requires:     %{_sbindir}/euca_conf

%provide_abi common-java

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

%provide_abi walrus

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
Requires:     %{euca_iscsi_client}
Requires:     %{euca_iscsi_server}

%provide_abi sc

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

%provide_abi cloud

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
Requires:     %{euca_dhcp}
Requires:     %{euca_httpd}
Requires:     %{_sbindir}/euca_conf
Requires(preun): systemd-units
Requires(postun): systemd-units
Requires(post): systemd-units

%provide_abi cc

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
Requires:     %{euca_curl}
Requires:     %{euca_httpd}
Requires:     %{euca_hypervisor}
Requires:     %{euca_iscsi_client}
Requires:     %{euca_libvirt}
Requires:     %{_sbindir}/euca_conf
Requires(preun): systemd-units
Requires(postun): systemd-units
Requires(post): systemd-units

%provide_abi nc

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
Requires:     %{euca_httpd}

%provide_abi gl

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
Requires:     python%{?pybasever}-eucadmin = %{version}-%{release}
Requires:     rsync
BuildArch:    noarch

%provide_abi admin-tools

%description admin-tools
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains command line tools necessary for managing a
Eucalyptus cluster.

%package -n python%{?pybasever}-eucadmin
Summary:      Elastic Utility Computing Architecture - administration Python library
License:      BSD
Requires:     PyGreSQL
Requires:     python%{?pybasever}-boto >= 2.1
Requires:     rsync
BuildArch:    noarch

%provide_abi python%{?pybasever}-eucadmin

%description -n python%{?pybasever}-eucadmin
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains the Python library used by Eucalyptus administration
tools.  It is neither intended nor supported for use by any other programs.

%prep
%setup -q
%patch0 -p1
# %patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1

# disable modules by removing their build.xml files
rm clc/modules/reporting/build.xml
# rm clc/modules/www/build.xml

# remove a class which depends on junit
rm clc/modules/core/src/main/java/edu/ucsb/eucalyptus/util/XMLParserTest.java

%build
export CFLAGS="%{optflags}"

# Eucalyptus does not assign the usual meaning to prefix and other standard
# configure variables, so we can't realistically use %%configure.
./configure --with-axis2=%{_datadir}/axis2-* --with-axis2c=%{axis2c_home} --with-wsdl2c-sh=%{S:1} --enable-debug --prefix=/ --with-apache2-module-dir=%{_libdir}/httpd/modules --with-db-home=/usr --with-extra-version=%{release}

# Untar the bundled cloud-lib Java dependencies.
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

%install
[ $RPM_BUILD_ROOT != "/" ] && rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
for x in $( cat %{S:2} | grep -v junit4 );
do
  rm $RPM_BUILD_ROOT/usr/share/eucalyptus/$( basename $x )
  ln -s $x $RPM_BUILD_ROOT/usr/share/eucalyptus/
done
rm $RPM_BUILD_ROOT/usr/share/eucalyptus/junit4*

sed -i -e 's#.*EUCALYPTUS=.*#EUCALYPTUS="/"#' \
       -e 's#.*HYPERVISOR=.*#HYPERVISOR="%{euca_hypervisor}"#' \
       -e 's#.*INSTANCE_PATH=.*#INSTANCE_PATH="/var/lib/eucalyptus/instances"#' \
       -e 's#.*VNET_BRIDGE=.*#VNET_BRIDGE="%{euca_bridge}"#' \
       -e 's#.*USE_VIRTIO_DISK=.*#USE_VIRTIO_DISK="1"#' \
       -e 's#.*USE_VIRTIO_ROOT=.*#USE_VIRTIO_ROOT="1"#' \
       $RPM_BUILD_ROOT/etc/eucalyptus/eucalyptus.conf

# Move init scripts into sbindir and call them from systemd
for x in $RPM_BUILD_ROOT/etc/init.d/*; do
   mv $x $RPM_BUILD_ROOT/%{_sbindir}/$( basename $x ).init
done
rmdir $RPM_BUILD_ROOT/etc/init.d

# Create the directories where components store their data
mkdir -p $RPM_BUILD_ROOT/var/lib/eucalyptus
touch $RPM_BUILD_ROOT/var/lib/eucalyptus/services
for dir in bukkits CC db keys ldap upgrade vmware volumes webapps; do
    install -d -m 0700 $RPM_BUILD_ROOT/var/lib/eucalyptus/$dir
done
install -d -m 0771 $RPM_BUILD_ROOT/var/lib/eucalyptus/instances

# Touch httpd config files that the init scripts create so we can %ghost them
touch $RPM_BUILD_ROOT/etc/eucalyptus/httpd-{cc,nc,tmp}.conf

# Add PolicyKit config on systems that support it
mkdir -p $RPM_BUILD_ROOT/var/lib/polkit-1/localauthority/10-vendor.d
cp -p tools/eucalyptus-nc-libvirt.pkla $RPM_BUILD_ROOT/var/lib/polkit-1/localauthority/10-vendor.d/eucalyptus-nc-libvirt.pkla

# Install systemd service files
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
install -p -m 644 $RPM_SOURCE_DIR/eucalyptus-cloud.service \
        $RPM_BUILD_ROOT%{_unitdir}/eucalyptus-cloud.service
install -p -m 644 $RPM_SOURCE_DIR/eucalyptus-cc.service \
        $RPM_BUILD_ROOT%{_unitdir}/eucalyptus-cc.service
install -p -m 644 $RPM_SOURCE_DIR/eucalyptus-nc.service \
        $RPM_BUILD_ROOT%{_unitdir}/eucalyptus-nc.service

%files
%doc LICENSE INSTALL README CHANGELOG
/etc/eucalyptus/eucalyptus.conf
/etc/eucalyptus/eucalyptus-version
/etc/eucalyptus/httpd.conf
%ghost /etc/eucalyptus/httpd-tmp.conf
%attr(-,root,eucalyptus) %dir /usr/lib/eucalyptus
%attr(4750,root,eucalyptus) /usr/lib/eucalyptus/euca_mountwrap
%attr(4750,root,eucalyptus) /usr/lib/eucalyptus/euca_rootwrap

/usr/sbin/euca_sync_key

%dir /usr/share/eucalyptus
/usr/share/eucalyptus/add_key.pl
/usr/share/eucalyptus/connect_iscsitarget.pl
/usr/share/eucalyptus/create-loop-devices
/usr/share/eucalyptus/disconnect_iscsitarget.pl
%doc /usr/share/eucalyptus/doc/
/usr/share/eucalyptus/euca_ipt
/usr/share/eucalyptus/euca_upgrade
/usr/share/eucalyptus/floppy
/usr/share/eucalyptus/get_iscsitarget.pl
/usr/share/eucalyptus/populate_arp.pl
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/eucalyptus
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/eucalyptus/db
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/eucalyptus/keys
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/eucalyptus/upgrade
# Can this file go into a single-component package?  What uses it?
/var/lib/eucalyptus/keys/cc-client-policy.xml
%attr(-,eucalyptus,eucalyptus) %dir /var/log/eucalyptus
%attr(-,eucalyptus,eucalyptus) %dir /var/run/eucalyptus

%files common-java
%{_unitdir}/eucalyptus-cloud.service
%{_sbindir}/eucalyptus-cloud
# cloud.d contains random stuff used by every Java component.  Most of it
# probably belongs in /usr/share, but moving it will be painful.
/etc/eucalyptus/cloud.d/
/usr/sbin/eucalyptus-cloud
/usr/share/eucalyptus/*jar*
# %doc /usr/share/eucalyptus/licenses/
%ghost /var/lib/eucalyptus/services
%attr(-,eucalyptus,eucalyptus) /var/lib/eucalyptus/webapps/

%files cloud
/etc/eucalyptus/cloud.d/init.d/01_pg_kernel_params
/usr/sbin/euca-lictool
/usr/share/eucalyptus/lic_default
/usr/share/eucalyptus/lic_template

%files walrus
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/eucalyptus/bukkits
/etc/eucalyptus/drbd.conf.example

%files sc
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/eucalyptus/volumes
/usr/share/eucalyptus/connect_iscsitarget_sc.pl
/usr/share/eucalyptus/disconnect_iscsitarget_sc.pl
/usr/lib/eucalyptus/liblvm2control.so

%files cc
%{_unitdir}/eucalyptus-cc.service
%{_sbindir}/eucalyptus-cc
%{axis2c_home}/services/EucalyptusCC/
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/eucalyptus/CC
%ghost /etc/eucalyptus/httpd-cc.conf
/etc/eucalyptus/vtunall.conf.template
/usr/lib/eucalyptus/shutdownCC
/usr/share/eucalyptus/dynserv.pl
# Is this used?
/var/lib/eucalyptus/keys/nc-client-policy.xml

%files nc
%config(noreplace) /etc/eucalyptus/libvirt.xsl
%dir /etc/eucalyptus/nc-hooks
/etc/eucalyptus/nc-hooks/example.sh
%{_unitdir}/eucalyptus-nc.service
%{_sbindir}/eucalyptus-nc
%{axis2c_home}/services/EucalyptusNC/
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/eucalyptus/instances
%ghost /etc/eucalyptus/httpd-nc.conf
/usr/sbin/euca_test_nc
/usr/share/eucalyptus/detach.pl
/usr/share/eucalyptus/gen_kvm_libvirt_xml
/usr/share/eucalyptus/gen_libvirt_xml
/usr/share/eucalyptus/getstats.pl
/usr/share/eucalyptus/get_sys_info
/usr/share/eucalyptus/get_xen_info
/usr/share/eucalyptus/partition2disk
/var/lib/polkit-1/localauthority/10-vendor.d/eucalyptus-nc-libvirt.pkla

%files gl
%{axis2c_home}/services/EucalyptusGL/

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

%files -n python%{?pybasever}-eucadmin
%{python_sitelib}/eucadmin*

%pre
getent group eucalyptus >/dev/null || groupadd -r eucalyptus
## FIXME:  Make QA (and Eucalyptus proper?) work with /sbin/nologin as the shell [RT:2092]
#getent passwd eucalyptus >/dev/null || \
#    useradd -r -g eucalyptus -d /var/lib/eucalyptus -s /sbin/nologin \
#    -c 'Eucalyptus' eucalyptus
getent passwd eucalyptus >/dev/null || \
    useradd -r -g eucalyptus -d /var/lib/eucalyptus \
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
    BACKUPDIR="/var/lib/eucalyptus/upgrade/eucalyptus.backup.`date +%%s`"
    ## FIXME:  What cleans this file up?
    echo "$BACKUPDIR" > /tmp/eucaback.dir
    mkdir -p "$BACKUPDIR"
    EUCABACKUPS=""
    for i in /var/lib/eucalyptus/keys/ /var/lib/eucalyptus/db/ /var/lib/eucalyptus/services /etc/eucalyptus/eucalyptus.conf /etc/eucalyptus/eucalyptus-version /usr/share/eucalyptus/; do
        if [ -e $i ]; then
            EUCABACKUPS="$EUCABACKUPS $i"
        fi
    done

    OLD_EUCA_VERSION=`cat /etc/eucalyptus/eucalyptus-version`
    echo "# This file was automatically generated by Eucalyptus packaging." > /etc/eucalyptus/.upgrade
    echo "$OLD_EUCA_VERSION:$BACKUPDIR" >> /etc/eucalyptus/.upgrade

    tar cf - $EUCABACKUPS 2>/dev/null | tar xf - -C "$BACKUPDIR" 2>/dev/null
fi
exit 0

%post
udevadm control --reload-rules

/usr/sbin/euca_conf -d / --instances /var/lib/eucalyptus/instances --hypervisor %{euca_hypervisor} --bridge %{euca_bridge}

if [ "$1" = "2" ]; then
    if [ -f /tmp/eucaback.dir ]; then
        BACKDIR=`cat /tmp/eucaback.dir`
        if [ -d "$BACKDIR" ]; then
            /usr/share/eucalyptus/euca_upgrade --old $BACKDIR --new / --conf >/var/log/eucalyptus/upgrade-config.log 2>&1
        fi
    fi
fi

# Final setup and set the new user
/usr/sbin/euca_conf --setup --user eucalyptus

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
# XXX: Is this right?
%{systemd_postun_with_restart} eucalyptus-cloud.service

%postun walrus
# XXX: Is this right?
%{systemd_postun_with_restart} eucalyptus-cloud.service

%postun sc
# XXX: Is this right?
%{systemd_postun_with_restart} eucalyptus-cloud.service

%preun common-java
%{systemd_preun} eucalyptus-cloud.service

%preun cc
%{_sbindir}/eucalyptus-cc.init cleanstop
%{systemd_preun} eucalyptus-cc.service

%preun nc
%{systemd_preun} eucalyptus-nc.service

%changelog
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

* Thu Jan 19 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.0.0-1
- Update to Eucalyptus 3.0

* Tue Jun  1 2010 Eucalyptus Release Engineering <support@eucalyptus.com> - 2.0.0-1
- Version 2.0 of Eucalyptus Enterprise Cloud
  - Windows VM Support
  - User/Group Management
  - SAN Integration
  - VMWare Hypervisor Support
