function output = fis(fuzzySystem, x, y, z)
    x = double( x );
    y = double( y );
    z = double( z );
    output = evalfis(fuzzySystem, [x y z]);

end
