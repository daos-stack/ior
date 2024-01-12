NAME                := ior
SRC_EXT             := gz
GITHUB_PROJECT      := hpc/$(NAME)
# This list of files that are in the upstream git repo but are not included in upstream's releases
PATCH_EXCLUDE_FILES := .travis.yml README_DAOS doc/sphinx/

include packaging/Makefile_packaging.mk
