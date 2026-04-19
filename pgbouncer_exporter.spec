%global debug_package %{nil}
%global user postgres
%global group postgres

Name: pgbouncer_exporter
Version: 0.12.0
Release: 1%{?dist}
Summary: Prometheus exporter for PgBouncer.
License: MIT
URL:     https://github.com/prometheus-community/pgbouncer_exporter

Source0: https://github.com/prometheus-community/pgbouncer_exporter/releases/download/v%{version}/%{name}-%{version}.linux-amd64.tar.gz
Source1: %{name}.unit
Source2: %{name}.default

%{?systemd_requires}
Requires(pre): shadow-utils

%description
Prometheus exporter for PgBouncer. Exports metrics at 9127/metrics

%prep
%setup -q -n %{name}-%{version}.linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}%{_sharedstatedir}/%{name}
install -D -m 755 %{name} %{buildroot}%{_bindir}/%{name}
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/%{name}
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

%pre
getent group postgres >/dev/null || groupadd -r postgres
getent passwd postgres >/dev/null || \
useradd -r -g postgres -d %{_sharedstatedir}/%{name} -s /sbin/nologin -c "pgbouncer_exporter service" postgres
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/default/%{name}
%dir %attr(755, %{user}, %{group}) %{_sharedstatedir}/%{name}
%{_unitdir}/%{name}.service

%changelog
* Tue Mar 31 2026 Ivan Garcia <igarcia@cloudox.org> - 0.12.0
- Initial packaging for the 0.12.0 branch
