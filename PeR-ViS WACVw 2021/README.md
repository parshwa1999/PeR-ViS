# Person-Retrieval-AVSS-2018
Implementation of our [IEEE WACVw 2021](http://wacv2021.thecvf.com/) paper ["PeR-ViS: Person Retrieval in Video Surveillance using Semantic Description"](https://openaccess.thecvf.com/content/WACV2021W/HADCV/html/Shah_PeR-ViS_Person_Retrieval_in_Video_Surveillance_Using_Semantic_Description_WACVW_2021_paper.html). If you find this code useful in your research, please consider citing:  

```@InProceedings{Shah_2021_WACV,
    author    = {Shah, Parshwa and Garg, Arpit and Gajjar, Vandit},
    title     = {PeR-ViS: Person Retrieval in Video Surveillance Using Semantic Description},
    booktitle = {Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision (WACV) Workshops},
    month     = {January},
    year      = {2021},
    pages     = {41-50}
}
```  

```@inproceedings{galiyawala2018person,
  title={Person retrieval in surveillance video using height, color and gender},
  author={Galiyawala, Hiren and Shah, Kenil and Gajjar, Vandit and Raval, Mehul S},
  booktitle={2018 15th IEEE International Conference on Advanced Video and Signal Based Surveillance (AVSS)},
  pages={1--6},
  year={2018},
  organization={IEEE}
}
```

This code was initially tested on an Ubuntu 16.04 system using Keras 2.0.8 with Tensorflow 1.12 backend.  

![Alt Text](https://github.com/Vanditg/PeR-ViS/tree/master/readme_files/PeR_ViS.jpeg)  

**The paper proposes a deep learning-based linear filtering approach for person retrieval using height, torso cloth color, and gender.**  

## Installation  

1) Clone this repository.  
```
git clone https://github.com/Vanditg/PeR-ViS.git    
```  

2) In the repository, execute `pip install -r requirements.txt` to install all the necessary libraries.  

3) Three deep learning models are used inorder to filter out the desired person.  
	1) *Mask_RCNN:- Used to determine the coordinates of the person and fetch the pixelwise segmentation*  
	2) *gender_model:- Used to determine gender of the person*  
	3) *color_model:- Used to determine torso color of the person*  

4) Download the pretrained weights.
	1) Mask_RCNN [pretrained weights](https://drive.google.com/drive/folders/1IQKvcGuxvT80dqWLDzRKmF-wsmDKzxnG?usp=sharing) and save it in root directory  
	2) gender_model [pretrained weights](https://drive.google.com/drive/folders/1IQKvcGuxvT80dqWLDzRKmF-wsmDKzxnG?usp=sharing) and save it in /modalities/gender/  
	3) color_model [pretrained weight](https://drive.google.com/drive/folders/1IQKvcGuxvT80dqWLDzRKmF-wsmDKzxnG?usp=sharing) and save it in /modalities/torso_color/   

### Usage

To use run
```
python Video_demo_person_identification.py
```  
This will read the input video file and based on the queries produces the Bounding-Box and Person Coordinates text file under the output folder.  

Many thanks to [Matterport](https://github.com/matterport/Mask_RCNN) for the Mask R-CNN code.  

## Media Coverage  

[New Scientist](https://goo.gl/Xj3bUA), [The Next Web](https://goo.gl/5mUyUT), [Digital Trends](https://tnw.to/I1gTz), [Make Tech Easier](https://goo.gl/Yb2FaW), [Tech The Lead](https://goo.gl/ZBn4Bs), [Outerplaces](https://goo.gl/rniz3N), [IMPORT AI by Jack Clark](https://goo.gl/SY8Lux), [Business Recorder](https://goo.gl/XAvc4q), [Inshorts](https://inshorts.com/en/news/indian-teams-ai-finds-people-in-videos-via-clothes-height-1540395247981), and [RT](https://goo.gl/9HbkgV)  

