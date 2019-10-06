#
# spec file for package container-registry-systemd
#
# Copyright (c) 2019 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


Name:           container-registry-systemd
Version:        0.0+git20191006.f22e281
Release:        0
Summary:        Systemd service files and config files for container-registry image
License:        MIT
URL:            https://github.com/thkukuk/container-registry-systemd
Source:         container-registry-systemd-%{version}.tar.xz
Requires:       certstrap
Requires(post): %fillup_prereq
BuildArch:      noarch

%description
This package contains the configuration files, systemd units and scripts
to run the openSUSE container registry managed by systemd.

%prep
%setup -q

%build

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_sysconfdir}/registry/certs
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_fillupdir}
install -m 644 container-registry.service %{buildroot}%{_unitdir}/
install -m 644 config.yml %{buildroot}%{_sysconfdir}/registry
install -m 644 sysconfig.container-registry %{buildroot}%{_fillupdir}/
install -m 755 create-container-registry-certs.sh %{buildroot}%{_bindir}/create-container-registry-certs
# create symlink for rccontainer-registry
ln -s /sbin/service %{buildroot}%{_sbindir}/rccontainer-registry

%pre
%service_add_pre container-registry.service

%post
%{fillup_only -n container-registry}
%service_add_post container-registry.service

%preun
%service_del_preun container-registry.service

%postun
%service_del_postun container-registry.service

%files
%license LICENSE
%dir %{_sysconfdir}/registry
%config(noreplace) %{_sysconfdir}/registry/config.yml
%{_unitdir}/container-registry.service
%{_fillupdir}/sysconfig.container-registry
%{_bindir}/create-container-registry-certs
%{_sbindir}/rccontainer-registry

%changelog
