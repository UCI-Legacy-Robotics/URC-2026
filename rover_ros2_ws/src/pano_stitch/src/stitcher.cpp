#include "pano_stitch_ros2/stitcher.hpp"

#include <opencv2/features2d.hpp>

#include <algorithm>
#include <cmath>
#include <iostream>
#include <stack>

namespace pano_stitch {

PanoStitcher::PanoStitcher(int min_good_matches, int min_inliers)
    : min_good_matches_(min_good_matches), min_inliers_(min_inliers) {}

cv::Mat PanoStitcher::cylindricalWarp(const cv::Mat& img, double focalLength) const {
  int width = img.cols;
  int height = img.rows;

  cv::Mat warped = cv::Mat::zeros(height, width, img.type());

  double cx = width / 2.0;
  double cy = height / 2.0;

  for (int y = 0; y < height; y++) {
    for (int x = 0; x < width; x++) {
      double xCentered = x - cx;
      double yCentered = y - cy;

      double theta = xCentered / focalLength;
      double h = yCentered / focalLength;

      double srcX = focalLength * std::tan(theta) + cx;
      double srcY = focalLength * h / std::cos(theta) + cy;

      if (srcX >= 0 && srcX < width - 1 && srcY >= 0 && srcY < height - 1) {
        warped.at<cv::Vec3b>(y, x) = img.at<cv::Vec3b>((int)srcY, (int)srcX);
      }
    }
  }

  return warped;
}

cv::Mat PanoStitcher::computeHomography(const ImageData& src, const ImageData& dst) const {
  cv::BFMatcher matcher(cv::NORM_L2);

  std::vector<std::vector<cv::DMatch>> knnMatches;
  matcher.knnMatch(src.descriptors, dst.descriptors, knnMatches, 2);

  std::vector<cv::DMatch> goodMatches;
  for (const auto& m : knnMatches) {
    if (m.size() == 2 && m[0].distance < 0.70 * m[1].distance) {
      goodMatches.push_back(m[0]);
    }
  }

  if (static_cast<int>(goodMatches.size()) < min_good_matches_) {
    return cv::Mat();
  }

  std::vector<cv::Point2f> srcPts;
  std::vector<cv::Point2f> dstPts;
  for (const auto& match : goodMatches) {
    srcPts.push_back(src.keypoints[match.queryIdx].pt);
    dstPts.push_back(dst.keypoints[match.trainIdx].pt);
  }

  cv::Mat inlierMask;
  cv::Mat H = cv::findHomography(srcPts, dstPts, cv::RANSAC, 3.0, inlierMask);

  if (H.empty()) {
    return cv::Mat();
  }

  int inliers = cv::countNonZero(inlierMask);
  if (inliers < min_inliers_) {
    return cv::Mat();
  }

  return H;
}

std::vector<cv::Point2f> PanoStitcher::getWarpedCorners(const cv::Mat& image, const cv::Mat& H) const {
  std::vector<cv::Point2f> corners = {
      {0, 0}, {(float)image.cols, 0}, {(float)image.cols, (float)image.rows}, {0, (float)image.rows}};

  std::vector<cv::Point2f> warped;
  cv::perspectiveTransform(corners, warped, H);
  return warped;
}

cv::Rect PanoStitcher::largestInscribedRect(const cv::Mat& mask) const {
  int rows = mask.rows;
  int cols = mask.cols;
  std::vector<int> heights(cols, 0);
  cv::Rect bestRect(0, 0, 0, 0);
  int bestArea = 0;

  for (int r = 0; r < rows; r++) {
    for (int c = 0; c < cols; c++) {
      heights[c] = mask.at<uchar>(r, c) > 0 ? heights[c] + 1 : 0;
    }

    std::stack<int> stk;
    for (int c = 0; c <= cols; c++) {
      int h = (c == cols) ? 0 : heights[c];
      while (!stk.empty() && heights[stk.top()] > h) {
        int height = heights[stk.top()];
        stk.pop();
        int left = stk.empty() ? 0 : stk.top() + 1;
        int width = c - left;
        if (height * width > bestArea) {
          bestArea = height * width;
          bestRect = cv::Rect(left, r - height + 1, width, height);
        }
      }
      stk.push(c);
    }
  }

  return bestRect;
}

cv::Mat PanoStitcher::stitch(const std::vector<cv::Mat>& inputImages) const {
  if (inputImages.size() < 2) {
    return cv::Mat();
  }

  auto sift = cv::SIFT::create();
  std::vector<ImageData> images;
  images.reserve(inputImages.size());

  for (const auto& raw : inputImages) {
    if (raw.empty()) {
      return cv::Mat();
    }

    ImageData data;
    double focalLength = raw.cols * 2.0;
    data.image = cylindricalWarp(raw, focalLength);

    sift->detectAndCompute(data.image, cv::noArray(), data.keypoints, data.descriptors);
    if (data.descriptors.empty()) {
      return cv::Mat();
    }

    images.push_back(std::move(data));
  }

  int n = static_cast<int>(images.size());
  int anchor = n / 2;

  std::vector<cv::Mat> toAnchor(n);
  toAnchor[anchor] = cv::Mat::eye(3, 3, CV_64F);

  for (int i = anchor - 1; i >= 0; i--) {
    cv::Mat H = computeHomography(images[i], images[i + 1]);
    if (H.empty()) {
      return cv::Mat();
    }
    toAnchor[i] = toAnchor[i + 1] * H;
  }

  for (int i = anchor + 1; i < n; i++) {
    cv::Mat H = computeHomography(images[i], images[i - 1]);
    if (H.empty()) {
      return cv::Mat();
    }
    toAnchor[i] = toAnchor[i - 1] * H;
  }

  std::vector<cv::Point2f> allCorners;
  for (int i = 0; i < n; i++) {
    auto warped = getWarpedCorners(images[i].image, toAnchor[i]);
    allCorners.insert(allCorners.end(), warped.begin(), warped.end());
  }

  float minX = allCorners[0].x, minY = allCorners[0].y;
  float maxX = allCorners[0].x, maxY = allCorners[0].y;
  for (const auto& p : allCorners) {
    minX = std::min(minX, p.x);
    minY = std::min(minY, p.y);
    maxX = std::max(maxX, p.x);
    maxY = std::max(maxY, p.y);
  }

  cv::Mat T = cv::Mat::eye(3, 3, CV_64F);
  T.at<double>(0, 2) = -minX;
  T.at<double>(1, 2) = -minY;

  int panoWidth = static_cast<int>(std::ceil(maxX - minX));
  int panoHeight = static_cast<int>(std::ceil(maxY - minY));

  cv::Mat accumulator = cv::Mat::zeros(panoHeight, panoWidth, CV_32FC3);
  cv::Mat weight = cv::Mat::zeros(panoHeight, panoWidth, CV_32F);

  for (int i = 0; i < n; i++) {
    cv::Mat warped;
    cv::warpPerspective(images[i].image, warped, T * toAnchor[i], cv::Size(panoWidth, panoHeight));

    cv::Mat gray;
    cv::cvtColor(warped, gray, cv::COLOR_BGR2GRAY);

    cv::Mat mask;
    cv::threshold(gray, mask, 1, 255, cv::THRESH_BINARY);

    cv::Mat warpedFloat;
    warped.convertTo(warpedFloat, CV_32FC3);

    cv::Mat maskFloat;
    mask.convertTo(maskFloat, CV_32F, 1.0 / 255.0);

    std::vector<cv::Mat> maskChannels = {maskFloat, maskFloat, maskFloat};
    cv::Mat mask3;
    cv::merge(maskChannels, mask3);

    cv::Mat weightedImage;
    cv::multiply(warpedFloat, mask3, weightedImage);

    accumulator += weightedImage;
    weight += maskFloat;
  }

  cv::Mat outputFloat = cv::Mat::zeros(panoHeight, panoWidth, CV_32FC3);
  for (int y = 0; y < panoHeight; y++) {
    for (int x = 0; x < panoWidth; x++) {
      float w = weight.at<float>(y, x);
      if (w > 0.0f) {
        outputFloat.at<cv::Vec3f>(y, x) = accumulator.at<cv::Vec3f>(y, x) / w;
      }
    }
  }

  cv::Mat panorama;
  outputFloat.convertTo(panorama, CV_8UC3);

  cv::Mat weightMask;
  weight.convertTo(weightMask, CV_8U, 255.0);

  cv::Rect bbox = cv::boundingRect(weightMask);
  cv::Mat cropped = panorama(bbox).clone();
  cv::Mat croppedMask = weightMask(bbox).clone();

  cv::Mat blackRegions;
  cv::threshold(croppedMask, blackRegions, 0, 255, cv::THRESH_BINARY_INV);

  cv::Mat labels, stats, centroids;
  int numComponents = cv::connectedComponentsWithStats(blackRegions, labels, stats, centroids);

  int maxHoleArea = cropped.cols * cropped.rows / 200;
  cv::Mat smallHolesMask = cv::Mat::zeros(blackRegions.size(), CV_8U);
  for (int i = 1; i < numComponents; i++) {
    if (stats.at<int>(i, cv::CC_STAT_AREA) < maxHoleArea) {
      smallHolesMask.setTo(255, labels == i);
    }
  }

  cv::Mat inpainted = cropped.clone();
  if (cv::countNonZero(smallHolesMask) > 0) {
    cv::inpaint(cropped, smallHolesMask, inpainted, 3, cv::INPAINT_TELEA);
  }

  cv::Mat updatedMask = croppedMask | smallHolesMask;
  cv::Rect innerRect = largestInscribedRect(updatedMask);

  return inpainted(innerRect).clone();
}

}  // namespace pano_stitch
