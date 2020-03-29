echo Run Tesseract for Training.. 
tesseract.exe %1.font.exp0.tif %1.font.exp0 -l eng -psm 7 nobatch box.train 
 
echo Compute the Character Set.. 
unicharset_extractor.exe %1.font.exp0.box 
rem shapeclustering -F font_properties -U unicharet %1.font.exp0.tr
mftraining -F font_properties -U unicharset -O %1.unicharset %1.font.exp0.tr 
 
echo Clustering.. 
cntraining.exe %1.font.exp0.tr 
 
echo Rename Files.. 
if exist %1.normproto del %1.normproto 
if exist %1.inttemp del %1.inttemp 
if exist %1.pffmtable del %1.pffmtable 
if exist %1.shapetable del %1.shapetable  
rename normproto %1.normproto 
rename inttemp %1.inttemp 
rename pffmtable %1.pffmtable 
rename shapetable %1.shapetable  
 
echo Create Tessdata.. 
combine_tessdata.exe %1. 
 
echo Copy Tessdata...
copy /Y %1.traineddata TESSDATA_PREFIX
 
echo. & pause