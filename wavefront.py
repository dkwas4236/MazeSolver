# Name: Darion Kwasnitza
# ID: 3122890
# Class: CMPT312 - Lab 7 Part 2

import cv2 as cv
import numpy as np

class WaveFront:

    def __init__(self, filename, startPoint, endPoint):
        self.filename = filename
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.frame = self.loadMap()
        self.distance = None
        self.wavefrontnow = self.createPath()
        self.wavefrontnew = None
        self.path = self.viewPath()

    def loadMap(self):
        # read in the image (0 for greyscale in case coloured map)
        grey_img = cv.imread(self.filename, 0)
        return grey_img

    def wavePropogate(self):
        # get how many rows and cols
        rows, cols = self.frame.shape
        # np.full(shape, fill value)
        # fill distances array with -1's for unexplored pixels
        self.distance = np.full((rows, cols), -1) 
        # mark the end point
        self.distance[self.endPoint[1], self.endPoint[0]] = 2
        # define the possible movements from each pixel
        pssibleDirections = [(-1, 0), (1, 0), (0, -1), (0, 1),  
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]  
        # start the new wavefront at the endpoint
        self.wavefrontnew = [self.endPoint]
        # while items in self.wavefrontnew loop
        while self.wavefrontnew:
            # pop the first element out of wavefrontnew and get it's x, y
            x, y = self.wavefrontnew.pop(0)
            updatedDistance = self.distance[y, x]
            for distancex, distancey in pssibleDirections:
                # set new position by adding all possibilities of direction to current x and y
                newx, newy = x + distancex, y + distancey
                # check to make sure its white and its a new unexplored pixel
                if (self.frame[newy, newx] > 127) & (self.distance[newy, newx] == -1):
                    # increment distance by 1
                    self.distance[newy, newx] = updatedDistance + 1 
                    # add to new wave front
                    self.wavefrontnew.append((newx, newy))

    def createPath(self):
        self.wavePropogate() 
        # start the path at the start point
        self.path = [self.startPoint]
        # get the x, y of the current start point
        x, y = self.startPoint
        possibleDirections = [(-1, 0), (1, 0), (0, -1), (0, 1),  
                      (-1, -1), (-1, 1), (1, -1), (1, 1)] 
        # loop until at endpoint
        while (x, y) != self.endPoint:
            # set next step to none
            next = None
            # set minimum distance, will start at maximum distance 
            # ex with maze 2 is 142
            minimumDistance = self.distance[y, x] 
            for distancex, distancey in possibleDirections:
                # record new position by adding all possibilities of direction to current x and y
                newx, newy = x + distancex, y + distancey
                # check if new distance values are less than current minimun distance
                if 0 < self.distance[newy, newx] < minimumDistance: 
                    # if less than minimum, update next and update minimum
                    next = (newx, newy)
                    minimumDistance = self.distance[newy, newx]
            # append next to the path
            if next:
                self.path.append(next)
                x, y = next
        return self.path

    def viewPath(self):
        # convert back to colour image
        img = cv.cvtColor(self.frame, 1)
        # loop until self.wavefrontnow -1 because will be out of bounds 
        # if checking next at final position, and draw the lines
        for i in range(len(self.wavefrontnow) - 1):
            cv.line(img, self.wavefrontnow[i], self.wavefrontnow[i + 1], (0, 0, 255), 1)
        # draw circles on start and end points
        cv.circle(img, self.startPoint, 1, (0, 0, 255), 1)
        cv.circle(img, self.endPoint, 1, (0, 0, 255),1)
        # scale the image
        scale=3
        w=int(self.frame.shape[1]*scale)
        h=int(self.frame.shape[0]*scale)
        newSize = (w,h)
        resized_img = cv.resize(img,newSize,cv.INTER_AREA)
        cv.imshow("Resized Image", resized_img)
        cv.waitKey(0)

if __name__ == "__main__":
    m = WaveFront("maze02.png", (94, 4), (4, 94))




   