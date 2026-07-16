#pragma once

#include <opencv2/opencv.hpp>
#include <vector>

namespace pano_stitch {

// Stitches an ordered sequence of overlapping images into a single
// cylindrical panorama. This is the same pipeline from the original
// offline main.cpp (cylindrical warp -> SIFT + BFMatcher -> RANSAC
// homography chained from a center anchor -> weighted-average blend
// -> hole inpainting -> largest clean inscribed rectangle crop),
// refactored so it can be called repeatedly on in-memory frames
// instead of reading a folder of images once.
class PanoStitcher {
public:
  // min_good_matches / min_inliers mirror the thresholds used in the
  // original computeHomography() (10 good Lowe-ratio matches, 8 RANSAC
  // inliers) required before a pairwise homography is accepted.
  explicit PanoStitcher(int min_good_matches = 10, int min_inliers = 8);

  // Stitches `images` (expected to be roughly ordered left-to-right or
  // right-to-left, taken from a single rotating/panning camera) into one
  // panorama. Returns an empty cv::Mat if fewer than 2 images are given,
  // or if any pairwise homography fails (insufficient matches/inliers).
  cv::Mat stitch(const std::vector<cv::Mat>& images) const;

private:
  struct ImageData {
    cv::Mat image;
    std::vector<cv::KeyPoint> keypoints;
    cv::Mat descriptors;
  };

  cv::Mat cylindricalWarp(const cv::Mat& img, double focalLength) const;
  cv::Mat computeHomography(const ImageData& src, const ImageData& dst) const;
  std::vector<cv::Point2f> getWarpedCorners(const cv::Mat& image, const cv::Mat& H) const;
  cv::Rect largestInscribedRect(const cv::Mat& mask) const;

  int min_good_matches_;
  int min_inliers_;
};

}  // namespace pano_stitch
