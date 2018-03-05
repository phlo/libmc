export SPHINX_APIDOC_OPTIONS = members,show-inheritance,inherited-members

.PHONY: test
test:
	python -m unittest discover -s tests -p "test_*.py"

.PHONY: doc
doc: test
	find docs/ -maxdepth 1 ! -name docs \
		! -name Makefile \
		! -name source \
		-exec rm -rf {} \;
	make -C docs html
	mv docs/build/html/* docs
	mv docs/build/html/.nojekyll docs
	rm -rf docs/build

.PHONY: apidoc
apidoc:
	-rm ./docs/source/libmc.rst
	cd docs && sphinx-apidoc --implicit-namespaces -T -o source ../libmc \
	../tests \
	../docs \
	../libmc/asynchronousComposition.py \
	../libmc/bdd.py \
	../libmc/boole.py \
	../libmc/fa.py \
	../libmc/lts.py \
	../libmc/markdown.py \
	../libmc/maximumBisimulation.py \
	../libmc/maximumSimulation.py \
	../libmc/printing.py \
	../libmc/tarjan.py \
	../libmc/traversal.py
	sed -i '/Module contents/d' docs/source/libmc.rst
	sed -i '/---------------/,+1d' docs/source/libmc.rst
