export PYTHONPATH := $(PYTHONPATH):$(pwd)

.PHONY: test
test: test/test.py
	@python $<

doc: libmc.py
	find docs/ -maxdepth 1 ! -name docs \
		! -name Makefile \
		! -name source \
		-exec rm -rf {} \;
	-rm ./docs/source/{modules,libmc}.rst
	cd docs && sphinx-apidoc -o source ../
	make -C docs html
	mv docs/build/html/* docs
	rm -rf docs/build
