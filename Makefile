NAME                := ior
SRC_EXT             := gz
GIT_COMMIT          := eca135ce939e24c17a3a4a4b490c741bead43363
# This list of files that are in the upstream git repo but are not included in upstream's releases
PATCH_EXCLUDE_FILES := .travis.yml README_DAOS doc/sphinx/

include packaging/Makefile_packaging.mk
