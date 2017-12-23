export PYTHONPATH := $(PYTHONPATH):$(pwd)

.PHONY: test
test: test/test.py
	@python $<

doc: libmc.py
	find doc/ -maxdepth 1 ! -name doc \
		! -name Makefile \
		! -name source \
		-exec rm -rf {} \;
	-rm ./doc/source/{modules,libmc}.rst
	cd doc && sphinx-apidoc -o source ../
	make -C doc html
	mv doc/build/html/* doc
	rm -rf doc/build
