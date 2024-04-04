# SimPan ⚛

<p align="center">
  <img src="./backup/assets/logo.png" alt="image-description", height=460 >
</p>

SimPan emerges as a pioneering application designed to revolutionize the creation and analysis of 3D worlds with AI support in the rapidly evolving domain of simulation technology and ML model development. This web-based platform would leverage artificial intelligence to facilitate the swift growth of highly detailed and realistic 3D environments. Aimed at reducing the technical barriers typically associated with simulation creation, SimPan offers an intuitive user interface that abstracts the complexities of coding, thereby significantly accelerating the development cycle. SimPan is not just a tool for visualizing 3D worlds but also will serve as a comprehensive ecosystem for simulating events, formulating behavioral models, pipelining various ML models, and annotating datasets across multiple domains. Stay tuned for updates!

## Objective 🎯
Design a single point web-application that would help us solve 3D vision problems.
* Create a easy-to-use platform for ML model development - 3D vision primarily.
* Define triggers for 3D environment creation.
* Support data annotation - be it event simulation or labeling.
* Provide analytical plugins.

## Prerequisites 📜
This project will be driven by external repositories (git submodules), therefore kindly refer to the instructions mentioned in the `README.md` of the following repositories before moving forward.
* [Self-Driving Car](https://github.com/NikhilKamathB/SDC/tree/master)
* [LiteGraph.js](https://github.com/jagenjo/litegraph.js/tree/master)

## Folder Structure 🧱
```
SDC Repo.

|- data (any data, structured/unstructured, goes here)
    |- assets (any static and long-lived objects goes here - will be public)
    |- config (holds all the generated/custom configurations)
    |- raw (holds unprocessed information)
    |- processed (holds processed information)
|- logs (logging of information will be done here; logging must be in the following format `log_<timestamp>.<extension>`)
|- pipelines (defined python wrapper to trigger appropriate tasks)
    |- data (data related wrappers must be defined here)
    |- model (this folder is for model wrappers)
    |- preprocess (wrapper for performing the preprocessing step - usually with data)
    |- utils (all helper functions/classes must be defined here)
|- simpan (Django web application)
    |- simpan (driver module)
    |- home (home app)
    |- static (holds static files for development)
    |- templates (holds web pages defintion)
|- requirements.txt (defines dependencies)
```

## How do I run the application? 🏃🏻‍♂️
That's very simple. One you have cloned this repository, `cd` into it. Then run `cd simpan`. This is where we define our Django web application. Once you are inside `*/SimPan/simpan` folder run `python manage.py runserver` to have the server up and running.

## Notes 📝
* As much as possible, try to stick to this template. Any improvement/suggestion to this organization is always welcome.
* Let us try to write a clean code. Comment where ever necessary so that others can understand and pickup easily. Jupyter notebooks, if used, must contain minimal code. What it means is, if you have a big function, the implementation falls into the appropriate scripting folders and this funciton gets called in the notebook. This stands for classes as well.
* If there is anything that you feel is important, please mention them under the appropriate Tasks subheadings.
* Any tasks that you take, see to it that you are not in the main/master branch. Checkout the main/master branch and start from there. Once done, create a pull request.
* To maintain consistency, the naming of all branches except main/master must be done as follows: `<property>/<branch-name>`. The property represents, the type of commit - it may be addition of features, bug fixes, etc. For example, if you are adding a new camera model to the player, the branch name would be `[feature]/addition-of-camera-module`.

## Environment Variables 🤫
```
export DEBUG=<DEBUG> # 1
export SECRET_KEY=<DJANGO_SECRET_KEY>
export STATIC_ROOT=<DJANGO_STATIC_ROOT> # 'static'
```

## References 🔗
* [Self-Driving Car](https://github.com/NikhilKamathB/SDC/tree/master)
* [LiteGraph.js](https://github.com/jagenjo/litegraph.js/tree/master)