DELETE FILE soh.cdx
CLOSE DATABASES
USE soh
INDEX on co_no TAG sohi OF soh
INDEX on DTOC(tgl,1)+co_no TAG sohj OF soh
INDEX on status_+cst+DTOC(tgl,1) TAG sohk OF soh
CLOSE data