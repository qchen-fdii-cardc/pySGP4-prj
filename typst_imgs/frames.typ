#set text(font: "Cambria", size: 10pt)

#let axis_color = rgb("#222222")
#let orbit_color = rgb("#444444")
#let guide_color = rgb("#7a7a7a")
#let u_color = rgb("#cc4b37")
#let v_color = rgb("#2c7fb8")
#let w_color = rgb("#2f9e44")

// Orbital parameters (all key geometry is derived from these)
#let raan = 42deg
#let inc = 48deg
#let argp = 35deg
#let e = 0.001
#let p = 1.05
#let nu_p = 28deg

// 3D vector helpers
#let vadd(a, b) = (a.at(0) + b.at(0), a.at(1) + b.at(1), a.at(2) + b.at(2))
#let vscale(s, a) = (s * a.at(0), s * a.at(1), s * a.at(2))
#let dot(a, b) = a.at(0) * b.at(0) + a.at(1) * b.at(1) + a.at(2) * b.at(2)
#let cross(a, b) = (
  a.at(1) * b.at(2) - a.at(2) * b.at(1),
  a.at(2) * b.at(0) - a.at(0) * b.at(2),
  a.at(0) * b.at(1) - a.at(1) * b.at(0),
)
#let norm(a) = calc.sqrt(dot(a, a))
#let unit(a) = {
  let n = norm(a)
  vscale(1 / n, a)
}

// ECI basis
#let x_hat = (1.0, 0.0, 0.0)
#let y_hat = (0.0, 1.0, 0.0)
#let z_hat = (0.0, 0.0, 1.0)

// Ascending-node direction and orbital angular-momentum direction
#let n_asc = unit((calc.cos(raan), calc.sin(raan), 0.0))
#let h_hat = unit((
  calc.sin(inc) * calc.sin(raan),
  -calc.sin(inc) * calc.cos(raan),
  calc.cos(inc),
))

// Orbital-plane basis and perifocal basis
#let b_node = unit(cross(h_hat, n_asc))
#let p_hat = unit(vadd(vscale(calc.cos(argp), n_asc), vscale(calc.sin(argp), b_node)))
#let q_hat = unit(cross(h_hat, p_hat))

// Orbital position vector from true anomaly nu
#let r_vec(nu) = {
  let r = p / (1 + e * calc.cos(nu))
  vscale(r, vadd(vscale(calc.cos(nu), p_hat), vscale(calc.sin(nu), q_hat)))
}

// 3D->2D projection
#let basis_x2 = (-1.05, 0.62)
#let basis_y2 = (1.20, 0.24)
#let basis_z2 = (0.0, -1.26)
#let draw_scale = 82pt
#let origin = (134pt, 150pt)

#let add2(a, b) = (a.at(0) + b.at(0), a.at(1) + b.at(1))
#let sub2(a, b) = (a.at(0) - b.at(0), a.at(1) - b.at(1))
#let scale2l(s, v) = (s * v.at(0), s * v.at(1))
#let dot2(a, b) = a.at(0) * b.at(0) + a.at(1) * b.at(1)
#let norm2l(v) = calc.sqrt((v.at(0) / 1pt) * (v.at(0) / 1pt) + (v.at(1) / 1pt) * (v.at(1) / 1pt)) * 1pt
#let unit2(v) = {
  let dx = v.at(0) / 1pt
  let dy = v.at(1) / 1pt
  let n = calc.sqrt(dx * dx + dy * dy)
  if n == 0 {
    (0.0, 0.0)
  } else {
    (dx / n, dy / n)
  }
}
#let unit2n(v) = {
  let n = calc.sqrt(v.at(0) * v.at(0) + v.at(1) * v.at(1))
  if n == 0 {
    (0.0, 0.0)
  } else {
    (v.at(0) / n, v.at(1) / n)
  }
}
#let perp2(v) = (-v.at(1), v.at(0))
#let proj(v) = (
  draw_scale * (v.at(0) * basis_x2.at(0) + v.at(1) * basis_y2.at(0) + v.at(2) * basis_z2.at(0)),
  draw_scale * (v.at(0) * basis_x2.at(1) + v.at(1) * basis_y2.at(1) + v.at(2) * basis_z2.at(1)),
)
#let pt(v) = add2(origin, proj(v))

#let draw(c) = place(top + left, dx: 0pt, dy: 0pt, c)
#let label_at(p2, body, color: axis_color, dx: 0pt, dy: 0pt) = {
  place(top + left, dx: p2.at(0) + dx, dy: p2.at(1) + dy, text(fill: color, body))
}

#let draw_arrow(start3, dir3, len, color: axis_color, thickness: 1.1pt, head_len: 8pt, head_w: 5pt) = {
  let p0 = pt(start3)
  let p1 = pt(vadd(start3, vscale(len, dir3)))
  let d = unit2(sub2(p1, p0))
  let n = perp2(d)
  let base = sub2(p1, scale2l(head_len, d))
  let l = add2(base, scale2l(head_w / 2, n))
  let r = sub2(base, scale2l(head_w / 2, n))
  draw(line(start: p0, end: p1, stroke: thickness + color))
  draw(polygon(p1, l, r, fill: color, stroke: none))
}

#let polyline(points, stroke: 1pt + axis_color) = {
  for i in range(0, points.len() - 1) {
    draw(line(start: points.at(i), end: points.at(i + 1), stroke: stroke))
  }
}

#let oriented_perp(base_dir, toward_vec) = {
  let p = perp2(base_dir)
  if dot2(p, toward_vec) >= 0pt { p } else { scale2l(-1.0, p) }
}

// Key points and UVW basis at P
#let r_peri = r_vec(0deg)
#let r_asc = r_vec(-argp)
#let r_p = r_vec(nu_p)
#let r_eq = norm(r_asc)
#let u_hat = unit(r_p)
#let w_hat = h_hat
#let v_hat = unit(cross(w_hat, u_hat))
#let omega_dir = unit(vadd(n_asc, p_hat))

// Curves
#let o2 = pt((0.0, 0.0, 0.0))
#let x_eq_pt = pt(vscale(1.00 * r_eq, x_hat))
#let an_pt = pt(r_asc)
#let y_eq_pt = pt(vscale(0.72 * r_eq, y_hat))

#let x_dir = unit2(sub2(x_eq_pt, o2))
#let y_dir = unit2(sub2(y_eq_pt, o2))
#let an_dir = unit2(sub2(an_pt, o2))
#let t_x = oriented_perp(x_dir, sub2(an_pt, x_eq_pt))
#let t_y = oriented_perp(y_dir, sub2(an_pt, y_eq_pt))
#let t_an = unit2n(add2(t_x, t_y))

#let d_xa = norm2l(sub2(an_pt, x_eq_pt))
#let d_ay = norm2l(sub2(y_eq_pt, an_pt))

#let l_end_x = 0.34 * d_xa
#let l_end_y = 0.24 * d_ay
#let l_an_left = 0.16 * d_xa
#let l_an_right = 0.06 * d_ay
#let c_x = add2(x_eq_pt, scale2l(l_end_x, t_x))
#let c_an_left = sub2(an_pt, scale2l(l_an_left, t_an))
#let c_an_right = add2(an_pt, scale2l(l_an_right, t_an))
#let c_y = sub2(y_eq_pt, scale2l(l_end_y, t_y))

#let orb_pts = range(0, 241).map(i => {
  let nu = -180deg + i * 1.5deg
  pt(r_vec(nu))
})
#let center_ellipse_pts = range(0, 181).map(i => {
  let t = i * 2deg
  add2(o2, (108pt * calc.cos(t), 53pt * calc.sin(t)))
})

#figure(
  alt: "Variable-driven orbital geometry with ECI frame, ascending node, RAAN Omega, and UVW at point P.",
  box(width: 28em, height: 25em)[
    #polyline(center_ellipse_pts, stroke: 0.85pt + guide_color)
    #polyline(orb_pts, stroke: 1pt + orbit_color)

    #draw_arrow((0.0, 0.0, 0.0), x_hat, 1.55, color: axis_color, thickness: 1.15pt, head_len: 9pt, head_w: 6pt)
    #draw_arrow((0.0, 0.0, 0.0), y_hat, 1.45, color: axis_color, thickness: 1.15pt, head_len: 9pt, head_w: 6pt)
    #draw_arrow((0.0, 0.0, 0.0), z_hat, 1.35, color: axis_color, thickness: 1.15pt, head_len: 9pt, head_w: 6pt)

    // Ray from inertial center to ascending node (used for RAAN definition)
    #draw(line(start: pt((0.0, 0.0, 0.0)), end: pt(r_asc), stroke: 1.05pt + axis_color))

    // Earth center and point P markers removed per requested style

    // Radius vector to P
    #draw(line(start: pt((0.0, 0.0, 0.0)), end: pt(r_p), stroke: 1pt + axis_color))

    // Dashed line from inertial origin to perigee
    #draw(line(
      start: pt((0.0, 0.0, 0.0)),
      end: pt(r_peri),
      stroke: (paint: axis_color, thickness: 0.9pt, dash: "dashed"),
    ))

    // UVW triad at P
    #draw_arrow(r_p, u_hat, 0.30, color: u_color, thickness: 1.2pt, head_len: 7pt, head_w: 5pt)
    #draw_arrow(r_p, v_hat, 0.35, color: v_color, thickness: 1.2pt, head_len: 7pt, head_w: 5pt)
    #draw_arrow(r_p, w_hat, 0.35, color: w_color, thickness: 1.2pt, head_len: 7pt, head_w: 5pt)

    // Labels
    #label_at(pt(vscale(1.55, x_hat)), [$ hat(x) $], dx: -8pt, dy: -4pt)
    #label_at(pt(vscale(1.45, y_hat)), [$ hat(y) $], dx: 2pt, dy: -4pt)
    #label_at(pt(vscale(1.35, z_hat)), [$ hat(z) $], dx: -2pt, dy: -10pt)

    #label_at(pt(r_p), [Satellite], dx: 8pt, dy: -10pt)
    #label_at(add2(pt(r_peri), (10pt, -12pt)), [Perigee])
    // #label_at(add2(pt(r_peri), (8pt, 8pt)), [Orbit])

    #label_at(pt(vscale(0., n_asc)), [Ω], dx: -8pt, dy: 4pt)
    #label_at(pt(vscale(-0.36, h_hat)), [$ i $], dx: -14pt, dy: 20pt)
    #label_at(pt(vscale(0.52, omega_dir)), [(ω)], dx: 40pt, dy: -16pt)

    #label_at(pt(vadd(r_p, vscale(0.32, u_hat))), [$ u $], color: u_color, dx: 3pt, dy: -5pt)
    #label_at(pt(vadd(r_p, vscale(0.36, v_hat))), [$ v $], color: v_color, dx: 2pt, dy: -2pt)
    #label_at(pt(vadd(r_p, vscale(0.36, w_hat))), [$ w $], color: w_color, dx: 2pt, dy: -3pt)

    // Ascending node label
    // #label_at(pt(r_asc), [AN], dx: 4pt, dy: -12pt)
  ],
)
