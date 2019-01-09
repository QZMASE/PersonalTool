FOR /R . %%d IN (.) DO rd /s /q "%%d\__pycache__" 2>nul  
FOR /R . %%d IN (.) DO rd /s /q "%%d\.ipynb_checkpoints" 2>nul  

  
rem 如果Properties文件夹为空，则删除它  
rem FOR /R . %%d in (.) do rd /q "%%d\Properties" 2> nul  