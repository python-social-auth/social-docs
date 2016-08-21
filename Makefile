build:
	@ sphinx-build docs/ build/

publish: build
	@ rsync -avkz site/ tarf:sites/psa/

clean:
	@ rm -rf build
