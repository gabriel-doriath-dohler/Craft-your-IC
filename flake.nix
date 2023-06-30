{
  description = "V-RISC-V";

  inputs = {
    nixpkgs.url = "nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    pre-commit-hooks.url = "github:cachix/pre-commit-hooks.nix";
  };

  outputs = { self, nixpkgs, flake-utils, pre-commit-hooks }:
    flake-utils.lib.eachDefaultSystem (system:
      let pkgs = import nixpkgs { inherit system; };
      in {
        checks = {
          pre-commit-check = pre-commit-hooks.lib.${system}.run {
            src = ./.;
            hooks = {
              # Nix
              deadnix.enable = true;
              nil.enable = true;
              nixfmt.enable = true;
              statix.enable = true;
              # Python
              isort.enable = true;
              black.enable = true;
              # Markdown
              markdownlint.enable = true;
            };
          };
        };

        devShell = pkgs.mkShell {
          buildInputs = [
            (pkgs.python3.withPackages (ps:
              [
                (ps.callPackage ./nix/litemapy.nix {
                  nbtlib = ps.callPackage ./nix/nbtlib.nix { };
                })
              ]))
          ];

          inherit (self.checks.${system}.pre-commit-check) shellHook;
        };
      });
}
