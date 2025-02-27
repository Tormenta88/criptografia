import cv2 as cv
import os

num_Matches = []
def are_images_same(main_image, sub_image, match_threshold=50):
    gray1 = cv.cvtColor(main_image, cv.COLOR_BGR2GRAY)
    gray2 = cv.cvtColor(sub_image, cv.COLOR_BGR2GRAY)

    sift = cv.SIFT_create()

    key_point1, descr1 = sift.detectAndCompute(gray1, None)
    key_point2, descr2 = sift.detectAndCompute(gray2, None)

    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=7)
    search_params = dict(checks=50)

    flann = cv.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(descr1, descr2, k=2)

    good_matches = [m for m, n in matches if m.distance < 0.75 * n.distance]

    print(f"Good matches found: {len(good_matches)}")

    return len(good_matches) >= match_threshold, len(good_matches)


img_paths = []
for filename in os.listdir('sample_inputs/'):
    img_path = os.path.join('sample_inputs/', filename)

    main_image = cv.imread('huellasBuscar/abuscar4.tif')
    sub_image = cv.imread(img_path)
    img_paths.append(img_path)

    same, matche = are_images_same(main_image, sub_image)
    num_Matches.append(matche)
    if same:
        print("Son iguales")
    else:
        #print("The images are different.")
        pass

print(max(num_Matches))
index_max = max(range(len(num_Matches)), key=num_Matches.__getitem__)
print(img_paths[index_max])


'''SIFT xfeatures2d
detect and compute
FlamBasedMatcher'''