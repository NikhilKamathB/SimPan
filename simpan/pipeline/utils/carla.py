from third_party.SDC import main


def generate_synthetic_data(synth_data_params: dict):
    """
        Given a bunch of configuration parameters, create actor configurations and generate synthetic data.
        Input parameters:
            - synth_data_params: arguments to be passed to the synthetic data generation function.
                                 ref - https://github.com/NikhilKamathB/SDC/blob/master/main.py
    """
    main.generate_synthetic_data(
        **synth_data_params
    )