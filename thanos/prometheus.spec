%define debug_package %{nil}
Name:prometheus		
Version:2.3.1	
Release:	1%{?dist}
Summary:Prometheus server

%define _user prometheus
%define _group prometheus

Group: Applications/Archiving
License: Apache2	
URL: https://github.com/prometheus/node_exporter/releases
Packager: amendge
Vendor: amendge
Source0: prometheus-2.3.1.linux-amd64.tar.gz
Source1:prometheus.service
BuildRoot: %_topdir/BUILDROOT

BuildRequires:	gcc make

%description
Prometheus server

%prep
%setup -q -n prometheus-2.3.1.linux-amd64


%build


%install
mkdir	-p %{buildroot}/data/app/prometheus
mkdir   -p %{buildroot}/data/app/prometheus/console_libraries
mkdir   -p %{buildroot}/data/app/prometheus/consoles
%{__install} -p -D -m 0755 prometheus %{buildroot}/data/app/prometheus
%{__install} -p -D -m 0755 promtool %{buildroot}/data/app/prometheus
%{__install} -p -D -m 0755 prometheus.yml %{buildroot}/data/app/prometheus
%{__install} -p -D -m 0644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/%{name}.service
for dir in console_libraries consoles; do
  for file in ${dir}/*; do
    install -m 644 ${file} %{buildroot}/data/app/prometheus/${file}
  done
done

#rpm安装前执行的脚本
%pre
if [ $1 == 1 ];then
    chmod 4755 /usr/sbin/ss
    if [ -z "`grep ^%{_user} /etc/passwd`" ]; then
        groupadd %{_group} 
        useradd -g prometheus -m %{_user} -s /sbin/nologin
    fi
fi

#rpm安装后执行的脚本
%post
if [ $1 == 1 ];then
	HNAME=$(ip addr | egrep -o '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' | egrep "^172\.[0-9]|^10\." | egrep -v "\.255$" | awk -F. '{print $1"."$2"."$3"."$4}' | head -n 1)
        sed -i s@"localhost"@"$HNAME"@g /data/app/prometheus/prometheus.yml
	systemctl enable %{name}.service
	systemctl start prometheus
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
/data/app/prometheus
/usr/lib/systemd/system/%{name}.service

%changelog

