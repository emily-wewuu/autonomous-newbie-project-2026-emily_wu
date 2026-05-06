# controller.py
#
# Faulty decision logic for the 2026 Autonomous Newbie Project.
# Recruits will mainly modify this file.
#
# Sign convention:
# lane_offset_m:
#   negative = vehicle is left of lane center
#   positive = vehicle is right of lane center
#
# heading_error_deg:
#   negative = vehicle heading points left of desired direction
#   positive = vehicle heading points right of desired direction
#
# Steering output semantics:
# "LEFT" means command the vehicle to steer / move left.
# "RIGHT" means command the vehicle to steer / move right.
# Therefore:
# - positive lane_offset_m means vehicle is right of center, so LEFT is corrective
# - positive heading_error_deg means vehicle points right of desired direction, so LEFT is corrective

VALID_STEERING = {"LEFT", "RIGHT", "STRAIGHT"}
VALID_SPEED = {"ACCELERATE", "SLOW", "STOP"}


# !!!!!!!!!!!!!!!CHANGE 1: GOT RID OF RETURN AT THE END AND INSTEAD RETURN AT EVERY BRANCH FOR FASTER COMPUTATION
# EFFICIENCY SO SKIPPED TIME TO CHANGE VARIABLES AND THEN RETURN, MIGHT BE NEGLIGIBLE IN ONE RUN BUT ASSUMING WE WILL
# RUN IT THOUSANDS/MILLIONS OF TIME IN A GAME THEIR SUM MIGHT BE WORTH CONSIDERING



def controller(

    # Parameters: inputs of the func
    obstacle_distance_m,
    lane_offset_m,
    heading_error_deg,
    speed_mps,
    e_stop,
    left_clear,
    right_clear,
    sensor_valid
):
    """
    Returns:
        (steering, speed_action)

        steering:
            "LEFT", "RIGHT", "STRAIGHT"

        speed_action:
            "ACCELERATE", "SLOW", "STOP"
    """

    DANGER_OBSTACLE_M = 1.0
    CAUTION_OBSTACLE_M = 2.0

    MILD_HEADING_DEG = 3.0
    LARGE_HEADING_DEG = 15.0

    MILD_OFFSET_M = 0.15
    LARGE_OFFSET_M = 0.40

    # !!!!!!!!!!!!!!!! CHANGE 4: CHANGED HIGH_SPEED TO 11 INSTEAD OF 3, AS a typical turning speed from past tournament?? is 40km/h -> roughly 11 m/s
    HIGH_SPEED_MPS = 11

    # CHANGE 8: SPEED AT WHICH WE CAN'T STOP THE CAR FROM HITTING OBSTACLE USING STOP
    CRITICAL_DAN_OBSTICAL_SPEED = 3.3

    # A boolean to see if offset is mild or not
    centered = abs(lane_offset_m) <= MILD_OFFSET_M

    # A boolean to see if heading error is mild or not
    small_heading_error = abs(heading_error_deg) <= MILD_HEADING_DEG

    steering = "STRAIGHT"
    speed_action = "ACCELERATE"

    # !!!!!!!!!!!!!!! CHANGE 2: DIDN'T NEED ANOTHER SEPARATE IF STATEMENT AT THE END FOR THE IDEAL SITUATION INSTEAD
    # IF GOES INTO ELSE IT WILL HAVE TO BE THE IDEAL SITUATION AND ALSO, PUTTING IT AT THE START DOESN'T TAKE OBSTACLES
    # DISTANCES INTO ACCOUNT SO IF THE CAR WAS CENTRED AND HAD SMALL HEADING ERROR THEN CAR COULD ACCELERATE INTO OBSTACLE

    # !!!!!!!!!!!!!!!! CHANGE 3: E-STOP IF STATEMENT SHOULD NOT HAVE A SUB-CONDI OF OBSTACLE DISTANCE <= DANGER_OBSTACLE_M
    # AS IT ACTS AS THE EMERGENCY STOP WHICH SHOULD IMMEDIATELY STOP THE CAR REGARDLESS OF ANYTHING ELSE

    # TRIVIAL CASE
    # Stops the car if sensor/other things not working or emergency stop is activated
    if not sensor_valid or e_stop:
        return "STRAIGHT", "STOP"


    # prioritise not hitting obstacles
    # ASSUMPTION!!: obstacle_distance is the distance from the centre of the front of the car
    elif obstacle_distance_m <= DANGER_OBSTACLE_M:

        # CHANGE 9: We can't avoid a crash at this speed and we would rather clip the cones on the side rather a head_on crash
        if speed_mps > 3.3:
            return "LEFT", "STOP"

        # stop if no safe side
        elif not left_clear and not right_clear:
            return "STRAIGHT", "STOP"

        # turn left if left is clear
        elif left_clear and not right_clear:
            # IN VISUALISER LARGE HEADING_DEG WAS NOT ENOUGH TO MAKE THAT TURN WITHOUT HITTING THE OBSTACLE EVEN WITH MILD OBSTACLE DISTANCE
            # LIMITATION!!!!! EVEN STOP DID NOT BRAKE THE CAR IN TIME, STILL HITS THE OBSTACLE. WILL HIT THE OBSTACLE AS LONG AS OBSTACLE DISTANCE IS <= DANGER DISTANCE AND SPEED EXCEEDS 3.3

            return "LEFT", "STOP"


            # # If car is already steered towards the left at a big angle
            # if heading_error_deg < -LARGE_HEADING_DEG:
            #     return "STRAIGHT", "SLOW"
            #
            # # if car is not pointed to the left with a relative large angle then turn left immediately
            # else:
            #     return "LEFT", "SLOW" # NEED TO DO!!!!!! MAYBE STOP INSTEAD? BUT THE CAR MIGHT FLIP OVER


        # turn right if right is clear
        elif right_clear and not left_clear:

            # IN VISUALISER LARGE HEADING_DEG WAS NOT ENOUGH TO MAKE THAT TURN WITHOUT HITTING THE OBSTACLE EVEN WITH MILD OBSTACLE DISTANCE
            # LIMITATION!!!!! EVEN STOP DID NOT BRAKE THE CAR IN TIME, STILL HITS THE OBSTACLE. WILL HIT THE OBSTACLE AS LONG AS OBSTACLE DISTANCE IS <= DANGER DISTANCE AND SPEED EXCEEDS 3.3

            return "RIGHT", "STOP"

            # # If car is already steered towards the right at a big angle
            # if heading_error_deg > LARGE_HEADING_DEG:
            #     return "STRAIGHT", "SLOW"
            #
            # # if car is not pointed to the right with a relative large angle then turn right immediately
            # else:
            #     return "RIGHT", "SLOW"# NEED TO DO!!!!!! MAYBE STOP INSTEAD? BUT THE CAR MIGHT FLIP OVER

        # if both sides clear and deviated to the right then turn left
        elif (right_clear and left_clear) and lane_offset_m > 0:

            # IN VISUALISER LARGE HEADING_DEG WAS NOT ENOUGH TO MAKE THAT TURN WITHOUT HITTING THE OBSTACLE EVEN WITH MILD OBSTACLE DISTANCE
            # LIMITATION!!!!! EVEN STOP DID NOT BRAKE THE CAR IN TIME, STILL HITS THE OBSTACLE. WILL HIT THE OBSTACLE AS LONG AS OBSTACLE DISTANCE IS <= DANGER DISTANCE AND SPEED EXCEEDS 3.3
            return "LEFT", "STOP"

            # # if car is already pointing to left with large angle, no more steering needed to prevent oversteering
            # if heading_error_deg <= -LARGE_HEADING_DEG:
            #     return "STRAIGHT", "SLOW"
            #
            # # if car is not pointed to the left with a relative large angle then turn left immediately
            # else:
            #     return "LEFT", "SLOW"


        # !!!!!!!!!!!!!!!! CHANGE 6: FOR WHEN CAR IS DANGEROUSLY/MILDLY CLOSE TO THE OBSTACLE - SEPARATED THE HEADING
        # ERROR AND OFFSET CASES AS IN THE ORIGINAL WE COULD HAVE A CASE WHERE THE CAR IS AT THE VERY LEFT EDGE BUT DIRECTED
        # TOWARDS THE RIGHT IN WHICH CASE WILL SATISFY THE heading_error_deg > MILD_HEADING_DEG CONDI AND WILL TURN EVEN MORE TO THE LEFT AND CRASH

        # if both sides clear and deviated to the left then turn right
        elif (right_clear and left_clear) and lane_offset_m < 0:

            # IN VISUALISER LARGE HEADING_DEG WAS NOT ENOUGH TO MAKE THAT TURN WITHOUT HITTING THE OBSTACLE EVEN WITH MILD OBSTACLE DISTANCE
            # LIMITATION!!!!! EVEN STOP DID NOT BRAKE THE CAR IN TIME, STILL HITS THE OBSTACLE. WILL HIT THE OBSTACLE AS LONG AS OBSTACLE DISTANCE IS <= DANGER DISTANCE AND SPEED EXCEEDS 3.3
            return "RIGHT", "STOP"

            # # if car is already pointing to right with large angle, no more steering needed to prevent oversteering
            # if heading_error_deg >= LARGE_HEADING_DEG:
            #     return "STRAIGHT", "SLOW"
            #
            # # if car is not pointed to right with large enough angle, turn right immediately
            # else:
            #     return "RIGHT", "SLOW"

        # if both sides clear & CAR IS CENTRED and POINTED to the right then turn RIGHT
        # STEERING WILL BE A LOT FASTER, GOING MORE LEFT FROM INITIALLY ALREADY POINTED TOWARDS LEFT VS GOING INITIALLY LEFT ALL THE WAY TO RIGHT WHEN WE COULD'VE WENT OFF WITH LEFT
        elif (right_clear and left_clear) and heading_error_deg > 0:

            # IN VISUALISER LARGE HEADING_DEG WAS NOT ENOUGH TO MAKE THAT TURN WITHOUT HITTING THE OBSTACLE EVEN WITH MILD OBSTACLE DISTANCE
            # LIMITATION!!!!! EVEN STOP DID NOT BRAKE THE CAR IN TIME, STILL HITS THE OBSTACLE. WILL HIT THE OBSTACLE AS LONG AS OBSTACLE DISTANCE IS <= DANGER DISTANCE AND SPEED EXCEEDS 3.3
            return "RIGHT", "STOP"

            # # if car is already pointing to left with large angle, no more steering needed to prevent oversteering
            # if heading_error_deg <= -LARGE_HEADING_DEG:
            #     return "STRAIGHT", "SLOW"
            #
            # # if car is not pointed to the left with a relative large angle then turn left immediately
            # else:
            #     return "LEFT", "SLOW"


        # if both sides clear & CAR IS CENTRED and POINTED to the left then turn LEFT
        # STEERING WILL BE A LOT FASTER, GOING MORE LEFT FROM INITIALLY ALREADY POINTED TOWARDS LEFT VS GOING INITIALLY LEFT ALL THE WAY TO RIGHT WHEN WE COULD'VE WENT OFF WITH LEFT
        elif (right_clear and left_clear) and heading_error_deg < 0:

            # IN VISUALISER LARGE HEADING_DEG WAS NOT ENOUGH TO MAKE THAT TURN WITHOUT HITTING THE OBSTACLE EVEN WITH MILD OBSTACLE DISTANCE
            # LIMITATION!!!!! EVEN STOP DID NOT BRAKE THE CAR IN TIME, STILL HITS THE OBSTACLE. WILL HIT THE OBSTACLE AS LONG AS OBSTACLE DISTANCE IS <= DANGER DISTANCE AND SPEED EXCEEDS 3.3
            return "LEFT", "STOP"

            # # if car is already pointing to right with large angle, no more steering needed to prevent oversteering
            # if heading_error_deg >= LARGE_HEADING_DEG:
            #     return "STRAIGHT", "SLOW"
            #
            # # if car is not pointed to right with large enough angle, turn right immediately
            # else:
            #     return "RIGHT", "SLOW"

        # If car is heading straight and on track AND BOTH SIDES ARE CLEAR IF IT GOES DOWN TO ELSE
        else:
            return "LEFT", "STOP"

    # take actions to steer away from obstacles early to minimise speed reduction
    elif obstacle_distance_m <= CAUTION_OBSTACLE_M:
        # slow down if no safe side - assuming sides are blocked by temporary obstacles so at least one side will clear up as car travels.
        if not left_clear and not right_clear:
            return "STRAIGHT", "SLOW"

        # turn left if left is clear
        elif left_clear and not right_clear:

            # IN VISUALISER LARGE HEADING_DEG WAS NOT ENOUGH TO MAKE THAT TURN WITHOUT HITTING THE OBSTACLE EVEN WITH MILD OBSTACLE DISTANCE
            return "LEFT", "SLOW"

            # # If car is already steered towards the left at a big angle
            # if heading_error_deg < -MILD_HEADING_DEG:
            #     return "STRAIGHT", "SLOW"
            #
            # # if car is not pointed to the left with a relative large angle then turn left immediately
            # else:
            #     return "LEFT", "SLOW"  # NEED TO DO!!!!!! MAYBE STOP INSTEAD? BUT THE CAR MIGHT FLIP OVER

        # turn right if right is clear
        elif right_clear and not left_clear:

            # IN VISUALISER LARGE HEADING_DEG WAS NOT ENOUGH TO MAKE THAT TURN WITHOUT HITTING THE OBSTACLE EVEN WITH MILD OBSTACLE DISTANCE
            return "RIGHT", "SLOW"

            # # If car is already steered towards the RIGHT at a big angle
            # if heading_error_deg > LARGE_HEADING_DEG:
            #     return "RIGHT", "SLOW" # CHANGED TO RIGHT INSTEAD OF STRAIGHT AS 18 DEGREES WAS NOT ENOUGH TO TURN INTO THE SIDE ROAD IN THE VISUALISER
            #
            # # if car is not pointed to the RIGHT with a relative large angle then turn RIGHT immediately
            # else:
            #     return "RIGHT", "SLOW"  # NEED TO DO!!!!!! MAYBE STOP INSTEAD? BUT THE CAR MIGHT FLIP OVER

        # if both sides clear and deviated to the right then turn left
        elif (right_clear and left_clear) and lane_offset_m > 0:

            # IN VISUALISER LARGE HEADING_DEG WAS NOT ENOUGH TO MAKE THAT TURN WITHOUT HITTING THE OBSTACLE EVEN WITH MILD OBSTACLE DISTANCE
            return "LEFT", "SLOW"

            # # if car is already pointing to left with large angle, no more steering needed to prevent oversteering
            # if heading_error_deg <= -LARGE_HEADING_DEG:
            #     return "STRAIGHT", "SLOW"
            #
            # # if car is not pointed to the left with a relative large angle then turn left immediately
            # else:
            #     return "LEFT", "SLOW"


        # if both sides clear and deviated to the left then turn right
        elif (right_clear and left_clear) and lane_offset_m < 0:

            # IN VISUALISER LARGE HEADING_DEG WAS NOT ENOUGH TO MAKE THAT TURN WITHOUT HITTING THE OBSTACLE EVEN WITH MILD OBSTACLE DISTANCE
            return "RIGHT", "SLOW"

            # # if car is already pointing to right with large angle, no more steering needed to prevent oversteering
            # if heading_error_deg >= LARGE_HEADING_DEG:
            #     return "STRAIGHT", "SLOW"
            #
            # # if car is not pointed to right with large enough angle, turn right immediately
            # else:
            #     return "RIGHT", "SLOW"

        # if both sides clear and POINTED to the right then turn RIGHT
        elif (right_clear and left_clear) and heading_error_deg > 0:

            # IN VISUALISER LARGE HEADING_DEG WAS NOT ENOUGH TO MAKE THAT TURN WITHOUT HITTING THE OBSTACLE EVEN WITH MILD OBSTACLE DISTANCE
            return "RIGHT", "SLOW"

            # # if car is already pointing to left with large angle, no more steering needed to prevent oversteering
            # if heading_error_deg <= -LARGE_HEADING_DEG:
            #     return "STRAIGHT", "SLOW"
            #
            # # if car is not pointed to the left with a relative large angle then turn left immediately
            # else:
            #     return "LEFT", "SLOW"


        # if both sides clear and pointed to the left then turn left
        elif (right_clear and left_clear) and heading_error_deg < 0:

            # IN VISUALISER LARGE HEADING_DEG WAS NOT ENOUGH TO MAKE THAT TURN WITHOUT HITTING THE OBSTACLE EVEN WITH MILD OBSTACLE DISTANCE
            return "LEFT", "SLOW"

            # # if car is already pointing to right with large angle, no more steering needed to prevent oversteering
            # if heading_error_deg >= LARGE_HEADING_DEG:
            #     return "STRAIGHT", "SLOW"
            #
            # # if car is not pointed to right with large enough angle, turn right immediately
            # else:
            #     return "RIGHT", "SLOW"

        # If car is heading straight and on track AND BOTH SIDES ARE CLEAR IF IT GOES DOWN TO ELSE
        else:
            return "RIGHT", "SLOW"

    # Correct car back on track by reducing lane offset
    # !!!! ASSUMPTION: no safe side means there are some form of obstacles on both sides of the car and car can't turn to either side otherwise will hit obstacle
    # !!! ASSUMPTION: there won't ever be a case where the car is largely deviated to the right but (immediate) left side is not clear as that would be the centre of the track which should be clear at all times

    # car is deviated to the right of track
    elif lane_offset_m >= LARGE_OFFSET_M:

        # obstacles are relatively far away if code goes into this branch
        # accelerate if speed is lower than the typical turning speed -> HIGH_SPEED
        if speed_mps < HIGH_SPEED_MPS:
            # if car is already pointing to left with large angle, no more steering needed to prevent oversteering
            if heading_error_deg < -LARGE_HEADING_DEG:

                # !!!!!!!!!!!!!!!! CHANGE 5: ADDED SPEED CONSIDERATION, IF SPEED IS LOWER THAN THE TYPICAL TURNING SPEED,
                # THEN WE CAN MAKE TURNS WHILE ACCELERATING TO IMPROVE PERFORMANCE WHILE THIS SEEMS ANTI-INTUITIVE IF WE
                # WERE TO RUN CONTROLLER UNDER HIGH FREQUENCY E.G. EVERY 0.1 SECOND THEN WE WOULD BE ABLE TO CATCH IT WHEN
                # IT GOES OVER TO THE OTHER SIDE AND START STEER BACK TO CENTRE THIS SPEED FEATURE ALLOWS US TO COME BACK
                # TO CENTRE AND CORRECT OUR POSITION FASTER!! THOUGH THIS IS ALL RELIED UPON THE ASSUMPTION THAT THE TURNING
                # SPEED IS 40 KM/HR (THE REASON WHY THIS CRASHES IN THE VISUALISATION WHICH IS ASSUMING 3M/S IS A HIGH SPEED)
                # MIGHT BE SLIGHTLY DIFFERENT WITH A AUTONOMOUS CAR E.G. NO DRIVER (LESS MASS) BUT COULD ALWAYS JUST CHANGE
                # THE VALUE OF THE HIGH-SPEED VAR, SO AS LONG AS WE CAN TUNE IT TO THE ACTUAL CAR IT'S WELL JUSTIFIED DECISION
                # AND WOULD OVERWEIGHT THE FAILURES IN VISUALISATION SINCE IT'S ONLY A MODEL

                return "STRAIGHT", "ACCELERATE"

            # if car is not pointed to the left with a relative large angle then turn left immediately
            else:
                return "LEFT", "ACCELERATE"

        # otherwise need to slow down for a safe turn/correct back to centre
        else:
            # if car is already pointing to left with large angle, no more steering needed to prevent oversteering
            if heading_error_deg < -LARGE_HEADING_DEG:
                return "STRAIGHT", "SLOW"

            # if car is not pointed to the left with a relative large angle then turn left immediately
            else:
                return "LEFT", "SLOW"

    # car is only deviated mildly to the right
    elif lane_offset_m > 0 and not centered:

        # obstacles are relatively far away if code goes into this branch
        # accelerate if speed is lower than the typical turning speed -> HIGH_SPEED
        if speed_mps < HIGH_SPEED_MPS:

            # if car is already pointing to left with MILD angle, no more steering needed to prevent oversteering
            if (heading_error_deg < -MILD_HEADING_DEG):
                return "STRAIGHT", "ACCELERATE"

            # if car is not pointed to the left with a relative large angle then turn left immediately
            else:
                return "LEFT", "ACCELERATE"
        # otherwise need to slow down for a safe turn/correct back to centre
        else:
            # if car is already pointing to left with MILD angle, no more steering needed to prevent oversteering
            if (heading_error_deg < -MILD_HEADING_DEG):
                return "STRAIGHT", "SLOW"

            # if car is not pointed to the left with a relative large angle then turn left immediately
            else:
                return "LEFT", "SLOW"

    # car is deviated to the very left of track
    elif lane_offset_m <= -LARGE_OFFSET_M:

        # obstacles are relatively far away if code goes into this branch
        # accelerate if speed is lower than the typical turning speed -> HIGH_SPEED
        if speed_mps < HIGH_SPEED_MPS:
            # if car is already pointing to right with large angle, no more steering needed to prevent oversteering
            if heading_error_deg >= LARGE_HEADING_DEG:
                return "STRAIGHT", "ACCELERATE"

            # if car is not pointed to the right with a relative large angle then turn right immediately
            else:
                return "RIGHT", "ACCELERATE"

        # otherwise need to slow down for a safe turn/correct back to centre
        else:
            # if car is already pointing to right with large angle, no more steering needed to prevent oversteering
            if heading_error_deg >= LARGE_HEADING_DEG:
                return "STRAIGHT", "SLOW"

            # if car is not pointed to the right with a relative large angle then turn right immediately
            else:
                return "RIGHT", "SLOW"

    # Car only mildly offseted to the left
    elif lane_offset_m < 0 and not centered:

        # obstacles are relatively far away if code goes into this branch
        # accelerate if speed is lower than the typical turning speed -> HIGH_SPEED
        if speed_mps < HIGH_SPEED_MPS:
            # if car is already pointing to RIGHT with MILD angle, no more steering needed to prevent oversteering
            if (heading_error_deg > MILD_HEADING_DEG) and (heading_error_deg > LARGE_HEADING_DEG):
                return "STRAIGHT", "ACCELERATE"

            # if car is not pointed to the RIGHT with a relative large angle then turn RIGHT immediately
            else:
                return "RIGHT", "ACCELERATE"

        # otherwise need to slow down for a safe turn/correct back to centre
        else:
            # if car is already pointing to RIGHT with MILD angle, no more steering needed to prevent oversteering
            if (heading_error_deg > MILD_HEADING_DEG) and (heading_error_deg > LARGE_HEADING_DEG):
                return "STRAIGHT", "SLOW"

            # if car is not pointed to the RIGHT with a relative large angle then turn RIGHT immediately
            else:
                return "RIGHT", "SLOW"

    # !!!! ASSUMPTION: heading error is the angle difference between the track's direction and the car's direction
    # car has large heading error but is generally on track physically

    # car is largely steered towards the right
    elif heading_error_deg > LARGE_HEADING_DEG:

        # obstacles are relatively far away if code goes into this branch
        # accelerate if speed is lower than the typical turning speed -> HIGH_SPEED
        if speed_mps < HIGH_SPEED_MPS:
            # steer left to get back to straight
            return "LEFT", "ACCELERATE"

        # otherwise need to slow down for a safe turn/correct back to centre
        else:
            # steer left to get back to straight
            return "LEFT", "SLOW"

    # car is largely steered towards the left
    elif heading_error_deg < -LARGE_HEADING_DEG:

        # obstacles are relatively far away if code goes into this branch
        # accelerate if speed is lower than the typical turning speed -> HIGH_SPEED
        if speed_mps < HIGH_SPEED_MPS:
            # steer right to get back to straight
            return "RIGHT", "ACCELERATE"

        else:
            # steer right to get back to straight
            return "RIGHT", "SLOW"

    # car is MILDLY steered towards the right
    elif not small_heading_error and heading_error_deg > 0:
        # steer left to get back to straight
        return "LEFT", "SLOW"

    # car is MILDLY steered towards the left
    elif heading_error_deg < 0 and not small_heading_error:
        # steer right to get back to straight
        return "RIGHT", "SLOW" 


    # IDEAL SITUATION
    # small/none heading errors don't need to be correct to prevent overfitting
    else:
        # neither var would be changed come down into the else branch and at the beginning it's set as straight and accelerate
        return steering,speed_action



    #













