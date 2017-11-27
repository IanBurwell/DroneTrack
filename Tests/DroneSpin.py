from DroneHelpers import *
import argparse
import buttonstart


# Set up option parsing to get connection string
parser = argparse.ArgumentParser(
    description='Print out vehicle state information. Connects to SITL on local PC by default.')
parser.add_argument('--connect',
                    help="vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None

# Start SITL if no connection string specified
if not connection_string:
    import dronekit_sitl

    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()

# Connect to the Vehicle.
#   Set `wait_ready=True` to ensure default attributes are populated before `connect()` returns.
print "\nConnecting to vehicle on: %s" % connection_string
vehicle = connect(connection_string, wait_ready=True, baud=921600)

vehicle.wait_ready('autopilot_version')

pause = False

print 'vehicle ready'
buttonstart.wait_go_button()


# safety precaustions
def ch6_change(self, attr_name, channels):
    value = channels['6']
    # print 'channel changed ',value,' ',channels
    if value > 1750:
        print 'Aborting and landing'
        vehicle.mode = VehicleMode('LAND')
        print "Close vehicle object"
        vehicle.close()
        # Shut down simulator if it was started.
        if sitl is not None:
            sitl.stop()
        sys.exit(1)
    elif value > 1100:
        print 'paused'
        pause = True
    else:
        pause = False


vehicle.add_attribute_listener("channels", ch6_change)

arm_and_takeoff(vehicle, 4)
time.sleep(4)

print "Set groundspeed to 2m/s (max)."
vehicle.groundspeed = 2
print "Position South 0 East 0"
goto(vehicle, 0, 0, goto_position_target_global_int)

print 'Turning'
condition_yaw(vehicle, 540, True)
time.sleep(4)

print 'landing'
vehicle.mode = VehicleMode('LAND')

print 'done'
