<!--
//////////////////////////////////////////////////////////////////////////
/ ssr f-host scenario f-host
///
-->
## SSR F-Host

Tags: f-host

Will need to connect and verify connection, then toggle output and read input

* Hard reset device
* Find "Routing tables" on "SS1" serial port "30"
* Find "default config." on "SS1" serial port "120"
* Hard reset device
* Clear "SS1" serial port
* Find "ssr_cfg_discovery" on "SS1" serial port "120"
* Wait "15"

<!--
//////////////////////////////////////////////////////////////////////////
/ ssr f-host scenario f-host
///
-->
## SSR F-Host OLD

Tags: old

Will need to connect and verify connection, then toggle output and read input

* Hard reset device
* Find "Routing tables" on "SS1" serial port "30"
* Find "default config." on "SS1" serial port "120"
* Write "\r\n" on "SS1" serial port
* Clear "SS1" serial port
* Read all on "SS1" serial port
* Write "ls\n" on "SS1" serial port
* Read all on "SS1" serial port
* Clear "SS1" serial port
* FTP connect "192.168.1.10"
* FTP login "root" "root"
* FTP cwd "/molex_fs"
* FTP mkd "bin"
* FTP mkd "lib"
* FTP nlst
* FTP cwd "/molex_fs/bin"
* FTP storebinary "sup"
* FTP storebinary "ssc"
* FTP storebinary "cfg"
* FTP storebinary "agent_alpha"
* FTP storebinary "agent_nab"
* FTP storebinary "agent_nat"
* FTP nlst
* Write "chmod +x /molex_fs/bin/*\n" on "SS1" serial port
* Read all on "SS1" serial port
* Clear "SS1" serial port
* FTP cwd "/molex_fs/lib"
* FTP storebinary "libssim_lib.so"
* FTP nlst
* Write "ln -s /molex_fs/lib/libssim_lib.so /molex_fs/lib/libssim_lib.so.1\n" on "SS1" serial port
* Read all on "SS1" serial port
* Clear "SS1" serial port
* Hard reset device
* Wait "60"