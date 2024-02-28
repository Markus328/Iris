{
  inputs = {
    nixpkgs = {
      url = "github:nixos/nixpkgs/nixpkgs-unstable";
    };
  };
  outputs = {
    nixpkgs,
    self,
    ...
  }: let
    system = "x86_64-linux";
    pkgs = import nixpkgs {
      inherit system;
    };

    python = pkgs.python3;
    shell = import ./dev.nix {inherit pkgs python;};

    iris = import ./iris.nix {inherit pkgs python;};
  in {
    devShells.${system} = {
      default = pkgs.mkShell shell;
    };
    packages.${system} = {
      default = iris;
    };
    apps.${system} = {
      default = {
        type = "app";
        program = "${self.packages.${system}.default}/bin/iris";
      };
    };
  };
}
