{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  buildInputs = [
    (pkgs.python3.withPackages (ps: [
      (ps.callPackage ./nix/litemapy.nix {
        nbtlib = ps.callPackage ./nix/nbtlib.nix { };
      })
    ]))
  ];
}
