NAME    := ior
SRC_EXT := gz

GIT_COMMIT := 8475c7d30025dd5e39147c251bf84e1ed24b9858

# this needs to be formalized into packaging/Makefile_packaging.mk
BUILD_DEFINES := --define "commit $(GIT_COMMIT)"
RPM_BUILD_OPTIONS := $(BUILD_DEFINES)

include packaging/Makefile_packaging.mk

# This not really intended to run in CI.  It's meant as a developer
# convenience to generate the needed patch and add it to the repo to
# be committed.
# Should figure out a way to formalize this into
# packaging/Makefile_packaging.mk
$(VERSION)..$(GIT_COMMIT).patch:
	# it really sucks that GitHub's "compare" returns such dirty patches
	#curl -O 'https://github.com/hpc/$(NAME)/compare/$@'
	git clone git@github.com:hpc/$(NAME).git
	pushd $(NAME) &&                                \
	trap 'popd && rm -rf $(NAME)' EXIT;             \
	git diff $(VERSION)..$(GIT_COMMIT) --stat --    \
	    ':!.travis.yml'                             \
	    ':!README_DAOS'                             \
	    ':!doc/sphinx/';                            \
	git diff $(VERSION)..$(GIT_COMMIT) --           \
	    ':!.travis.yml'                             \
	    ':!README_DAOS'                             \
	    ':!doc/sphinx/'                             \
	    > ../$@
	git add $@
