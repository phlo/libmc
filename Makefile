export PYTHONPATH := $(PYTHONPATH):$(pwd)

test: test/test.py
	@python $<

doc: apidoc
	rm -rf doc/html
	make -C doc html
	mv doc/build/html doc
	rm -rf doc/build

apidoc:
	-rm ./doc/source/{modules,libmc}.rst
	cd doc && sphinx-apidoc -o source ../

.PHONY: apidoc doc test
