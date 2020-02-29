#include <TROOT.h>
#include <TStyle.h>

void doubleMuon(){
  TCanvas *can = new TCanvas("can", "", 700, 700);
  TChain *doubleMuon = new TChain("Events");
  doubleMuon->Add("DoubleMuon.root");

  TString diMuon = "(nMuon==2)";
  TString diMuonCharge = "(Muon_pdgId[0]*Muon_pdgId[1]<0)";
  TString diMuonSelection = "(Sum$(Muon_pt>25 && abs(Muon_eta)<2.4 && Muon_mediumId&Muon_miniPFRelIso_all<0.1)==2)";
  TString eventSelection = diMuon + "&&" + diMuonCharge + "&&" + diMuonSelection;

  TString invariantMass = "sqrt(2*Muon_pt[0]*Muon_pt[1]*(cosh(Muon_eta[0]-Muon_eta[1]) - cos(Muon_phi[0]-Muon_phi[1])))";

  TH1F *mass = new TH1F("mass", "", 100, 80, 100);

  doubleMuon->Draw(invariantMass+">>mass", eventSelection);

  can->Print("invariantMass.png");
  can->Print("invariantMass.pdf");
  can->Print("invariantMass.root");
}
