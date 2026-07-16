#include <deque>
#include <memory>
#include <mutex>
#include <string>

#include "cv_bridge/cv_bridge.h"
#include "image_transport/image_transport.hpp"
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/image.hpp"
#include "std_msgs/msg/header.hpp"
#include "std_srvs/srv/trigger.hpp"

#include "pano_stitch_ros2/stitcher.hpp"

using std::placeholders::_1;
using std::placeholders::_2;

// Subscribes to a single ZED2 image topic (e.g. the rectified left color
// image) and keeps a rolling buffer of the most recent frames. On a call
// to the "~/stitch" service, it stitches whatever is currently in the
// buffer into one panorama and publishes it on "~/panorama". This assumes
// the rover is panning/rotating while frames accumulate in the buffer
// (e.g. an operator calls "~/clear_buffer", pans the camera, then calls
// "~/stitch" once enough overlapping frames have been collected).
class PanoStitchNode : public rclcpp::Node {
public:
  PanoStitchNode() : Node("pano_stitch_node") {
    image_topic_ = this->declare_parameter<std::string>(
        "image_topic", "/zed2/zed_node/left/image_rect_color");
    max_buffer_size_ = this->declare_parameter<int>("max_buffer_size", 8);

    image_sub_ = image_transport::create_subscription(
        this, image_topic_,
        std::bind(&PanoStitchNode::imageCallback, this, _1), "raw");

    pano_pub_ = image_transport::create_publisher(this, "~/panorama");

    stitch_service_ = this->create_service<std_srvs::srv::Trigger>(
        "~/stitch", std::bind(&PanoStitchNode::handleStitch, this, _1, _2));

    clear_service_ = this->create_service<std_srvs::srv::Trigger>(
        "~/clear_buffer", std::bind(&PanoStitchNode::handleClear, this, _1, _2));

    RCLCPP_INFO(
        this->get_logger(),
        "pano_stitch_node ready. Subscribed to '%s', buffering up to %d frames. "
        "Call '~/stitch' to generate a panorama from the current buffer, "
        "'~/clear_buffer' to reset it.",
        image_topic_.c_str(), max_buffer_size_);
  }

private:
  void imageCallback(const sensor_msgs::msg::Image::ConstSharedPtr& msg) {
    cv_bridge::CvImageConstPtr cv_ptr;
    try {
      cv_ptr = cv_bridge::toCvShare(msg, "bgr8");
    } catch (const cv_bridge::Exception& e) {
      RCLCPP_WARN(this->get_logger(), "cv_bridge conversion failed: %s", e.what());
      return;
    }

    std::lock_guard<std::mutex> lock(buffer_mutex_);
    buffer_.push_back(cv_ptr->image.clone());
    if (static_cast<int>(buffer_.size()) > max_buffer_size_) {
      buffer_.pop_front();
    }
  }

  void handleStitch(
      const std::shared_ptr<std_srvs::srv::Trigger::Request> /*request*/,
      std::shared_ptr<std_srvs::srv::Trigger::Response> response) {
    std::vector<cv::Mat> frames;
    {
      std::lock_guard<std::mutex> lock(buffer_mutex_);
      frames.assign(buffer_.begin(), buffer_.end());
    }

    if (frames.size() < 2) {
      response->success = false;
      response->message =
          "Need at least 2 buffered frames to stitch (have " +
          std::to_string(frames.size()) + ").";
      return;
    }

    cv::Mat panorama = stitcher_.stitch(frames);

    if (panorama.empty()) {
      response->success = false;
      response->message =
          "Stitching failed: insufficient feature matches or a pairwise "
          "homography did not meet the inlier threshold. Try panning more "
          "slowly for greater frame overlap.";
      return;
    }

    std_msgs::msg::Header header;
    header.stamp = this->now();
    header.frame_id = "panorama";
    auto out_msg = cv_bridge::CvImage(header, "bgr8", panorama).toImageMsg();
    pano_pub_.publish(out_msg);

    response->success = true;
    response->message =
        "Published panorama (" + std::to_string(panorama.cols) + "x" +
        std::to_string(panorama.rows) + ") from " +
        std::to_string(frames.size()) + " frames on '~/panorama'.";
  }

  void handleClear(
      const std::shared_ptr<std_srvs::srv::Trigger::Request> /*request*/,
      std::shared_ptr<std_srvs::srv::Trigger::Response> response) {
    std::lock_guard<std::mutex> lock(buffer_mutex_);
    buffer_.clear();
    response->success = true;
    response->message = "Buffer cleared.";
  }

  std::string image_topic_;
  int max_buffer_size_;

  std::deque<cv::Mat> buffer_;
  std::mutex buffer_mutex_;

  pano_stitch::PanoStitcher stitcher_;

  image_transport::Subscriber image_sub_;
  image_transport::Publisher pano_pub_;
  rclcpp::Service<std_srvs::srv::Trigger>::SharedPtr stitch_service_;
  rclcpp::Service<std_srvs::srv::Trigger>::SharedPtr clear_service_;
};

int main(int argc, char** argv) {
  rclcpp::init(argc, argv);
  auto node = std::make_shared<PanoStitchNode>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
