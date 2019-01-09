@echo Off  
del /s /a *.exe *.suo *.ncb *.user *.pdb *.netmodule *.aps *.ilk *.sdf *.log *.obj *.idb *.lastbuildstate *.tlog 2>nul  
FOR /R . %%d IN (.) DO rd /s /q "%%d\x64" 2>nul  
FOR /R . %%d IN (.) DO rd /s /q "%%d\Release" 2>nul  

  
rem 如果Properties文件夹为空，则删除它  
rem FOR /R . %%d in (.) do rd /q "%%d\Properties" 2> nul  