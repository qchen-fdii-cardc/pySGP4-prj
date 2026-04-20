from numpy import radians, acos, sqrt, degrees
import pysgp4 as sgp4
import pandas as pd
import matplotlib.pyplot as plt
import pathlib
# Sun Synchronous Orbit

# A sun-synchronous orbit is a type of near-polar orbit that allows a satellite to pass over the same part of the Earth at roughly the same local solar time on each orbit. This is achieved by having the orbital plane precess at the same rate as the Earth's revolution around the Sun, which is approximately 1 degree per day.
dot_omega = 360  # degrees per year

# degrees per year -> rad/s
seconds_per_year = 365.25 * 24 * 3600
dot_omega_rad_s = radians(dot_omega) / seconds_per_year

print(
    f"Required nodal precession rate for sun-synchronous orbit: {dot_omega_rad_s:.12e} rad/s")

Re = sgp4.EnvGetGeoConst(sgp4.XF_GEOCON_KMPER)  # Earth radius in km
# Gravitational parameter in km^3/s^2
mu = sgp4.EnvGetGeoConst(sgp4.XF_GEOCON_MU)
J2 = sgp4.EnvGetGeoConst(sgp4.XF_GEOCON_J2)  # J2 coefficient

e = 0.0  # circular orbit
height_km = 622  # typical sun-synchronous orbit altitude


def incli(height_km):
    a = Re + height_km
    i = acos(
        - 2.0 / 3.0 * dot_omega_rad_s *
            (a * (1 - e ** 2) / Re) ** 2 / J2 * sqrt(a ** 3 / mu)
    )
    return i


print(
    f"Required inclination for sun-synchronous orbit at {height_km} km altitude: {degrees(incli(height_km)):.4f} degrees")


results = pd.DataFrame(columns=["Height_km", "Inclination_deg"])
print(f"| {'Height in km':>12} | {'Inclination (deg)':>17} |")
print(f"|{'-'*14}|{'-'*19}|")
for h in [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]:
    i_deg = degrees(incli(h))
    results = pd.concat([results, pd.DataFrame(
        {"Height_km": [h], "Inclination_deg": [i_deg]})], ignore_index=True)
    print(f"| {h:12.4f} | {i_deg:17.4f} |")

results.plot(x="Height_km", y="Inclination_deg", title="Inclination vs Altitude for Sun-Synchronous Orbits",
             xlabel="Altitude (km)", ylabel=r"Inclination ($^\circ$)", grid=True)

# Ensure imgs directory exists and save plot
img_dir = pathlib.Path(__file__).parent / ".." / "imgs"
img_dir = img_dir.resolve()
img_dir.mkdir(parents=True, exist_ok=True)
img_path = img_dir / "sun_sync_inclination.png"
# save the plot to the specified path
plt.savefig(img_path)
print(f"Plot saved to: {img_path}")
