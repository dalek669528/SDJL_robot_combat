import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Pose2D

class Move(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.theta = 0
        
        self.node_name = rospy.get_name()
        rospy.loginfo("[%s] Initializing..." %(self.node_name))
    
        # Subscribers
        self.GetPos = rospy.Subscriber('position',Pose2D, self.GetPos_callback, queue_size=1)

        # Publishers
        self.pub_msg = rospy.Publisher('motor_cmd', String, queue_size=1)
    
    def GetPos_callback(self, data):
        self.x = data.x;
        self.y = data.y;
        self.theta = data.theta;
    
    def Move2Pos(self,data):
        cmd= "4 " + str(data.x) + " "  + str(data.y) + " " + str(data.theta)
        self.pub_msg.publish(cmd)
        
    def Move2PosX(self,data):
        cmd= "4 " + str(data) + " "  + str(0) + " " + str(0)
        self.pub_msg.publish(cmd)
        
    def Move2PosY(self,data):
        cmd= "4 " + str(0) + " "  + str(data) + " " + str(0)
        self.pub_msg.publish(cmd)
    
    def Move2Pos1(self):
        self.Move2PosY(80)
    
    def Move2Pos2(self,flag):
        self.Move2PosX(50)
        if(flag):
            self.Move2PosY(55)
        else:
            self.Move2PosY(70)
    
    def Move2Pos3(self,flag):
        self.Move2PosX(-50)
        if(flag):
            self.Move2PosY(55)
        else:
            self.Move2PosY(70)
            
    def Move2Pos4(self,flag):
        self.Move2PosX(50)
        if(flag):
            self.Move2PosY(100)
        else:
            self.Move2PosY(115)
        self.Move2PosX(-50)
    
if __name__ == '__main__':
    rospy.init_node("Move",anonymous=False)
    move = Move()
    flag = True
    print('run')
    move.Move2Pos1()
    while(move.y<80): 
        print(move.y)
    move.Move2Pos2(flag)
    move.Move2Pos3(flag)
    move.Move2Pos4(flag)
    
