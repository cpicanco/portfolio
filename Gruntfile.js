// Do grunt-related things in here
module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    concat: {
      cssac: {
        src: [
              'css/min/bootstrap.min.css',
              'css/min/sticky-footer.min.css',
              'css/min/academicons.min.css',
              'css/min/achievements.min.css',
              'css/min/timeline.min.css',
              'css/min/self.min.css'
              ],

        dest: 'css/portfolio-styles-achievements.concat.css'

      },

      csscover: {
        src: ['css/min/bootstrap.min.css',
              'css/min/cover.min.css'
              ],
        dest: 'css/cover-styles.concat.css',
      },    
      cssport: {
        src: ['css/min/bootstrap.min.css',
              'css/min/starter-template.min.css',
              'css/min/sticky-footer.min.css',
              'css/min/academicons.min.css',
              'css/min/self.min.css'
              ],
        dest: 'css/portfolio-styles.concat.css',
      }
    },

    cssmin: {
      dynamic: {
        files: [
          {          
            expand: true,     // Enable dynamic expansion.
            cwd: 'css/src',      // Src matches are relative to this path.
            src: ['*.css', '!achievements-full.css'], // Actual pattern(s) to match.
            dest: 'css/min',   // Destination path prefix.
            ext: '.min.css',   // Dest filepaths will have this extension.
            extDot: 'first'   // Extensions in filenames begin after the first dot
          },
        ],
      }     
    },

    uglify: {
      // options: {
      //   banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n'
      // },
      dynamic: {
        files: [
          {
            expand: true,     // Enable dynamic expansion.
            cwd: 'js/src',      // Src matches are relative to this path.
            src: ['*.js'], // Actual pattern(s) to match.
            dest: 'js',   // Destination path prefix.
            ext: '.min.js',   // Dest filepaths will have this extension.
            extDot: 'first'   // Extensions in filenames begin after the first dot
          },
        ],
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.registerTask('default', [ 'cssmin:dynamic','uglify:dynamic', 'concat' ]);

};