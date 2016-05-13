#####################################
#
# 'BASIC FUNCTIONALITY' RooFit tutorial macro #102
# 
# Importing data from ROOT TTrees and THx histograms
#
#
#
# 07/2008 - Wouter Verkerke 
# 
####################################/

from ROOT import *
from array import array

def rf102_dataimport():

  ############################
  # I m p o r t i n g   R O O T   h i s t o g r a m s  #
  ############################

  # I m p o r t   T H 1   i n t o   a   R o o D a t a H i s t
  # ---------------------------------------------------------

  # Create a ROOT TH1 histogram
  hh = makeTH1()

  # Declare observable x
  x = RooRealVar("x","x",-10,10)

  # Create a binned dataset that imports contents of TH1 and associates its contents to observable 'x'
  dh = RooDataHist("dh","dh",RooArgList(x),RooFit.Import(hh))


  # P l o t   a n d   f i t   a   R o o D a t a H i s t
  # ---------------------------------------------------

  # Make plot of binned dataset showing Poisson error bars (RooFit default)
  frame = x.frame(RooFit.Title("Imported TH1 with Poisson error bars"))
  dh.plotOn(frame)

  # Fit a Gaussian p.d.f to the data
  mean = RooRealVar("mean","mean",0,-10,10)
  sigma = RooRealVar("sigma","sigma",3,0.1,10)
  gauss = RooGaussian("gauss","gauss",x,mean,sigma)
  gauss.fitTo(dh)
  gauss.plotOn(frame)

  # P l o t   a n d   f i t   a   R o o D a t a H i s t   w i t h   i n t e r n a l   e r r o r s
  # ---------------------------------------------------------------------------------------------

  # If histogram has custom error (i.e. its contents is does not originate from a Poisson process
  # but e.g. is a sum of weighted events) you can data with symmetric 'sum-of-weights' error instead
  # (same error bars as shown by ROOT)
  frame2 = x.frame(RooFit.Title("Imported TH1 with internal errors"))
  dh.plotOn(frame2,RooFit.DataError(RooAbsData.SumW2))
  gauss.plotOn(frame2)

  # Please note that error bars shown (Poisson or SumW2) are for visualization only, the are NOT used
  # in a maximum likelihood fit
  #
  # A (binned) ML fit will ALWAYS assume the Poisson error interpretation of data (the mathematical definition
  # of likelihood does not take any external definition of errors). Data with non-unit weights can only be correctly
  # fitted with a chi^2 fit (see rf602_chi2fit.C)


  ########################
  # I m p o r t i n g   R O O T  T T r e e s   #
  ########################


  # I m p o r t   T T r e e   i n t o   a   R o o D a t a S e t
  # -----------------------------------------------------------

  tree = makeTTree()

  # Define 2nd observable y
  y = RooRealVar("y","y",-10,10)

  # Construct unbinned dataset importing tree branches x and y matching between branches and RooRealVars
  # is done by name of the branch/RRV
  #
  # Note that ONLY entries for which x,y have values within their allowed ranges as defined in
  # RooRealVar x and y are imported. Since the y values in the import tree are in the range [-15,15]
  # and RRV y defines a range [-10,10] this means that the RooDataSet below will have less entries than the TTree 'tree'

  ds = RooDataSet("ds","ds",RooArgSet(x,y),RooFit.Import(tree))


  # P l o t   d a t a s e t   w i t h   m u l t i p l e   b i n n i n g   c h o i c e s
  # ------------------------------------------------------------------------------------

  # Print number of events in dataset
  ds.Print()

  # Print unbinned dataset with default frame binning (100 bins)
  frame3 = y.frame(RooFit.Title("Unbinned data shown in default frame binning"))
  ds.plotOn(frame3) ;

  # Print unbinned dataset with custom binning choice (20 bins)
  frame4 = y.frame(RooFit.Title("Unbinned data shown with custom binning"))
  ds.plotOn(frame4,RooFit.Binning(20))

  # Draw all frames on a canvas
  c = TCanvas("rf102_dataimport","rf102_dataimport",800,800)
  c.Divide(2,2)
  c.cd(1) ; gPad.SetLeftMargin(0.15) ; frame.GetYaxis().SetTitleOffset(1.4) ; frame.Draw() ;
  c.cd(2) ; gPad.SetLeftMargin(0.15) ; frame2.GetYaxis().SetTitleOffset(1.4) ; frame2.Draw() ;
  c.cd(3) ; gPad.SetLeftMargin(0.15) ; frame3.GetYaxis().SetTitleOffset(1.4) ; frame3.Draw() ;
  c.cd(4) ; gPad.SetLeftMargin(0.15) ; frame4.GetYaxis().SetTitleOffset(1.4) ; frame4.Draw() ;

  c.SaveAs("rf102_dataimport.png")

def makeTH1():

  # Create ROOT TH1 filled with a Gaussian distribution

  hh = TH1D("hh","hh",25,-10,10)
  for i in range(100):
    hh.Fill(gRandom.Gaus(0,3))
  return hh



def makeTTree():
  # Create ROOT TTree filled with a Gaussian distribution in x and a uniform distribution in y

  tree = TTree("tree","tree")
  px = array( 'd', [ 0 ] )
  py = array( 'd', [ 0 ] )
  tree.Branch("x",px,"x/D")
  tree.Branch("y",py,"y/D")
  for i in range(100):
    px[0] = gRandom.Gaus(0,3)
    py[0] = gRandom.Uniform()*30 - 15
    tree.Fill()
  return tree


if __name__ == "__main__":
  rf102_dataimport()
  