# PDF_Fractals
A way of creating a PDF file that will draw a fractal (not just contain an image of a fractal)

This was written almost 20 years ago, in c.2005.

The basic idea is that the PDF file format, much like Postscript, can use code (specifically mathematical functions coded in Reverse Polish Notation) to generate images.

The simplest bit of code is one that is the same for every pixel - such as a Mandelbrot Set fractal.

So a couple of (text) pages of PDF file can create a Julia Set and the zoom function is **managed by the PDF viewer**, so zoom does not require the detailed pixels to exist in an image, they are generated on the fly.

It worked, but the CPU load on a computer of that time was extreme (it was slow and cumbersome)

In addition, PDF viewers seem to only zoom in so far.  And eventually the machine precision would lead to blockiness.

But with a modern computer it runs OK, as long as enough time is given for the recalculation.  Viewers I have tested do not use multiple cores, so it does not work as well as it could.  Different viewers perform differently - Acrobat zooms much better than the default viewer in Edge.

The initial PDFs were hand generated, but this repo includes a simple python script to make a PDF file.  Doesn't rely on any external libraries, which is why it still works after many years.

The core code for a Mandelbrot Set is z<sub>n+1</sub>=z<sub>n</sub><sup>2</sup> + c.  If we assume z = a + ib and c = x + iy, and the stack contains y,x,b,a in downwards order, then we obtain an updated z (a,b on the stack) via: 

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
