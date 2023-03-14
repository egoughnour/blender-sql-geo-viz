# blender-sql-geo-viz
Currently a work in progress.  Implementing, documenting and possibly packaging various programmatic animation workflows, such as the process of using SQL for path animation 



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
    

TODO (Immediate)
=====

    [ ] Validate the query that provides points along a great circle. 
    [x] Animate base Earth image (check notebook)
    [ ] Apply path to pythreejs image.
    [ ] Port to another animation framework?
    [ ] Record from within Jupyter?

Text-to-Speech
=======

When generating audio files directly from text I have used a relatively simple method.  I will include links or a more comprehensive explanation relatively soon.  The key is to open a text editor and then under the application drop-down to select _Services > Service Preferences..._.
This ought to open the _Keyboard_ settings, or at least they should be reachable from this window.

Note below the option to save text as audio (_Add to Music as a Spoken Track_). Check this box or its parent in the tree. After this change to the preferences, only two steps are needed to generate audio files.

  1. Select the text to convert, then select the option to save as audio in the context menu.
  2. Save to a directory other than music, such as a directory in which you have various media collected for inclusion in an iMovie.
<img width="497" alt="service_preferences" src="https://user-images.githubusercontent.com/457471/224579744-e85e24b1-2a3b-44c6-b773-582eb846f435.png">
