%Experiment with optimum weights
clearvars, close all

n = 512;
d = 6;
coordwts(1,:) = (1:50).^-2;
[ssdiscopt,ssdisc,xlat,optfwtsall] = discrepancy(n,d,coordwts);
loglog(1:n,ssdisc,'.','MarkerSize',20)
hold on
h = loglog(1:n,ssdiscopt,'s','MarkerSize',10);
h.MarkerFaceColor=h.Color;

%Look at some weights
nlook = [7, 12, 14, 15, 17];
for n = nlook
    disp(['For n = ', int2str(n), ', function wts and nodes are'])
    disp([optfwtsall(1:n,n) xlat(1:n,:)])
end