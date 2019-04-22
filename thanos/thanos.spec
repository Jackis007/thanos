%define debug_package %{nil}
Name:thanos		
Version:0.1.0	
Release:	1%{?dist}
Summary:Prometheus sidecar (thanos)	

Group: Applications/Archiving
License: Apache2	
URL: https://github.com/prometheus/node_exporter/releases
Packager: amendge
Vendor: amendge
Source0: thanos-0.1.0.linux-amd64.tar.gz	
Source1:thanos.service
Source2:thanos
BuildRoot: %_topdir/BUILDROOT

BuildRequires:	gcc make 

%description
premetheut sidecar (thanos)

%prep
%setup -q -n thanos-0.1.0.linux-amd64


%build


%install
mkdir	-p %{buildroot}/data/app/thanos
mkdir   -p %{buildroot}/etc/sysconfig/
%{__install} -p -D -m 0755 thanos %{buildroot}/data/app/thanos
%{__install} -p -D -m 0644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/%{name}.service

#rpm安装执行的脚本
%post
if [ $1 == 1 ];then
	echo '
#thanos
S3_BUCKET="prom_thanos"
S3_ENDPOINT=""
S3_ACCESS_KEY=""
S3_SECRET_KEY=""
	'>>/etc/sysconfig/thanos

	HNAME=$(ip addr | egrep -o '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' | egrep "^172\.[0-9]|^10\." | egrep -v "\.255$" | awk -F. '{print $1"."$2"."$3"."$4}' | head -n 1)
	sed -i s@"9.9.9.9"@"$HNAME"@g /usr/lib/systemd/system/thanos.service
	systemctl enable %{name}.service
	systemctl daemon-reload
        systemctl start thanos
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
/data/app/thanos
/usr/lib/systemd/system/%{name}.service

%changelog

