build:
	@ sphinx-build docs/ build/

publish: build
	@ rsync -avkz site/ tarf:sites/psa/

open:
	@ $(BROWSER) build/index.html

clean:
	@ rm -rf build
