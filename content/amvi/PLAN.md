# AMVI flashcards — plan

Flashcard notes for the Kerala PSC exam **Assistant Motor Vehicle Inspector**
(Motor Vehicles Department, Cat. No. 517/2022, 610/2022, 613/2022, 100 marks)
and exams like it (Kerala PSC technical/automobile posts, MVI, AMVI by-transfer).

The cards will feed a new module made with the Course Module Builder (fact
generator / question bank features).

## Who the cards are for

A learner of about average ability (think "90 IQ") who is tired, busy and
reads on a phone. So every card follows these rules:

- **One idea per card.** If it needs two ideas, it becomes two cards.
- **Short sentences.** The main line is 35 words or less.
- **Everyday words first, exam word second.** "Viscosity is how thick a liquid
  is — honey has high viscosity."
- **Always the reason** (`why`) and, where it helps, an **everyday example**
  from Kerala life (bus, autorickshaw, scooter, pressure cooker, coconut oil).
- **A recall question** with a few-word answer, so the card can be revised by
  self-testing.
- **Explain simply**: the same idea said a second, even easier way.
- Formulas are written in plain text: `Power = Force × Velocity`.
- Exam facts PSC likes (numbers, section numbers, "who invented", units) are
  stated exactly.

## Format

Cards are written in easy-to-edit YAML, one file per unit, in `units/`.
`build.py` turns them into a Recallio / Spaced Loop content pack
(`schema_version 1.0`, see the recallio skill) in `dist/amvi-pack.json`
and a review sheet `dist/review.csv`.

YAML card (fact):

```yaml
- id: viscosity.f01          # unique inside the unit
  topic: u1.fluid.properties # topic id from the tree below
  learn: "Viscosity is how thick a liquid is, or how much it resists flowing."
  why: "Thick liquids have strong inner friction between their layers."
  example: "Honey flows slowly. Water flows fast. Honey has more viscosity."
  q: "What does viscosity measure?"
  a: "Resistance to flow (thickness of a fluid)."
  simple: "Thick = high viscosity. Thin = low viscosity."
  difficulty: 1
```

Each topic also gets one `summary` card (3–5 points) for revision and cram.

- Language: **English** (the AMVI question paper is in English). Malayalam can
  be added later as a second language in the same files.
- Every card starts as `status: needs_review`. Law cards (MV Act, KMVT Act,
  Driving Regulations) must be checked against the current bare Act before
  going live, because the Act was amended in 2019 and fines change.
- No past-paper questions are pasted in as lesson cards. Practice MCQs are
  labelled "Practice — exam pattern".

## Topic tree and card targets

Marks show weight; the card count follows it. Total target **2,000+ cards**
(vivek's choice, 17 Nov 2026): every syllabus term, formula, number and
section gets its own card, plus cards on common PSC traps (look-alike terms,
'which is higher', units) and worked numericals as step cards.

### Unit I — Fluid mechanics and hydraulic machines (10 marks, ~180 cards)
| Topic id | Covers |
|---|---|
| u1.properties | density, specific weight, specific volume, specific gravity, viscosity, kinematic viscosity, Newton's law of viscosity, compressibility, surface tension, capillarity |
| u1.pressure | pressure, pressure head, absolute / gauge / atmospheric / vacuum pressure, Pascal's law |
| u1.measure | piezometer, pressure gauge (Bourdon), manometer, U-tube, differential manometer |
| u1.fluidtypes | ideal, real, Newtonian, non-Newtonian fluids |
| u1.flow | orifice, notches, venturimeter, steady/unsteady, uniform/non-uniform, laminar/turbulent, Reynolds number, continuity equation |
| u1.losses | major and minor losses, Darcy's and Chezy's formula |
| u1.oils | hydraulic oil properties: viscosity index, oxidation stability, demulsibility, lubricity, rust prevention, pour point, flash & fire point, neutralisation number |
| u1.machines | pumps (centrifugal, reciprocating), slip, efficiency, discharge, specific speed, turbines (impulse, reaction), comparison |

### Unit II — Thermal engineering (10 marks, ~180 cards)
| Topic id | Covers |
|---|---|
| u2.laws | zeroth, first, second law of thermodynamics |
| u2.process | isothermal, isentropic (adiabatic), work done, PV diagrams |
| u2.cycles | air-standard assumptions, Carnot, Otto, Diesel, Joule (Brayton), dual cycle |
| u2.engines | 2-stroke & 4-stroke petrol and diesel, PV diagrams, valve timing |
| u2.performance | IP, BP, FP, mechanical / indicated thermal / brake thermal / relative efficiency, fuel consumption, SFC, Morse test, heat balance sheet |
| u2.compressors | uses, types, single/multi stage, single/double acting, work and efficiency |
| u2.heat | conduction, convection, radiation, Fourier's law, thermal conductivity |

### Unit III — Strength of materials (10 marks, ~180 cards)
| Topic id | Covers |
|---|---|
| u3.stress | tensile, compressive, shear stress and strain, longitudinal/lateral strain, Poisson's ratio, volumetric strain |
| u3.diagram | stress–strain diagram, mild steel vs brittle, limit of proportionality, elastic limit, yield point, ultimate stress, working stress, factor of safety |
| u3.elastic | Hooke's law, E, K, G and their relation, superposition, varying and composite sections |
| u3.thermal | thermal stress and strain, composite bars |
| u3.friction | types, laws of friction |
| u3.cg | centre of gravity, moment of inertia |
| u3.beams | beam types, loads, shear force and bending moment (cantilever, simply supported; point load, UDL) |
| u3.rivets | rivets, lap/butt joints, failures, strength, efficiency |
| u3.bolts_springs | bolts, springs, spring index, deflection, stiffness |
| u3.welds | fillet and butt welds, terms, strength |

### Unit IV — Machine elements, materials and boilers (10 marks, ~180 cards)
| Topic id | Covers |
|---|---|
| u4.bearings | functions, radial/thrust, sliding/rolling, journal, bearing characteristic number, heat generated |
| u4.governors | function, types, height, equilibrium speeds, sensitiveness, stability, hunting, isochronism |
| u4.flywheel | function, vs governor, fluctuation of speed and energy, coefficients, energy stored |
| u4.gears | types, spur gear terms, velocity ratio, gear trains |
| u4.boilers | types, mountings, accessories, steam engine parts and working |
| u4.materials | cast iron types, steel types and composition, heat treatment, alloy steels, non-ferrous metals and alloys |

### Module V — Engine construction and systems (10 marks, ~200 cards)
| Topic id | Covers |
|---|---|
| u5.block | cylinder block, liners, head, gasket |
| u5.piston | pistons, rings, connecting rod, crankshaft |
| u5.valves | valve types, sodium cooled valves, valve mechanisms (side cam, OHC), materials, camshaft and drives |
| u5.petrolfuel | fuel feed (AC mechanical pump, SU electric pump), filters, air cleaners |
| u5.carb | simple carburettor, compensation, mixture strength, modern carburettor circuits, choke |
| u5.manifold | inlet manifold, variable intake, VVT, CVVT, exhaust manifold, catalytic converter, muffler |
| u5.dieselfuel | diesel fuel system parts, distributor/rotary pump, feed pump, priming, filters, injectors, turbocharger, turbo lag |
| u5.lube | wet/dry sump, splash/pressure feed, oil pump, relief valve, coolers, filters, seals, crankcase ventilation |
| u5.cooling | air/water cooling, thermosyphon, pump circulation, thermostat, radiator, pressure cap, coolant, antifreeze, fan |

### Module VI — Chassis (10 marks, ~180 cards)
| Topic id | Covers |
|---|---|
| u6.frame | chassis, frame types and sections, bumpers, sub-frames, materials |
| u6.axle | front axle, dead/live, cross section, stub axle types |
| u6.suspension | front and rear suspension, leaf/coil springs, helper spring, shackle, telescopic shock absorber |
| u6.steering | Ackermann, Davis, steering gearboxes, linkages, power steering, collapsible column, wheel alignment (camber, caster, toe, KPI) |
| u6.brakes | mechanical, hydraulic, air, servo brakes, drum/disc, master cylinder, wheel cylinder, bleeding |

### Module VII — Transmission and electrical (10 marks, ~220 cards)
| Topic id | Covers |
|---|---|
| u7.clutch | friction clutch principle, single plate, diaphragm, cone, centrifugal, semi-centrifugal, vacuum, hydraulic, electromagnetic, multiplate, fluid flywheel |
| u7.gearbox | sliding, constant, synchromesh, progressive, epicyclic, torque converter, selector, 2-wheeler, CVT, automatic |
| u7.driveline | propeller shaft, universal joint, torque tube, Hotchkiss, CV joint, FWD, differential, rear axle types |
| u7.wheels | wheel types, tyre construction, tubeless, tread, inflation, tyre performance |
| u7.charging | dynamo, alternator, regulators |
| u7.starting | starter motor, Bendix, overrunning clutch, axial, pre-engaged |
| u7.ignition | coil ignition parts, cam angle, condenser, distributor, spark plugs, advance, magneto, electronic, transistorised, computer controlled, DLI |

### Unit VIII — Transport management and modern technology (10 marks, ~200 cards)
| Topic id | Covers |
|---|---|
| u8.mvact_basics | features of MV Act, driver/conductor tests and duties, registration, traffic signs, MVD wings |
| u8.road | highway width, gradient, cross section, camber, super elevation, sight distance, intersections |
| u8.insurance | insurance surveying, policy types, factors in assessing loss |
| u8.efi | EFI, MPFI, GDI, TBI, sensors, actuators, CRDI, ECM, injectors |
| u8.pollution | sources, controls, PCV, after burner, cat converter, EGR, EVAP canister, diesel smoke, Bharat Stage norms |
| u8.accessories | cruise control, power seat/mirror, rain-sensing wiper, climate control, noise control, parking sensors, seat belt, airbag, ESC, ABS, keyless entry, immobiliser, traction control, GPS |
| u8.ev | EV and hybrid benefits, challenges, policies, EV drive and parts, hybrid types and parts |

### Part II — Driving licence (10 marks, ~150 cards)
| Topic id | Covers |
|---|---|
| dl.regulations | Motor Vehicles (Driving) Regulations, 2017: lane driving, overtaking, signals, parking, speed, use of horn, hand signals, right of way |
| dl.licensing | MV Act 1988 Chapter II, sections 3–28: need for licence, age limits, learner's licence, DL classes, tests, validity, renewal, disqualification, endorsement |

### Part III — Job related laws (10 marks, ~250 cards)
| Topic id | Covers |
|---|---|
| law.defs | Section 2 definitions listed in the syllabus (adapted vehicle … unladen weight) |
| law.registration | Sections 39, 44, 46, 52, 53, 55, 56 |
| law.permits | Section 66, Section 99 |
| law.construction | Sections 109, 110A, 110B |
| law.traffic | Sections 112–136A listed |
| law.insurance | Section 146 |
| law.offences | Sections 177–208 listed, 213 |
| law.kmvt | Kerala MV Taxation Act 1976: sections 2(e), 3, 3A, 4, 5, 6, 7, 10, 11, 12, 13, 26 |

## Stages and git pushes

1. This plan + YAML format + `build.py`. **Push.**
2. Unit I. **Push.**
3. Unit II. **Push.**
4. Unit III. **Push.**
5. Unit IV. **Push.**
6. Module V. **Push.**
7. Module VI. **Push.**
8. Module VII. **Push.**
9. Unit VIII. **Push.**
10. Driving licence. **Push.**
11. MV Act + KMVT Act. **Push.**
12. Build full pack, validate, review sheet. **Push.**

## Notes for the reviewer

- Exam date for these category numbers has passed; the pack uses a placeholder
  date marked `estimated`. Set the real date of the next AMVI exam in the
  builder.
- Law cards quote the MV Act as amended by the MV (Amendment) Act, 2019.
  Fines and section text must be checked against the current India Code text.
