# PDF_Fractals
A way of creating a PDF file that will draw a fractal (not just contain an image of a fractal)

This was first written (as hand-created PDF - see https://opensource.adobe.com/dc-acrobat-sdk-docs/pdfstandards/pdfreference1.5_v6.pdf) almost 20 years ago, in c.2005.

The PDF file format allows Postscript functions code (specifically mathematical functions coded in Reverse Polish Notation) to generate images at runtime, as an alternative to an embedded image.

The simplest bit of code is one that is the same for every pixel - such as a Mandelbrot Set fractal.

So a couple of (text) pages of PDF file can create a Mandelbrot Set and the zoom function is **managed by the PDF viewer**, so zoom does not require the detailed pixels to exist in an image, they are generated on the fly.  You therefore start getting Blade Runner-levels of zoom.

It worked, but the CPU load on a computer of that time was extreme (it was slow and cumbersome)

In addition, PDF viewers seem to only zoom in so far.  And eventually the machine precision would lead to blockiness.

But with a modern computer it runs OK, as long as enough time is given for the recalculation.  Viewers I have tested do not use multiple cores, so it does not work as well as it could.  Different viewers perform differently - Acrobat zooms much better than the default viewer in Edge.  And Acrobat seems to show colours that Edge does not.

The initial PDFs were hand-generated, but this repo includes a later simple python script to make a PDF file.  Doesn't rely on any external libraries, which is why it still works after many years.

## Mandelbrot Set
The core code for a Mandelbrot Set is z<sub>n+1</sub>=z<sub>n</sub><sup>2</sup> + c, with z<sub>0</sub>=0 and hence z<sub>1</sub>=c.  If we assume z = a + ib and c = x + iy, and the stack contains y,x,b,a in downwards order, then we obtain an updated z (a,b on the stack) via: 

```postscript
2 copy % another z to work with
2 mul mul % calc 2ab
4 index % obtain y
add % Gives Im(z)(n+1) = 2ab + y
3 1 roll
dup mul % a^2
exch dup mul % b^2
sub % a^2 - b^2
2 index % get old x
add % Gives Re(z) (n+1) = x - b^2 + a^2
```

We then see if the z created is beyond a defined distance from the origin (in this case, $\sqrt{15}$) using:

```postscript
2 copy % another z
dup mul % a^2
exch dup mul % b^2
add % a^2 + b^2
15 ge % greater than or equal to 15?
{ pop pop pop pop 255 255 255 }  % clean stack, return RGB pixel values (255 is white)
```

And repeat the n+1 generation for further equipotential cases.  A different colour at different generations gives an impressive image.

## Julia Set
The core code for a Julia Set is also z<sub>n+1</sub>=z<sub>n</sub><sup>2</sup> + c, however z<sub>0</sub>=the candidate value, and c is a fixed constant.  If we assume z = a + ib, and the stack contains b,a in downwards order, then we obtain an updated z (a,b on the stack) via: 

```postscript
2 copy % another z to work with
2 mul mul % calc 2ab
0.156 % set y
add % Gives Im(z)(n+1) = 2ab + y
3 1 roll
dup mul % a^2
exch dup mul % b^2
sub % a^2 - b^2
-0.8 % set x
add % Gives Re(z) (n+1) = x - b^2 + a^2
```

Note x,y are now set explicitly - in this example to -0.8 and 0.156 respectively.