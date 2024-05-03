from enum import Enum
from pydantic import BaseModel
from typing import Optional, List


class Status(Enum):

    OK = "OK"
    ERROR = "ERROR"


class ActorType(Enum):

    VEHICLE = "vehicle"
    PEDESTRIAN = "pedestrian"


class ExchangeName(Enum):

    SDC = "sdc"


class QueueName(Enum):

    SDC = "sdc"


class RoutingKey(Enum):

    SDC = "sdc_routing_key"


class ActorGeneratorValidator(BaseModel):

    actor_type: ActorType = ActorType.VEHICLE
    number_of_actors: Optional[int] = 1
    config_dir: Optional[str] = "/home/tyche/nikhil/SDC/data/config/vehicles"
    reference_config_file: Optional[str] = "/home/tyche/nikhil/SDC/data/config/vehicles/vehicle0.yaml"


class SyntheticDataGeneratorValidator(BaseModel):

    hostname: Optional[str] = "localhost"
    port: Optional[int] = 2000
    carla_client_timeout: Optional[float] = 10.0
    synchronous: Optional[bool] = True
    fixed_delta_seconds: Optional[float] = 0.05
    tm_port: Optional[int] = 8001
    tm_hybrid_physics_mode: Optional[bool] = True
    tm_hybrid_physics_radius: Optional[float] = 70.0
    tm_global_distance_to_leading_vehicle: Optional[float] = 2.5
    tm_seed: Optional[int] = 42
    tm_speed: Optional[float] = 60.0
    rfps: Optional[int] = None
    spectator_enabled: Optional[bool] = True
    spectator_attachment_mode: Optional[str] = 'v'
    spectator_location_offset_x: Optional[float] = -7.0
    spectator_location_offset_y: Optional[float] = 0.0
    spectator_location_offset_z: Optional[float] = 5.0
    spectator_rotation_pitch: Optional[float] = -15.0
    spectator_rotation_yaw: Optional[float] = 0.0
    spectator_rotation_roll: Optional[float] = 0.0
    max_simulation_time: Optional[int] = 100000
    max_vechiles: Optional[int] = 50
    vechile_config_dir: Optional[str] = "/home/tyche/nikhil/SDC/data/config/vehicles"
    max_pedestrians: Optional[int] = 100
    pedestrian_config_dir: Optional[str] = "/home/tyche/nikhil/SDC/data/config/pedestrians"
    map: Optional[str] = "Town01"
    map_dir: Optional[str] = "/Game/Carla/Maps"
    world_configuration: Optional[str] = "/home/tyche/nikhil/SDC/data/config/town01_default.yaml"
    output_directory: Optional[str] = "/home/tyche/nikhil/SDC/data/raw"

    def spectator_location_offset(self) -> List[float]:
        return [
            self.spectator_location_offset_x,
            self.spectator_location_offset_y,
            self.spectator_location_offset_z
        ]
    
    def spectator_rotation(self) -> List[float]:
        return [
            self.spectator_rotation_pitch,
            self.spectator_rotation_yaw,
            self.spectator_rotation_roll
        ]


class SyntheticDataReportGeneratorValidator(BaseModel):

    data_dir: Optional[str] = "/home/tyche/nikhil/SDC/data/raw"
    output_directory: Optional[str] = "/home/tyche/nikhil/SDC/data/interim"
    prefix_tag: Optional[bool] = False
    prefix_dir: Optional[bool] = False
    need_file_name: Optional[bool] = False
