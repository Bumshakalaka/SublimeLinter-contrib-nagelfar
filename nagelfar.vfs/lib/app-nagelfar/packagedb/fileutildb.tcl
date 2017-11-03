# Extracted from fileutil version 1.14.6
lappend ::knownPackages fileutil
set ::syntax(fileutil::appendToFile) {r 0}
set ::syntax(fileutil::cat) {r 0}
set ::syntax(fileutil::fileType) 1
set ::syntax(fileutil::find) {r 0 2}
set ::syntax(fileutil::findByPattern) {r 1}
set ::syntax(fileutil::foreachLine) {n x c}
set ::syntax(fileutil::fullnormalize) 1
set ::syntax(fileutil::grep) {r 1 2}
set ::syntax(fileutil::insertIntoFile) {r 0}
set ::syntax(fileutil::install) {r 0}
set ::syntax(fileutil::jail) 2
set ::syntax(fileutil::lexnormalize) 1
set ::syntax(fileutil::relative) 2
set ::syntax(fileutil::relativeUrl) 2
set ::syntax(fileutil::removeFromFile) {r 0}
set ::syntax(fileutil::replaceInFile) {r 0}
set ::syntax(fileutil::stripN) 2
set ::syntax(fileutil::stripPath) 2
set ::syntax(fileutil::stripPwd) 1
set ::syntax(fileutil::tempdir) {r 0}
set ::syntax(fileutil::tempdirReset) 0
set ::syntax(fileutil::tempfile) {r 0 1}
set ::syntax(fileutil::test) {x x n. x.}
set ::syntax(fileutil::touch) {r 0}
set ::syntax(fileutil::updateInPlace) {r 0}
set ::syntax(fileutil::writeFile) {r 0}
