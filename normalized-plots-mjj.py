import time
import CMS_lumi, tdrstyle
from ROOT import *

tdrstyle.setTDRStyle()
CMS_lumi.lumi_13TeV = ""
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Simulation Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 0
if( iPos==0 ): CMS_lumi.relPosX = 0.12
iPeriod=4

rebin = 50

setmax = 0.59
prefix = '80X/GEN/'
addBKG = False
doFit = True


def getCanvas():
  c = TCanvas("c","c",800,800)
  c.GetWindowHeight()
  c.GetWindowWidth()
  c.SetTitle("")
  return c
  
  
def get_palette(mode):

 palette = {}
 palette['gv'] = [] 
 
 colors = ['#40004b','#762a83','#9970ab','#de77ae','#a6dba0','#5aae61','#1b7837','#00441b','#92c5de','#4393c3','#2166ac','#053061']
 colors = ['#762a83','#de77ae','#a6dba0','#92c5de','#4393c3','#2166ac','#053061']

 for c in colors:
  palette['gv'].append(c)
 
 return palette[mode]
 
palette = get_palette('gv')

col = TColor()
  
files = [ 'ExoDiBosonAnalysis.BulkWW_13TeV_1800GeV.VV.root',
          'ExoDiBosonAnalysis.BulkZZ_13TeV_1800GeV.VV.root',
          'ExoDiBosonAnalysis.ZprimeWW_13TeV_1800GeV.VV.root',
          'ExoDiBosonAnalysis.WprimeWZ_13TeV_1800GeV.VV.root',
          # 'ExoDiBosonAnalysis.QstarQW_13TeV_1800GeV.VV.root',
       #    'ExoDiBosonAnalysis.QstarQZ_13TeV_1800GeV.VV.root',
          'ExoDiBosonAnalysis.BulkWW_13TeV_4000GeV.VV.root',
          'ExoDiBosonAnalysis.BulkZZ_13TeV_4000GeV.VV.root',
          'ExoDiBosonAnalysis.ZprimeWW_13TeV_4000GeV.VV.root',
          'ExoDiBosonAnalysis.WprimeWZ_13TeV_4000GeV.VV.root'
          # 'ExoDiBosonAnalysis.QstarQW_13TeV_4000GeV.VV.root',
          # 'ExoDiBosonAnalysis.QstarQZ_13TeV_4000GeV.VV.root',
          ]


legendname = [ "G_{B}#rightarrow WW (Madgraph)",
               "G_{B}#rightarrow ZZ (Madgraph)",
               "Z'#rightarrow WW (Madgraph)",       
               "W#rightarrow WZ (Madgraph)"   
               # "q*#rightarrow qW (Madgraph)",
               # "q*#rightarrow qZ (Madgraph)",   
             ]
                
histonames = ['gen_PrunedMass','gen_SoftdropMass','gen_Mass','gen_SoftdropMassUnCorr']
titles     = ['Pruned mass (GeV)','PUPPI softdrop mass (GeV)','Mass (GeV)','PUPPI softdrop mass (no L2l3) (GeV)']

histonames = ['gen_Tau21','gen_PUPPITau21','gen_DDT']
titles     = ['#tau_{21}','PUPPI #tau_{21}','DDT']

histonames = ['gen_SoftdropMass','gen_SoftdropMassUnCorr','gen_SoftdropMass_pt500','gen_SoftdropMassCHSCorr']
titles     = ['PUPPI softdrop mass (GeV)','PUPPI softdrop mass (no L2l3) (GeV)','PUPPI softdrop mass (GeV)','PUPPI softdrop mass (CHS L2L3) (GeV)']

histonames = ['gen_SoftdropMass_eta1v3','gen_SoftdropMass_etaUP1v3','gen_SoftdropMassUnCorr']
titles     = ['PUPPI softdrop mass (no L2l3) (GeV)','PUPPI softdrop mass (no L2l3) (GeV)','PUPPI softdrop mass (no L2l3) (GeV)']

histonames = ['Mjj_final']
titles     = ['M_{jj}']

lineStyle = [1,1,1,1,1,1,3,3,3,3,3,3]
lineStyle = [1,1,1,1,3,3,3,3]


ii = -1
for hname in histonames:
  print "Working on histogram " ,hname
  ii += 1
  
  min = 0
  max = 155
  if hname.find("Mjj") != -1:
    min = 935
    max = 4990
  if hname.find("gen_Mass") != -1:
    min = 0
    max = 305
  
  if hname.find("Tau21") != -1 or hname.find("DDT") != -1 :
    min = 0
    max = 1  

  #l = TLegend(.16,.7,.4,.9)
  l = TLegend(0.4861809,0.7020725,0.6859296,0.9209845)
  l.SetTextSize(0.035)
  l.SetLineColor(0)
  l.SetShadowColor(0)
  l.SetLineStyle(1)
  l.SetLineWidth(1)
  l.SetFillColor(0)
  l.SetFillStyle(0)
  l.SetMargin(0.35)

  l2 = TLegend(0.7613065,0.6088083,0.9937186,0.6761658)
  l2.SetTextSize(0.033)
  l2.SetLineColor(0)
  l2.SetShadowColor(0)
  l2.SetLineStyle(1)
  l2.SetLineWidth(1)
  l2.SetFillColor(0)
  l2.SetFillStyle(0)
  l2.SetMargin(0.35)

  filelist = []
  histos = []

  for f in files:
    filename = prefix + f
    filetmp = TFile.Open(filename,"READ") 
    print "Opening " ,filetmp.GetName()
    filelist.append(filetmp)
    
  for f in filelist:
      histtmp = TH1F(f.Get(hname))
      histtmp.SetName(f.GetName())
      print "Getting histogram %s for file %s " %(hname,f.GetName())
      print "Entries = " ,histtmp.GetEntries()
      histos.append(histtmp)

  for j in xrange(0,len(histos)):
    histos[j].SetLineColor(col.GetColor(palette[j %4]))
    histos[j].SetLineStyle(lineStyle[j])
    histos[j].SetLineWidth(3)
    histos[j].Rebin(rebin)
    histos[j].Scale(1./histos[j].Integral())
    if j < 4:
      legend = legendname[j]
      l.AddEntry(histos[j],legend,"l")
    if j == 0: l2.AddEntry(histos[j],"1.8 TeV","l")
    if j == 4: l2.AddEntry(histos[j],"4.0 TeV","l")
  
  fits = []
  for h in histos:
    fittmp = TGraph(h)
    fits.append(fittmp)
  
  if addBKG:
    bkgfile = TFile.Open('80X/GEN/ExoDiBosonAnalysis.QCD_gen.root','READ')
    bkghist = TH1F(bkgfile.Get(hname))
    bkghist.SetName("BKG")
    bkghist.SetFillStyle(3002)
    bkghist.SetFillColor(kBlack)
    bkghist.SetLineColor(kBlack)
    bkghist.SetLineStyle(1)
    bkghist.Scale(1./bkghist.Integral())
    bkghist.Rebin(rebin)
    bkghist.SetMaximum(setmax)
    l.AddEntry(bkghist,'QCD (Pythia8)',"f")

  yTitle = "Arbitrary scale"
   
  canv = getCanvas()
  canv.cd()
  setmax = histos[0].GetMaximum()*1.5
  vFrame = canv.DrawFrame(min,0.000005,max,setmax)  
  vFrame.SetXTitle(titles[ii])
  vFrame.SetYTitle(yTitle)
  vFrame.GetXaxis().SetTitleSize(0.06)
  vFrame.GetXaxis().SetTitleOffset(0.95)
  vFrame.GetXaxis().SetLabelSize(0.05)
  vFrame.GetYaxis().SetTitleSize(0.06)
  #vFrame.GetYaxis().SetTitleOffset(1.0)
  vFrame.GetYaxis().SetLabelSize(0.05)
  vFrame.GetXaxis().SetNdivisions(408)
  vFrame.GetYaxis().SetNdivisions(404)


  if doFit:
    for f in fits: f.Draw("Csame")      
    if addBKG: bkghist.Draw('HISTsame')
  else:
    for h in histos: h.Draw("sameHIST")
    if addBKG: bkghist.Draw('HISTsame')
  


  l1 = TLatex()
  l1.SetNDC()
  l1.SetTextAlign(12)
  l1.SetTextFont(42)
  l1.SetTextSize(0.025)
  l1.DrawLatex(0.20,0.86, "AK, R= 0.8")
  if hname.find("pt500") != -1: 
    l1.DrawLatex(0.20,0.80, "p_{T} > 500 GeV, |#eta| < 2.5")
  elif hname.find("eta1v3") != -1: 
    l1.DrawLatex(0.20,0.80, "p_{T} > 200 GeV, |#eta| < 1.3")  
  elif hname.find("etaUP1v3") != -1: 
    l1.DrawLatex(0.20,0.80, "p_{T} > 200 GeV, 1.3 < |#eta| < 2.5")  
  else:
       l1.DrawLatex(0.20,0.80, "p_{T} > 200 GeV, |#eta| < 2.5")
  
  #
  # if hname.find("CHSCorr") != -1:
  #   l1.DrawLatex(0.20,0.83, "L2L3 CHS corrected")
  # elif hname.find("Mass") != -1 and not hname.find("UnCorr") != -1 and not hname.find("1v3") != -1:
  #   l1.DrawLatex(0.20,0.83, "L2L3 corrected")
  # elif hname.find("NEWCORR") != -1:
  #   l1.DrawLatex(0.20,0.83, "New mass corr. applied")
  # if not hname.find("Mass") != -1: l1.DrawLatex(0.20,0.76, "65 GeV < M_{G} < 105 GeV")

  # l1.DrawLatex(0.7,0.42,"65 GeV < M_{p} < 105 GeV")
  

   
  l.Draw("same")
  l2.Draw("same")
  CMS_lumi.CMS_lumi(canv, iPeriod, iPos)
  canv.Update()
  canvname = "plots80X/%s.pdf"%hname
  canv.SaveAs(canvname,"pdf")
  canv.SaveAs(canvname.replace("pdf","root"),"pdf")
  time.sleep(20)
