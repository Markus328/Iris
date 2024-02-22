{
  inputs = {
    nixpkgs = {
      url = "github:nixos/nixpkgs/nixpkgs-unstable";
    };
    flake-utils = {
      url = "github:numtide/flake-utils";
    };
  };
  outputs = {
    nixpkgs,
    flake-utils,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs {
        inherit system;
      };

      app = pkgs.writeShellScriptBin "run-app" ''python3 ./app.py'';
      shell = {
        packages = with pkgs; [
          python3
          app

          #Coding helpers
          nodejs
          pyright
          black
          isort
        ];
      };
    in {
      devShells = {
        default = pkgs.mkShell shell;
      };
      defaultPackage = app;
    });
}
