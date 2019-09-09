
On UCSD T2

Get your proxy and export it
```
voms-proxy-init -voms cms -valid 100:00 -out /tmp/x509up_YOURUSER; export X509_USER_PROXY=/tmp/x509up_YOURUSER
```

For a sample with around 50k events (100k -> 50k due to filter efficiency), NLSP mass of 500 GeV and LSP mass of 1 GeV, do
```
python submitJobsToCondor.py WH_had --fragment WHhadronic_template.py --nevents 1000 --njobs 100 --mnlsp 500 --mlsp 1 --executable makeHadronicSample.sh --rseed-start 500
```
