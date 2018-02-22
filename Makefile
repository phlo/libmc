# .PHONY: bdd
# bdd: bddtest
	# @/tmp/bddtest > /tmp/cbdd.log
	# @python test/test.py > /tmp/pybdd.log
	# gview -d /tmp/pybdd.log /tmp/cbdd.log
	# # diff --color -u -W $$(tput cols) /tmp/pybdd.log /tmp/cbdd.log
#
# bddtest: bddtest.c
	# gcc -m32 -g -Wall -Wextra -pedantic -I ../bdd4teaching $< -o /tmp/$@

.PHONY: test
test:
	python -m unittest discover --locals -s tests -p "test_*.py"

doc: libmc
	find docs/ -maxdepth 1 ! -name docs \
		! -name Makefile \
		! -name source \
		-exec rm -rf {} \;
	-rm ./docs/source/{modules,libmc}.rst
	cd docs && sphinx-apidoc -d 1 -o source ../
	make -C docs html
	mv docs/build/html/* docs
	mv docs/build/html/.nojekyll docs
	rm -rf docs/build
