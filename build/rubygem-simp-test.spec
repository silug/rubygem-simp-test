%{lua:
--
-- When building the RPM, declare macro 'pup_module_info_dir' with the path to
-- the top-level project directory.  This directory should contain the
-- following items:
--   * 'build' directory
--   * 'README.md' file
--
package_release = '1'
local potential_src_dirs = {
  rpm.expand('%{pup_module_info_dir}'),
  rpm.expand('%{_sourcedir}'),
  posix.getcwd(),
}
local src_dir = "\0"

for _k,dir in pairs(potential_src_dirs) do
  if (posix.stat(dir .. '/build', 'type') == 'directory') and (posix.stat(dir .. '/README.md', 'type') == 'regular') then
    src_dir = dir
    break
  end
end

if src_dir == "\0" then
  error(
    "FATAL: Cannot determine RPM project's src_dir!\n" ..
    "\t* Paths tried: '" .. table.concat(potential_src_dirs, "', '") .."\n" ..
    "\t* PROTIP: Declare macro %pup_module_info_dir\n"
  )
end

rel_file = (io.open(src_dir .. "/build/rpm_metadata/release", "r") or io.open(src_dir .. "/release", "r"))
if rel_file then
  for line in rel_file:lines() do
    if not (line:match("^%s*#") or line:match("^%s*$")) then
      package_release = line
      break
    end
  end
end
}

%global gemname simp-test

%global gemdir /usr/share/simp/ruby
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}
%global cli_version 0.4.13

# gem2ruby's method of installing gems into mocked build roots will blow up
# unless this line is present:
%define _unpackaged_files_terminate_build 0

Summary: a cli interface to configure/manage SIMP
Name: rubygem-%{gemname}
Version: %{cli_version}
Release: %{lua: print(package_release)}
Group: Development/Languages
License: Apache-2.0
URL: https://github.com/simp/rubygem-simp-test
Source0: %{name}-%{cli_version}-%{release}.tar.gz
Source1: %{gemname}-%{cli_version}.gem

BuildRequires: ruby(rubygems)
BuildRequires: ruby
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{cli_version}

%description
simp-test provides the 'simp' command to configure and manage SIMP.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{cli_version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
%setup -q

%build

%install
echo "======= %setup PWD: ${PWD}"
echo "======= %setup gemdir: %{gemdir}"

mkdir -p %{buildroot}/%{gemdir}
mkdir -p %{buildroot}/%{_bindir} # NOTE: this is needed for el7
gem install --local --install-dir %{buildroot}/%{gemdir} --force %{SOURCE1}

cat <<EOM > %{buildroot}%{_bindir}/simp
#!/bin/bash

PATH=/opt/puppetlabs/bin:/opt/puppetlabs/puppet/bin:\$PATH

EOM

%files
%defattr(0644, root, root, 0755)
%{geminstdir}
%exclude %{gemdir}/cache/%{gemname}-%{cli_version}.gem
%{gemdir}/specifications/%{gemname}-%{cli_version}.gemspec

%files doc
%doc %{gemdir}/doc

%changelog
* Thu Jun 24 2021 Chris Tessmer <8979062+op-ct@users.noreply.github.com> - 0.4.13
- New test: model on simp-cli to test RPM build

