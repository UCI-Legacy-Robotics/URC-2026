#include <cstring>
#include <memory>
#include <string>

#include <linux/can.h>
#include <linux/can/raw.h>
#include <net/if.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <unistd.h>

#include "rclcpp/rclcpp.hpp"
#include "spectro_sensor/srv/get_spectro_data.hpp"

using GetSpectroData = spectro_sensor::srv::GetSpectroData;

static constexpr const char *CAN_INTERFACE = "can0";
static constexpr canid_t REQUEST_ID = 0x4C8;   // Pi -> ESP32
static constexpr canid_t RESPONSE_ID = 0x028;  // ESP32 -> Pi

class SpectroSensorNode : public rclcpp::Node {
public:
    SpectroSensorNode() : Node("spectro_sensor_node") {
        can_fd_ = open_can_socket(CAN_INTERFACE);

        if (can_fd_ < 0) {
            RCLCPP_ERROR(this->get_logger(), "Failed to open CAN interface can0");
        } else {
            RCLCPP_INFO(this->get_logger(), "Opened CAN interface can0");
        }

        service_ = this->create_service<GetSpectroData>(
            "get_spectro_data",
            std::bind(
                &SpectroSensorNode::handle_request,
                this,
                std::placeholders::_1,
                std::placeholders::_2
            )
        );

        RCLCPP_INFO(this->get_logger(), "Spectro Sensor Service Ready");
    }

    ~SpectroSensorNode() {
        if (can_fd_ >= 0) {
            close(can_fd_);
        }
    }

private:
    int can_fd_ = -1;
    rclcpp::Service<GetSpectroData>::SharedPtr service_;

    int open_can_socket(const std::string &interface_name) {
        int fd = socket(PF_CAN, SOCK_RAW, CAN_RAW);
        if (fd < 0) {
            return -1;
        }

        struct ifreq ifr;
        std::memset(&ifr, 0, sizeof(ifr));
        std::strncpy(ifr.ifr_name, interface_name.c_str(), IFNAMSIZ - 1);

        if (ioctl(fd, SIOCGIFINDEX, &ifr) < 0) {
            close(fd);
            return -1;
        }

        struct sockaddr_can addr;
        std::memset(&addr, 0, sizeof(addr));
        addr.can_family = AF_CAN;
        addr.can_ifindex = ifr.ifr_ifindex;

        if (bind(fd, reinterpret_cast<struct sockaddr *>(&addr), sizeof(addr)) < 0) {
            close(fd);
            return -1;
        }

        struct timeval timeout;
        timeout.tv_sec = 8;
        timeout.tv_usec = 0;

        if (setsockopt(fd, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof(timeout)) < 0) {
            close(fd);
            return -1;
        }

        return fd;
    }

    bool send_can_request() {
        if (can_fd_ < 0) {
            RCLCPP_ERROR(this->get_logger(), "CAN socket is not open");
            return false;
        }

        struct can_frame frame;
        std::memset(&frame, 0, sizeof(frame));

        frame.can_id = REQUEST_ID;
        frame.can_dlc = 0;   // Empty request frame

        int bytes_written = write(can_fd_, &frame, sizeof(frame));

        if (bytes_written != static_cast<int>(sizeof(frame))) {
            RCLCPP_ERROR(this->get_logger(), "Failed to send CAN request");
            return false;
        }

        RCLCPP_INFO(this->get_logger(), "Sent CAN request to spectrophotometer");
        return true;
    }

    bool wait_for_can_response(float &voltage, float &absorbance) {
        if (can_fd_ < 0) {
            RCLCPP_ERROR(this->get_logger(), "CAN socket is not open");
            return false;
        }

        while (rclcpp::ok()) {
            struct can_frame frame;
            int bytes_read = read(can_fd_, &frame, sizeof(frame));

            if (bytes_read < 0) {
                RCLCPP_ERROR(this->get_logger(), "Timed out waiting for CAN response");
                return false;
            }

            if (bytes_read < static_cast<int>(sizeof(struct can_frame))) {
                continue;
            }

            if (frame.can_id == RESPONSE_ID && frame.can_dlc == 8) {
                std::memcpy(&voltage, &frame.data[0], sizeof(float));
                std::memcpy(&absorbance, &frame.data[4], sizeof(float));
                return true;
            }
        }

        return false;
    }

    void handle_request(
        const std::shared_ptr<GetSpectroData::Request> request,
        std::shared_ptr<GetSpectroData::Response> response
    ) {
        (void)request;

        float voltage = -1.0f;
        float absorbance = -1.0f;

        if (!send_can_request()) {
            response->voltage = -1.0f;
            response->absorbance = -1.0f;
            return;
        }

        if (!wait_for_can_response(voltage, absorbance)) {
            response->voltage = -1.0f;
            response->absorbance = -1.0f;
            return;
        }

        response->voltage = voltage;
        response->absorbance = absorbance;

        RCLCPP_INFO(
            this->get_logger(),
            "Spectro data returned: V=%.3f, A=%.4f",
            voltage,
            absorbance
        );
    }
};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<SpectroSensorNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
