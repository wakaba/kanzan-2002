all: build

WGET = wget
CURL = curl
GIT = git

updatenightly: local/bin/pmbp.pl build
	$(CURL) -s -S -L https://gist.githubusercontent.com/wakaba/34a71d3137a52abb562d/raw/gistfile1.txt | sh
	$(GIT) add modules
	perl local/bin/pmbp.pl --update
	$(GIT) add config
	$(CURL) -sSLf https://raw.githubusercontent.com/wakaba/ciconfig/master/ciconfig | RUN_GIT=1 REMOVE_UNUSED=1 perl

## ------ Setup ------

deps: always
	true # dummy for make -q
ifdef PMBP_HEROKU_BUILDPACK
else
	$(MAKE) git-submodules
endif
	$(MAKE) pmbp-install

git-submodules:
	$(GIT) submodule update --init

PMBP_OPTIONS=

local:
	mkdir -p local

local/bin/pmbp.pl: local
	mkdir -p local/bin
	$(CURL) -s -S -L https://raw.githubusercontent.com/wakaba/perl-setupenv/master/bin/pmbp.pl > $@
pmbp-upgrade: local/bin/pmbp.pl
	perl local/bin/pmbp.pl $(PMBP_OPTIONS) --update-pmbp-pl
pmbp-update: git-submodules pmbp-upgrade
	perl local/bin/pmbp.pl $(PMBP_OPTIONS) --update
pmbp-install: pmbp-upgrade
	perl local/bin/pmbp.pl $(PMBP_OPTIONS) --install \
            --create-perl-command-shortcut @perl \
            --create-perl-command-shortcut @prove \
	    --create-perl-command-shortcut @plackup=perl\ modules/twiggy-packed/script/plackup

build: local local/misc-a1.txt intro.ja.html kanzan.cgi

intro.ja.html: intro.ja.html.orig local/misc-a1.txt
	perl -p -e 's{<!--FooterA1-->}{open F,"local/misc-a1.txt";local$$/=undef;<F>}e;$$_' < intro.ja.html.orig > $@
kanzan.cgi: kanzan.cgi.orig local/misc-a1.txt
	perl -p -e 's{<!--FooterA1-->}{open F,"local/misc-a1.txt";local$$/=undef;<F>}e;$$_' < kanzan.cgi.orig > $@

local/misc-a1.txt:
	$(CURL) -sSf https://gist.githubusercontent.com/wakaba/e6ba0fb1c4a75c0d4824e1d27107342e/raw/misc-a1.txt > $@

create-commit-for-heroku:
	git remote rm origin
	rm -fr deps/pmtar/.git deps/pmpp/.git modules/*/.git
	git add -f deps/pmtar/* #deps/pmpp/*
	#rm -fr ./t_deps/modules
	#git rm -r t_deps/modules
	git rm .gitmodules
	git rm modules/* --cached
	git add -f modules/*/*
	git commit -m "for heroku"

## ------ Tests ------

PROVE = ./prove

test: test-deps test-main

test-deps: deps

test-main:
	$(PROVE) t/*.t

always:

## License: Public Domain.
