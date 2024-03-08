# Twitter Bot Project Template

A Twitter bot using Django that uses OAuth 2.0 to authenticate and Twitter API v2 to post tweets automatically using Github Actions.

## HOW TO USE THIS TEMPLATE

> **DO NOT FORK** this is meant to be used from **[Use this template](https://github.com/aeswibon/twitter-bot-project-template/generate)** feature.

1. Click on **[Use this template](https://github.com/aeswibon/twitter-bot-project-template/generate)**
2. Give a name to your project  
   (e.g. `tweet_bot` recommendation is to use all lowercase and underscores separation for repo names.)
3. Wait until the first run of CI finishes  
   (Github Actions will process the template and commit to your new repo)
4. Then clone your new project and happy coding!

> **NOTE**: **WAIT** until first CI run on github actions before cloning your new project.

### What is included on this template?

- 🍾 A Twitter bot to post tweet automatically
- 🤖 A [Makefile](Makefile) with the most useful commands to install, run, and commands for Docker
- 🐋 A simple [Dockerfile](docker/Dockerfile) to build a container image for your project.  
- ✅ Code linting using [flake8](https://flake8.pycqa.org/en/latest/)
- ☑️ Code format using [black](https://black.readthedocs.io/en/stable/)
- 🔄 Continuous integration using [Github Actions](.github/workflows/) with jobs to tweet

<!--  DELETE THE LINES ABOVE THIS AND WRITE YOUR PROJECT README BELOW -->

---

## project_name Django Application

project_description

## Installation

From source:

```bash
git clone https://github.com/author_name/project_urlname project_name
cd project_name
make install
```

## Executing

1. Rename the `.env.example` file to `.env` and fill the environment variables
2. Run the applicaiton using Docker if Redis is not available

```bash
make up
```

otherwise

```bash
make run
```

Go to:

- API schema: <http://localhost:9000/swagger>
