//The build will inline common dependencies into this file.

//For any third party dependencies, like jQuery, place them in the lib folder.

//Configure loading modules from the lib directory,
//except for 'app' ones, which are in a sibling
//directory.
requirejs.config({
	//baseUrl: "{{ STATIC_URL }}js/consumption",
    paths: {
        lib: './lib',
        dc: 'lib/dc',
        d3: 'lib/d3',
        crossfilter: 'lib/crossfilter',
        reductio: 'lib/reducito'
    },
    shim: {
        'lib/d3': {
            exports: 'd3'
        },
        'lib/dc': {
			deps: ['lib/crossfilter','lib/d3'],
            exports: 'dc'
        },

		"lib/c3": {
            exports: 'c3'
        },

        'lib/crossfilter': {
			exports: 'crossfilter'
        },

		"lib/jquery": {
            exports: 'jquery'
        },

		"lib/reductio": {
            deps: ['lib/crossfilter'],
			exports: 'reductio'
		}
    }
});
