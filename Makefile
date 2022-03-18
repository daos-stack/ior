NAME                := ior
SRC_EXT             := gz
PKG_GIT_COMMIT      := d3574d536643475269d37211e283b49ebd6732d7
GITHUB_PROJECT      := hpc/$(NAME)
# This list of files that are in the upstream git repo but are not included in upstream's releases
PATCH_EXCLUDE_FILES := .travis.yml README_DAOS doc/sphinx/

include packaging/Makefile_packaging.mk
