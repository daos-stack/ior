NAME                := ior
SRC_EXT             := gz
PKG_GIT_COMMIT      := eca135ce939e24c17a3a4a4b490c741bead43363
GITHUB_PROJECT      := hpc/$(NAME)
# This list of files that are in the upstream git repo but are not included in upstream's releases
PATCH_EXCLUDE_FILES := .travis.yml README_DAOS doc/sphinx/

include packaging/Makefile_packaging.mk
