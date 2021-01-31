'''
    extract the "viscom"-style calibration grid with big and small markers
    where big markers are not filled and contain zero (origin), one (x), two (y) dots
'''
# pylint: disable=invalid-name
#   (migrate old tested code)

import cv2
import numpy as np

def child_object_count(hierarch, idx):
    '''
        hierarch: hierarchy list
        idx index queried

        returns:
            number of inner objects (not contours)
            number of inner contours
    '''
    objects = 0
    inner_cnt = 0

    stack = [(idx, 0), ]
    while stack:
        cur_idx, level = stack.pop()
        [_next, _prev, _child, _parent] = hierarch[cur_idx]
        level += 1
        if _child >= 0: #has child
            #check every contour if current is their parent
            for i, [_n, _b, _c, _p] in enumerate(hierarch):
                if _p == cur_idx:    
                    stack.append( (i, level) )
                    inner_cnt += 1
                    if level % 2 == 0: #an even numbered (=outer) contour, so must be a nested object inside
                        objects += 1

    #print(idx, objects)                
    return objects, inner_cnt


def sort_features(features, pivotpos):
    ''' sort features by eucledian distance to pivot position ascending

        features: list [x,y] feature vector (important: first two columns are image coords)
        pivotpos: [x,y] image coord of pivot position

        return index-array of new order (of course, the pivot-element will be the first within the returned array)
    '''
    feat = np.copy(features).astype(float)
    pivot_x, pivot_y = pivotpos
    feat[:,0] -= float(pivot_x)
    feat[:,1] -= float(pivot_y)
    distances = np.hypot(feat[:,0],feat[:,1])

    indices = np.argsort(distances)
    return indices


def homography_from_image(gray, scale_mm=1):
    if gray.ndim == 3:
        gray = cv2.cvtColor(gray, cv2.COLOR_RGB2GRAY)
    # gray = cv2.GaussianBlur(gray, ksize=(0,0), sigmaX=2, sigmaY=0, borderType=cv2.BORDER_DEFAULT  )
    h, binary = cv2.threshold(gray, 128, 255,  cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    c_copy = np.require(binary, dtype=np.uint8).copy() #find contours is destructive, so make a copy first
    r = cv2.findContours(c_copy, mode = cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE )
    contours,  [hierarch] = r


    #just some debugging...
    debug = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB) #make color image from grayscale (it remains gray, but we can draw into in color)

    #now extract
    features = []
    centers = []
    markers = {}
    for ii, (h, cnt) in enumerate(zip(hierarch, contours)):
        #filter size
        length = cv2.arcLength(cnt, False)
        area = cv2.contourArea(cnt)
        if length > 1 and area > 1:
            roundness = 4.0* np.sqrt(area) / length
        else:
            continue

        if area < 300:
            #print('a', area)
            continue

        #filter roundness
        if roundness < 0.92:
            #print('r', roundness)
            continue

        [_next, _prev, _child, parent] = h
        #if (parent >= 0): #only outer contours
        #    continue

        M = cv2.moments(cnt)          #calc center point of assumed inner contour
        cx = int(round(M['m10']/M['m00']))
        cy = int(round(M['m01']/M['m00']))
        #if length < 80:
        #    print("l", length)
        #    continue

        color = (255,64,0)
        inner_obj, inner_cnt = child_object_count(hierarch, ii)

        if inner_cnt and area > 4000: #one of the big hollow ones
            if inner_obj == 0:
                color = (0,255,0)
                cv2.putText(debug ,"o", (cx - 5,cy), cv2.FONT_HERSHEY_SIMPLEX, 2.2, (127,255,0),3)
                markers[0] = np.array([cx,cy])
            elif inner_obj == 1:
                color = (255,127,0)
                cv2.putText(debug ,"x", (cx - 5,cy), cv2.FONT_HERSHEY_SIMPLEX, 2.2, (127,255,0),3)
                markers[1] = np.array([cx,cy])
            elif inner_obj == 2:
                cv2.putText(debug ,"y", (cx - 5,cy), cv2.FONT_HERSHEY_SIMPLEX, 2.2, (127,255,0),3)
                color = (0,127,255)
                markers[2] = np.array([cx,cy])

            print("big object:", inner_cnt, inner_obj)

        features.append(cnt)
        centers.append( (cx,cy) )
        cv2.drawContours(debug, [cnt], -1, color, 1)    #into debug-image, draw filtered contours, all of them, in red

    if len(markers) == 3:
        print("markers found, estimating base")
        origin = markers[0]
        vx = (1.0 / 4.0) * (markers[1] - origin)   #x-base vector
        vy = (1.0 / 4.0) * (markers[2] - origin)   #y-base vector

        # estimate a homography from guessing the (1,1) point
        p11 = origin + 1 * vx + 1 * vy
        order = sort_features(centers, p11)
        p11 = centers[order[0]]
        logical = np.array([[0,0], [0,4], [4,0], [1,1]], dtype=float)
        image = np.array([markers[0], markers[1], markers[2], p11])
        H1, _ = cv2.findHomography(logical, image, 0)

        all_logical = []
        all_image = []
        for x in range(5):
            for y in range(5):
                p = H1.dot([x,y,1])
                p *= 1.0 / p[-1]
                cv2.putText(debug ,"{x},{y}".format(x=x, y=y), (int(p[0]) + 5,int(p[1])-0), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,255,0),1)
                # find feature nearest to H estimate
                center = centers[sort_features(centers, p[0:2])[0]]
                cv2.circle(debug, (int(round(center[0])), int(round(center[1]))), 5, (0,127,255), 2)

                all_logical.append([x*scale_mm,y*scale_mm])
                all_image.append(center)

        all_logical = np.array(all_logical)
        all_image = np.array(all_image)

        H, _ = cv2.findHomography(all_logical, all_image, 0)

    return H, debug
