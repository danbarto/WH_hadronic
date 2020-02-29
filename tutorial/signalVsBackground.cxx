#include <TROOT.h>
#include <TStyle.h>

void signalVsBackground(){
    gStyle->SetOptStat(0);
    TCanvas *can = new TCanvas("can", "", 700, 700);
    can->SetLogy();

    TChain *TChiWH_500 = new TChain("Events");
    TChiWH_500->Add("WH_had_500_150_v1.root");

    TChain *TChiWH_750 = new TChain("Events");
    TChiWH_750->Add("WH_had_750_1_v1.root");

    TChain *TTJets = new TChain("Events");
    TTJets->Add("TTJets.root");

    TString cut = "Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_jetId>1)==4&&Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_jetId>1&&Jet_btagDeepB>0.4184)==2";

    TH1F *Signal1_MET = new TH1F("Signal1_MET", "", 50, 0, 500);
    TH1F *Signal2_MET = new TH1F("Signal2_MET", "", 50, 0, 500);
    TH1F *TTJets_MET = new TH1F("TTJets_MET", "", 50, 0, 500);

    TChiWH_750->Draw("MET_pt>>Signal1_MET", cut);
    TChiWH_500->Draw("MET_pt>>Signal2_MET", cut);
    TTJets->Draw("MET_pt>>TTJets_MET", cut);

    Signal1_MET->SetLineColor(kBlue+1);
    Signal1_MET->GetXaxis()->SetTitle("p_{T}^{miss} (GeV)");
    Signal1_MET->GetYaxis()->SetTitle("Events");
    Signal1_MET->SetMaximum(10000);
    Signal2_MET->SetLineColor(kGreen+2);
    TTJets_MET->SetLineColor(kRed+1);

    TLegend *leg = new TLegend(0.50, 0.75, 0.90, 0.90);
    leg->AddEntry(Signal1_MET, "TChiWH(750,1)", "l");
    leg->AddEntry(Signal2_MET, "TChiWH(500,150)", "l");
    leg->AddEntry(TTJets_MET, "t#bar{t}+jets", "l");

    Signal1_MET->Draw();
    Signal2_MET->Draw("SAME");
    TTJets_MET->Draw("SAME");

    leg->Draw();
    can->Print("signalVsBackground.png");
    can->Print("signalVsBackground.pdf");
    can->Print("signalVsBackground.root");
}
