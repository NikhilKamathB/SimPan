import { getCookie } from "./utils.js";

/*======================= Keep specific nodes ========================*/
function keepSpecificNodes(keepTypes) {
    // Handle registered node types
    const nodeTypes = LiteGraph.registered_node_types;
    const keepSet = new Set(keepTypes);
    for (let typeName in nodeTypes) {
        if (nodeTypes.hasOwnProperty(typeName)) {
            if (!keepSet.has(typeName)) {
                delete LiteGraph.registered_node_types[typeName];
            }
        }
    }
    // Handle search box | Search box extras will contain only the custom built nodes
    LiteGraph.searchbox_extras = {};
}
/*=====================================================================*/

/*============== Add Environment specefic nodes here ==================*/
/*=====================================================================*/

/*======================= Add Carla nodes here ========================*/
class ActorGeneratorNode extends LGraphNode {

    constructor() {
        super();
        this.title = "Actor Generator";
        this.addOutput("Output Directory", "string");
        this.properties = {
            actorType: "vehicle",
            numberOfActors: 0,
            referenceSourceFile: "/home/tyche/nikhil/SDC/data/config/vehicles/vehicle0.yaml",
            outputDirectory: "/home/tyche/nikhil/SDC/data/config/vehicles",
            byPass: true
        };
        this.addWidget("combo", "Actor Type", this.properties.actorType, value => {
            this.properties.actorType = value;
        }, { values: ["vehicle", "pedestrian"] });
        this.addWidget("number", "Number of Actors", this.properties.numberOfActors, value => {
            this.properties.numberOfActors = value;
        }, { min: 0, max: 100, step: 10, precision: 0 });
        this.addWidget("text", "Reference Source File", this.properties.referenceSourceFile, value => {
            this.properties.referenceSourceFile = value;
        });
        this.addWidget("text", "Output Directory", this.properties.outputDirectory, value => {
            this.properties.outputDirectory = value;
        });
        this.addWidget("toggle", "By Pass", this.properties.byPass, value => {
            this.properties.byPass = value;
        });
        this.size = [500, 150];
    }

    onExecute() {
        const csrftoken = getCookie('csrftoken');
        $.ajax({
            async: false,
            timeout: 0,
            url: "/comfyui/carla/actor-generator/",
            method: "POST",
            headers: { 'X-CSRFToken': csrftoken },
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify({
                actor_type: this.properties.actorType,
                number_of_actors: this.properties.numberOfActors,
                reference_config_file: this.properties.referenceSourceFile,
                config_dir: this.properties.outputDirectory,
                by_pass: this.properties.byPass
            }),
            success: response => {
                this.setOutputData(0, this.properties.outputDirectory);
                alert("Actor generated successfully.");
            },
            error: (xhr, status, error) => {
                console.log(xhr);
                console.log(status);
                console.log(error);
                alert("An error occurred while generating actor.");
            }
        });
    }
}

class SyntheticDataGenerator extends LGraphNode {

    constructor() {
        super();
        this.title = "Synthetic Data Generator";
        this.addInput("Vehicle Configuration Directory", "string");
        this.addInput("Pedestrian Configuration Directory", "string");
        this.addOutput("Output Directory", "string");
        this.properties = {
            hostname: "localhost",
            port: 2000,
            carlaClientTimeout: 10.0,
            synchronous: true,
            fixedDeltaSeconds: 0.05,
            tmPort: 8001,
            tmHybridPhysicsMode: true,
            tmHybridPhysicsModeRadius: 70.0,
            tmGlobalDistanceToLeadingVehicle: 2.5,
            tmSeed: 42,
            rfps: null,
            spectatorEnable: true,
            spectatorAttachmentMode: "v",
            spectatorLocationOffsetX: -7.0,
            spectatorLocationOffsetY: 0.0,
            spectatorLocationOffsetZ: 5.0,
            spectatorRotationPitch: -15.0,
            spectatorRotationYaw: 0.0,
            spectatorRotationRoll: 0.0,
            maxSimulationTime: 100000.0,
            maxVehicles: 50,
            maxPedestrians: 100,
            map: "Town01",
            mapDirectory: "/Game/Carla/Maps",
            worldConfigFile: "/home/tyche/nikhil/SDC/data/config/town01_default.yaml",
            outputDirectory: "/home/tyche/nikhil/SDC/data/raw",
            vechile_config_dir: "/home/tyche/nikhil/SDC/data/config/vehicles",
            pedestrian_config_dir: "/home/tyche/nikhil/SDC/data/config/pedestrians"
        };
        this.addWidget("text", "Hostname", this.properties.hostname, value => {
            this.properties.hostname = value;
        });
        this.addWidget("number", "Port", this.properties.port, value => {
            this.properties.port = value;
        }, { min: 0, max: 65535, step: 10, precision: 0 });
        this.addWidget("number", "Carla Client Timeout", this.properties.carlaClientTimeout, value => {
            this.properties.carlaClientTimeout = value;
        }, { min: 0, max: 20, step: 1, precision: 1 });
        this.addWidget("toggle", "Synchronous Mode", this.properties.synchronous, value => {
            this.properties.synchronous = value;
        });
        this.addWidget("number", "Fixed Delta Seconds", this.properties.fixedDeltaSeconds, value => {
            this.properties.fixedDeltaSeconds = value;
        }, { min: 0, max: 10, step: 0.1, precision: 2 });
        this.addWidget("number", "Traffic Manager Port", this.properties.tmPort, value => {
            this.properties.tmPort = value;
        }, { min: 0, max: 65535, step: 10, precision: 0 });
        this.addWidget("toggle", "Traffic Manager Hybrid Physics Mode", this.properties.tmHybridPhysicsMode, value => {
            this.properties.tmHybridPhysicsMode = value;
        });
        this.addWidget("number", "Traffic Manager Hybrid Physics Mode Radius", this.properties.tmHybridPhysicsModeRadius, value => {
            this.properties.tmHybridPhysicsModeRadius = value;
        }, { min: 0, max: 100, step: 1, precision: 1 });
        this.addWidget("number", "Traffic Manager Global Distance to Leading Vehicle", this.properties.tmGlobalDistanceToLeadingVehicle, value => {
            this.properties.tmGlobalDistanceToLeadingVehicle = value;
        }, { min: 0, max: 10, step: 1, precision: 1 });
        this.addWidget("number", "Traffic Manager Seed", this.properties.tmSeed, value => {
            this.properties.tmSeed = value;
        }, { min: 0, max: 100, step: 10, precision: 0 });
        this.addWidget("number", "RFPS", this.properties.rfps, value => {
            this.properties.rfps = value;
        }, { min: 0, max: 120, step: 10, precision: 0 });
        this.addWidget("toggle", "Spectator Enable", this.properties.spectatorEnable, value => {
            this.properties.spectatorEnable = value;
        });
        this.addWidget("combo", "Spectator Attachment Mode", this.properties.spectatorAttachmentMode, value => {
            this.properties.spectatorAttachmentMode = value;
        }, { values: ["d", "t", "v"] });
        this.addWidget("number", "Spectator Location Offset X", this.properties.spectatorLocationOffsetX, value => {
            this.properties.spectatorLocationOffsetX = value;
        }, { step: 0.1, precision: 2 });
        this.addWidget("number", "Spectator Location Offset Y", this.properties.spectatorLocationOffsetY, value => {
            this.properties.spectatorLocationOffsetY = value;
        }, { step: 0.1, precision: 2 });
        this.addWidget("number", "Spectator Location Offset Z", this.properties.spectatorLocationOffsetZ, value => {
            this.properties.spectatorLocationOffsetZ = value;
        }, { step: 0.1, precision: 2 });
        this.addWidget("number", "Spectator Rotation Pitch", this.properties.spectatorRotationPitch, value => {
            this.properties.spectatorRotationPitch = value;
        }, { step: 0.1, precision: 2 });
        this.addWidget("number", "Spectator Rotation Yaw", this.properties.spectatorRotationYaw, value => {
            this.properties.spectatorRotationYaw = value;
        }, { step: 0.1, precision: 2 });
        this.addWidget("number", "Spectator Rotation Roll", this.properties.spectatorRotationRoll, value => {
            this.properties.spectatorRotationRoll = value;
        }, { step: 0.1, precision: 2 });
        this.addWidget("number", "Max Simulation Time", this.properties.maxSimulationTime, value => {
            this.properties.maxSimulationTime = value;
        }, { min: 0, max: 1000000, step: 1000, precision: 0 });
        this.addWidget("number", "Max Vehicles", this.properties.maxVehicles, value => {
            this.properties.maxVehicles = value;
        }, { min: 0, max: 100, step: 10, precision: 0 });
        this.addWidget("number", "Max Pedestrians", this.properties.maxPedestrians, value => {
            this.properties.maxPedestrians = value;
        }, { min: 0, max: 100, step: 10, precision: 0 });
        this.addWidget("combo", "Map", this.properties.map, value => {
            this.properties.map = value;
        }, { values: ["Town01", "Town01_Opt", "Town02", "Town02_Opt", "Town03", "Town03_Opt", "Town04", "Town04_Opt", "Town05", "Town05_Opt", "Town10HD", "Town10HD_Opt"] });
        this.addWidget("text", "Map Directory", this.properties.mapDirectory, value => {
            this.properties.mapDirectory = value;
        });
        this.addWidget("text", "World Config File", this.properties.worldConfigFile, value => {
            this.properties.worldConfigFile = value;
        });
        this.addWidget("text", "Output Directory", this.properties.outputDirectory, value => {
            this.properties.outputDirectory = value;
        });
        this.addWidget("button", "Generate Synthethic Data", null, () => {
            if (this.graph) {
                this.graph.runStep();
            }
        });
        this.size = [500, 700];
    }

    onExecute() {
        const csrftoken = getCookie('csrftoken');
        $.ajax({
            async: false,
            url: "/comfyui/carla/synthetic-data-generator/",
            method: "POST",
            timeout: 0,
            headers: { 'X-CSRFToken': csrftoken },
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify({
                vechile_config_dir: this.getInputData(0) === null ? this.properties.vechile_config_dir : this.getInputData(0),
                pedestrian_config_dir: this.getInputData(1) === null ? this.properties.pedestrian_config_dir : this.getInputData(1),
                hostname: this.properties.hostname,
                port: this.properties.port,
                carla_client_timeout: this.properties.carlaClientTimeout,
                synchronous: this.properties.synchronous,
                fixed_delta_seconds: this.properties.fixedDeltaSeconds,
                tm_port: this.properties.tmPort,
                tm_hybrid_physics_mode: this.properties.tmHybridPhysicsMode,
                tm_hybrid_physics_radius: this.properties.tmHybridPhysicsModeRadius,
                tm_global_distance_to_leading_vehicle: this.properties.tmGlobalDistanceToLeadingVehicle,
                tm_seed: this.properties.tmSeed,
                rfps: this.properties.rfps,
                spectator_enabled: this.properties.spectatorEnable,
                spectator_attachment_mode: this.properties.spectatorAttachmentMode,
                spectator_location_offset_x: this.properties.spectatorLocationOffsetX,
                spectator_location_offset_y: this.properties.spectatorLocationOffsetY,
                spectator_location_offset_z: this.properties.spectatorLocationOffsetZ,
                spectator_rotation_pitch: this.properties.spectatorRotationPitch,
                spectator_rotation_yaw: this.properties.spectatorRotationYaw,
                spectator_rotation_roll: this.properties.spectatorRotationRoll,
                max_simulation_time: this.properties.maxSimulationTime,
                max_vechiles: this.properties.maxVehicles,
                max_pedestrians: this.properties.maxPedestrians,
                map: this.properties.map,
                map_dir: this.properties.mapDirectory,
                world_configuration: this.properties.worldConfigFile,
                output_directory: this.properties.outputDirectory
            }),
            success: response => {
                this.setOutputData(0, this.properties.outputDirectory);
                alert("Synthetic data generated successfully.");
            },
            error: (xhr, status, error) => {
               alert("An error occurred while generating synthetic data.");
            }
        });
    }
}
/*=====================================================================*/

/*======================= Execute pre-commits =========================*/
function executePreCommits() {
    keepSpecificNodes();
    LiteGraph.registerNodeType("Carla/Actor Generator", ActorGeneratorNode);
    LiteGraph.registerNodeType("Carla/Synthetic Data Generator", SyntheticDataGenerator);
}
/*=====================================================================*/

export { executePreCommits };