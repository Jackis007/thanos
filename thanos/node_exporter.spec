%define debug_package %{nil}
Name:node_exporter		
Version:0.16.0	
Release:	1%{?dist}
Summary:Prometheus agent (node_export)	

Group: Applications/Archiving
License: Apache2	
URL: https://github.com/prometheus/node_exporter/releases
Packager: amendge
Vendor: amendge
Source0: node_exporter-0.16.0.linux-amd64.tar.gz	
Source1: node_exporter.service
Source2: prometheus.sh
BuildRoot: %_topdir/BUILDROOT

BuildRequires:	gcc make

%description
premetheut agent (node_export)

%prep
%setup -q -n node_exporter-0.16.0.linux-amd64


%build


%install
mkdir	-p %{buildroot}/data/app/node_exporter
%{__install} -p -D -m 0755 node_exporter %{buildroot}/data/app/node_exporter
%{__install} -p -D -m 0644 %_topdir/SOURCES/node_exporter.service %{buildroot}/usr/lib/systemd/system/%{name}.service
%{__install} -p -D -m 0755 %_topdir/SOURCES/prometheus.sh %{buildroot}/data/app/node_exporter


%post
#rpm安装执行的脚本
if [ $1 == 1 ];then
	systemctl enable %{name}.service
	systemctl start node_exporter
	/bin/sh /data/app/node_exporter/prometheus.sh
fi

#rpm卸载前执行的脚本
%preun
if [ $1 == 0 ];then
	systemctl stop %{}.service >/dev/null 2>&1
	systemctl disable %{name}.service
fi


%clean
rm -rf %{buildroot}

%files
/data/app/node_exporter
/usr/lib/systemd/system/%{name}.service
/data/app/node_exporter/prometheus.sh

%changelog


prometheus.sh
#!/bin/bash

ip=$(ip addr show eth0|grep inet | awk '{ print $2; }' | sed 's/\/.*$//')
ahost=`echo $HOSTNAME`
#hostname=$(cat /etc/hostname)
idc=$(echo $ahost|awk -F "-" '{print $1}')
app=$(echo $ahost|awk -F "-" '{print $2}')
group=$(echo $ahost|awk -F "-" '{print $3}')

if [ "$app" != "test" ]
then
curl -X PUT -d "{\"ID\": \"${ahost}_${ip}\", \"Name\": \"node_exporter\", \"Address\": \"${ip}\", \"tags\": [\"idc=${idc}\",\"group=${group}\",\"app=${app}\",\"server=${hostname}\"], \"Port\": 9100,\"checks\": [{\"tcp\":\"${ip}:9100\",\"interval\": \"60s\"}]}" http://consul_Ip:8500/v1/agent/service/register
fi
