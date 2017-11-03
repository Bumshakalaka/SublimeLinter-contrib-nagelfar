# This syntax definition is for the sqlite3 package
# package require sqlite3 3.8.6

##nagelfar syntax _stdclass_sqlite3 s x*
##nagelfar subcmd _stdclass_sqlite3 authorizer backup busy cache changes close collate collation_needed commit_hook complete copy enable_load_extension errorcode eval exists function incrblob interrupt last_insert_rowid nullvalue onecolumn profile progress rekey restore rollback_hook status timeout total_changes trace transaction unlock_notify update_hook version wal_hook

##nagelfar syntax _stdclass_sqlite3\ transaction x? c
##nagelfar syntax _stdclass_sqlite3\ eval 1: x 2: x c : x n c
##nagelfar syntax _stdclass_sqlite3\ onecolumn x
##nagelfar syntax _stdclass_sqlite3\ exists x
##nagelfar syntax _stdclass_sqlite3\ close

##nagelfar syntax _stdclass_sqlite3\ authorizer        x?
##nagelfar syntax _stdclass_sqlite3\ backup            x? x
##nagelfar syntax _stdclass_sqlite3\ busy              x
##nagelfar syntax _stdclass_sqlite3\ cache             s x*
##nagelfar subcmd _stdclass_sqlite3\ cache flush size
##nagelfar syntax _stdclass_sqlite3\ cache\ flush      0
##nagelfar syntax _stdclass_sqlite3\ cache\ size       x
##nagelfar syntax _stdclass_sqlite3\ changes           0
##nagelfar syntax _stdclass_sqlite3\ close             0
##nagelfar syntax _stdclass_sqlite3\ collate           x x
##nagelfar syntax _stdclass_sqlite3\ collation_needed  x
##nagelfar syntax _stdclass_sqlite3\ commit_hook       x?
##nagelfar syntax _stdclass_sqlite3\ complete          x
##nagelfar syntax _stdclass_sqlite3\ copy              x x x x? x?
##nagelfar syntax _stdclass_sqlite3\ enable_load_extension x
##nagelfar syntax _stdclass_sqlite3\ errorcode         x*
##nagelfar syntax _stdclass_sqlite3\ eval              1: x 2: x c : x n c
##nagelfar syntax _stdclass_sqlite3\ exists            x
##nagelfar syntax _stdclass_sqlite3\ function          x p? x
##nagelfar syntax _stdclass_sqlite3\ incrblob          o? x? x x x
##nagelfar syntax _stdclass_sqlite3\ interrupt         x*
##nagelfar syntax _stdclass_sqlite3\ last_insert_rowid 0
##nagelfar syntax _stdclass_sqlite3\ nullvalue         x
##nagelfar syntax _stdclass_sqlite3\ onecolumn         x
##nagelfar syntax _stdclass_sqlite3\ profile           x?
##nagelfar syntax _stdclass_sqlite3\ progress          x x?
##nagelfar syntax _stdclass_sqlite3\ rekey             x
##nagelfar syntax _stdclass_sqlite3\ restore           x? x
##nagelfar syntax _stdclass_sqlite3\ rollback_hook     x?
##nagelfar syntax _stdclass_sqlite3\ status            s
##nagelfar syntax _stdclass_sqlite3\ timeout           x
##nagelfar syntax _stdclass_sqlite3\ total_changes     0
##nagelfar syntax _stdclass_sqlite3\ trace             x?
##nagelfar syntax _stdclass_sqlite3\ transaction       x? c
##nagelfar syntax _stdclass_sqlite3\ unlock_notify     x?
##nagelfar syntax _stdclass_sqlite3\ update_hook       x?
##nagelfar syntax _stdclass_sqlite3\ version           0
##nagelfar syntax _stdclass_sqlite3\ wal_hook          x?

##nagelfar syntax sqlite3 do=_stdclass_sqlite3 x p*
##nagelfar option sqlite3 -vfs -readonly -create -nomutex -fullmutex -uri

##nagelfar package known sqlite3
