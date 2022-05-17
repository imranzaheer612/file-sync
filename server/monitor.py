##
# wait wor changes from the client on the socket
# 
# client disconnected --- connected again --> registered ->>> monitor changes
# 
# 
# received command --> {mkdir "path"} --> mkdir at path 
# received command --> {rmdir "path"} --> remove dir at path
#  
# received command --> {mkFile "path"} --> make file at path 
# received command --> {rmFile "path"} --> remove file at path 
# #