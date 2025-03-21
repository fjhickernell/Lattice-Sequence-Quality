function [ssdiscopt,ssdisc,xlat,optfwtsall] = discrepancy(n,d,coordwts)
    arguments
        n = 50  %number of points
        d = 2 %dimension
        coordwts(1,:) = (1:50).^-2
    end
    optfwtsall = zeros(n,n);
    ssdiscopt(n) = 0;
    ssdisc(n) = 0;
    xlat = gail.lattice_gen(1,n,d); %lattice points
    kernellat = GramMat(xlat,coordwts);
    for m = 1:n
        K = kernellat(1:m,1:m);
        optfwts = K\ones(m,1);
        optfwtsall(1:m,m) = optfwts;
        ssdiscopt(m) = 1 - 2*sum(optfwts) + optfwts'*K*optfwts;
        ssdisc(m) = -1 + ones(1,m)*K*ones(m,1)/m^2;
    end
        



