{
  description = "python312";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05";
  };
  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in {
      devShells.${system}.default = pkgs.mkShell {
        packages = [
          pkgs.python312
          pkgs.poetry
          pkgs.openssl
          pkgs.libffi
          pkgs.pkg-config
          pkgs.rustc
          pkgs.cargo
        ];
        shellHook = ''
          if [ ! -d .venv ]; then
            poetry install
          fi
          source .venv/bin/activate
        '';
      };
    };
}
