import numpy as np
import mcdc


def submit_mcdc(seed, output):
    # =============================================================================
    # Set model
    # =============================================================================
    # Three slab layers with different purely-absorbing materials

    # Set materials
    m1 = mcdc.material(capture=np.array([0.90]))
    m2 = mcdc.material(capture=np.array([0.15]))
    m3 = mcdc.material(capture=np.array([0.60]))

    # Set surfaces
    s1 = mcdc.surface("plane-x", x=-1.0, bc="vacuum")
    s2 = mcdc.surface("plane-x", x=2.0)
    s3 = mcdc.surface("plane-x", x=5.0)
    s4 = mcdc.surface("plane-x", x=6.0, bc="vacuum")

    # Set cells
    mcdc.cell([+s1, -s2], m1)
    mcdc.cell([+s2, -s3], m2)
    mcdc.cell([+s3, -s4], m3)

    # =============================================================================
    # Set source
    # =============================================================================
    # Incident beam source
    mcdc.source(point=[0.0, 0.0, 0.0], direction=[1.0, 0.0, 0.0])

    # =============================================================================
    # Set tally, setting, and run mcdc
    # =============================================================================

    # Tally: cell-average fluxes
    mcdc.tally(
        scores=["exit"],
        x=np.linspace(0.0, 6.0, 2)
    )

    # Setting
    mcdc.setting(N_particle=1E3, N_batch=1E3, rng_seed=seed, output_name=output)

    mcdc.uq(material=m1, distribution="uniform", capture=np.array([0.7]))
    mcdc.uq(material=m2, distribution="uniform", capture=np.array([0.12]))
    mcdc.uq(material=m3, distribution="uniform", capture=np.array([0.5]))

    # Run
    mcdc.run()


for i in range(10):
    seed = np.random.randint(10000000)
    output = 'output' + str(i)
    submit_mcdc(seed, output)