export PYTHONPATH := $(PYTHONPATH):$(pwd)

test: test/test.py
	@python $<

doc: apidoc
	make -C doc clean
	make -C doc html

apidoc:
	-rm ./doc/source/{modules,libmc}.rst
	cd doc && sphinx-apidoc -o source ../

.PHONY: apidoc doc test
