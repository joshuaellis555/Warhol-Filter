from PIL import Image
import sys
import warnings
import os
from random import randint as RI
from random import shuffle
from mpBuddy import Buddy

import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    import imp
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import Birch
import numpy as np

if __name__=='__main__':
    
    file='22 - Mansell V Senna.jpg'

    image=Image.open(file)

    width=image.width
    height=image.height

    framesW=4
    framesH=4
    frames={}

    def clusterImage(image):
        from PIL import Image
        import warnings
        from random import randint as RI
        from random import shuffle

        import warnings
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            import imp
        from sklearn.cluster import Birch
        import numpy as np

        pixels=list(image.getdata())

        width=image.width
        height=image.height

        clusters=10+RI(0,10)
        R,G,B=1,1,1
        color=1+RI(0,10)/10

        features=[]
        for i in range(len(pixels)):
            x=i%width
            y=int(i//width)
            r,g,b=pixels[i]
            features+=[[(r/255)*R*color,(g/255)*G*color,(b/255)*B*color,x/width,y/height]]

        NParr=np.array(features)

        clustering = Birch(branching_factor=clusters*2, n_clusters=clusters, threshold=1/clusters*2,compute_labels=False) 

        clustering.fit(features)

        clusteredPixels=list(clustering.predict(features))

        colors=[(RI(0,255),RI(0,255),RI(0,255)) for c in range(clusters)]
        '''
        colors=[[0,0,0] for i in range(clusters)]
        counts=[0 for i in range(clusters)]
        for i in range(len(clusteredPixels)):
            r,g,b=pixels[i]
            colors[clusteredPixels[i]][0]+=r
            colors[clusteredPixels[i]][1]+=g
            colors[clusteredPixels[i]][2]+=b
            counts[clusteredPixels[i]]+=1
        colors=[(int(colors[i][0]/counts[i]),int(colors[i][1]/counts[i]),int(colors[i][2]/counts[i])) for i in range(clusters)]
        #'''

        return [colors[clusteredPixels[i]] for i in range(len(clusteredPixels))]

    frames=Buddy(clusterImage,{f: [image] for f in range(framesW*framesH)})
    
    output=[(0,0,0) for x in range(width*framesW) for y in range(height*framesH)]

    for fx in range(framesW):
        for fy in range(framesH):
            for y in range(height):
                for x in range(width):
                    #print(fy*height*width*framesW+y*width*framesW+fx*width+x,fy*framesW+fx,y*width+x,fy,fx,y,x)
                    #frames[fy*framesW+fx][y*width+x]
                    output[fy*height*width*framesW+y*width*framesW+fx*width+x]=frames[fy*framesW+fx][y*width+x]

    r = Image.new('RGB',(width*framesW,height*framesH))
    r.putdata(output)
    path='.'.join(file.split('.')[:-1]+['war.png'])
    r.save(path)
