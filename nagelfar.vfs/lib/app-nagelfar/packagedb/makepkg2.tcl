# This is a utility to create the basis of a package database by parsing
# It tries to locate the source, or is given the source to parse
# Use it like this:
# tclsh packagedb/makepkg2.tcl <pkgname>
# tclsh packagedb/makepkg2.tcl <pkgname> <file names>

if {$argc < 1} {
    puts "Usage: tclsh packagedb/makepkg2.tcl <pkgname> ?file names?"
    exit
}
set pkg [lindex $argv 0]
set outfile _f_pkg_[string map ":: _" $pkg]db.tcl

set donepkg {Tcl Tk}

if {$argc == 1} {
    set todopkg [list $pkg]
    while {[llength $todopkg] > 0} {
        set pkg [lindex $todopkg 0]
        set todopkg [lrange $todopkg 1 end]
        lappend donepkg $pkg
    
        # Try to get the files through some guesses
        if {[catch {exec tclsh << "puts \[package require $pkg\] ; exit"} ver]} {
            puts "Could not find package $pkg, skipping"
            continue
        }
        puts "Detected version $ver of package $pkg"
        set ifn [exec tclsh << "package require $pkg ; puts \[package ifneeded $pkg $ver\] ; exit"]
        set psrc {}
        foreach line [split $ifn \n] {
            set line [string trimleft $line]
            if {![string match "source *" $line]} continue
            lappend psrc [lindex $line 1]
        }
        # Look through sources
        foreach f $psrc {
            lappend src $f
            set ch [open $f]
            set data [read $ch]
            close $ch
            foreach stmt [regexp -all -inline -line {package require .*$} $data] {
                if {[catch {llength $stmt}]} {
                    set stmt [regexp -all -inline {\S+} $stmt]
                }
                set subpkg [lindex $stmt 2]
                if {$subpkg in $donepkg} {
                    continue
                }
                puts "Detected sub-require: $stmt"
                lappend todopkg $subpkg
            }
            foreach stmt [regexp -all -inline -line {^\s*source .*$} $data] {
                set stmt [string trimleft $stmt]
                # Recognise common source idiom
                if {[regexp {join.*dirname.*script.*?(\S+)\]} $stmt -> other]} {
                    set other [file join [file dirname $f] $other]
                    if {[file exists $other]} {
                        lappend src $other
                    } else {
                        puts "Detected but could not find '$other'"
                    }
                } elseif {[regexp {source .*?(\S+)\]$} $stmt -> other]} {
                    set other [file join [file dirname $f] $other]
                    if {[file exists $other]} {
                        lappend src $other
                    } else {
                        puts "Detected but could not find '$other'"
                    }
                } elseif {[regexp {source\s+(\S+)} $stmt -> other]} {
                    set other [file join [file dirname $f] $other]
                    if {[file exists $other]} {
                        lappend src $other
                    } else {
                        puts "Detected but could not find '$other'"
                    }
                }
            }
        }
    }
    puts "Detected sources:"
    puts [join $src \n]
} else {
    set src [lrange $argv 1 end]
    puts "Given sources:"
    puts [join $src \n]
}

puts "Generating $outfile"
exec ./nagelfar.tcl -header $outfile {*}$src
