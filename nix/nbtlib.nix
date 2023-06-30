{ lib
, buildPythonPackage
, fetchFromGitHub
, poetry-core
, numpy
}:

buildPythonPackage rec {
  pname = "nbtlib";
  version = "2.0.4";
  format = "pyproject";

  src = fetchFromGitHub {
    owner = "vberlier";
    repo = "nbtlib";
    rev = "v${version}";
    hash = "sha256-L8eX6/0qiQ4UxbmDicLedzj+oBjYmlK96NpljE/A3eI=";
  };

  patches = [
    ./0001-pyproject-fix-build-system-with-poetry-core.patch
  ];

  nativeBuildInputs = [
    poetry-core
  ];

  propagatedBuildInputs = [
    numpy
  ];

  pythonImportsCheck = [ "nbtlib" ];

  meta = with lib; {
    description = "A python library to read and edit nbt data";
    homepage = "https://github.com/vberlier/nbtlib";
    changelog = "https://github.com/vberlier/nbtlib/blob/${src.rev}/CHANGELOG.md";
    license = licenses.mit;
    maintainers = with maintainers; [ ];
  };
}
