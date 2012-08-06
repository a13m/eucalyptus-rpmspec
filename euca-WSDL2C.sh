#!/bin/sh

CLASSPATH=$( build-classpath axis2/codegen axis2/adb axis2/adb-codegen axis2/kernel neethi wsdl4j commons-logging axiom/axiom-api axiom/axiom-dom axiom/axiom-impl XmlSchema backport-util-concurrent xalan-j2-serializer xalan-j2 ):${CLASSPATH} java org.apache.axis2.wsdl.WSDL2C $*

