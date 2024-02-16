# highscore-micro-two

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/bcorfman/highscore-micro-two)

A FastAPI containerized microservice to create/query a high score list using SQLModel. Connects to a separate PostgreSQL database deployed on the ElephantSQL cloud, so I could try Python's asyncio functionality with latency.

I'm using this project to practice simple microservice design with Python.

## How to set up your own version of this project

0. Fork this highscore-micro-two repo on your own GitHub account.
    - In other words, at the top right of this page, click the Fork button!
    - Check the box that says "Copy the main branch only" (my suggestion), leave the rest of the details the same, and click Create Fork.
1. Create a PostgreSQL DB instance on the ElephantSQL cloud.
    - Visit the [ElephantSQL website](https://www.elephantsql.com/plans.html) and choose the free Tiny Turtle plan.
    - Sign up for your account.
    - Select a name for your plan. (The name is not important, but I chose "highscore".)
    - Pick a region and data center that's close(st) to you. This will help your cloud service performance.
    - Review the final details, then click Create Instance.
    - On the Instances page, click the name of your newly created Instance.
    - On the resulting Details page, copy the connection URL to the clipboard.
    - Finally, make sure your system tests work correctly! In your forked repo on GitHub: find and click your Settings tab, then, on the left sidebar, expand the Secrets and Variables menu, and click Actions. Click the "New repository secret" button, type in ELEPHANTSQL_URL as the name, paste your connection URL into the "Secret" text box, and change the first part of the connection URL to read postgresql+asyncpg:// instead of postgres://
2. Create a Back4App account and use their "Container as a Service" feature to deploy a database API microservice.
    - Visit the [Back4App website](https://www.back4app.com/) and sign up for a free account.
    - At their opening menu, choose Back4App's "Container as a Service" feature.
    - Point to your forked highscore-micro-two repo on GitHub via their "Import GitHub repo" button. NOTE: You will need to give permission to GitHub to install and use "Back4App Containers" during this process.
    - Under the "Configure your initial deployment" settings, choose an App Name (I named mine "highscore") and, under the "Build and Deploy" menu, assign your Port as 443. NOTE: Back4App will automatically handle the configuration of certificates needed for Secure HTTP to work with your container.)
    - Under the "Environment Variables" menu, define a variable with a name of ELEPHANTSQL_URL, paste your connection URL into the Value text box (same as in step 1 above), and change the first part of the connection URL to read postgresql+asyncpg:// instead of postgres:// before you push the Save Settings button.
    - Check your email for a confirmation link to enable deployment.

## Project startup

- Clone the project to your system
- At a command prompt in the project directory, type `make devinstall` to set up the project dependencies.

Also important:
- To run Pytest locally, the FastAPI setup code in main.py looks for a .env file in your project directory. This file will need to contain a single line, which is the same ELEPHANTSQL_URL environment variable as defined in the final part of step 1 under "How to set up your own version" above, e.g.
`ELEPHANTSQL_URL=postgresql+asyncpg://{username}:{password}@{your_prefix_here}.db.elephantsql.com/{username}`

## Deployment

- If you follow the *How to set up your own version* instructions above, Back4App will deploy your containerized microservice to its cloud each time you do a `git push` to your `main` branch.
- Any app built using FastAPI also has a default /docs page that allows you to interact with your published web API. For example, my original HighScore microservice has its own docs page [here](https://highscore-ibq0itxr.b4a.run/docs). You will need to find the link to your own container on your Back4App dashboard; make sure you add the /docs suffix onto the end of your URL to bring up the page correctly.
- If you set both environment variables correctly in the *How to set up your own version* instructions above, your microservice will connect to the ElephantSQL cloud and read/write from the PostgreSQL database there. If something goes wrong, make sure you've checked the connection URLs for correctness.  
- Check out (or fork) my Anvil-based app for a web frontend that provides a better user experience for the database microservice.
