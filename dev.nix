{pkgs, ...}: {
  packages = with pkgs; [
    python3
    (writeShellScriptBin "run-app" ''python3 ./app.py $@'')
    #Coding helpers
    nodejs
    pyright
    black
    isort
  ];
}
