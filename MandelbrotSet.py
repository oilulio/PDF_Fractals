#!/usr/bin/python3

# Code generation script for PDF fractals.
# PDF file will generate fractal on the fly pixel by pixel.  It is not an image.
# Just writes to pdf file, rather than uses libraries ..

"""	
Copyright (C) 2014-2023  S Combes

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>."""


import datetime
import time

TITLE="Mandelbrot Set"
AUTHOR="S Combes"
XSHIFT="-0.6"  # note strings
SCALE="0.8" # Works on the default A4
DEPTH=32   # Equipotentials to show.  Don't exceed 32 if using colours
SQ_THRESHOLD="15" # Squared distance, as string, considered to show out of set
BANDW=False  # Use colour?

#From https://stackoverflow.com/questions/16500656/which-color-gradient-is-used-to-color-mandelbrot-in-wikipedia; by q9f 
#  R   G   B
COLOURS=\
[[66,30,15], # brown 3
 [25,7,26], # dark violett
 [9,1,47], # darkest blue
 [4,4,73], # blue 5
 [0,7,100], # blue 4
 [12,44,138], # blue 3
 [24,82,177], # blue 2
 [57,125,209], # blue 1
 [134,181,229], # blue 0
 [211,236,248], # lightest blue
 [241,233,191], # lightest yellow
 [248,201,95], # light yellow
 [255,170,0], # dirty yellow
 [204,128,0], # brown 0
 [153,87,0], # brown 1
 [106,52,3]] # brown 2

newline="\x0D" #\x0A"  # May be CR, LF or CRLF
index=[0]*20
XREF_STATES={"used":"n", "free":"f"}

result="%PDF-1.5"+newline  # Header
# See https://opensource.adobe.com/dc-acrobat-sdk-docs/pdfstandards/pdfreference1.5_v6.pdf

def addObject(n,text,anObject=True):   # append nth Object

  global result
  global index
  
  index[n]=len(result)
  if (anObject):
    result+=str(n)+" 0 obj"+newline
  for t in text:
    result+=(t+newline)
  if (anObject):
    result+="endobj"+newline

  result+=newline

  return

def streamLength(stream):
  length=0
  for s in stream:
    if (s!="endstream" and s!="stream"):
      length+=len(s)+2   # +2 for newline chars

  return str(length)
    

addObject(1,["<< /Type /Catalog","/Outlines 2 0 R","/Pages 3 0 R",">>"])
addObject(2,["<< /Type /Outlines","/Count 0",">>"])
addObject(3,["<< /Type /Pages",
             "/Kids [4 0 R]",
             "/Count 1",
             ">>"])

addObject(4,["<< /Type /Page",
             "/Parent 3 0 R",
             "/MediaBox [0 0 842 595]  % A4",
             "/CropBox [0 0 842 595]","/Rotate 00","/Contents 5 0 R",
             "/Resources << /ProcSet 6 0 R",
             "  /Pattern << /P1 11 0 R >>",
             "  >>",
             ">>"])

stream=["stream","0.0 G","W n","q",\
       "/Pattern cs  %colourspace is pattern",
       "/P1 scn   % non stroking colour ",
       "  1.0 0.0000 0.0000 1.0 421.0 297.0 cm      % translate",
       "%  25.0 0.0000 0.0000  25.0 0.0 0.0 cm      % scale",
       "-500 -350 999 700  re","f  % fill path","Q","endstream"]

stream.insert(0,"<< /Length "+streamLength(stream)+" >>")

addObject(5,stream)

#addObject(6,["[/PDF /Text]"])
addObject(6,["[/PDF]"])

addObject(7,["<< /ShadingType 1              % Function-based shading",
          "/ColorSpace /DeviceRGB         % RGB easiest (required)",
          "/Domain [-2.0 2.0 -1.0 1.0]    % optional.  This is default",
          "/Function 8 0 R                % 2 in (x,y); n-out (n is 3 for RGB)",
          "/Extend [false false]          % for testing only",">>"])


stream=["stream","{",SCALE+" div","exch "+SCALE+" div",XSHIFT+" add %  Maps x to align on screen (x -> (x + XSHIFT))",
        "2 copy",
        "2 copy    %  another z to work with",
        "2 mul mul   %  calc 2ab",
        "4 index  %  get y",
        "add %  Gives Im(z)(n+1) = 2ab + y",
        "3 1 roll",
        "dup mul  %  a^2",
        "exch dup mul  %  b^2",
        "sub  %  Re(z) (n+1) = x - b^2 + a^2",
        "2 index add % obtain x",
        "% stack should be c; z(n+1)",
        "2 copy dup mul exch dup mul add % calc arg^2",
        SQ_THRESHOLD+" ge {pop pop pop pop 255 255 255 }"]


for i in range(DEPTH):
  stream.append(" "*i+"{")
  stream.append(" "*i+" 2 copy 2 mul mul 4 index add 3 1 roll dup mul exch dup mul sub 2 index add 2 copy dup mul exch dup mul add")
  if (i%2==0):
    colR=0
    colG=0
    colB=0
  else:
    if (BANDW):
      colR=255
      colG=255
      colB=255
    else:
      colR=COLOURS[int(i/2)][0]
      colG=COLOURS[int(i/2)][1]
      colB=COLOURS[int(i/2)][2]
      
  stream.append(" "*i+" "+SQ_THRESHOLD+" ge { pop pop pop pop "+str(colR)+" "+str(colG)+" "+str(colB)+" }")


stream.append(" "*DEPTH+"{ 0 0 0 } ifelse")

for i in range(DEPTH):
  stream.append(" "*(DEPTH-1-i)+"} ifelse")  

stream.append("}")
stream.append("endstream")
stream.insert(0,"/Length "+streamLength(stream)+" >>")


stream.insert(0,"/Range [0 255 0 255 0 255]     % Required (type 0 & 4).  Output as RGB (any 8 bit value)")
stream.insert(0,"/Domain [-1000 1000 -500 500]    % (-2,-1)to(2,1)")
stream.insert(0,"<< /FunctionType 4             % Postscript calculator function")

addObject(8,stream)

t=datetime.datetime.now(datetime.timezone.utc) # Always use UTC
MODDATE=t.strftime("D:%Y%m%d%H%M%S00'00")

addObject(9,["<< /Title ("+TITLE+")",
             "/Author ("+AUTHOR+")",
             "/Subject (Fractal)",
             "/Creator (PDF_Fractals https://github.com/oilulio/PDF_Fractals)",
             "/ModDate ("+MODDATE+")",
             "/CreationDate ("+MODDATE+")",
             ">>"])

addObject(10,["<< /FunctionType 4 % postscript calculator function", # Unused??
             "/Domain [-500 500 -500 500]",
             "/Range [-500 500 -500 500]  % required (type 0 & 4)",
             "/Length 5207",
             ">>","stream",
             "{",
             "2 copy % another z to work with",
             "2 mul mul % calc 2ab",
             "4 index % obtain y",
             "add % Gives Im(z)(n+1) = 2ab + y",
             "3 1 roll",
             "dup mul % a^2",
             "exch dup mul % b^2",
             "sub % Re(z) (n+1) = x - b^2 + a^2",
             "2 index % obtain x"
             "add",
             "}",
             "endstream"])

addObject(11,["<< /Type /Pattern",
             "/PatternType 2 % 2 is shading pattern",
             "/Shading 7 0 R",
             "/Matrix [255 0.0 0.0 250  421.0 297.0]",
             ">>"])

OBJECTS=12 # Hardcode - TODO - make auto
startXREF=len(result)
result+="xref"+newline
result+="0 "+str(OBJECTS)+newline  
for i in range(OBJECTS):
  result+="{:010d}".format(index[i])
  if (i==0):
    result+=" {:05d}".format(65535)+" "+XREF_STATES["free"]+newline
  else:
    result+=" {:05d}".format(0)+" "+XREF_STATES["used"]+newline

result+=newline
result+="trailer"+newline

addObject(-1,["<<","/Size "+str(OBJECTS),
              "/Root 1 0 R",
              "/Info 9 0 R",
              ">>"],False)

result+="startxref"+newline
result+=str(startXREF)+newline
result+="%%EOF"+newline

if (BANDW):
  colour="Black and White"
else:
  colour="Colour"
  
f = open("Mandelbrot Set "+colour+".pdf","w")
f.write(result)
f.close()

