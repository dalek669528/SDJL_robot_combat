int ChirpSine(int T, float t, float f0, float f1){
  float k = (f1-f0)/T;
  float phi = 2*PI*(f0+t*k/2)*t;
  float dphi = 2*PI*f0+2*k*PI*t+1;
  int P =  200*sin(phi);
  return P;
}
