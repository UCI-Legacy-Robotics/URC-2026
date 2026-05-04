#include <chrono>
#include <cstring>
#include <fcntl.h>
#include <memory>
#include <string>
#include <termios.h>
#include <thread>
#include <unistd.h>
#include <vector>

#include "rclcpp/rclcpp.hpp"
#include "npk_sensor/srv/get_soil_data.hpp"

using GetSoilData = npk_sensor::srv::GetSoilData;

class SoilSensorNode : public rclcpp::Node {
public:
    SoilSensorNode() : Node("soil_sensor_node") {
        serial_fd_ = open_serial("/dev/ttyAMA0");

        if (serial_fd_ < 0) {
            RCLCPP_ERROR(this->get_logger(), "Failed to open serial port /dev/ttyAMA0");
        } else {
            RCLCPP_INFO(this->get_logger(), "Opened serial port /dev/ttyAMA0");
        }

        service_ = this->create_service<GetSoilData>(
            "get_soil_data",
            std::bind(
                &SoilSensorNode::handle_request,
                this,
                std::placeholders::_1,
                std::placeholders::_2
            )
        );

        RCLCPP_INFO(this->get_logger(), "Soil Sensor Service Ready");
    }

    ~SoilSensorNode() {
        if (serial_fd_ >= 0) {
            close(serial_fd_);
        }
    }

private:
    int serial_fd_;
    rclcpp::Service<GetSoilData>::SharedPtr service_;

    int open_serial(const std::string &port) {
        int fd = open(port.c_str(), O_RDWR | O_NOCTTY | O_SYNC);

        if (fd < 0) {
            return -1;
        }

        struct termios tty;
        memset(&tty, 0, sizeof tty);

        if (tcgetattr(fd, &tty) != 0) {
            close(fd);
            return -1;
        }

        cfsetospeed(&tty, B9600);
        cfsetispeed(&tty, B9600);

        tty.c_cflag = (tty.c_cflag & ~CSIZE) | CS8;
        tty.c_iflag &= ~IGNBRK;
        tty.c_lflag = 0;
        tty.c_oflag = 0;

        tty.c_cc[VMIN] = 0;
        tty.c_cc[VTIME] = 10;  // 1 second timeout

        tty.c_iflag &= ~(IXON | IXOFF | IXANY);
        tty.c_cflag |= (CLOCAL | CREAD);
        tty.c_cflag &= ~(PARENB | PARODD);
        tty.c_cflag &= ~CSTOPB;
        tty.c_cflag &= ~CRTSCTS;

        if (tcsetattr(fd, TCSANOW, &tty) != 0) {
            close(fd);
            return -1;
        }

        return fd;
    }

    std::vector<uint8_t> hex_to_bytes(const std::string &hex) {
        std::vector<uint8_t> bytes;
        std::string clean;

        for (char c : hex) {
            if (c != ' ') {
                clean += c;
            }
        }

        for (size_t i = 0; i < clean.length(); i += 2) {
            std::string byte_string = clean.substr(i, 2);
            uint8_t byte = static_cast<uint8_t>(std::stoi(byte_string, nullptr, 16));
            bytes.push_back(byte);
        }

        return bytes;
    }

    std::vector<uint8_t> send_request(const std::string &cmd_hex, int expected_len = 11) {
        std::vector<uint8_t> response;

        if (serial_fd_ < 0) {
            RCLCPP_ERROR(this->get_logger(), "Serial port is not open");
            return response;
        }

        std::vector<uint8_t> cmd = hex_to_bytes(cmd_hex);

        ssize_t written = write(serial_fd_, cmd.data(), cmd.size());

        if (written < 0) {
            RCLCPP_ERROR(this->get_logger(), "Serial write failed");
            return response;
        }

        std::this_thread::sleep_for(std::chrono::milliseconds(100));

        response.resize(expected_len);
        ssize_t bytes_read = read(serial_fd_, response.data(), expected_len);

        if (bytes_read <= 0) {
            RCLCPP_ERROR(this->get_logger(), "No response from NPK sensor");
            response.clear();
            return response;
        }

        response.resize(bytes_read);
        return response;
    }

    float parse_value(const std::vector<uint8_t> &data, float div = 1.0f) {
        if (data.size() >= 7) {
            uint16_t val = (static_cast<uint16_t>(data[3]) << 8) | data[4];
            return static_cast<float>(val) / div;
        }

        return -1.0f;
    }

    void handle_request(
        const std::shared_ptr<GetSoilData::Request> request,
        std::shared_ptr<GetSoilData::Response> response
    ) {
        (void)request;

        // 1. pH
        auto res_ph = send_request("01 03 00 06 00 01 64 0B");
        float ph = parse_value(res_ph, 100.0f);

        // 2. Humidity / moisture
        auto res_h = send_request("01 03 00 12 00 01 24 0F");
        float hum = parse_value(res_h, 10.0f);

        // 3. Temperature
        auto res_t = send_request("01 03 00 13 00 01 75 CF");
        float temp = parse_value(res_t, 10.0f);

        // 4. Conductivity
        auto res_ec = send_request("01 03 00 15 00 01 95 CE");
        float ec = parse_value(res_ec, 1.0f);

        // 5. NPK
        auto res_npk = send_request("01 03 00 1E 00 03 65 CD");

        float n = -1.0f;
        float p = -1.0f;
        float k = -1.0f;

        if (res_npk.size() >= 11) {
            n = static_cast<float>((static_cast<uint16_t>(res_npk[3]) << 8) | res_npk[4]);
            p = static_cast<float>((static_cast<uint16_t>(res_npk[5]) << 8) | res_npk[6]);
            k = static_cast<float>((static_cast<uint16_t>(res_npk[7]) << 8) | res_npk[8]);
        }

        response->ph = ph;
        response->moisture = hum;
        response->temperature = temp;
        response->conductivity = ec;
        response->nitrogen = n;
        response->phosphorus = p;
        response->potassium = k;

        RCLCPP_INFO(this->get_logger(), "Soil data returned");
    }
};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<SoilSensorNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
