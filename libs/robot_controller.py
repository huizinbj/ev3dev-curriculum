"""
  Library of EV3 robot functions that are useful in many different applications
  For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For
  organizational purposes try to only write methods into this library that
  are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example,
  don't make a connection to the remote control that sends the arm up if
  the ir remote control up button is pressed.
  That's a specific input --> output task.  Maybe some other task would want
  to use the IR remote up button for something different.
  Instead just make a method called arm_up that could be called.
  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import time
import math


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many
    different programs."""

    def __init__(self):
        """
        Creates motors and sensors for the Snatcher and makes sure they
        are connected.
        """
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.touch_sensor = ev3.TouchSensor()
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.running = True
        self.color_sensor = ev3.ColorSensor()
        self.ir_sensor = ev3.InfraredSensor()
        self.beacon_seeker = ev3.BeaconSeeker(channel=1)
        self.pixy = ev3.Sensor(driver_name="pixy-lego")
        self.mqtt_client = None

        self.light_level = 90
        self.light_calibrated = False
        self.dark_calibrated = False
        self.dark_level = 10

        self.obstructed = False

        self.origin_x = 240
        self.origin_y = 240
        self.current_x = 240
        self.current_y = 240
        self.last_x = 240
        self.last_y = 240

        assert self.arm_motor.connected
        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.touch_sensor.connected
        assert self.color_sensor.connected
        assert self.ir_sensor.connected
        # assert self.pixy.connected

    def set_mqtt_client(self, mqtt_client):
        """
       Creates the mqtt client variable for the ev3
       """
        self.mqtt_client = mqtt_client

    def drive_inches(self, inches, speed):
        """
        Drives motors the given inches and the given speed
        """
        print(inches)
        pos = inches * 90
        self.left_motor.run_to_rel_pos(position_sp=pos, speed_sp=-speed,
                                       stop_action="brake")
        self.right_motor.run_to_rel_pos(position_sp=pos, speed_sp=-speed,
                                        stop_action="brake")
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        """Drives motors at the same given speed, but in opposite
        directions, to turn the robot the given degrees"""
        pos = degrees_to_turn * 4.5
        self.left_motor.run_to_rel_pos(position_sp=-pos,
                                       speed_sp=turn_speed_sp,
                                       stop_action="brake")
        self.right_motor.run_to_rel_pos(position_sp=pos,
                                        speed_sp=turn_speed_sp,
                                        stop_action="brake")
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def arm_calibration(self):
        """
        Calibrates the Snatcher arm sending it upwards and downwards and
        sets the arm_motor.position to 0.
        :return:
        """
        self.arm_motor.run_forever(speed_sp=900)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action='brake')
        ev3.Sound.beep()
        arm_revolutions_for_full_range = 14.2
        self.arm_motor.run_to_rel_pos(
            position_sp=-arm_revolutions_for_full_range*360, speed_sp=900)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep()

        self.arm_motor.position = 0

    def arm_up(self):
        """
        Sends the Snatcher arm to the upward position.
        :return:
        """
        self.arm_motor.run_forever(speed_sp=900)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action='brake')

    def arm_down(self):
        """
        Sends the Snatcher arm to the downward position.
        """
        self.arm_motor.run_to_abs_pos(
            position_sp=0, speed_sp=900)
        self.arm_motor.wait_while(
            ev3.Motor.STATE_RUNNING)

    def shutdown(self):
        """
       Shuts down the Snatcher by killing all motors, turning off the Led's
       printing "Goodbye" and sets self.running to False to kill an mqtt
       client.
       :return self.running False
       """
        self.running = False
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        self.arm_motor.stop(stop_action='brake')
        self.left_motor.stop(stop_action='brake')
        self.right_motor.stop(stop_action='brake')
        print('Goodbye')
        ev3.Sound.speak('Goodbye')

    def loop_forever(self):
        """
        Used for mqtt clients  within the Snatcher to make the robot
        constantly send and receive data.
        :return: self.running
        """
        self.running = True
        while self.running:
            time.sleep(0.1)

    def stop(self):
        """
        Stops the Snatchers motors to cease them from moving.
        """
        self.left_motor.stop(stop_action='brake')
        self.right_motor.stop(stop_action='brake')
        ev3.Sound.speak("Stopping")

    def drive_forward(self, leftspeed, rightspeed):
        """
        Drives the Snatcher forward at the given input speeds.
        Can also be use for turning if one speed is greater than the other.
        """
        self.left_motor.run_forever(speed_sp=leftspeed)
        self.right_motor.run_forever(speed_sp=rightspeed)

    def seek_beacon(self):
        """
        Uses the IR Sensor in BeaconSeeker mode to find the beacon.
        If the beacon is found this return True.
        If the beacon is not found and the attempt is cancelled by hitting
        the touch sensor, return False.
        """
        forward_speed = 300
        turn_speed = 100
        while not self.touch_sensor.is_pressed:
            current_heading = self.beacon_seeker.heading
            current_distance = self.beacon_seeker.distance
            if current_distance == -128:
                print("IR Remote not found. Distance is -128")
                self.stop()
            else:
                if math.fabs(current_heading) < 2:
                    print("On the right heading. Distance: ", current_distance)
                    if current_distance < 10:
                        print("Driving forward to beacon")
                        self.drive_forward(forward_speed, forward_speed)
                        time.sleep(0.01)

                    if math.fabs(current_distance) <= 1:
                        self.stop()
                        time.sleep(0.1)
                        print("Found Beacon", current_distance)
                        self.drive_inches(4, 200)
                        return True
                if math.fabs(current_heading) > 2 and math.fabs(
                        current_heading) \
                        < 10:
                    print("Robot Needs to turn")
                    if current_heading < 1:
                        print("Turn left")
                        print(current_heading, "left")
                        self.drive_forward(-turn_speed, turn_speed)
                        time.sleep(0.01)
                    if current_heading > 1:
                        print("Turn Right")
                        print(current_heading, "right")
                        self.drive_forward(turn_speed, -turn_speed)
                        time.sleep(0.01)
                    time.sleep(0.01)
                if math.fabs(current_heading) > 10:
                    self.stop()
                    print(current_heading)
                    print("Heading to far off")
            time.sleep(0.02)
        print("Abandon ship!")
        self.stop()
        return False

    def calibrate_light(self):
        """Calibrates the Color Sensor's upper bound for line-following"""
        ev3.Sound.speak("Calibrate Light Color")
        time.sleep(0.05)
        self.light_level = self.color_sensor.reflected_light_intensity
        self.light_calibrated = True

    def calibrate_dark(self):
        """Calibrates the Color Sensor's lower bound for line-following"""
        ev3.Sound.speak("Calibrate Dark Color")
        time.sleep(0.05)
        self.dark_level = self.color_sensor.reflected_light_intensity
        self.dark_calibrated = True

    def wave_hello(self, n):
        """Uses the arm motor's up/down to 'wave' hello n times"""
        self.stop()
        ev3.Sound.speak("Hello")
        for k in range(n):
            self.arm_up()
            time.sleep(0.1)
            self.arm_down()
            time.sleep(0.1)

    def flex(self, n):
        """Uses the arm motor to open/close the claw n times"""
        self.stop()
        ev3.Sound.speak("Flex")
        for k in range(n):
            self.arm_motor.run_to_rel_pos(position_sp=5*360, speed_sp=900)
            self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
            self.arm_motor.run_to_rel_pos(position_sp=-5*360, speed_sp=900)
            self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def return_start(self):
        """Utilizes the turn_degrees and drive_inches to return to the point
        where the robot started, which is tracked in the use of those
        functions via the instance variables self.x, self.y,
        and self.degrees_turned"""
        ev3.Sound.speak("Going Home")
        # TODO: Implement a function to return the robot to the start
        # Note: Need to have some instance variables in movement methods
        # above so that return_start can do some math with them and "backtrack"
        # to the start

    def line_follow(self):
        """Continuously checks if the robot's dark and light values are
        calibrated correctly, and if so, follows a line of the dark color
        indefinitely, recalibrating the dark color as it follows the line so a
        line of changing color can still be followed. The light color must
        remain constant for this to function properly."""
        while True:
            if not self.light_calibrated or not self.dark_calibrated:
                break
            if self.touch_sensor.is_pressed:
                self.stop()
                break
            elif self.ir_sensor.proximity < 10:
                ev3.Sound.speak("Obstruction")
                self.obstructed = True
                self.mqtt_client.send_message("obstructed")
                self.stop()
                break
            if self.color_sensor.reflected_light_intensity < self.dark_level \
                    + 10:
                self.drive_forward(300, 300)
            else:
                self.turn_degrees(10, 300)
                time.sleep(0.1)
                self.dark_level = self.color_sensor.reflected_light_intensity

    def wrong_input(self):
        """In the case of an incorrect command entry, gives audio cue of the
        error"""
        ev3.Sound.speak("Bad Command")

    def move_obstruction(self):
        self.drive_forward(100, 100)
        if self.ir_sensor.proximity < 3:
            self.stop()
            self.arm_up()
            self.turn_degrees(90, 300)
            self.drive_inches(10, 300)
            self.arm_down()
            self.drive_inches(-10, 300)
            self.turn_degrees(-90, 300)

    def go_around(self):
        self.turn_degrees(90, 300)
        self.drive_inches(10, 300)
        self.turn_degrees(-90, 300)
        self.drive_inches(5, 300)
        self.turn_degrees(-90, 300)
        self.drive_inches(10, 300)

    def drive_to_waypoint(self, x, y, speed):
        """
        Drives motors the waypoint received by a canvas click. It determines
        where to drive by calculating the difference and converting it to
        inches to drive forward and when to turn.
        """
        if self.current_y > y:
            self.last_y = self.current_y
            print("Drive Forward")
            print("I was at:", self.current_x, self.current_y)
            drive_y_axis = self.current_y - y
            inches_to_drive_y = drive_y_axis/10
            print("I have to drive:", inches_to_drive_y)
            self.drive_inches_botwards(inches_to_drive_y, speed)
            print("Now Im here:", self.current_x, self.current_y)
            self.current_y = y

        elif self.current_y < y:
            self.last_y = self.current_y
            print("Drive Backward")
            drive_y_axis = y - self.current_y
            inches_to_drive_y = drive_y_axis/10
            print("Conversion", inches_to_drive_y)
            self.drive_inches_bot(inches_to_drive_y, -speed)
            self.current_y = y

        while self.left_motor.state and self.right_motor.state:
            time.sleep(0.01)

        if self.current_x > x:
            self.last_x = self.current_x
            self.turn_degrees(90, speed)
            drive_x_axis = self.current_x - x
            inches_to_drive_x = drive_x_axis / 10
            self.drive_inches(inches_to_drive_x, speed)
            self.turn_degrees(-90, speed)
            self.current_x = x

        elif self.current_x < x:
            self.last_x = self.current_x
            self.turn_degrees(-90, speed)
            drive_x_axis = x - self.current_x
            inches_to_drive_x = drive_x_axis / 10
            self.drive_inches(inches_to_drive_x, speed)
            self.turn_degrees(90, speed)
            self.current_x = x


    def drive_inches_botwards(self, inches, speed):
        """
        Drives motors the given inches and the given speed backwards
        """
        print(inches)
        pos = inches * 90
        self.left_motor.run_to_rel_pos(position_sp=pos, speed_sp=speed,
                                       stop_action="brake")
        self.right_motor.run_to_rel_pos(position_sp=pos, speed_sp=speed,
                                        stop_action="brake")

    def drive_inches_bot(self, inches, speed):
        """
        Drives motors the given inches and the given speed Forwards
        """
        print(inches)
        pos = inches * 90
        self.left_motor.run_to_rel_pos(position_sp=-pos, speed_sp=speed,
                                       stop_action="brake")
        self.right_motor.run_to_rel_pos(position_sp=-pos, speed_sp=speed,
                                        stop_action="brake")

    def reset_xy(self):
        """
        Resets the bots Coordinates manually to (240,240) Used for testing
        purposes.
        """
        self.current_y = 240
        self.current_x = 240

    def return_bot_origin(self):
        """
        Method used to make the robot return to its original position when it
        was created.
        """
        self.drive_to_waypoint(self.origin_x, self.origin_y, 300)
