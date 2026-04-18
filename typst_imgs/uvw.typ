Given the Keplerian elements:

#table(
  columns: (auto, auto, 1fr),
  align: (right, center, left),
  stroke: none,
  inset: 4pt,
  [$ a $], [=], [semi-major axis],
  [$ e $], [=], [eccentricity],
  [$ i $], [=], [inclination],
  [$ Omega $], [=], [right ascension of the ascending node],
  [$ omega $], [=], [argument of perigee],
  [$ M $], [=], [mean anomaly],
)

The position in the perifocal frame:

$ r_p = frac(a (1 - e^2), 1 + e cos nu) $

$
  mat(delim: "[", x_p; y_p; z_p)
  = frac(a (1 - e^2), 1 + e cos nu)
  mat(delim: "[", cos nu; sin nu; 0)
$

The velocity in the perifocal frame:

$
  mat(delim: "[", v_(x,p); v_(y,p); v_(z,p))
  = sqrt(frac(mu, a (1 - e^2)))
  mat(delim: "[", -sin nu; e + cos nu; 0)
$

Transformation to the inertial frame (ECI):

$
  bold(r)
  = R_z(-Omega) R_x(-i) R_z(-omega)
  mat(delim: "[", x_p; y_p; z_p)
$

$
  bold(v)
  = R_z(-Omega) R_x(-i) R_z(-omega)
  mat(delim: "[", v_(x,p); v_(y,p); v_(z,p))
$

UVW (RTN) frame:

$ hat(u) = frac(bold(r), norm(bold(r))) $

$ hat(w) = frac(bold(h), norm(bold(h))) $

$ hat(v) = hat(w) times hat(u) $

where $ bold(h) = bold(r) times bold(v) $ is the specific angular momentum.
