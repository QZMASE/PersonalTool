FOR /R . %%d IN (.) DO rd /s /q "%%d\__pycache__" 2>nul  
FOR /R . %%d IN (.) DO rd /s /q "%%d\.ipynb_checkpoints" 2>nul  

  
rem ���Properties�ļ���Ϊ�գ���ɾ����  
rem FOR /R . %%d in (.) do rd /q "%%d\Properties" 2> nul  