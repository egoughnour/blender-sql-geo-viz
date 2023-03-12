# blender-sql-geo-viz
Currently WIP.  Documenting process of using SQL for path calculation and blender API for video generation



## Big Picture
I am using postgis to generate animations as part of an attempt to generate video content that is polished enough to share or post, _e.g._, to YouTube.
I am also using manim for generation of animations. (_n.b._: for simplicity's sake I will only target MacOS when the alternative is to investigate or code against multiple operating systems or architectures.)  After trying various approaches to recording or generating audio, I found that MacOS built-in text-to-speech is probably sufficient.

In the long term then this repository will comprise:
    
    1. Container-handling code
    2. Postgis queries
    3. Possibly: Manim animation source [for mathematical animation creation] or links to relevant code
    4. Possibly: Python source corresponding to the topic of various videos, or again, links.
        - the topics of prospective videos are largely mathematical in nature
        - this makes visualization of various kinds an obvious, attractive alternative to recording live audio and video. 
    5. Non-mathematical visualization/animation code
    6. Description of and/or links to details of techniques that facilitate non-programmatic steps in production of video content. 
    

TODO
=====


    [x] Detail ways to generate audio files from text directly.
    [x] Set up colima and pull appropriate docker image for a shape/geom-capable database. Else install locally.
    [x] Parametrize a query that provides, e.g.,  points along a great circle, given two locations.
    [x] create a texture map of the earth's surface and 
    [x] apply the map to a globe mesh in a Blender scene
    [x] create a sphere mesh for each point in the set of interpolating point on the path
    [x] animate


Details
=======

When generating audio files directly from text I have used a relatively simple method.  I will include links or a more comprehensive explanation relatively soon.  The key is to open a text editor and then under the application drop-down to select _Services > Service Preferences..._.
This ought to open the _Keyboard_ settings, or at least they should be reachable from this window.

Note below the option to save text as audio. Check this box or its parent in the tree. After this change to the preferences, only two steps are needed to generate audio files.

  1. Select the text to convert, then select the option to save as audio in the context menu.
  2. Save to a directory other than music, such as a directory in which you have your various media collected for a specific iMovie.
<img width="497" alt="service_preferences" src="https://user-images.githubusercontent.com/457471/224579744-e85e24b1-2a3b-44c6-b773-582eb846f435.png">
