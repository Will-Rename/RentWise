{pkgs}: {
  deps = [
    pkgs.python312Packages.flask
    pkgs.libev
    pkgs.libmysqlclient
  ];
}
