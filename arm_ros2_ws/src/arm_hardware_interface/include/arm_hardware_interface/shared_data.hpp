#pragma once

#include <memory>
#include <mutex>
#include <vector>

struct ArmSharedData
{
  std::array<double, 7> commands{};
  std::array<double, 7> position_feedback{};
  std::array<double, 7> velocity_feedback{};

  std::mutex command_mutex;
  std::mutex feedback_mutex;

  // Constructor ensures arrays start at 0
  void SharedData() {
    commands.fill(0.0);
    position_feedback.fill(0.0);
    velocity_feedback.fill(0.0);
  }
};

inline std::shared_ptr<ArmSharedData> get_arm_shared_data()
{
  static std::shared_ptr<ArmSharedData> instance =
    std::make_shared<ArmSharedData>();
  return instance;
}