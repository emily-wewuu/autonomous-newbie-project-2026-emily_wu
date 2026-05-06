# scenarios.py
#
# Sign convention:
# lane_offset_m:
#   negative = vehicle is left of lane center
#   positive = vehicle is right of lane center
#
# heading_error_deg:
#   negative = vehicle heading points left of desired direction
#   positive = vehicle heading points right of desired direction

scenarios = [
    {
        # LIMITATION 1: RIGHT COMMAND DOESN'T STEER CAR QUICKLY ENOUGH TO AVOID OBSTACLE
        # WE CAN IMPROVE THE SYSTEM BY ADDING SAY 3 DIFFERENT LEVELS OF STEERING INTENSITY INSTEAD JUST RIGHT/LEFT. E.G. CATEGORISED BY ANGLE CHANGE PER SECOND. SO THAT WE CAN HOPEFULLY START STEERING AHEAD OF TIME AND WON'T END UP IN A CASE WHERE STEERING INTENSITY IS NOT STRONG ENOUGH AND WE HAVE NO CHOICE EXCEPT CRASHING
        # SAFETY CONSIDERATION WEIGHING: TOP PRIORITY TO SOLVE AS HERE THE CAR ENDS UP HITTING THE OBSTACLE SIDEWAYS WHICH IS A LOT MORE DANGEROUS THAN CRASHING HEAD-ON FOR THE PASSENGERS AND ALSO MORE LIKELY TO CAUSE MORE DAMAGE ON THE CAR'S STRUCTURE SENSORS AND OTHER COMPONENTS COMPARE TO A HEAD-ON CRASH.

        "name": "Left-Blocked Escape Right",
        "inputs": {
            "obstacle_distance_m": 1.5,
            "lane_offset_m": -0.3, # Deviated left toward the blockage
            "heading_error_deg": 0.0,
            "speed_mps": 2.0,
            "e_stop": False,
            "left_clear": False,
            "right_clear": True,
            "sensor_valid": True
        }
    },
    {
        # LIMITATION 2: IF OBSTACLE DISTANCE <= DANGER_DISTANCE AND SPEED > 3.3 IT WILL CRASH INTO OBSTACLE NO MATTER WHAT AS STOP IS NOT REDUCING THE SPEED QUICK ENOUGH
        # WE CAN IMPROVE THE SYSTEM BY ADDING SAY 3 DIFFERENT LEVELS OF BRAKING INSTEAD JUST SLOW AND STOP. E.G. CATEGORISED BY SPEED REDUCTION PER SECOND. SO THAT WE CAN HOPEFULLY START REDUCING SPEED AHEAD OF TIME AND WON'T END UP IN A CASE WHERE SPEED REDUCTION IS NOT STRONG ENOUGH AND WE HAVE NO CHOICE EXCEPT CRASHING
        "name": "Centered Danger Obstacle",
        "inputs": {
            "obstacle_distance_m": 0.5,
            "lane_offset_m": 0.0,
            "heading_error_deg": 0.0,
            "speed_mps": 2.0,
            "e_stop": False,
            "left_clear": True,
            "right_clear": True,
            "sensor_valid": True
        }
    },
    {
        # LIMITATION 3:SINCE THE INPUTS DON'T UPDATE, IT WILL JUST KEEP TURNING LEFT
        # ASSUMPTION: IN REALITY WE WILL RUN CONTROLLER.PY IN SAY EVERY 0.5 SECOND THEN IT WILL BE ABLE TO PICK UP THE CHANGES IN OFFSET AND OBSTACLE DISTANCE AND WILL STEER AWAY AT SOME POINT AND EVENTUALLY GET BACK ON TRACK. TRACK WILL LOOK LIKE A DAMPED OSCILLATION
        "name": "High-Speed Mild Drift",
        "inputs": {
            "obstacle_distance_m": 999.0,
            "lane_offset_m": 0.20,
            "heading_error_deg": 0.0,
            "speed_mps": 5.0,
            "e_stop": False,
            "left_clear": True,
            "right_clear": True,
            "sensor_valid": True
        }
    },
    {
        # LIMITATION 3: SAME AS ABOVE, DOESN'T UPDATE...
        "name": "Large Heading Boundary Conflict",
        "inputs": {
            "obstacle_distance_m": 999.0,
            "lane_offset_m": 0.2,
            "heading_error_deg": -10,
            "speed_mps": 2.0,
            "e_stop": False,
            "left_clear": True,
            "right_clear": True,
            "sensor_valid": True
        }
    },
    {
        "name": "Clear Path, Centered",
        "inputs": {
            "obstacle_distance_m": 999.0,
            "lane_offset_m": 0.0,
            "heading_error_deg": 0.0,
            "speed_mps": 2.0,
            "e_stop": False,
            "left_clear": True,
            "right_clear": True,
            "sensor_valid": True
        }
    },
    {
        "name": "Close Obstacle Ahead, No Safe Side",
        "inputs": {
            "obstacle_distance_m": 0.8,
            "lane_offset_m": 0.0,
            "heading_error_deg": 0.0,
            "speed_mps": 2.5,
            "e_stop": False,
            "left_clear": False,
            "right_clear": False,
            "sensor_valid": True
        }
    },
    {
        "name": "Obstacle Ahead, Left Clear",
        "inputs": {
            "obstacle_distance_m": 1.8,
            "lane_offset_m": 0.0,
            "heading_error_deg": 0.0,
            "speed_mps": 3.0,
            "e_stop": False,
            "left_clear": True,
            "right_clear": False,
            "sensor_valid": True
        }
    },
    {
        "name": "Obstacle Ahead, Right Clear",
        "inputs": {
            "obstacle_distance_m": 1.8,
            "lane_offset_m": 0.0,
            "heading_error_deg": 0.0,
            "speed_mps": 3.0,
            "e_stop": False,
            "left_clear": False,
            "right_clear": True,
            "sensor_valid": True
        }
    },
    {
        "name": "Large Heading Error at Speed",
        "inputs": {
            "obstacle_distance_m": 999.0,
            "lane_offset_m": 0.1,
            "heading_error_deg": 22.0,
            "speed_mps": 4.5,
            "e_stop": False,
            "left_clear": True,
            "right_clear": True,
            "sensor_valid": True
        }
    },
    {
        "name": "Emergency Stop Active",
        "inputs": {
            "obstacle_distance_m": 2.0,
            "lane_offset_m": -0.4,
            "heading_error_deg": -12.0,
            "speed_mps": 3.0,
            "e_stop": True,
            "left_clear": True,
            "right_clear": False,
            "sensor_valid": True
        }
    },
    {
        "name": "Obstacle Plus Heading Conflict",
        "inputs": {
            "obstacle_distance_m": 1.7,
            "lane_offset_m": -0.2,
            "heading_error_deg": 18.0,
            "speed_mps": 3.5,
            "e_stop": False,
            "left_clear": False,
            "right_clear": True,
            "sensor_valid": True
        }
    },
    {
        "name": "Mild Drift, No Obstacle",
        "inputs": {
            "obstacle_distance_m": 999.0,
            "lane_offset_m": 0.25,
            "heading_error_deg": 5.0,
            "speed_mps": 2.2,
            "e_stop": False,
            "left_clear": True,
            "right_clear": True,
            "sensor_valid": True
        }
    },
    {
        "name": "Obstacle Plus Heading Conflict",
        "inputs": {
            "obstacle_distance_m": 1.7,
            "lane_offset_m": 0.2,
            "heading_error_deg": -18.0,
            "speed_mps": 3.5,
            "e_stop": False,
            "left_clear": True,
            "right_clear": False,
            "sensor_valid": True
        }
    }
]
