import rclpy
from rclpy.node import Node
from rclpy.time import Duration

from cfe_msgs.msg import SimpleRobotAppFlightCmdt, SimpleRobotAppFlightTlmt, SimpleRobotAppJointConfigt

class ReceiveCmdSendTlm(Node):
    """
    Send motion command
    """
    def __init__(self):
        super().__init__('receive_cmd_send_tlm')
        self._publish_tlm = self.create_publisher(SimpleRobotAppFlightTlmt, "/flightsystem/simple_robot_app_flight_tlm", 10)
        self._subscribe_cmd = self.create_subscription(SimpleRobotAppFlightCmdt, "/flightsystem/simple_robot_app_flight_cmd", self.cmd_cb, 10)
        self.create_timer(0.2, self.timer_update)
        self._jg = SimpleRobotAppJointConfigt()
        self._js = SimpleRobotAppJointConfigt()    
        
    def timer_update(self):
        
      # Update telemetry with error reduction if needed
      errors = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0];
      errors[0] = self._jg.shoulder_pan_joint - self._js.shoulder_pan_joint;
      errors[1] = self._jg.shoulder_lift_joint - self._js.shoulder_lift_joint;
      errors[2] = self._jg.elbow_joint - self._js.elbow_joint;
      errors[3] = self._jg.wrist_1_joint - self._js.wrist_1_joint;
      errors[4] = self._jg.wrist_2_joint - self._js.wrist_2_joint;
      errors[5] = self._jg.wrist_3_joint - self._js.wrist_3_joint;

      # Update state (telemetry) stored. It will be sent back to a lower rate
      Kp = 0.01;
      self._js.shoulder_pan_joint += + Kp * errors[0];
      self._js.shoulder_lift_joint += + Kp * errors[1];    
      self._js.elbow_joint += Kp * errors[2];    
      self._js.wrist_1_joint += Kp * errors[3];        
      self._js.wrist_2_joint += Kp * errors[4];
      self._js.wrist_3_joint += Kp * errors[5];
           
      # Send back js
      tlm = SimpleRobotAppFlightTlmt()
      #tlm.cmd_header.sec.function_code = 1 # CC code. 1 = Command. 0 = Noop
      tlm.joint_state = self._js
        
      self._publish_tlm.publish(tlm)
                            
                    
    def cmd_cb(self, msg):
        self.get_logger().info("Getting command!!!")
        self._jg =  msg.joint_goal

        
#########################
def main(args=None):

    rclpy.init(args=args) 
    test_node = ReceiveCmdSendTlm()
    
    # Spin and receive telemetry data 
    rclpy.spin(test_node)
    
if __name__ == '__main__':
    main()
