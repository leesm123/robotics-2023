using namespace std::chrono_literals;

class SelfDrive : public rclcpp::Node
{
  rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr scan_sub_;
  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr pose_pub_;
  int step_;

public:
  SelfDrive() : rclcpp::Node("self_drive"), step_(0)
  {
    auto lidar_qos_profile = rclcpp::QoS(rclcpp::KeepLast(1));
    lidar_qos_profile.reliability(rclcpp::ReliabilityPolicy::BestEffort);
    auto callback = std::bind(&SelfDrive::subscribe_scan, this, std::placeholders::_1);
    scan_sub_ = this->create_subscription<sensor_msgs::msg::LaserScan>("/scan", lidar_qos_profile,
                                                                       callback);
    auto vel_qos_profile = rclcpp::QoS(rclcpp::KeepLast(1));
    pose_pub_ = this->create_publisher<geometry_msgs::msg::Twist>("/cmd_vel", vel_qos_profile);
  }

  void subscribe_scan(const sensor_msgs::msg::LaserScan::SharedPtr scan)
   {
    geometry_msgs::msg::Twist vel;
    // 벽과의 거리가 25cm 이하이면 정지 (근접 후 회피)
    if (scan->ranges[0] < 0.25)
    {
      vel.linear.x = 0.0;
      vel.angular.z = -1.57; // 좌회전하여 회피
    }   
    else
    {
      // 벽을 따라 이동
      vel.linear.x = 0.15;
      vel.angular.z = 0.0;
   
      
   if (scan->ranges[90] < 0.25)
   {
   vel.linear.x = 0.0;
   vel.angular.z = -1.57;
   }
       }
   
    
   }

 
};
