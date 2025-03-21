%Experiment with optimum weights
clearvars, close all

n = 512;
d = 6;
coordwts(1,:) = (1:50).^-2;
[ssdiscopt,ssdisc,xlat,optfwts] = discrepancy(n,d,coordwts);
loglog(1:n,ssdisc,'.','MarkerSize',20)
hold on
h = loglog(1:n,ssdiscopt,'s','MarkerSize',10);
h.MarkerFaceColor=h.Color;
