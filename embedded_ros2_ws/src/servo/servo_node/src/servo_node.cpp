#include "servo_node/servo_node.hpp"
// #include "epoll_event_loop.hpp"
#include <chrono>
#include <cmath>
#include <cerrno>
#include <cstring>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/i2c-dev.h>

// ---------- PCA9685 minimal helper (file-local) ----------
static int g_i2c_fd = -1;
static constexpr uint8_t PCA9685_ADDR = 0x40;   // default address
static constexpr uint8_t MODE1 = 0x00;
static constexpr uint8_t MODE2 = 0x01;
static constexpr uint8_t PRESCALE = 0xFE;
static constexpr uint8_t LED0_ON_L = 0x06;

static bool i2c_write8(uint8_t reg, uint8_t val) {
    uint8_t buf[2] = {reg, val};
    return (::write(g_i2c_fd, buf, 2) == 2);
}

static bool i2c_read8(uint8_t reg, uint8_t &val) {
    if (::write(g_i2c_fd, &reg, 1) != 1) return false;
    return (::read(g_i2c_fd, &val, 1) == 1);
}

// Set PWM frequency (servo typical ~50Hz)
static bool pca9685_set_freq_hz(float hz) {
    constexpr float osc = 25000000.0f;
    float prescale_f = (osc / (4096.0f * hz)) - 1.0f;
    uint8_t prescale = (uint8_t)std::floor(prescale_f + 0.5f);

    uint8_t oldmode{};
    if (!i2c_read8(MODE1, oldmode)) return false;

    // sleep
    if (!i2c_write8(MODE1, (oldmode & 0x7F) | 0x10)) return false;
    if (!i2c_write8(PRESCALE, prescale)) return false;
    // wake + auto-increment
    if (!i2c_write8(MODE1, (oldmode & 0xEF) | 0x20)) return false;

    ::usleep(5000);
    return true;
}

static bool pca9685_set_pulse_us(uint8_t channel, float pulse_us, float hz) {
    if (channel > 15) return false;

    float period_us = 1000000.0f / hz;
    float counts_f = (pulse_us / period_us) * 4096.0f;
    if (counts_f < 0.0f) counts_f = 0.0f;
    if (counts_f > 4095.0f) counts_f = 4095.0f;

    uint16_t off = (uint16_t)counts_f;

    uint8_t reg = LED0_ON_L + 4 * channel;
    uint8_t buf[5] = {
        reg,
        0, 0,                     // ON_L, ON_H
        (uint8_t)(off & 0xFF),     // OFF_L
        (uint8_t)((off >> 8) & 0x0F) // OFF_H
    };

    return (::write(g_i2c_fd, buf, 5) == 5);
}

enum CommandType : uint8_t {
    kVelocityControl = 0,
    kPositionControl = 1
};

ServoNode::ServoNode(const std::string& node_name) : rclcpp::Node(node_name) {
    
    rclcpp::Node::declare_parameter<uint8_t>("channel_id", 0);
    this->declare_parameter<bool>("use_hw", true);
    rclcpp::Node::declare_parameter<uint16_t>("initial_angle_deg", 0);
    rclcpp::Node::declare_parameter<uint16_t>("min_angle_deg", 0);
    rclcpp::Node::declare_parameter<uint16_t>("max_angle_deg", 360);
    rclcpp::Node::declare_parameter<uint16_t>("min_pwm_micro_s", 500);
    rclcpp::Node::declare_parameter<uint16_t>("max_pwm_micro_s", 2500);

    rclcpp::QoS control_message_qos(rclcpp::KeepLast(1));
    subscriber_ = rclcpp::Node::create_subscription<ControlMessage>("control_message", control_message_qos, std::bind(&ServoNode::subscriber_callback, this, _1));
}

void ServoNode::deinit() {
    // sub_evt_.deinit();

    if (g_i2c_fd >= 0) {
        ::close(g_i2c_fd);
        g_i2c_fd = -1;
    }
}

bool ServoNode::init(/* EpollEventLoop* event_loop */) {
    channel_id_         = rclcpp::Node::get_parameter("channel_id").as_int();
    use_hw_             = this->get_parameter("use_hw").as_bool();
    initial_angle_deg_  = rclcpp::Node::get_parameter("initial_angle_deg").as_int();
    min_angle_deg_      = rclcpp::Node::get_parameter("min_angle_deg").as_int();
    max_angle_deg_      = rclcpp::Node::get_parameter("max_angle_deg").as_int();
    min_pwm_micro_s_    = rclcpp::Node::get_parameter("min_pwm_micro_s").as_int();
    max_pwm_micro_s_    = rclcpp::Node::get_parameter("max_pwm_micro_s").as_int();

    // Set current target position to initial angle
    current_target_pos_deg_ = static_cast<float>(initial_angle_deg_);
    send_stepped_position_control_flag_ = false;
    last_velocity_loop_time_seconds_ = this->get_clock()->now().seconds();

    // if (!sub_evt_.init(event_loop, std::bind(&CubemarsCanNode::ctrl_msg_callback, this))) {
    //     RCLCPP_ERROR(rclcpp::Node::get_logger(), "Failed to initialize subscriber event");
    //     return false;
    // }

    RCLCPP_INFO(rclcpp::Node::get_logger(), "Servo channel_id: %d", channel_id_);
    RCLCPP_INFO(rclcpp::Node::get_logger(), "Servo initial_angle_deg: %d", initial_angle_deg_);
    RCLCPP_INFO(rclcpp::Node::get_logger(), "Servo min_angle_deg: %d", min_angle_deg_);
    RCLCPP_INFO(rclcpp::Node::get_logger(), "Servo max_angle_deg: %d", max_angle_deg_);
    RCLCPP_INFO(rclcpp::Node::get_logger(), "Servo min_pwm_micro_s: %d", min_pwm_micro_s_);
    RCLCPP_INFO(rclcpp::Node::get_logger(), "Servo max_pwm_micro_s: %d", max_pwm_micro_s_);

    if (use_hw_) {
        // --- Open I2C and init PCA9685 ---
        g_i2c_fd = ::open("/dev/i2c-1", O_RDWR);
        if (g_i2c_fd < 0) {
            RCLCPP_ERROR(this->get_logger(), "Failed to open /dev/i2c-1: %s", strerror(errno));
            return false;
        }
        if (ioctl(g_i2c_fd, I2C_SLAVE, PCA9685_ADDR) < 0) {
            RCLCPP_ERROR(this->get_logger(), "Failed to set I2C addr 0x%02X: %s", PCA9685_ADDR, strerror(errno));
            ::close(g_i2c_fd);
            g_i2c_fd = -1;
            return false;
        }

        (void)i2c_write8(MODE2, 0x04); // Totem pole (push-pull) output

        if(!pca9685_set_freq_hz(50.0f)) {
            RCLCPP_ERROR(this->get_logger(), "Failed to set PCA9685 frequency");
            ::close(g_i2c_fd);
            g_i2c_fd = -1;
            return false;
        }

        // Write initial position immediately
        float init_pwm = get_pwm_from_position(current_target_pos_deg_);
        (void)pca9685_set_pulse_us(channel_id_, init_pwm, 50.0f);
    } else {
        RCLCPP_WARN(this->get_logger(), "use_hw:=false -> DRY RUN (no I2C)");
        float init_pwm = get_pwm_from_position(current_target_pos_deg_);
        RCLCPP_INFO(this->get_logger(), "[DRY RUN] ch=%u pwm_us=%.1f", channel_id_, init_pwm);
    }

    // Start velocity loop timer
    start_velocity_output_timer();

    RCLCPP_INFO(rclcpp::Node::get_logger(), "Servo successfully initialized!");

    return true;
}

void ServoNode::subscriber_callback(const ControlMessage::SharedPtr msg) {
    {
        std::lock_guard<std::mutex> guard(control_message_mutex_);
        control_message_ = *msg;
        // sub_evt_.set();
    }
    control_message_callback();
}

void ServoNode::control_message_callback() {
    ControlMessage locked_msg;
    {
        std::lock_guard<std::mutex> guard(control_message_mutex_);
        locked_msg = control_message_;
    }

    // By default, don't send constant position commands (only for velocity mode)
    send_stepped_position_control_flag_ = false;

    switch (locked_msg.control_mode) {
        case CommandType::kVelocityControl: {
            RCLCPP_DEBUG(rclcpp::Node::get_logger(), "Servo velocity input: %.2f", locked_msg.input_vel_deg);

            // Reset timer so we don't see a huge position jump
            last_velocity_loop_time_seconds_ = this->get_clock()->now().seconds();
            
            // Convert pseudo-velocity to position control by stepping target position
            // Set velocity for future updates
            current_target_vel_deg_ = locked_msg.input_vel_deg;

            // Convert position from pseudo-velocity loop to pwm
            float pwm = get_pwm_from_position(current_target_pos_deg_);
            
            // Enable repeated position streaming when in velocity mode
            send_stepped_position_control_flag_ = true;

            if (use_hw_) {
                (void)pca9685_set_pulse_us(channel_id_, pwm, 50.0f);
            } else {
                RCLCPP_INFO(this->get_logger(), "[DRY RUN] ch=%u pwm_us=%.1f", channel_id_, pwm);
            }

            break;
        }
        case CommandType::kPositionControl: {
            RCLCPP_DEBUG(rclcpp::Node::get_logger(), "Servo position input: %.2f", locked_msg.input_pos_deg);
            
            // Convert position to pwm
            float pwm = get_pwm_from_position(locked_msg.input_pos_deg);

            if (use_hw_) {
                (void)pca9685_set_pulse_us(channel_id_, pwm, 50.0f);
            } else {
                RCLCPP_INFO(this->get_logger(), "[DRY RUN] ch=%u pwm_us=%.1f", channel_id_, pwm);
            }

            break;
        }
        default: 
            RCLCPP_ERROR(rclcpp::Node::get_logger(), "Unsupported control_mode: %d", locked_msg.control_mode);
            return;
    }
}

float ServoNode::get_pwm_from_position(float input_pos_deg) {
    // Clamp input to valid range
    if (input_pos_deg < min_angle_deg_) input_pos_deg = min_angle_deg_;
    if (input_pos_deg > max_angle_deg_) input_pos_deg = max_angle_deg_;

    // Convert degree position input to pwm output
    // Example implementation:
    // Get target angle as fraction of allowed movement range
    // E.g. for target deg 270, min angle 180 max angle 360, 
    // target_pos_fractional = (270 - 180) / (360 - 180) = 0.5
    double target_pos_fractional = ((input_pos_deg - min_angle_deg_) / 
                                        static_cast<double>(max_angle_deg_ - min_angle_deg_));

    // Now we find the PWM output corresponding to this fraction of the PWM range
    // E.g. for target_pos_fractional 0.5, min pwm 500, max pwm 2500,
    // target_pwm_micro_s = 500 + 0.5 * (2500 - 500) = 1500
    float target_pwm_micro_s = static_cast<float>(min_pwm_micro_s_ + target_pos_fractional *
                                    (max_pwm_micro_s_ - min_pwm_micro_s_));

    return target_pwm_micro_s;
}

void ServoNode::start_velocity_output_timer() {
    // Asynchronously publish position command messages
    velocity_command_timer_ = this->create_wall_timer(
        std::chrono::milliseconds(20), // 50Hz
        [this]()
        {
            // Return early if we aren't in velocity control mode, as there is no need
            // to continously publish position
            if (!send_stepped_position_control_flag_) {
                return;
            }

            std::lock_guard<std::mutex> guard(control_message_mutex_); // Ensure safe command writing

            // Step target position by velocity * time between loops
            double now_s = this->get_clock()->now().seconds();
            double elapsed_time_seconds = now_s - last_velocity_loop_time_seconds_;
            last_velocity_loop_time_seconds_ = now_s;

            current_target_pos_deg_ += current_target_vel_deg_ * elapsed_time_seconds;

            float pwm = get_pwm_from_position(current_target_pos_deg_);

            if (use_hw_) {
                (void)pca9685_set_pulse_us(channel_id_, pwm, 50.0f);
            } else {
                RCLCPP_INFO(this->get_logger(), "[DRY RUN] ch=%u pwm_us=%.1f", channel_id_, pwm);
            }
        }
    );
}