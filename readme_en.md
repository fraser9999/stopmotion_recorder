#  StopMotion-Webcam  Recorder 
 
 A  **Python-based  stop-motion  recording  tool**  with  USB  webcam.

 It  offers  a  **live  preview**  that  transparently  overlays  up  to
 **  3  previous  still  images**,  and  allows  
 **  capture  in  full  camera  resolution**.
 

 ##  Features  -  Capture  individual  images  using  the  **spacebar** 
     or  button-  Preview  in  **640×480  pixels**  (stable  size)-
     Saved  images  in  **full  camera  resolution**- 
     Up  to  **3  background  images**  as  a  transparent  reference- 
     Webcam  and  background  image  transparency  adjustable  via  **slider**-
     Folder  selection  for  saved  images-  Delete  function  for  the  last
     saved  image-  Faster  start  via  DirectShow  (Windows)


 ##  Requirements-  Python  3.10+  -  Windows  

    (optimal  for  DirectShow;  minor  adjustments  may  be  necessary  under  Linux)-
    USB  webcam  (Logitech  recommended,  but  any  UVC-compatible  camera  will  work)


 ###  Required  Python  packages
 
    ```bash  
    pip  install  opencv-python  Pillow 