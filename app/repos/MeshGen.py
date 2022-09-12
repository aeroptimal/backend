class YplusCalculator:
  def __init__(self,V,rho,mu,yplus):
    self.V = V
    self.rho = rho
    self.mu = mu
    self.yplus = yplus
    
  def ComputeDeltaS(self):
    Rex = self.rho*self.V*1/self.mu
    Cf = 0.026/(Rex**(1/7))
    taowall = Cf*self.V*self.V*self.rho/2
    ufric = (taowall/self.rho)**0.5
    DeltaS = self.yplus*self.mu/(ufric*self.rho)
    return DeltaS