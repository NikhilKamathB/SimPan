import time
from celery import shared_task
from third_party.SDC import main
from workers.validators import (
    Status,
    ActorType,
    ActorGeneratorValidator,
    SyntheticDataGeneratorValidator,
    SyntheticDataReportGeneratorValidator
)
from simpan.simpan.validator import ResponseValidator


@shared_task(name="generate_actor")
def generate_actor(config: dict) -> dict:
    config = ActorGeneratorValidator.model_validate(config)
    try:
        # TODO: remove this
        # time.sleep(5)
        start_time = time.time()
        for_vehicle = config.actor_type == ActorType.VEHICLE
        main.generate_configuration(
            number_of_actors=config.number_of_actors,
            config_dir=config.config_dir,
            reference_config_file=config.reference_config_file,
            for_vehicle=for_vehicle,
            for_pedestrian=not for_vehicle
        )
        return ResponseValidator.model_validate({
            "status": Status.OK,
            "message": "Actor generation completed successfully.",
            "body": {
                "time_elapsed": (time.time() - start_time) / 60,  # in minutes
                "actor_type": config.actor_type,
                "output_directory": config.config_dir,
            }
        }).model_dump(mode="json")
    except Exception as e:
        return ResponseValidator.model_validate({
            "status": Status.ERROR,
            "message": "Actor generation failed.",
            "body": {
                "error": str(e),
            }
        }).model_dump(mode="json")

@shared_task(name="generate_synthetic_data")
def generate_synthetic_data(carla_config: dict) -> dict:
    carla_config = SyntheticDataGeneratorValidator.model_validate(carla_config)
    try:
        start_time = time.time()
        # time.sleep(3)
        main.generate_synthetic_data(
            hostname=carla_config.hostname,
            port=carla_config.port,
            carla_client_timeout=carla_config.carla_client_timeout,
            synchronous=carla_config.synchronous,
            fixed_delta_seconds=carla_config.fixed_delta_seconds,
            tm_port=carla_config.tm_port,
            tm_hybrid_physics_mode=carla_config.tm_hybrid_physics_mode,
            tm_hybrid_physics_radius=carla_config.tm_hybrid_physics_radius,
            tm_global_distance_to_leading_vehicle=carla_config.tm_global_distance_to_leading_vehicle,
            tm_seed=carla_config.tm_seed,
            tm_speed=carla_config.tm_speed,
            rfps=carla_config.rfps,
            spectator_enabled=carla_config.spectator_enabled,
            spectator_attachment_mode=carla_config.spectator_attachment_mode,
            spectator_location_offset=carla_config.spectator_location_offset(),
            spectator_rotation=carla_config.spectator_rotation(),
            max_simulation_time=carla_config.max_simulation_time,
            max_vechiles=carla_config.max_vechiles,
            vechile_config_dir=carla_config.vechile_config_dir,
            max_pedestrians=carla_config.max_pedestrians,
            pedestrian_config_dir=carla_config.pedestrian_config_dir,
            map=carla_config.map,
            map_dir=carla_config.map_dir,
            world_configuration=carla_config.world_configuration,
            output_directory=carla_config.output_directory
        )
        return ResponseValidator.model_validate({
            "status": Status.OK,
            "message": "Synthetic data generation completed successfully.",
            "body": {
                "time_elapsed": (time.time() - start_time) / 60, # in minutes
                "hostname": carla_config.hostname,
                "port": carla_config.port,
                "map": carla_config.map,
                "output_directory": carla_config.output_directory
            }
        }).model_dump(mode="json")
    except Exception as e:
        return ResponseValidator.model_validate({
            "status": Status.ERROR,
            "message": "Synthetic data generation failed.",
            "body": {
                "error": str(e),
            }
        }).model_dump(mode="json")
    

@shared_task(name="generate_synthetic_data_report")
def generate_synthetic_data_report(carla_config: dict) -> dict:
    carla_config = SyntheticDataReportGeneratorValidator.model_validate(carla_config)
    try:
        start_time = time.time()
        # TODO: remove this
        # time.sleep(3)
        main.generate_synthetic_data_report(
            **carla_config.model_dump(mode="dict")
        )
        return ResponseValidator.model_validate({
            "status": Status.OK,
            "message": "Synthetic data report generation completed successfully.",
            "body": {
                "time_elapsed": (time.time() - start_time) / 60,  # in minutes
                "output_directory": carla_config.output_directory
            }
        }).model_dump(mode="json")
    except Exception as e:
        return ResponseValidator.model_validate({
            "status": Status.ERROR,
            "message": "Synthetic data report generation failed.",
            "body": {
                "error": str(e),
            }
        }).model_dump(mode="json")
