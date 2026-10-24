function K = GramMat(x,coordwts) 
arguments
    x = [0, 0; 0.5, 0.5; 0.25, 0.25] 
    coordwts(1,:) = (1:50).^-2
end
[n,d] = size(x);
xmat = mod(reshape(x,[n,1,d]) - reshape(x,[1,n,d]),1);
K = prod(1 + 0.5*reshape(coordwts(1:d),[1,1,d]).*(xmat.*(xmat-1) + 1/6),3);