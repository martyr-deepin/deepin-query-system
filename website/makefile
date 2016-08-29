dist: clean npm-install build GIT_HEAD
	tar zcf code-dist.tar.gz -C dest .
	rm -rf dest

develop:
	node node_modules/gulp/bin/gulp.js develop

build:
	node node_modules/gulp/bin/gulp.js build

GIT_HEAD:
	git rev-parse HEAD > dest/GIT_HEAD

npm-install:
	npm --registry=https://registry.npm.taobao.org install

clean:
	rm -f code-dist.tar.gz
	rm -rf dest

