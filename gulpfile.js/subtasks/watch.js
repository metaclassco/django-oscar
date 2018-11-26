var gulp = require('gulp');

gulp.task('watch', function() {
    gulp.watch('src/oscar/static/oscar/scss/**/*.scss', gulp.parallel('scss'));
});
