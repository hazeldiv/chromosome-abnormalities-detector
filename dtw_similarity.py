import numpy as np
from scipy.spatial.distance import cdist
from skimage.morphology import medial_axis, skeletonize
from skimage.measure import profile_line
from scipy.ndimage import rotate
import cv2


class ChromosomeDTW:
    def __init__(self, threshold=0.85):
        self.threshold = threshold

    def extract_medial_axis_profile(self, image, num_points=64):
        """
        Extract medial axis density profile from chromosome image.
        """
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        coords = np.column_stack(np.where(binary > 0))
        if len(coords) == 0:
            return np.zeros(num_points)

        y_min, x_min = coords.min(axis=0)
        y_max, x_max = coords.max(axis=0)
        crop = binary[y_min:y_max+1, x_min:x_max+1]

        if crop.shape[0] < 3 or crop.shape[1] < 3:
            return np.zeros(num_points)

        try:
            skel = skeletonize(crop > 0)
        except:
            return np.zeros(num_points)

        skel_points = np.argwhere(skel > 0)
        if len(skel_points) < 2:
            return np.zeros(num_points)

        cy, cx = skel_points.mean(axis=0)

        angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
        profile = np.zeros(num_points)

        for i, angle in enumerate(angles):
            dx = np.cos(angle)
            dy = np.sin(angle)
            p1 = (cx - dx * 200, cy - dy * 200)
            p2 = (cx + dx * 200, cy + dy * 200)

            try:
                line_profile = profile_line(crop.astype(np.float32), p1, p2, mode='reflect')
                profile[i] = np.sum(line_profile > 0)
            except:
                profile[i] = 0

        profile = profile / (profile.max() + 1e-8)
        return profile

    def dtw_distance(self, seq1, seq2):
        """
        Compute DTW distance between two sequences.
        """
        n, m = len(seq1), len(seq2)
        dtw_matrix = np.full((n + 1, m + 1), np.inf)
        dtw_matrix[0, 0] = 0

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                cost = abs(seq1[i - 1] - seq2[j - 1])
                dtw_matrix[i, j] = cost + min(
                    dtw_matrix[i - 1, j],
                    dtw_matrix[i, j - 1],
                    dtw_matrix[i - 1, j - 1]
                )

        return dtw_matrix[n, m]

    def compute_similarity(self, profile1, profile2):
        """
        Compute normalized similarity score (0-1) using DTW.
        """
        if np.sum(profile1) == 0 or np.sum(profile2) == 0:
            return 0.0

        distance = self.dtw_distance(profile1, profile2)
        max_possible = len(profile1) + len(profile2)
        similarity = 1.0 - (distance / max_possible)
        return max(0.0, min(1.0, similarity))

    def is_similar(self, image1, image2):
        """
        Check if two chromosome images are similar based on DTW.
        """
        profile1 = self.extract_medial_axis_profile(image1)
        profile2 = self.extract_medial_axis_profile(image2)
        similarity = self.compute_similarity(profile1, profile2)
        return similarity >= self.threshold, similarity