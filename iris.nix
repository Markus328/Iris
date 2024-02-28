{
  pkgs,
  python,
  ...
}:
with pkgs;
  writeShellScriptBin "iris" ''
    ${python}/bin/python3 ${./app.py} $@
  ''
