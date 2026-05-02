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

    HIGH_SPEED_MPS = 3.0

    # A boolean to see if offset is mild or not
    centered = abs(lane_offset_m) <= MILD_OFFSET_M

    # A boolean to see if heading error is mild or not
    small_heading_error = abs(heading_error_deg) <= MILD_HEADING_DEG

    steering = "STRAIGHT"
    speed_action = "ACCELERATE"

    # TRIVIAL CASE
    # Stops the car if sensor/other things not working or emergency stop is activated
    if not sensor_valid or e_stop:
        return "STRAIGHT", "STOP"

    #NEED TO DO????? stop instead of turning at high speeds to prevent car from flipping sideways.
    # prioritise not hitting obstacles
    # ASSUMPTION!!: obstacle_distance is the distance from the centre of the front of the car
    elif obstacle_distance_m <= DANGER_OBSTACLE_M:

        # stop if no safe side
        if not left_clear and not right_clear:
            return "STRAIGHT", "STOP"

        # turn left if left is clear
        elif left_clear and not right_clear:
            return "LEFT", "SLOW" # NEED TO DO!!!!!! MAYBE STOP INSTEAD? BUT THE CAR MIGHT FLIP OVER


        # turn right if right is clear
        elif right_clear and not left_clear:
            return "RIGHT", "SLOW"# NEED TO DO!!!!!! MAYBE STOP INSTEAD? BUT THE CAR MIGHT FLIP OVER

        # if both sides clear and deviated to the right then turn left
        elif (right_clear and left_clear) and lane_offset_m > 0:

            # if car is already pointing to left with large angle, no more steering needed to prevent oversteering
            if heading_error_deg <= -LARGE_HEADING_DEG:
                return "STRAIGHT", "SLOW"

            # if car is not pointed to the left with a relative large angle then turn left immediately
            else:
                return "LEFT", "SLOW"


        # if both sides clear and deviated to the left then turn right
        elif (right_clear and left_clear) and lane_offset_m < 0:

            # if car is already pointing to right with large angle, no more steering needed to prevent oversteering
            if heading_error_deg >= LARGE_HEADING_DEG:
                return "STRAIGHT", "SLOW"

            # if car is not pointed to right with large enough angle, turn right immediately
            else:
                return "RIGHT", "SLOW"

        # If car is heading straight and on track AND BOTH SIDES ARE CLEAR IF IT GOES DOWN TO ELSE
        else:
            return "RIGHT", "SLOW" # NEED TO DO!!!!!!! HERE JUST PICKED A RANDOM DIRECTION TO TURN INSTEAD OF STOPPING CONSIDERING THE CAR IS STILL RACING SO WOULD WANT TO MAINTAIN THE SPEED IF POSSIBLE

    # take actions to steer away from obstacles early to minimise speed reduction
    elif obstacle_distance_m <= CAUTION_OBSTACLE_M:
        # slow down if no safe side - assuming sides are blocked by temporary obstacles so at least one side will clear up as car travels.
        if not left_clear and not right_clear:
            return "STRAIGHT", "SLOW"

        # turn left if left is clear
        elif left_clear and not right_clear:
            return "LEFT", "SLOW"  # NEED TO DO!!!!!! MAYBE STOP INSTEAD? BUT THE CAR MIGHT FLIP OVER

        # turn right if right is clear
        elif right_clear and not left_clear:
            return "RIGHT", "SLOW"  # NEED TO DO!!!!!! MAYBE STOP INSTEAD? BUT THE CAR MIGHT FLIP OVER

        # if both sides clear and deviated to the right then turn left
        elif (right_clear and left_clear) and lane_offset_m > 0:

            # if car is already pointing to left with large angle, no more steering needed to prevent oversteering
            if heading_error_deg <= -LARGE_HEADING_DEG:
                return "STRAIGHT", "SLOW"

            # if car is not pointed to the left with a relative large angle then turn left immediately
            else:
                return "LEFT", "SLOW"


        # if both sides clear and deviated to the left then turn right
        elif (right_clear and left_clear) and lane_offset_m < 0:

            # if car is already pointing to right with large angle, no more steering needed to prevent oversteering
            if heading_error_deg >= LARGE_HEADING_DEG:
                return "STRAIGHT", "SLOW"

            # if car is not pointed to right with large enough angle, turn right immediately
            else:
                return "RIGHT", "SLOW"

        # If car is heading straight and on track AND BOTH SIDES ARE CLEAR IF IT GOES DOWN TO ELSE
        else:
            return "RIGHT", "SLOW"  # NEED TO DO!!!!!!! HERE JUST PICKED A RANDOM DIRECTION TO TURN INSTEAD OF STOPPING CONSIDERING THE CAR IS STILL RACING SO WOULD WANT TO MAINTAIN THE SPEED IF POSSIBLE

    # Correct car back on track by reducing lane offset
    # !!!! ASSUMPTION: no safe side means there are some form of obstacles on both sides of the car and car can't turn to either side otherwise will hit obstacle
    # !!! ASSUMPTION: there won't ever be a case where the car is largely deviated to the right but (immediate) left side is not clear as that would be the centre of the track which should be clear at all times

    # car is deviated to the right of track
    elif lane_offset_m >= LARGE_OFFSET_M:
        # if car is already pointing to left with large angle, no more steering needed to prevent oversteering
        if heading_error_deg < -LARGE_HEADING_DEG:
            return "STRAIGHT", "SLOW"

        # if car is not pointed to the left with a relative large angle then turn left immediately
        else:
            return "LEFT", "SLOW"

    # car is only deviated mildly to the right
    elif lane_offset_m >= MILD_OFFSET_M:
        # if car is already pointing to left with MILD angle, no more steering needed to prevent oversteering
        if (heading_error_deg < -MILD_HEADING_DEG) and (heading_error_deg > -LARGE_HEADING_DEG):
            return "STRAIGHT", "SLOW" #!!!!! NEED TO DO no speed command instead to maintain speed since it's going straight anyways?

        # if car is not pointed to the left with a relative large angle then turn left immediately
        else:
            return "LEFT", "SLOW"

    # car is deviated to the very left of track
    elif lane_offset_m <= -LARGE_OFFSET_M:
        # if car is already pointing to right with large angle, no more steering needed to prevent oversteering
        if heading_error_deg >= LARGE_HEADING_DEG:
            return "STRAIGHT", "SLOW"

        # if car is not pointed to the right with a relative large angle then turn right immediately
        else:
            return "RIGHT", "SLOW"

    # Car only mildly offseted to the left
    elif lane_offset_m <= -MILD_OFFSET_M:
        # if car is already pointing to RIGHT with MILD angle, no more steering needed to prevent oversteering
        if (heading_error_deg > MILD_HEADING_DEG) and (heading_error_deg > LARGE_HEADING_DEG):
            return "STRAIGHT", "SLOW"  # !!!!! NEED TO DO no speed command instead to maintain speed since it's going straight anyways?

        # if car is not pointed to the RIGHT with a relative large angle then turn RIGHT immediately
        else:
            return "RIGHT", "SLOW"

    # !!!! ASSUMPTION: heading error is the angle difference between the track's direction and the car's direction
    # car has large heading error but is generally on track physically

    # car is largely steered towards the right
    elif heading_error_deg > LARGE_HEADING_DEG:
        # steer left to get back to straight
        return "LEFT", "SLOW"

    # car is largely steered towards the left
    elif heading_error_deg < -LARGE_HEADING_DEG:
        # steer right to get back to straight
        return "RIGHT", "SLOW"

    # car is MILDLY steered towards the right
    elif heading_error_deg > MILD_HEADING_DEG:
        # steer left to get back to straight
        return "LEFT", "SLOW" #!!!!! NEED TO DO HEADING ERROR IS ONLY MILD STEER LEFT NEEDED???

    # car is MILDLY steered towards the left
    elif heading_error_deg < -MILD_HEADING_DEG:
        # steer right to get back to straight
        return "RIGHT", "SLOW" #!!!!! NEED TO DO HEADING ERROR IS ONLY MILD STEER LEFT NEEDED???


    # IDEAL SITUATION
    # small/none heading errors don't need to be correct to prevent overfitting
    else:
        # neither var would be changed come down into the else branch and at the beginning it's set as straight and accelerate
        return steering,speed_action


    # # At high speeds
    # elif speed_mps >= HIGH_SPEED_MPS:
    #
    #     # Car severely deviates to the RIGHT
    #     if heading_error_deg > LARGE_HEADING_DEG or lane_offset_m > LARGE_OFFSET_M:
    #         steering = "LEFT"
    #         speed_action = "SLOW"
    #
    #     # Car severely deviates to the LEFT
    #     elif heading_error_deg < -LARGE_HEADING_DEG or lane_offset_m < -LARGE_OFFSET_M:
    #         steering = "RIGHT"
    #         speed_action = "SLOW"
    #
    #     #??????? appropriate to all other remaining cases????
    #     else:
    #         steering = "STRAIGHT"
    #         speed_action = "SLOW"
    #
    # # IDEAL SITUATION
    # # small/none heading errors don't need to be correct to prevent overfitting
    # if centered and small_heading_error:
    #     steering = "STRAIGHT"
    #     speed_action = "ACCELERATE"
    #
    # return steering, speed_action
