
# Instructions for usage on UCSD T2

The following scripts allow to produce events of C1N2 production with decays to WH(W->qq, H->bb).
Both miniAOD and nanoAOD files are produced, and are stored under
```
/hadoop/cms/store/user/YOUR_USER/WH_hadronic
```
As an example, see
```
/hadoop/cms/store/user/dspitzba/WH_hadronic/
```


In order to start, get your proxy and export it
```
voms-proxy-init -voms cms -valid 100:00 -out /tmp/x509up_YOUR_USER; export X509_USER_PROXY=/tmp/x509up_YOUR_USER
```

For a sample with around 50k events (100k -> 50k due to filter efficiency), NLSP mass of 500 GeV and LSP mass of 1 GeV, do
```
python submitJobsToCondor.py WH_had --fragment WHhadronic_template.py --nevents 1000 --njobs 100 --mnlsp 500 --mlsp 1 --executable makeHadronicSample.sh --rseed-start 500
```
