# Extracted from ftp version 2.4.12
lappend ::knownPackages ftp
set ::syntax(ftp::Append) {r 1}
set ::syntax(ftp::Cd) {r 1 2}
set ::syntax(ftp::Close) 1
set ::syntax(ftp::CloseDataConn) 1
set ::syntax(ftp::Command) {r 2}
set ::syntax(ftp::CopyNext) {r 2 3}
set ::syntax(ftp::Delete) 2
set ::syntax(ftp::DisplayMsg) {r 2 3}
set ::syntax(ftp::ElapsedTime) 2
set ::syntax(ftp::FileSize) {r 1 2}
set ::syntax(ftp::Get) {r 1}
set ::syntax(ftp::HandleData) 2
set ::syntax(ftp::HandleList) 2
set ::syntax(ftp::HandleOutput) 2
set ::syntax(ftp::HandleVar) 2
set ::syntax(ftp::InitDataConn) 4
set ::syntax(ftp::LazyClose) 1
set ::syntax(ftp::List) {r 1 2}
set ::syntax(ftp::ListPostProcess) 1
set ::syntax(ftp::MkDir) 2
set ::syntax(ftp::ModTime) {r 1 3}
set ::syntax(ftp::ModTimePostProcess) 1
set ::syntax(ftp::NList) {r 1 2}
set ::syntax(ftp::Newer) {r 2 3}
set ::syntax(ftp::Open) {r 3}
set ::syntax(ftp::OpenActiveConn) 1
set ::syntax(ftp::OpenControlConn) {r 1 2}
set ::syntax(ftp::OpenPassiveConn) 2
set ::syntax(ftp::Put) {r 1}
set ::syntax(ftp::PutsCtrlSock) {r 1 2}
set ::syntax(ftp::Pwd) 1
set ::syntax(ftp::Quote) {r 1}
set ::syntax(ftp::Reget) {r 2 5}
set ::syntax(ftp::Rename) 3
set ::syntax(ftp::RmDir) 2
set ::syntax(ftp::StateHandler) {r 1 2}
set ::syntax(ftp::Timeout) 1
set ::syntax(ftp::Type) {r 1 2}
set ::syntax(ftp::WaitComplete) 2
set ::syntax(ftp::WaitOrTimeout) 1
