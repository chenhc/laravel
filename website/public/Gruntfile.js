module.exports = function (grunt) {
    var path = require('path');
    var config = {
        pkg: grunt.file.readJSON('package.json'),
        watch: {
            livereload: {
                options: {
                    livereload: true
                },
                files: [
                    '*.html',
                    'css/*.css',
                    'app/**/*',
                    'js/**/*'
                ]
            },
            sass: {
                files: ['css/*.scss'],
                tasks: ['sass']
            }
        },
        shell: {
            bower: {
                command: path.resolve('node_modules/.bin/bower --allow-root install'),
                options: {
                    stdout: true,
                    stdin: true
                }
            }
        },
        uglify: {
            js: {
                files: [{
                    src: 'build/ilive.js',
                    dest: 'build/ilive.min.js'
                }]
            }
        },
        concat: {

        },

        sass: {
            compile: {
                options: {
                    outputStyle: 'compressed'
                },
                files: [{
                    src: 'css/app.scss',
                    dest: 'css/app.css'
                }]
            }
        },

        autoprefixer: {
            prefix: {
                files: [{
                    src: 'css/app.css',
                    dest: 'css/app.css'
                }]
            }
        }
    };
    require('matchdep').filterDev(['grunt-*', '!grunt-cli']).forEach(grunt.loadNpmTasks);


    grunt.initConfig(config);

};