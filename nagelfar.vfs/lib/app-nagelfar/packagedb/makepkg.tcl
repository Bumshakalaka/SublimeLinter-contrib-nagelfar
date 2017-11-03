# This is a utility to create the basis of a package database by extraction
# It does "package require" on it and sees what it gets.
# Use it like this:
# tclsh packagedb/makepkg.tcl <pkgname>

# Script used to extract things in syntaxbuild.tcl
set script {
    if {[catch { package require %pkg% }]} exit
    puts "PkgVersion: [package require %pkg%]"
    set ::tcl_interactive 1
    set ::syntaxbuild_allnamespace 1
    source syntaxbuild.tcl
    if {"%pkg%" ni $::kP} {
        lappend ::kP %pkg%
    }
    buildFile "%out%"
    exit
}

set pkgs [lrange $argv 0 end]
# Also process with base Tcl/Tk to give base database
lappend pkgs Tcl Tk
foreach pkg $pkgs {
    set outfile _pkg_[string map ":: _" $pkg]db.tcl
    puts "Collecting $pkg to $outfile"
    catch {
        #puts [string map "%pkg% $pkg" $script]
        exec tclsh << [string map "%pkg% $pkg %out% $outfile" $script]
    } out
    if {![file exists $outfile]} {
        puts "No file created. Bad package name?"
        exit
    }
    if {[regexp {PkgVersion: (\S+)} $out -> pkgVer]} {
        set v($pkg) $pkgVer
    } else {
        set v($pkg) Unknown
    }
}

proc preprocDb {data} {
    set resultLines {}
    set prevLine {}
    foreach line [split $data \n] {
        if {$prevLine ne ""} {
            append prevLine " " $line
            if {[catch {llength $prevLine}]} {
                # Not complete yet
                continue
            }
            set line $prevLine
            set prevLine ""
        }

        if {[string match "set ::known*" $line]} {
            if {[catch {llength $line}]} {
                # Not complete yet
                set prevLine $line
                continue
            }
            set var [lindex $line 1]
            set items [lindex $line 2]
            foreach item $items {
                lappend resultLines "lappend $var $item"
            }
        } else {
            lappend resultLines $line
        }
    }
    return $resultLines
}

# Packages that should not be included
foreach pkg {Tcl Tk} {
    set ch [open _pkg_${pkg}db.tcl]
    set lines [preprocDb [read $ch]]
    close $ch
    foreach line $lines {
        set done($line) 1
    }
}

set pkgs [lrange $argv 0 end]
foreach pkg $pkgs {
    set pkgfile _pkg_[string map ":: _" $pkg]db.tcl
    set outfile _f$pkgfile
    puts "Processing $pkgfile to $outfile"
    set ch [open $pkgfile]
    set lines [preprocDb [read $ch]]
    close $ch
    set resultLines {}
    foreach line $lines {
        if {[info exists done($line)]} continue
        lappend resultLines $line
    }
    if {[llength $resultLines] == 0} continue
    set ch [open $outfile w]
    puts $ch "# Extracted from $pkg version $v($pkg)"
    puts $ch [join $resultLines \n]
    close $ch
}
