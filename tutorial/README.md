

# ROOT tutorial
#### Daniel Spitzbart (Boston University)

<img class="plain"  src="https://codimd.web.cern.ch/uploads/upload_562f77c4f278ce1b90aa37544f233c41.png" height=60> <img class="plain"  src="https://codimd.web.cern.ch/uploads/upload_11561a8eb405d67138b3a7d7fbb3750d.png" height=60>

# Disclaimer

This tutorial is a WIP :ghost:

# Prerequisites

You can e.g. use [anaconda](https://www.anaconda.com/distribution/) to install [ROOT](https://root.cern.ch) within a virtual environment.
```=
conda create -n cmsNano python=2.7
conda activate cmsNano
conda install -c conda-forge root 
```
Check out the following repository:
```
git clone https://github.com/danbarto/WH_hadronic.git
```
Download the following files (password: tutorial):
[TChiWH sample 1,](https://cernbox.cern.ch/index.php/s/Wpb9IVEYxC3Pj4A)  [TChiWH sample 2,](https://cernbox.cern.ch/index.php/s/UTCbZbce47xC43Y)  [TTJets sample](https://cernbox.cern.ch/index.php/s/Ckr8vFsQhq0T4I5)

# PyROOT

Start up ipython and then do

```python=
import ROOT
ROOT.gStyle.SetOptStat(0) # deactivate annoying stat box in histograms

# Load a root file to a chain
TChiWH_750_1 = ROOT.TChain("Events")
TChiWH_750_1.Add("WH_had_750_1_v1.root")

# Explore the content of the file
TChiWH_750_1.ls() # shows you the ROOT trees that you loaded
TChiWH_750_1.GetListOfBranches().ls() # shows the branches of the tree

TChiWH_750_1.Scan("MET_pt:MET_phi")
```

# Histogramming
That's what we usually mean when we say "Let's make a plot".

```python=
can = ROOT.TCanvas("can", "", 700,700)
myFirstHisto = ROOT.TH1F("myFirstHisto", "", 10, -0.5, 9.5)
nJet = "Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_jetId>1)"
TChiWH_750_1.Draw("%s>>myFirstHisto"%nJet)
```

# Formating a plot

Let's make the plot a bit more beautiful, and normalize it to 1.

```python=
myFirstHisto.Scale(1/myFirstHisto.Integral())
myFirstHisto.GetXaxis().SetTitle("N_{jet}")
myFirstHisto.GetYaxis().SetTitle("frac. of events")
myFirstHisto.GetYaxis().SetTitleOffset(1.5)
myFirstHisto.SetLineColor(ROOT.kRed+2)
myFirstHisto.SetLineWidth(2)
myFirstHisto.Draw("hist")
```

# Physics detour

What are we actually lookind at, and what's TChiWH??

<img class="plain"  src="https://codimd.web.cern.ch/uploads/upload_fd73c03644b583349948a78887c82e4f.png" height=160>


[CMS paper from 2017](https://arxiv.org/abs/1706.09933), [ATLAS paper from 2019](https://arxiv.org/abs/1909.09226)

# Objects in the ROOT file

- Electrons, Muons, Photons
- Taus
- Jets, FatJets
- different versions of MET
- Generator truth objects
- Triggers & Filters

[Documentation](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookNanoAOD)

### Selecting a subset of events

We can also make a plot with only a subset of the events.

```python=
cut = "Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_jetId>1)<=4"
TChiWH_750_1.Draw("%s>>myFirstHisto"%nJet, cut)
```

### Simple event loop

Although one can do a lot of things with the formulas within the `Draw` function we sometimes want to do something more complicated.
In this case, we loop over the events, access the objects we're interested in and do our calculation.

```python=
from helpers import * # import some functions.

mbb_histo = ROOT.TH1F("mbb_histo", "", 50,20,220)

# select events with 4 jets
cut = "Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_jetId>1)==4"

# get the events passing the cut into an eventlist
TChiWH_750_1.Draw('>>eList',cut)
elist = ROOT.gDirectory.Get("eList")
number_events = elist.GetN()

# start the loop
for i in range(number_events):
    # Get the proper entry from the chain
    TChiWH_750_1.GetEntry(elist.GetEntry(i))
    
    # We expect two b-jets, create the vectors
    b1 = ROOT.TLorentzVector()
    b2 = ROOT.TLorentzVector()
    
    bJets = getBJets(TChiWH_750_1, year=2018)
    
    # we only care for events with 2 b-tagged jets
    if len(bJets)==2:
        b1.SetPtEtaPhiM(bJets[0]['pt'], bJets[0]['eta'], bJets[0]['phi'], 0)
        b2.SetPtEtaPhiM(bJets[1]['pt'], bJets[1]['eta'], bJets[1]['phi'], 0)
        mbb = (b1+b2).M()
        mbb_histo.Fill(mbb)
```

### Invariant mass

We calculate an invariant mass of the b-tagged jets - what do we expect?

### FatJet mass

 - Jets are clustered using a certain cone size parameter.
 - If the object is boosted (large momentum compared to mass), "skinny" jets can merge into "fat" jets
 - Instead of the invariant mass of two "skinny" jets we can then look at the mass of the fat jet (FatJet_mass or FatJet_msoftdrop in the samples)

<img class="plain"  src="https://codimd.web.cern.ch/uploads/upload_e1bed6960588c9d013fc203fa18d15df.png" height=300>


<img class="plain"  src="https://codimd.web.cern.ch/uploads/upload_e3f858faaf38e8bac6428a8b98120d8e.png" height=300>


### Signal vs Background

Crate another ROOT chain and make plots of the missing transverse energy.

<img class="plain"  src="https://codimd.web.cern.ch/uploads/upload_8e4ddba9b27225feccd4347e141e9726.png" height=250>

Here we compare "shapes". The signal has a x-sec that is $10^{-5}$ of that of the background.


### Adding a legend

```python=
leg = ROOT.TLegend(0.6,0.4,0.85,0.5)
leg.AddEntry(TTJets_MET_histo, 't#bar{t}+jets', 'l')

leg.Draw()
```

### Bonus: Find the Z boson in actual CMS data!


[Small subset of DoubleMuon data from 2018](https://cernbox.cern.ch/index.php/s/kkMfHjA6W0apiAQ)
 - What is a promising decay channel?
 - Which objects would you use?
 - Which variable can you use?


As the the name of the data set suggests, looking for the Z->mu+mu- decay is the best option.
In order to select events with exactly two muons, we can use the following variable already contained in the provided root file:
```
nMuon==2
```
We also know that two muons from a Z boson decay have opposite electric charge.
In order to enforce that we can use the `Muon_pdgId` variable.
The [pdgId](http://pdg.lbl.gov/2007/reviews/montecarlorpp.pdf) is a standard numbering scheme for particles, and the sign determines whether the particle is the "particle" or the "anti-particle" and therefore its electric charge.
Therefore, by requiring
```
Muon_pdgId[0]*Muon_pdgId[1]<0
```
we make sure that the two muons we previously selected have opposite electric charge.

Additionally, we apply some quality criteria: a minimum transverse momentum, a certain range within the detector, an ID requirement, and an isolation requirement. We will learn what all those mean a bit later.
The final event selection can look like this:
```
eventSelection = "Sum$(Muon_pt>25&&abs(Muon_eta)<2.4&&Muon_mediumId&&Muon_miniPFRelIso_all<0.1)==2 && nMuon==2 && Muon_pdgId[0]*Muon_pdgId[1]<0"
```

As discussed earlier, ROOT understands formulas and we don't always need to loop over events with an event loop written by ourselves. Instead, we let ROOT do all the work.
For the invariant mass of the two muons that we select we can use the following formula:
```
invariantMass  = "sqrt(2*Muon_pt[0]*Muon_pt[1]*(cosh(Muon_eta[0]-Muon_eta[1])-cos(Muon_phi[0]-Muon_phi[1])))"
```

We can then create a histogram with appropriate `lowerLimit` and `upperLimit`. Tip: check out the value of the Z boson mass on wikipedia or the [PDG](http://pdg.lbl.gov) to find a good starting point.
(The PDG is also a very valuable resource for the future)
```
mass = ROOT.TH1F("mass", "", 100,lowerLimit,upperLimit)
```
and draw the invariant mass:
```
DoubleMuon.Draw("%s>>mass"%invariantMass, eventSelection)
```
